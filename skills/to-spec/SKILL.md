---
name: to-spec
description: Use when you have finished discussing a feature or change and want to capture the decisions in a durable spec document. Synthesizes what was agreed without re-interviewing you.
---

# To Spec

Turn the current conversation into a local spec document. This is a synthesis step — do NOT interview the user. Just capture what has already been discussed and agreed.

## Process

1. **Read context.** Check the repo's CLAUDE.md, AGENTS.md, or equivalent for project conventions. Look at the current codebase state if you haven't already. Use the project's domain vocabulary throughout the spec.

2. **Sketch test seams.** Identify where you'd test the feature. Prefer existing seams over new ones — the ideal number is one. Show the user your seam choices before writing the spec.

3. **Write the spec** using the template below. Save it to a local file at a path that makes sense for the project (e.g. `docs/specs/YYYY-MM-DD-<slug>.md` or alongside the relevant code).

4. **Ask the user to review** the spec. Do not auto-invoke `to-tickets` or any other skill — stop after writing.

## Spec Template

```markdown
# <Title>

Date: YYYY-MM-DD
Status: Draft

## Problem Statement

The problem the user is facing, from the user's perspective.

## Solution

The proposed solution, from the user's perspective.

## Acceptance Criteria

A numbered list of concrete, testable outcomes. Each criterion should be observable — you can tell when it's done.

1. <actor> can <action> so that <benefit>

## Out of Scope

What is explicitly not covered by this spec. Helps prevent scope creep.
```

Write concise acceptance criteria. Prefer concrete scenarios over ceremony. Use user stories only when actor/need/benefit framing clarifies behavior.
