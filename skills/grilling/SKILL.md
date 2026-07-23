---
name: grilling
description: Use when you need to stress-test a plan, decision, or idea before committing to implementation. A grilling agent will relentlessly interview you about every aspect until boundaries are clear.
---

## What it is

Grilling turns a fuzzy plan into a sharp one. Instead of letting you assume things silently, the agent interviews you about every decision until nothing is left unquestioned.

**When to use it**: You have a half-baked idea, a design you're unsure about, or a decision with hidden dependencies. Type `/grilling` and paste in what you want to stress-test.

## How it works

### Design tree

Every decision branches into the decisions that depend on it. For example, "use Postgres" branches into "what hosting?", "what connection pool size?", "what migration tool?". The agent models the whole discussion as a tree of branching decisions.

### Rounds and the frontier

The agent works the tree in **rounds**. The **frontier** is every question whose prerequisites are already settled — questions the agent can ask right now without guessing. In each round, the agent asks the entire frontier at once.

Numbering is `R1-Q1`, `R1-Q2`, `R2-Q1`, `R2-Q2a`, etc. — unique labels across the whole session so you can refer back to anything.

### Recommended answers

The agent doesn't just ask — it gives a **recommended answer** for each question. You can agree, disagree, or adjust. This keeps the pace fast and gives you something to push against.

### What happens each round

1. Agent asks every question in the frontier (with recommended answers).
2. You answer them all.
3. Agent reshapes the tree based on your answers.
4. Settled decisions push the frontier outward, unblocking new questions.
5. If a question depends on another question still open in the same round, it waits for a later round.

### Facts vs. decisions

If something is a **fact** the agent can look up (filesystem, tools, existing code), it does that in parallel rather than asking you. **Decisions** are yours — every one gets put to you explicitly.

### When does it stop?

The frontier is empty. Every branch of the design tree has been visited. Nothing is silently assumed. The agent stops and reports back. It doesn't act on the result until you confirm you've reached a shared understanding.

## Example flow

```
You:  /grilling I want to add a notification system to the CLI tool.

Agent: R1-Q1: Should notifications be push (real-time) or pull (polling)?
       Recommended: Start with polling — simpler, no server needed.
       
R1-Q2: Where should notification state live?
       Recommended: A local SQLite DB in ~/.myapp/notifications.db.

R1-Q3: What triggers a notification?
       Recommended: Only command failures at first.
       *Looking up existing error handling... found error.ts — can hook in there.*

You:  Q1: polling is fine. Q2: SQLite works. Q3: yes, failures, but also long-running completions.

Agent: [next round with new frontier]
```
