# <Pilot Title>

Pilot ID: `<stable-id>`
Lifecycle Status: `ready`
Result: `pending`
Created: `YYYY-MM-DD`
Updated: `YYYY-MM-DD`

## Binding

- Source spec: `<repository-relative path or none>`
- Source commit: `<git commit or none>`
- Selected slice: `<sections / acceptance IDs / bounded behavior>`
- Separately gated actions: `<model calls / production / remote / irreversible>`

## Pilot Card

- Hypothesis: `<one testable claim>`
- Control: `<current behavior>`
- Treatment: `<candidate behavior>`
- Frozen inputs: `<paths, IDs>`
- Leakage exclusions: `<denied inputs and contamination boundary>`
- Allowed writes: `<experiment-local paths>`
- Non-goals: `<explicit exclusions>`
- Budget: `<calls, time, files, or other ceiling>`
- PASS: `<observable condition>`
- WEAK: `<observable condition>`
- FAIL: `<observable condition>`
- INVALID: `<protocol or evidence failure>`
- Retry rule: `<execution-invalid replacement rule>`
- Hard stop: `<exact stop condition>`

## Implementation Slice

- `<smallest end-to-end behavior>`

## Validation

- `<command>` — `<expected evidence>`

## Execution State

- Completed: `<durable completed work>`
- Current step: `<single current step>`
- Next action: `<single next action>`
- Blockers: `<exact blockers or none>`
- Resume from: `<path, artifact, command, or line>`

## Evidence

- Raw artifacts: `<paths or none>`
- Validation results: `<concise results>`
- Budget consumed: `<actual usage>`
- Confirmed facts: `<facts>`
- Inference and limitations: `<bounded interpretation>`
