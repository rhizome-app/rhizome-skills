# Rhizome vocabulary, German ↔ English

The German interface and docs are the original; the English is a translation
of them. Use the German words with German speakers, the English ones with
English speakers, and never mix the two in one text. The skills are written in
English; with a German speaker, take every Rhizome term from this file rather
than translating it yourself. The English column is the
app's English interface; the English docs sometimes word it differently
("Solved", "Consultation"), and the German is what both translate. The third
column is the value the tools and the API use.

## Topics

| EN | DE | Tools / API |
| --- | --- | --- |
| Topic | Thema | `topic` |
| Topic type: New topic / Idea / Problem / Question / Quick decision / Concept work | Neues Thema / Idee / Problem / Frage / Einfache Entscheidung / Konzeptarbeit | `topic` / `idea` / `problem` / `proposal_collection` / `quick_decision` / `concept` |
| Open / Settled / Archived | Offen / Geklärt / Archiviert | `open` / `solved` / `archived` |
| Settle, Reopen, Archive | Klären, Wiedereröffnen, Archivieren | `solve` / `reopen` / `archive` |
| Conclusion (asked for when solving) | Fazit | `conclusion` |
| Priority: none / low / medium / high / urgent | Priorität | `priority` |
| Deadline | Frist | `deadline` |
| Tags | Schlagwörter | `tags` |
| Related / blocks / blocked by / duplicate | Verwandt / blockiert / blockiert durch / Duplikat | relationship |

A topic is *settled* (geklärt; `solved` in the tools), never "resolved" or
"closed": resolved is what happens to an objection. Solving needs no decision – most topics end in the
conversation.

## Conversation

| EN | DE | Tools / API |
| --- | --- | --- |
| Thread, post, reply, reaction | Thread, Beitrag, Antwort, Reaktion | `post`, `reply_to`, `reaction` |
| Mention | Erwähnung | `@[Full Name]` |
| Document | Dokument | `document` |
| Protocol (a discussion written up as a document) | Protokoll | – |
| Section (of a document or record) | Abschnitt | `section` |
| Comment (on a document) | Kommentar | – |

## Proposals and decisions

| EN | DE | Tools / API |
| --- | --- | --- |
| Question (gathers proposals) | Frage | `proposal_collection` |
| Proposal | Vorschlag | `proposal` |
| Option (what a decision chooses between) | Option, Entscheidungsoption | `option` |
| Description (of a proposal) / Note (on a task) | Beschreibung / Notiz | `description` |
| Decision, method (mode), procedure | Entscheidung, Methode (Entscheidungsmodus), Verfahren | `decision`, `decision_mode` |
| Binding / Pulse check / Experiment | Verbindlich / Stimmungsbild / Experiment | – |
| Together / On behalf of | Gemeinsam / Stellvertretend | – |
| I decide / Assign directly / Nomination round (who decides on behalf) | Ich entscheide / Direkt zuweisen / Nominierungsrunde | – |
| Remix (a new decision from a finished one) | Remix | – |
| Objection / Veto / Step aside / Alternative | Einwand / Veto / Beiseitetreten / Alternative | `objection` / `veto` / `step_aside` / – |
| Objection pending | Einwand offen | – |
| Insight (consultation input) | Perspektive | `consult` |
| Clarifying question (role-based) | Verständnisfrage | `question` |
| Feedback (after a decision finished) | Feedback | `comment` |
| None of these | Nichts davon | – |
| Quorum, required majority, points budget, disqualifying resistance value | Quorum, nötige Mehrheit, Punktebudget, disqualifizierender Widerstandswert | – |

*Vorschlag* is only ever a proposal. What a decision chooses between is an
*Option*. The eight decision modes and their German names are in
`decision-modes.md`.

## Tasks

| EN | DE | Tools / API |
| --- | --- | --- |
| Task | Aufgabe | `task` |
| Open / In Progress / Completed / Discarded | Offen / In Bearbeitung / Erledigt / Verworfen | `open` / `in_progress` / `completed` / `cancelled` |
| Unassigned | Nicht delegiert | – |

## Records (ODRs)

| EN | DE | Tools / API |
| --- | --- | --- |
| ODR (Organizational Decision Record) | ODR | `record` |
| Register (all ODRs of a workspace) | ODRs | `list_records` |
| Valid | Gültig | `in_force` |
| Superseded | Abgelöst | `superseded` |
| Publish | Veröffentlichen | – |
| Draft | Entwurf | – |
| My drafts (where drafts wait, visible to their author only) | Meine Entwürfe | `list_record_drafts` |
| Replaces (on publishing) | Löst ab | `supersedes` |
| Decided on, Source | Entschieden am, Quelle | `decided_at`, `source_url` |
| Context / Decision / Consequences / Rejected options (sections) | Kontext / Entscheidung / Konsequenzen / Verworfene Optionen | `context` / `decision` / `consequences` / `rejected_options` |

An ODR is what the workspace has settled: numbered, published out of a
decision or brought in from outside, and from then on readable by the whole
workspace. Nothing in the register is deleted or rewritten. An ODR that no
longer holds is **superseded** by a newer one, and both stay readable. People
say *gültig* / *valid*; the tools say `in_force`. Don't call an ODR "active",
"current", "replaced" or "outdated", and don't call it a document or a
protocol.

## Workspace

| EN | DE | Tools / API |
| --- | --- | --- |
| Workspace | Workspace | `workspace` |
| Group, Project group | Gruppe, Projektgruppe | `group`, `is_project` |
| Co-creating (anyone in a topic's groups) | Mitgestalten / Mitgestaltende | co-create |
| Settings → Integrations | Einstellungen → Integrationen | – |
| API access, MCP access (switches there, for workspace managers) | API-Zugriff, MCP-Zugriff | – |
| Security and Access → Connected apps, Disconnect | Sicherheit und Zugriff → Verbundene Apps, Trennen | – |
| Terminate all sessions | Alle Sitzungen beenden | – |
| Read only / Read and write (on the consent page) | Nur lesen / Lesen und schreiben | – |
| Inbox, Tasks, Saved, Archive | Eingang, Aufgaben, Gespeichert, Archiv | – |

## Slash commands

In the composer, EN → DE where they differ: /decision, /question, /proposal
(/vorschlag), /task (/aufgabe), /file, /related, /blocker, /blocking
(/blockiert), /duplicate, /group, /project, /people, /priority (/prio), /due
(/frist), /tag.
