# Agent Instructions for YC Skills

These are personal workflow skills for Codex + GPT 5.6 sol subagent mode.

## Skill Loading

Each skill is user-invoked only (no auto-trigger). The user types `/skill-name` to invoke.

## Core Rules

1. Do not auto-invoke any of these four skills without the user's explicit command.
2. Do not chain skills automatically. After `/grilling` completes, do NOT start `/run-pilot` — wait for the user.
3. These skills assume a Codex environment with subagent support. Adapt terminology (model names, tool names) to the current Codex runtime.
4. Keep skill bodies concise. Users should read and understand them quickly.

## When NOT to Use These Skills

- If the work is small and obvious, just do it. These skills add planning overhead.
- If you're exploring or learning, you don't need a spec. Just code.
- For new project ideas, chat with web GPT first before using grilling.
