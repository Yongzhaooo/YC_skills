---
name: grilling
description: Interview the user in batched rounds to stress-test a plan, decision, or design until nothing is silently assumed.
---

Interview me relentlessly about every aspect of this until we reach a shared understanding. Model the discussion as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled — the questions you can ask now without guessing. Ask the whole frontier in one round: number each question with a round-prefixed label (R1-Q1, R1-Q2, ..., R2-Q1, R2-Q2a, ...) so labels are unique across the entire session. Give your recommended answer for each. Wait for all answers before the next round.

Each round reshapes the tree. Settled decisions push the frontier outward and unblock questions that depended on them. A question whose answer depends on another question still open in the same round belongs to a later round, not this one.

If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking me. Do the lookups in parallel where possible — do not block the round on a single lookup. The *decisions*, though, are mine — put each one to me and wait for my answer.

Stop when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until I confirm we have reached a shared understanding.

## Lessons

- Round-prefixed labels exist for a reason: plain `Q1/Q2/Q3` got reused across rounds and sub-labels like `Q2a` cross-contaminated, so decisions could no longer be traced to the round that raised them.
- A settled frontier is not a mandate. Wait for confirmation, then a separate request, before writing a spec or starting implementation.
