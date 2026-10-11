"""MCP framing, bound wakeups and question/reply lifecycle without model calls."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'skills/agy-execution/scripts'))
import pi_background as background
from pi_dialogue import reply, save

THREAD = '22222222-2222-4222-8222-222222222222'
REQUEST = '11111111-1111-4111-8111-111111111111'


class BackgroundTests(unittest.TestCase):
    def test_real_mcp_pipe_handshake_errors_and_timeout(self):
        source = '''import json,sys
for line in sys.stdin:
 r=json.loads(line)
 if 'id' not in r: continue
 if r['method']=='initialize': result={}
 elif r['method']=='tools/list': result={'tools':[{'name':'send_message_to_thread'}]}
 else:
  assert r['params']['_meta']['codexThreadId']==r['params']['arguments']['threadId']
  result={'content':[{'type':'text','text':json.dumps({'threadId':r['params']['arguments']['threadId']})}]}
 print(json.dumps({'jsonrpc':'2.0','id':r['id'],'result':result}),flush=True)
'''
        command = [sys.executable, '-u', '-c', source]
        result = background.app_call(command, THREAD, 'send_message_to_thread', {'threadId': THREAD, 'prompt': '中文'})
        self.assertEqual(json.loads(result['content'][0]['text'])['threadId'], THREAD)
        with self.assertRaises(ValueError):
            background.app_call(command, THREAD, 'missing', {})
        with self.assertRaises(TimeoutError):
            background.app_call([sys.executable,'-c','import time; time.sleep(30)'], THREAD,
                                'send_message_to_thread', {}, timeout=.05)

    def test_worker_waits_for_answer_then_notifies_completion_once(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            run = root/'run'
            question = run/'questions'/REQUEST/'request.json'
            save(question, {'status':'waiting','request_id':REQUEST,'question':{'question':'7 or 8?'}})
            event = {'event':'primary_request','request_id':REQUEST,'run_dir':str(run)}
            fake = root/'runner.py'
            fake.write_text('import json,time\nfrom pathlib import Path\n'
                            f'print(json.dumps({event!r}),flush=True)\n'
                            f'p=Path({str(question.parent / "answer.json")!r})\n'
                            'while not p.exists(): time.sleep(.01)\n'
                            'assert json.loads(p.read_text())["answer"]=="7"\n'
                            'print(json.dumps({"event":"primary_answered"}),flush=True)\n'
                            'print(json.dumps({"ok":True,"result":{"response":"7"}}),flush=True)\n',encoding='utf-8')
            job = {'thread_id':THREAD,'command':[sys.executable,str(fake)],'cwd':str(root),'app_tools_command':['mcp']}
            save(root/'job.json',job)
            calls=[]
            def app(command, thread, name, args):
                calls.append(args)
                self.assertEqual(thread, THREAD)
                self.assertEqual(args['threadId'], THREAD)
                self.assertNotIn('model',args)
                if len(calls)==1:
                    reply(run,REQUEST,'7')
                return {'content':[{'type':'text','text':json.dumps({'threadId':THREAD})}]}
            with patch.object(background,'app_call',side_effect=app):
                self.assertEqual(background.worker(root),0)
                background.notify(root,job,'terminal','duplicate')
            self.assertEqual(len(calls),2)
            self.assertEqual(json.loads((root/'status.json').read_text())['state'],'completed')
            with self.assertRaises(FileExistsError):
                background.worker(root)

    def test_notification_failure_retained_without_automatic_replay(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            job={'thread_id':THREAD,'app_tools_command':['mcp']}
            with patch.object(background,'app_call',side_effect=TimeoutError('unknown delivery')) as call:
                background.notify(root,job,'terminal','message')
                background.notify(root,job,'terminal','message')
            call.assert_called_once()
            self.assertEqual(json.loads((root/'notifications/terminal.json').read_text())['state'],'delivery_unconfirmed')

    def test_launch_requires_dispatch_environment_and_verified_thread(self):
        with patch.dict(os.environ,{},clear=True), self.assertRaisesRegex(ValueError,'environment'):
            background.launch(__file__,['--background'],{})
        with patch.dict(os.environ,{'CODEX_THREAD_ID':THREAD,'CODEX_APP_TOOLS_PIPE_PATH':'pipe'}), \
                patch.object(background,'app_call',return_value={'content':[{'type':'text','text':'{"thread":{"id":"wrong"}}'}]}), \
                self.assertRaisesRegex(ValueError,'identity'):
            background.launch(__file__,['--background'],{'codex_app_tools_command':['mcp']})


if __name__ == '__main__':
    unittest.main()
