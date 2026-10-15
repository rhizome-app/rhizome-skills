---
name: draft-minutes
description: Write up a Rhizome topic's discussion as minutes – a new document on the topic with what was discussed, what came out of it and what is still open – and offer to turn the open points into tasks. Shows everything as a draft and writes only after an OK. Use when someone wants minutes, a summary, a protocol or a write-up of a Rhizome topic or its conversation, or wants absent colleagues to catch up – also in German („Protokoll“, „Fass das Thema zusammen“, „Protokolliere die Diskussion“, „Zusammenfassung für die, die nicht dabei waren“, „offene Punkte als Aufgaben“).
license: Apache-2.0
compatibility: Needs the Rhizome MCP server connected (the setup skill checks it).
---

# Rhizome minutes

Turn a topic's conversation into minutes: one new document on the topic, and,
if the person wants, a task per open point. Nothing is written before the
person has seen the draft and said yes.

Read first:

- `references/conventions.md` – draft before
  write, mentions, times, the markdown documents and tasks hold, refusals.
- `references/vocabulary.md` – say *post*, *proposal*, *option*, *task*,
  *settled* (in German *Beitrag*, *Vorschlag*, *Option*, *Aufgabe*,
  *geklärt*) as the app does.

## 1. Find the topic

If the person gives no topic id, find it with `list_topics` (`q` = words from
its title). Several match → ask which one; don't guess.

## 2. Read the whole conversation

`read_topic` gives the documents, proposals, decisions and only the **newest
25 posts**. Minutes of those 25 alone are wrong for a longer topic.

- If its answer ends with `Older posts: read_posts(…)`, call exactly that, and
  keep calling the `read_posts(…)` each answer ends with, until one says
  `Nothing older.` or `No older posts.`
- Read every page before drafting. Each page comes oldest first, and the
  pages go back in time: the earliest page you read is the start of the
  conversation.

## 3. Draft the minutes

A **new** document with `create_document` – never `append_to_document`, which
refuses protocols, and never over an existing document.

**Title:** `Minutes: <Topic title>` (German: `Protokoll: <Topic title>`),
shortened if long.

**Content**, in the workspace's language and in the markdown documents hold
(conventions.md): sections under `##` only – the title is the document's own,
so no `#` – with bulleted lists:

- `## What it is about` (`## Worum es geht`) – the question in two or three
  sentences.
- `## Discussion` (`## Verlauf`) – the main lines of argument, in order, with
  who brought them. Names as plain text, not `@[Full Name]`: minutes would
  otherwise notify everyone they name. Summarise, don't retell each post.
- `## Outcomes` (`## Ergebnisse`) – what was agreed, proposals made, decisions
  and how they stand, the conclusion if the topic is settled. Only what the
  conversation shows; nothing agreed → say so.
- `## Open points` (`## Offene Punkte`) – what is unanswered, undecided or
  promised but not done. One bullet each, phrased so someone could act on it.

State only what the posts say. No evaluation of who was right, no outcome
the group didn't reach. An offer stays an offer ("Rosa offered to write the
guide"), not a result ("Rosa writes the guide").

## 4. Offer the open points as tasks

Under the draft, list the open points again as **task drafts**: a title (one
line, what is to be done) and, if useful, a short note. Leave out a point a
task already carries: the posts show those as "… opened the task **…**".

**Never propose who does it.** Not from who raised the point, not from who
volunteered in a post, not from roles. Every task draft is *unassigned*
(*nicht delegiert*) until the person names someone. Ask: "Shall I turn these
into tasks? If so, tell me who takes which." A name they give is
resolved by the tool; if it matches nobody or several people, pass the
tool's sentence on and ask. A deadline only when the person gives one.

## 5. Show, then write

Show the full draft – document title and text, then the task list with the
assignee each has (or *unassigned*) – and ask for an OK. Changes go into
the draft and it is shown again. Then:

1. After an OK for the minutes: `create_document(topic_id, title, content)`.
2. After an OK for the tasks – a separate question, the person may want the
   minutes only, or only some tasks: one `create_task` per approved task,
   with `assignee` only if the person named one for it.

A yes to the minutes is not a yes to the tasks. Tasks the person didn't approve
are not written.

Report what was written with the links the tools answer with. Refusals and
errors as in conventions.md: after a failed write, `read_topic` before writing
again, so nothing lands twice.
