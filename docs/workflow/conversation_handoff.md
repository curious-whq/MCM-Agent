# Cross-conversation research memory

MCM-Agent does not rely on chat history for project continuity.

Stable project knowledge lives in `docs/research/`:

- `GOAL.md` — long-lived objective;
- `METHOD.md` — current method;
- `DECISIONS.md` — decisions not to casually revisit;
- `LESSONS.md` — cross-module lessons;
- `ROADMAP_3W.md` — manual-bootstrap time box;
- `STATUS.md` — current project state;
- `CURRENT_HANDOFF.md` — generated self-contained snapshot for a fresh conversation.

Each workflow run also owns:

- `SUMMARY.md` — generated machine-readable-to-human summary of the current run state;
- `EXPERIENCE.md` — durable manual lessons categorized as input/prompt/schema/validator/model/generalization lessons.

`SUMMARY.md` is refreshed automatically when a manual task is exported/imported and after semantic validation. `EXPERIENCE.md` is never overwritten once created.

Generate a fresh cross-conversation handoff with:

```bash
python3 -m workflow.cli handoff \
  --repo-root . \
  --run-root runs
```

If the current experiment lives outside the normal run root:

```bash
python3 -m workflow.cli handoff \
  --repo-root . \
  --task-dir /path/to/current/task
```

In a new ChatGPT conversation, provide `docs/research/CURRENT_HANDOFF.md` first. If the next action is an LLM/manual semantic task, also provide that run's `prompt.md`.
