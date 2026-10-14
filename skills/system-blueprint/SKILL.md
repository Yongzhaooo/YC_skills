---
name: system-blueprint
description: Create or revise a project's target architecture and route (docs/architecture.md) - the end-state structure, chosen approach with its long-term trade-offs, and milestones from today's system to it. Use when work crosses modules or stages, changes an interface, data model or deployment shape, or the user asks for global or architecture-first planning. Not for a single local change (plan-work), what the product should do (product-spec), or progress state (wayfinder).
---

# System Blueprint

`docs/architecture.md` states how the system should be built to reach the product's
destination: the target structure and the route to it. `docs/product.md` says what the
product should be; a change plan says how one step gets made; wayfinder says where the
work stands. Keep one blueprint per project and revise an equivalent existing authority
instead of creating a competitor.

The blueprint widens understanding, not the diff. Each step can stay small; it must sit on
the route to the target instead of being a dead end that later work has to undo.

## When it is needed

Write or revise the blueprint before planning when the work:

- crosses module or ownership boundaries, or spans several stages or sessions;
- changes a public or shared interface, persistent data shape, or deployment shape;
- would otherwise force later work to reverse an early choice;
- or when the user asks for global, architecture-first, or long-term planning.

A local fix or feature inside one module with stable interfaces needs none; check an
existing blueprint for fit and proceed. When a blueprint exists and the change does not
alter it, do not touch it.

## Ground it

Read the product spec, repository instructions, existing design records, and the current
structure that the target touches: entry points, module boundaries, data flow, state
ownership, and external contracts. Use `repo-map` for the mapping and `codebase-design`
for the boundary criteria. Map the current system only as far as the target reaches;
untouched subsystems need a sentence, not an inventory.

## Write it

Keep it readable in one sitting and link detailed contracts instead of copying them.

1. **Target structure** - components, their responsibilities, interfaces between them,
   data flow, and who owns each piece of state. Describe the end state, not the next step.
2. **Approach** - when a material choice has more than one viable answer, compare the real
   options (normally two or three) on long-term cost: change locality, migration,
   compatibility, operations, and what each makes hard later. Record the choice and why.
   Do not invent a strawman when one approach is clearly right; say so in one line.
3. **Route** - milestones from today's system to the target. Each milestone leaves a
   working system with its own observable acceptance. Name irreversible points
   (data migrations, published interfaces) and their rollback or compatibility plan.
   Mark any temporary scaffolding with the milestone that removes it.
4. **Open decisions** - each with what it blocks. The user settles material product,
   contract, and compatibility choices; propose, do not decide them silently.

Mark expectations the user has not confirmed with `(proposed)`. Record each settled
decision once: in the project's existing decision log when it has one, otherwise in the
blueprint's approach section. Do not create a second decision authority.

Milestones stay coarse. Work items, file paths, and validation belong to `plan-work`, one
milestone or change at a time. When the project has `docs/wayfinder.md`, its Milestones
reference the blueprint's route instead of restating it.

```markdown
# <System> architecture

Last confirmed: <YYYY-MM-DD | not yet confirmed>
Product spec: <path, if any>

## Target structure
## Approach
## Route
## Open decisions
```

## Keep it current

Revise the blueprint in the same change that alters the target structure or route. When
implementation evidence, a pilot, or a review contradicts it, report the gap and propose
the revision; do not quietly build around it or quietly rewrite it to match the code.
Replace superseded content in place; history lives in Git.

## Boundaries

Writing or revising the blueprint does not authorize implementation. If the user already
authorized implementation and no material decision remains open, continue with the first
milestone through `plan-work` or direct work.
