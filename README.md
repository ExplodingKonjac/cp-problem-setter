# cp-problem-setter

A cross-platform plugin scaffold for competitive programming problem setters.

The repository is both a plugin and a single-plugin marketplace. Both
marketplace catalogs point their only entry at the repository root:

```text
.
├── .agents/plugins/marketplace.json
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
├── .codex-plugin/plugin.json
├── examples/
├── skills/
└── opencode.json
```

`skills/` is reserved for future skills covering testlib, problem package
management, problem-setting workflows, and solution writing. `examples/` is
reserved for future reference problem packages. Both directories are
intentionally empty.

No scripts, third-party dependencies, MCP servers, hooks, or runtime tools are
included in this initial scaffold.
