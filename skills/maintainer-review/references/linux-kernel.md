# Linux Kernel Review

Read the affected subsystem's current rules and the official documentation relevant to
the change. Apply these checks through concrete paths and invariants; do not run a
universal tool suite or print every item for every patch.

Use the target tree's `MAINTAINERS` entries to locate ownership and linked guides, then
the [maintainer profiles](https://docs.kernel.org/process/maintainer-handbooks.html).
Check each affected subsystem's requirements and each explicitly requested destination
(for example development, fixes or stable), including tests, dependency order and tags.
Do not infer the destination from a branch name alone or apply one subsystem's style to
another. Consult target-revision documentation for APIs; online latest documentation may
describe a different kernel. Record policy conflicts rather than treating a prior email
as an undocumented universal exception.

For concurrency/lifetime, link state, register access or public-interface changes, read
the applicable section of [Linux contract guides](linux-contracts.md). These route to
specific source contracts and decisive checks rather than an unconditional test matrix.

- **Context and ordering:** process/IRQ/atomic context, sleepability and allocation flags;
  lock ordering, reference counting, RCU grace periods, and memory ordering where used.
  Explain who keeps an object alive after an asynchronous user outlives the initiating
  call. An existing helper is reusable only in the required context and lifetime.
  Trace subsystem serialization (such as RTNL), per-object locks and workqueues before
  claiming concurrent writers. Protect snapshot/change/restore as one transaction when
  required; a bus or regmap access lock may not do so. A dedicated lock needs a coherent
  ownership boundary and ordering, including error paths. Do not wait for callbacks or
  teardown while holding a lock those callbacks need.
- **Failure and teardown:** partial initialization, allocation failure, cancellation of
  queued work, device removal, and module unload as applicable. Unregistering one source
  of callbacks does not establish that other users or queued work are gone; inspect the
  actual API guarantees and cleanup ordering.
- **Compatibility:** userspace ABI and regressions differ from internal kernel APIs.
  Internal API changes require migrating affected in-tree callers, not preserving an
  arbitrary private ABI. Public interfaces have long-lived compatibility obligations:
  syscall flags, sized argument structures, and unknown-input validation can be
  justified extension mechanisms before a second variant exists. Assess specific ABI
  layouts, meanings, errors, and supported compat paths, not just function signatures.
  Preserve established device modes when adding a new one. Narrowing an existing reset,
  pause or workaround scope is a separate behavior change that needs evidence; it is not
  automatically safe because the new board does not use those modes.
- **Configuration and cost:** relevant Kconfig/build combinations, supported architectures,
  resource/security boundaries, and hot-path costs. Optimization needs workload and
  trade-off evidence. Do not introduce unrelated portability or performance work.
- **Series and validation:** one logical change per patch, with buildable and usable
  intermediate states for bisect. Choose existing builds, selftests/KUnit, lockdep,
  sanitizers, or fault injection according to the affected risk. State actual coverage.
  A review request alone does not authorize booting a test kernel or changing a live
  system; missing execution evidence remains visible in the verdict.
  For hardware claims, distinguish source inclusion, built-image inclusion, running
  device identity and exercised behavior. Check whether a downstream backport replaces
  or bypasses the upstream function, topology or interface mode under review.
  Read register definitions for the applicable device/revision; distinguish reserved,
  latched and real-time status and non-atomic reads. Another device's helper or a mock
  register value does not establish this device's contract.

Authoritative starting points, to consult as needed:

- [Submitting patches](https://docs.kernel.org/process/submitting-patches.html): explain
  the problem and costs; separate logical changes and preserve bisectability.
- [Development and internal APIs](https://docs.kernel.org/process/4.Coding.html): integration,
  regressions, and in-tree API migration responsibilities.
- [Adding syscalls](https://docs.kernel.org/process/adding-syscalls.html): permanent public
  contracts, existing facilities, and deliberate extension mechanisms.
- [Reviewing patches](https://docs.kernel.org/process/7.AdvancedTopics.html#reviewing-patches)
  and the reviewer's statement in Submitting patches: report the aspects actually
  examined and unresolved serious issues; do not equate an approach endorsement with
  complete technical review.
- [netdev guide](https://docs.kernel.org/process/maintainer-netdev.html), for networking:
  verify current target-tree, test and submission requirements. Its current guidance
  requires `Fixes:` for fixes regardless of tree; `net-next` alone is not a reason to
  remove the tag. Resolve whether a disputed patch is a fix and whether a scoped
  maintainer instruction changes its treatment. Recheck policy at review time.

## Lessons

- Trace errors from the hardware operation through polling, return types, casts, and
  read-modify-write consumers. A negative errno must not become valid register data
  or a successful completion; include cleanup and reset paths where relevant.
- Reusing a lock still needs a call-graph check: establish lock order and cover the
  entire state transaction, including restore failures and concurrent callbacks.
- Separate a generic mechanism from its evidence-backed activation scope. One tested
  board does not prove family-wide support, and missing evidence does not prove a
  sibling chip is unsupported. Preserve established modes while resolving new ones.
- A newly found pre-existing bug can deserve a standalone fix and target tree even
  when it blocks a feature series. Put required protection before the feature that
  exposes it; submission dependency does not always require prior upstream merge.
  Distinguish an actual regression/field report from an error-handling defect found by
  inspection or injection, and follow the subsystem's target-tree and Fixes guidance.
- A status reader may update speed or flags without notifying the MAC or another
  consumer. Check state-machine transitions and notification gating before claiming an
  end-to-end fix. Returning an errno, preserving old state and reporting link down have
  different recovery effects; none is a neutral default for an unclassified state.
