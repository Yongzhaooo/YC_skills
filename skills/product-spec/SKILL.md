---
name: product-spec
description: Create or revise a project's living product spec (docs/product.md), the current expected shape of the product. Use when the user asks to write or update the product spec, or when a settled decision changes what the product should be. Not for one change's plan (plan-work) or progress state (wayfinder).
---

# Product Spec

`docs/product.md` states what the product should be now: the destination. Wayfinder
records where the work stands; code and tests record what exists; a change plan records
how one change gets made. Keep one product spec per project. If the project already has
an equivalent authority, revise that instead of creating a competitor.

## When to update

Update on events, not on a calendar:

- a grilling round, pilot result, review, or user decision settles a change to the
  product's shape;
- a wayfinder route reassessment finds an expectation no longer holds;
- the user changes an expectation.

Update the spec in the same change that alters the product's shape. Work that leaves the
shape unchanged does not touch it.

## Write it

- Present tense, current expectations only. Replace a superseded expectation in place;
  history lives in Git and dated change specs.
- Write each expectation as observable behavior: who or what, what happens, and how one
  could tell it holds. Group by user-facing capability, not by implementation module.
- List consciously excluded shapes under Non-goals.
- List undecided shape questions under Open questions, each with what it blocks. The user
  settles them; writing the spec does not.
- Mark expectations the user has not confirmed with `(proposed)`. `Last confirmed` is the
  date the user last confirmed the whole document, or `not yet confirmed`; partial edits
  do not refresh it.
- Link detailed contracts such as API docs or schemas instead of copying them. Keep the
  document readable in one sitting.

For a new spec, draft from the user's statements, the README, and the wayfinder Project
outcome; ask only for shape decisions you cannot find. When the project has
`docs/wayfinder.md`, link the spec's actual path from its Project outcome.

```markdown
# <Product> product spec

Last confirmed: <YYYY-MM-DD | not yet confirmed>

## Purpose
<who it serves and the result it delivers>

## Expectations
### <capability>
- <observable expectation>

## Non-goals
- <excluded shape>

## Open questions
- <question>; blocks: <what>
```

## Boundaries

Editing the spec does not authorize implementation. When code and spec disagree, report
the gap; change either side only under authority for that change.
