# Evidence at Review Boundaries

Use only the rows implicated by the change. Work through the proof while reviewing;
publish the decisive evidence and gaps, not a filled-out template for every patch.

| Claim | Evidence needed to decide it |
| --- | --- |
| The change solves the stated problem | A concrete trigger, exercised when effectiveness rests on testing rather than code, before/after behavior, and path from input to the consumer-visible result. Separate failing behavior, an unreached trigger and an invalid fixture. Check differences in setup, timing, instrumentation or other writers only where they could change the verdict. |
| The proposed mechanism explains the failure | Compare plausible explanations against the observed sequence, including when required state first becomes valid and is consumed. Name a distinguishing prediction or source contract; an effective workaround alone does not identify the cause. |
| A smaller intervention is sufficient | Keep relevant conditions comparable and check the removed part's role in other supported modes. Separate a successful bundle, a locally sufficient subset and a generally safe production change; use only controls needed for the decision. |
| Concurrent execution is safe or unsafe | Actual execution contexts, shared accesses, outer serialization and a permitted ordering. For a defect, show the interleaving that violates an invariant; for protection, explain which edge excludes it. A missing local lock alone proves neither. |
| An object remains alive | Allocation/publication, reference acquisition before handoff, all asynchronous owners, last use, cancellation/drain and final release. Follow rejected submissions and partial initialization too. A reference counter does not protect a pointer before a reference is safely acquired. |
| A state change reaches a consumer | Old/new states, notification gate, scheduling/coalescing, consumer callback and externally visible action. Include unchanged-state updates and failure recovery when relevant. |
| Failure preserves the contract | Track the error value and any state already changed through callers, rollback and retry. Identify what remains valid if rollback itself fails; do not assume returning an error restores state. |
| An existing interface remains compatible | Affected callers/modes, meaning and encoding before/after, and migration or fallback behavior. Include old users of shared code, not only the new caller. |
| Validation supports acceptance | Exact revision/configuration, exercised path, assertion or observable outcome, and limits. Name the smallest missing observation that could change the verdict. |

Try to falsify consequential claims using supported inputs and actual callers. Check
whether existing locks, ownership or API guarantees defeat the suspected failure before
reporting it. A concrete missing guarantee can block acceptance without a reproduced
failure, but label it as such. Do not invent callers, require impossible exhaustive
testing, or keep searching merely to produce a finding. Accept a sound change when the
relevant contracts hold.

Historical discussions can explain a contract. Read the original patch, substantive
replies and subsequent revision or disposition before extracting a lesson. Record the
message/commit identity and applicable scope; distinguish a suggestion from the adopted
resolution. A merged patch can still contain defects, and an inaccessible thread is not
evidence of consensus. Prefer a focused history search over collecting unrelated threads.
