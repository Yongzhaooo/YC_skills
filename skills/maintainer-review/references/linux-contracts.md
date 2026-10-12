# Linux Contract Guides

Read only sections implicated by the change. The linked guides are starting points;
confirm symbols and guarantees in the target revision. The questions below are review
methods derived from those sources, not quotations or universal subsystem policy.

## Synchronization and lifetime

Use [kref](https://docs.kernel.org/core-api/kref.html),
[lockdep](https://docs.kernel.org/locking/lockdep-design.html) and the target's relevant
locking, workqueue, timer or RCU API documentation.

Trace references before cross-thread handoff and lookup protection before reference
acquisition. Follow the last put into its release callback and inspect subsequent
accesses, including pointer dereferences used only to recover a lock or owner. A live
owner does not make it safe to retrieve its pointer through an already freed object.
For failed open/queue/registration operations, verify who actually executes
cleanup; success-path release callbacks may never run. For teardown, enumerate callback
sources and their descendants: stopping a timer does not by itself drain work it queued.
Distinguish lock ordering, object lifetime and multi-step transaction consistency.

When a caller-held lock is part of the contract, inspect all relevant callers and any
existing `lockdep_assert_held()`; consider an assertion where useful rather than relying
only on prose. The [tip guide](https://docs.kernel.org/process/maintainer-tip.html) gives
this example, but its other conventions are not automatically rules for every subsystem.
Lockdep depends on observed lock chains and its modeling assumptions; a quiet run does
not establish unexercised paths, reference safety or device-level transaction correctness.

## PHY, phylink and network state

Use [phylink](https://docs.kernel.org/networking/sfp-phylink.html),
[PHY library](https://docs.kernel.org/networking/phy.html), and the target revision's
`include/linux/phy.h`, `include/linux/phylink.h` and corresponding implementations.

Identify PHY, fixed or in-band mode and which layer owns carrier, negotiation and MAC
configuration. Trace status read, state-machine gate and MAC callbacks, including changes
while link remains up. Check suspend/resume and stop/start if modified. The phylink guide
warns that direct carrier manipulation can interfere with its callback tracking; verify
the actual owner before accepting such calls. Passing traffic alone does not establish
correct pause, duplex, mode negotiation or recovery.

## Register and hardware semantics

Use the applicable device/revision datasheet or errata alongside the bus accessor and
driver implementations. Cite register/bit definitions, not another chip's helper as a
substitute. Check access width, errno representation, reserved encodings, latch/read-clear
behavior and read-modify-write side effects where implicated. A bus lock may serialize
transfers without making a multi-register status snapshot coherent.

Separate a code-level invalid-state response from evidence that hardware reaches that
state. Choose a test whose observable result distinguishes competing explanations;
synthetic inputs and real-device observations answer different questions.

## Public interfaces and supported modes

Use [Adding syscalls](https://docs.kernel.org/process/adding-syscalls.html),
[ioctl design](https://docs.kernel.org/process/botching-up-ioctls.html), and applicable
ABI or Devicetree binding definitions when those surfaces change.

Check old and new users, unknown flags/values, layout and compat handling where relevant.
For a new firmware mode, trace binding/example through parsing, validation and actual
driver behavior. A schema-accepted configuration need not be operationally supported.
Do not preserve arbitrary internal APIs as if they were userspace ABI; inspect and migrate
their affected callers instead.

## Choosing verification

Use the [submission checklist](https://docs.kernel.org/process/submit-checklist.html)
and target subsystem's requirements. Derive required builds and runtime checks from
changed dependencies and contracts: relevant built-in/module/disabled combinations,
error unwind, state transitions, locking paths or ABI consumers. Distinguish required
subsystem checks from optional additional confidence. Record missing evidence without
silently waiving an explicit requirement or demanding the entire checklist for every edit.
