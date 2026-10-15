---
name: setup
description: Check whether the agent is connected to Rhizome, say in plain words what is wrong when it isn't, and explain how to sign in, allow writing or switch to another workspace. Use when someone sets up the Rhizome skills or MCP server, asks whether Rhizome works, sees no Rhizome tools, gets an error from a Rhizome tool, or wants to use another workspace – also in German („Rhizome einrichten“, „Ist Rhizome verbunden?“, „Rhizome geht nicht“, „anderer Workspace“).
license: Apache-2.0
compatibility: Python 3 and network access to the Rhizome server, for the connection probe.
---

# Rhizome setup

Find out whether the Rhizome connection works, and if not, name the one cause
and the one fix. Answer in the language the person writes in; the app's
labels below are in English with the German in brackets, so name the one the
person sees. The connection
signs in through Rhizome's own page in the browser: never ask for a password,
a token or a code in the chat.

## 1. Are the tools there?

If the Rhizome tools are available, call `my_tasks` – a cheap read.

- **It answers:** the connection works. Say so. Then check the tool list for
  `create_topic`:
  - present → the connection may read and write. Done.
  - missing → **the connection may only read.** Questions and briefings work;
    posting and creating topics, decisions and tasks don't. Fix: reconnect
    (step 4) and choose **Read and write** („Lesen und schreiben“) on the consent
    page.
- **It answers with an error sentence:** pass it on as it is and explain it
  with the table in step 3. Do not retry.

## 2. No Rhizome tools

Either the server isn't added to this agent, or nobody has signed in yet.

Look for a server named `rhizome` in the agent's MCP list – in Claude Code
`claude mcp list` (the plugin's shows as `plugin:rhizome:rhizome`), in Codex
`codex mcp list`, in other agents their MCP settings.

- **Not there:** the person adds the Rhizome MCP server's address – it ends in
  `/mcp` – to the agent. In Rhizome, **Settings → Integrations** („Einstellungen → Integrationen“) shows
  the address and how to connect.
- **There, but "Needs authentication", "needs login" or not connected:** the
  person signs in – in Claude Code `/mcp`, choose the Rhizome server, "Authenticate";
  in Codex `codex mcp login rhizome`; in Gemini CLI `/mcp auth rhizome`; in
  Cursor the server's "Connect" button in the MCP settings. The browser opens
  Rhizome's sign-in, then the consent page: they choose the workspace and
  whether the agent may only read or also write, and allow it. Back in the
  agent, the Rhizome tools appear.
- **The browser never opens, or the sign-in fails before Rhizome's page:**
  probe the address without signing in:

  ```bash
  python3 scripts/probe.py '<the server address>'
  ```

  The script is `scripts/probe.py`, relative to this skill's folder (Python 3, standard
  library only). It sends one `ping` without credentials and prints the
  status and whether the server offers sign-in.

  | Answer | Cause | Fix |
  | --- | --- | --- |
  | `status: certificates` | **This machine's Python trusts no HTTPS certificates** – common with Python from python.org on macOS. Rhizome is not the problem. | Follow the sentence the script prints, then probe again. |
  | `status: 000` | Nothing answers at that address: a typo, or the server is down. | Correct the address, or try again later. |
  | `status: 404` | **MCP is switched off on this server**, or the address does not end in `/mcp`. | Check the address. Only the Rhizome team can switch MCP on for a server. |
  | `status: 401`, `sign-in offered: yes` | The server is ready for sign-in. | The agent's own sign-in is the problem: sign in again as above, or update the agent. |
  | `status: 401`, `sign-in offered: no` | **This server does not offer sign-in.** | Only the Rhizome team can change that. |
  | anything else | Name the status and the address; don't guess. | |

## 3. Signed in, but it doesn't work

Match the sentence the tool, the agent or the consent page gives:

| Sentence or symptom | Cause | Fix |
| --- | --- | --- |
| The consent page doesn't offer the workspace | That workspace has its **API or MCP switched off**; only workspaces that let agents in are offered. | A workspace manager turns on **API access** („API-Zugriff“) and **MCP access** („MCP-Zugriff“) under **Settings → Integrations** („Einstellungen → Integrationen“). Then sign in again. |
| "The API is turned off for this workspace" | The workspace's **API was switched off** after the connection was made. | A workspace manager turns on **API access** („API-Zugriff“) under **Settings → Integrations** („Einstellungen → Integrationen“). |
| "MCP is turned off for this workspace" | **MCP was switched off** for the workspace. | A workspace manager turns on **MCP access** („MCP-Zugriff“) under **Settings → Integrations** („Einstellungen → Integrationen“). |
| It worked before, now "Needs authentication" or `401` | **The connection was ended**: under **Connected apps** („Verbundene Apps“), by **Terminate all sessions** („Alle Sitzungen beenden“), or after thirty days unused. | Sign in again (step 2). |
| anything else | Pass it on verbatim; don't guess. | |

After any fix the person reconnects in the agent (Claude Code: `/mcp`) or
starts a new session, then asks again whether Rhizome works.

## 4. Another workspace, or writing allowed

One connection works in one workspace, with the access chosen on the consent
page. To change either, the person signs in again from the agent – in Claude
Code `/mcp`, choose the Rhizome server, clear its authentication and
authenticate; in Codex `codex mcp logout rhizome`, then `codex mcp login
rhizome` – and chooses the workspace and **Read and write** („Lesen und
schreiben“) on the consent page, which comes every time.

Rhizome lists every connected agent, one entry per workspace, under **Security
and Access → Connected apps** („Sicherheit und Zugriff → Verbundene Apps“),
with its access; **Disconnect** („Trennen“) ends one the person no longer needs.
