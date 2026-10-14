# Private Forgejo Actions with external runners

Read before setting up or changing remote CI on a self-hosted Forgejo whose server runs
on low-power hardware (a NAS or small home server).

## Topology

- **Forgejo server = controller and storage.** It hosts Git, queues jobs, and stores
  artifacts and logs. It runs no runner.
- **Compute machine = worker.** A dedicated workstation (or its WSL) runs the
  `forgejo-runner` daemon, polls the server for jobs whose labels it serves, and executes
  them locally.

Do not run a runner on the NAS. Its low-power CPU and small memory cannot carry a heavy
build or test: dependency installs and test runs take many times longer, memory pressure
swaps or OOM-kills the job, and the same box is serving Git, so CI load also slows every
push and fetch. The runner only needs outbound access to the server; the server does not
connect to it.

## Runner deployment

- **Labels route the work.** Register the runner with a project-specific label and target
  it in the workflow (`runs-on: my-project`). The label suffix chooses execution:
  `my-project:host` runs directly on the machine with its preinstalled environment;
  `my-project:docker://<image>` runs in a container built from a prepared image. Don't use
  generic labels such as `ubuntu-latest` for a machine-specific environment, or jobs land
  on whatever runner claims them.
- **One job at a time.** Set `runner.capacity: 1` in the runner config. Heavy jobs on one
  machine compete for CPU, GPU and memory, and a shared device or dataset is not safe
  for two jobs at once.
- **Preinstall the environment.** Keep runtime dependencies and the toolchain in a persistent
  virtualenv on the host (host label) or baked into the image (docker label). A job that
  installs heavy dependencies from scratch spends most of its time downloading. The workflow
  verifies the environment through the entry script's own preflight; it does not install it.
- **Isolate the host runner.** Run the daemon as a dedicated user without access to
  personal data or credentials beyond what the jobs need. Jobs from the server execute
  with that user's rights.
- Run the daemon as a service (systemd, or a scheduled task that starts WSL) so it
  survives reboots; a sleeping or offline worker just leaves jobs queued.

## Native lifecycle, no hand-built machinery

Let Forgejo own queueing, cancellation, timeouts and result storage. Do not rebuild them
with shell polling loops, PID or lock files, log-file sentinels, or by pushing results
to a branch.

- **Concurrency:** one group per workflow and ref, newer runs cancel older ones.

  ```yaml
  concurrency:
    group: ${{ github.workflow }}-${{ github.ref }}
    cancel-in-progress: true
  ```

  Check that the server version honors `concurrency`; older Forgejo releases ignore the
  key silently. Without it, `capacity: 1` still serializes jobs but stale runs are not
  cancelled.
- **Timeouts:** set `timeout-minutes` on every job, a margin above its normal duration,
  so a hung test or device frees the runner.
- **Artifacts and logs:** upload the entry script's output directory (for example
  `build-work/ci/`) with `upload-artifact`, using `if: always()` so failures keep their
  logs. Use the major version the server supports (`v3` works on all Forgejo Actions
  releases; newer versions need a recent server). Set `retention-days` so artifacts do
  not fill the NAS.

## Workflow contract

The workflow file stays thin: check out, call the repository's single CI entry, archive
the results. Business logic lives in the entry script, where it runs and is tested
locally the same way.

```yaml
name: ci
on: [push, pull_request]
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
jobs:
  package:
    runs-on: my-project
    timeout-minutes: 60
    steps:
      - uses: actions/checkout@v4
      - run: python ci/run.py package
      - if: always()
        uses: actions/upload-artifact@v3
        with:
          name: ci-${{ github.run_number }}
          path: build-work/ci/
          retention-days: 14
```

If a step needs more than one line of shell, it belongs in the entry script. Action
references resolve against the server's default actions URL (often
`code.forgejo.org`); pin a full URL if the server's default differs.
