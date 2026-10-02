# Third-party notices

The following skills are personally adapted from the MIT-licensed
[mattpocock/skills](https://github.com/mattpocock/skills) repository:

| Skills | Upstream revision | Adaptation |
| --- | --- | --- |
| `grilling`, `run-pilot`, `plan-work` | `9603c1cc8118d08bc1b3bf34cf714f62178dea3b` | Personal workflow adaptation; bounded experiments and proportional planning. |
| `wayfinder` | `9603c1cc8118d08bc1b3bf34cf714f62178dea3b` | Simplified to a local project map; adds outcome, current answer, focus and optional milestones, reader-first reports with dated evidence, and route reassessment without granting execution authority. Sharing copy synchronized from MyAgents `16def2a4caac968a02c43d121780ee80d24315ee`. |
| `code-review`, `codebase-design` | `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` | Retained standards/spec review and module design guidance; removed mandatory delegation and assumed project tools. |
| `handoff` | `2ab958093e83e0ec752e6c1c5932da465bf23e0c` | Removed upstream `argument-hint` and implicit-invocation metadata, added Claude compatibility in MyAgents, and otherwise kept the upstream handoff body. The public copy also omits deployment metadata. |
| `improve-codebase-architecture` | `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` | Kept evidence-based architectural analysis while making delegation and visuals optional and removing assumed project-specific companion skills and workflows. |

`plan-work` also draws on
[`writing-plans`](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/writing-plans/SKILL.md)
from `obra/superpowers` at revision `8ca22dba9a94f28898bbce59f2537ff4d87c747d`.
The adaptation adds concrete interfaces, acceptance evidence, explicit execution
dependencies, and separate authorization for human communication and financial actions.
Its MIT license is retained in [LICENSE.superpowers](skills/plan-work/LICENSE.superpowers).

These are adapted skills, not unmodified upstream snapshots. Sharing adaptations also
omit personal deployment metadata. Ponytail and Stop That Shit are linked for separate
installation; their plugin code is not bundled here.

## mattpocock/skills license

MIT License

Copyright (c) 2026 Matt Pocock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
