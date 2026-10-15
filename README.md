# Rhizome skills

Skills for working in [Rhizome](https://get-rhizome.app), where teams raise
topics, decide together and keep their decisions in a register of ODRs. With
these skills, your coding agent raises topics, prepares decisions, writes
minutes, records decisions taken elsewhere, checks plans against the register
and answers from the Rhizome docs.

| Skill | What it does |
| --- | --- |
| `setup` | Checks the connection to Rhizome and says what to fix |
| `create-topic` | Turns a mail, a note or an idea into a topic |
| `draft-decision` | Prepares a decision in a topic, with the mode that fits |
| `draft-minutes` | Writes up a topic's discussion as minutes |
| `draft-odr` | Drafts an ODR from a decision taken outside Rhizome |
| `import-to-odrs` | Turns a pile of minutes and exports into ODR drafts |
| `compliance` | Checks a plan against the decisions in force |
| `mirror` | A private sparring partner before you raise something |
| `docs` | Answers how Rhizome works, from the docs |

Every skill shows its draft and writes only after your OK. `docs`, `mirror`,
`setup` and `import-to-odrs` run a small Python 3 script from their
`scripts/` folder (standard library only).

## Install

**Claude Code** – the plugin brings the skills and connects the Rhizome MCP
server in one step:

```
/plugin marketplace add rhizome-app/rhizome-skills
/plugin install rhizome@rhizome
```

Then `/mcp`, choose `plugin:rhizome:rhizome`, **Authenticate**.

**Any other agent** (Codex, Cursor, Gemini CLI, GitHub Copilot, …) – the
skills follow the open [Agent Skills](https://agentskills.io) format:

```bash
npx skills add rhizome-app/rhizome-skills
```

and connect the MCP server below.

## Connect the MCP server

The skills work through Rhizome's MCP server at
`https://api.get-rhizome.app/mcp`. Every agent signs in through Rhizome in the
browser: you sign in, choose the workspace and whether the agent may only read
or also write, and allow it.

Sign-in offers only workspaces where a workspace manager has switched on both
**API access** and **MCP access** under **Settings → Integrations**. API access
is off in a new workspace.

| Agent | Add the server | Sign in |
| --- | --- | --- |
| Claude Code (without the plugin) | `claude mcp add --transport http rhizome https://api.get-rhizome.app/mcp` | `/mcp` → `rhizome` → Authenticate |
| Codex | `codex mcp add rhizome --url https://api.get-rhizome.app/mcp` | `codex mcp login rhizome` |
| Gemini CLI | `gemini mcp add --transport http rhizome https://api.get-rhizome.app/mcp` | `/mcp auth rhizome` |
| Cursor | `"rhizome": { "url": "https://api.get-rhizome.app/mcp" }` under `mcpServers` in `~/.cursor/mcp.json` | the server's **Connect** button in the MCP settings |

Then ask your agent whether Rhizome works; the `setup` skill checks and tells
you what to fix. Your connected agents are listed in Rhizome under
**Security and Access → Connected apps**, where you can disconnect any of them.
To switch workspace, sign in again from the agent and choose the other one.

## Contributing

This repository is a copy: the skills are developed in Rhizome's own
repository and copied here with every release, so a commit made here directly
is overwritten. Issues are welcome.

## License

[Apache-2.0](LICENSE). The licence covers these skills, not the Rhizome name
or the Rhizome service.
