## Global additions (this session)

- **graphify** (CLI, `uv tool install graphifyy`) — local knowledge-graph mapper, project-scoped install, see below.
- **karpathy-guidelines** (global skill, `~/.claude/skills/karpathy-guidelines/`) — auto-triggers on code tasks: surface assumptions, no speculative scope, surgical edits, verifiable success criteria. From `multica-ai/andrej-karpathy-skills`.
- **i-have-adhd** (global skill, `~/.claude/skills/i-have-adhd/`) — manual, invoke with `/i-have-adhd`. Lead-with-action, numbered steps, no preamble/recap. From `ayghri/i-have-adhd`.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
