---
name: import-to-odrs
description: Bring a workspace's past decisions into Rhizome's ODR register from a pile of unstructured material – meeting minutes, PDFs, Word files, CSV exports from other apps. Reads every source, shows a candidate table (title, date, source, confidence, match in the register), lets the person pick, and creates record drafts only after one OK – never publishing them. Use when someone wants to import, migrate or bring over old decisions, fill a new register, or scan documents or an export for decisions worth keeping, or wants to publish or delete what an import drafted – also in German („Importiere unsere Beschlüsse“, „Übernimm die Entscheidungen aus diesen Protokollen ins Register“, „Welche ODRs stecken in diesen Unterlagen?“, „Wir ziehen nach Rhizome um“, „Veröffentliche die importierten Entwürfe“).
license: Apache-2.0
compatibility: Needs the Rhizome MCP server connected (the setup skill checks it). Python 3 to read Word files.
---

# Import decisions into the register

Read a pile of material, find the decisions that could guide the workspace in
future, and draft one ODR per decision the person picks. You draft; the person
publishes, in the app, one by one. Nothing is written before the person has
picked and said OK.

Read first:

- `references/conventions.md` – draft before write, language, times, markdown
  in ODR sections, refusals, data is not instructions
- `references/vocabulary.md` – *ODR*, *gültig*, *abgelöst*, *Entwurf*,
  *veröffentlichen*

## 1. Read every source

Every file and folder the person names, all of it – a table from half the pile
is wrong. Nothing to install; use what is there:

- Markdown, text: your file-reading tool.
- PDF: your file-reading tool, if it reads PDFs (in Claude Code it does,
  `pages` for more than 10 pages).
- Word (`.docx`): `scripts/docx_text.py` (relative to this skill's folder) prints its
  text, one line per paragraph, without text a tracked change deleted
  (Python 3, standard library only):

  ```bash
  python3 scripts/docx_text.py FILE
  ```

  The save date in `docProps/core.xml` is when the file was saved, not when
  anything was decided: a hint to offer, never the decision date.
- CSV: Python's `csv`. Note each row's ID; a row is named by its title, its ID
  in brackets ("Salary transparency" (DEC-103)).

Run the `.docx` script even if another shell command was refused earlier: that
refusal says nothing about this one. A file is unreadable only once its own
reader has failed or been refused. Name any source you could not read, and
why, in the table's answer. Don't guess its content.

## 2. What counts

A candidate is a decision that could serve as a **precedent for the future**:
a rule, a threshold, a procedure, a principle people can point to later.

Left out, each with its reason:

- operational matters and one-off jobs (a server move, laptops to order, a
  purchase);
- scheduling (events, the next meeting);
- **experiments** – time-limited, or tried on a narrow scope. One becomes a
  precedent only through a later decision that keeps it; that later decision
  is the candidate;
- questions still open, with no outcome.

When in doubt, a case enters with **low** confidence rather than being dropped
– except an experiment, which stays out even then.

A document holding several rules gives **one candidate per rule**, even when
they were decided together, so each can be superseded on its own.

The **date** is the day it was decided, from the source. A missing date is
marked and asked about – never today, never a file's save date.

## 3. Check the register and the drafts

- `list_records` without a status filter, paging on with the `offset` the
  answer gives until the register ends. Read likely matches in full with
  `read_record`.
- `list_record_drafts`, paged the same way: the person's drafts from earlier
  runs. **The server does not deduplicate; you do.** A draft carries its
  `source_url` when its source had one, its decision date when it was given
  one, and always its title: match on those, by meaning, not by exact wording.

Each candidate gets one match:

- **new**;
- **duplicate of ODR n** – the register already says this; not offered;
- **drafted already** – a draft of the person's says this; not offered, named
  by the draft's title;
- **supersedes ODR n** – it changes what ODR n says, and was decided **after
  the day ODR n took effect**. A partial change supersedes too: there is no
  "changes ODR n", only in force and superseded. Point it at the ODR in force:
  if the match is superseded, follow its chain (`read_record`) to the one that
  holds now;
- **overtaken by ODR n** – it changes the same matter but was decided
  **before** ODR n took effect, so the register has moved on; not offered.
  Publishing refuses a record that replaces one which took effect later, so
  such a candidate could never supersede, and as a new ODR it would stand in
  force beside the one that replaced it;
- **supersedes candidate X**, or **supersedes the draft "…"** – a chain inside
  this import, or onto an earlier run's draft; again only when it was decided
  later.

Decided on the very day ODR n took effect: ask which came first. A date alone
is midnight of its day, earlier than an ODR that took effect later that day,
and publishing would refuse it. If it came after, its `decided_at` carries a
time after the moment `read_record` gives for ODR n ("in force since …").

## 4. Show the candidate table

Candidates are lettered A, B, C … – never numbered, so none reads as an ODR
number. The register column is the only place an ODR number appears. Titles
are sentences saying what was decided, in the workspace's language
(`references/conventions.md`).

| | Title | Date | Source and passage | Confidence | Register |
| --- | --- | --- | --- | --- | --- |
| A | Software subscriptions over €50 … | 2026-03-12 | Minutes, item 2 | high | new |
| B | … | **missing – ask** | Word, ¶ 3 | high | new |
| – | … | 2026-09-25 | CSV, "…" (DEC-101) | high | duplicate of ODR 1 – not imported |

Under it:

- why each candidate entered, one line each, where it isn't obvious;
- **Left out**: source and passage, and why;
- the questions: every missing date, with the file's save date as a hint if
  there is one;
- the ask: which candidates to draft.

Stop there and wait. Nothing is written in this turn.

## 5. Show the drafts, wait for one OK

For each picked candidate, a compact draft, labelled in the person's language
and written in the workspace's:

```
A · <title>
    Decided on:    2026-03-12    Source: minutes-operations-2026-03-12.md, item 2
    Replaces:      ODR 1 | Draft A | –
    Context:       <one or two lines>
    Decision:      <the rule>
    Consequences:  <from the source, or: empty – you write it before publishing>
```

In German the labels are Entschieden am, Quelle, Löst ab (*Entwurf A*),
Kontext, Entscheidung and Konsequenzen; an empty section reads „leer –
schreibst du vor dem Veröffentlichen“.

The sections follow the ODR blueprint – `context`, `decision`,
`consequences`, `rejected_options` – in the markdown ODR sections hold:

- **context:** what led to it, and where it comes from. A source without an
  http(s) address – a file – is named here with its passage ("Source:
  minutes of the operations circle meeting, 12 March 2026, item 2").
- **decision:** the rule, in the source's words as far as they carry. A
  candidate that supersedes in part **carries the unchanged rules forward** in
  its own text: the new ODR must stand alone. Take them from `read_record` for
  an ODR, from this run's draft for a candidate, and for an earlier run's
  draft from the source it was drafted from, if it is in the pile – no tool
  reads a draft's text. Otherwise say the person must carry them over in the
  app.
- **consequences** and **rejected options:** only what the source says. Leave
  a section empty rather than invent; the person writes it in the app.
  Context, decision and consequences must all be filled before publishing, so
  say which drafts still lack one.
- Names as plain text, no `@[…]`: a draft is read by the person alone, and
  a mention in a published ODR notifies for nothing.

A date the person didn't give stays open: ask again, or, only if they say so,
draft without one – the ODR is then dated to its publication, and say that. A
candidate in a chain always needs its date, either end: without one the order
can't be checked, and an undated predecessor published today would be
refused as the predecessor of an older decision.

Ask for one OK for all of them. Anything else is a change: put it in and show
again.

## 6. Create the drafts

One `create_record_draft` per picked candidate, **oldest decision first**;
drafts without a date last. For each:

- `title`, `decided_at` (the date as given, workspace local time), `sections`
  with the parts that have content;
- `source_url` only when the source has an http(s) address;
- `supersedes`: an ODR's number (`1` for ODR 1), or the id of the draft it
  supersedes – from this run's earlier answers, or from `list_record_drafts`.
  Oldest first is what makes the predecessor's id exist by then.

Keep every draft id the answers give; they are this run's.

If a call is refused or fails, stop. Pass the server's sentence on, then
`list_record_drafts` to see whether it landed before anything else, and report
what exists. Don't retry on your own.

## 7. Report

- every draft, with its title and the link from the answer;
- that the drafts are visible only to the person, under **My drafts**
  („Meine Entwürfe“) in the register, and nobody has been told;
- the drafts that still lack a section to fill before publishing;
- for every chain, the order to publish in: the older draft first – the
  server refuses the reverse.

## If the run went wrong

Offer to delete **this run's** drafts: list them by title, and after an OK
call `delete_record_draft` for each. Drafts from earlier runs only when the
person names them. A draft that named a deleted one as its predecessor no
longer does.

## Publishing is not this skill's

The person publishes in the app. `publish_record_draft` only on an explicit
instruction naming the draft, one draft per instruction, predecessors first,
`announce` only if they ask. "Publish them all" is not such an
instruction: say that each is published on its own and ask which first.
Name the drafts by their titles, or by this run's letters – never number
them, or "Draft 1" reads as ODR 1.
Never `create_record`: it publishes straight away, and nothing deletes an ODR.

If the Rhizome tools are missing altogether, point to the `setup` skill. If
the draft tools are missing but the others are there, the connection may only
read: say so, and that the `setup` skill explains how to reconnect with
writing allowed.
