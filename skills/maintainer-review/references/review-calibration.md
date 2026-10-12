# Behavioral Calibration

Use when materially revising this skill, not as a stage in every code review. Follow the
owning skill-authoring and delegation workflows; this reference grants no extra authority.

Choose a small set of real patches or historical source revisions not used to formulate
the new rules. Keep immutable source identities and enough callers, cleanup paths and
destination guidance to make the task answerable. Include a corrected or otherwise sound
control so that indiscriminate objections cannot pass.

Give an independent trial the review request, skill and source context, withholding the
later review, fix explanation and expected findings. For historical cases, prevent answer
lookup during the trial while providing the API and policy references it needs. Preserve
the actual code; label synthetic policy or environment assumptions explicitly. Test rule
discovery by supplying the destination and guide locations without summarizing their rules.

After the trial, compare its concrete claims with the later discussion/fix and inspect
the code for both missed issues and unsupported objections. Historical outcomes are a
reference, not infallible ground truth. Check correct acceptance of the control, source
traceability and separation of defects from unresolved guarantees. Correct a failed rule
and recheck the affected case; use an old-version comparison only if improvement itself
is in dispute. Reusing a case after editing is a regression check, not a fresh holdout.

Report cases, actual findings, misses, false positives and limits. Do not claim general
accuracy from a few trials. Keep temporary inputs and raw outputs in the owner's scratch
area; no new benchmark framework or permanent review gate is required.
