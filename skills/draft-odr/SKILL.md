---
name: draft-odr
description: Turn one decision taken outside Rhizome – in a meeting, a mail, a chat, a ticket – into an ODR draft that the person reviews and publishes themselves. Checks the register for duplicates and records it would supersede, checks the person's own drafts so a source isn't drafted twice, writes context, decision and consequences, and asks for the decision date instead of guessing it. Use when someone wants to record, document or bring into the register a decision made elsewhere, or hands over minutes, a mail or a link and says what was decided – also in German („Mach daraus ein ODR“, „Trag das ins Register ein“, „Wir haben im Meeting beschlossen, dass …“, „Halte diese Entscheidung als ODR fest“, „ODR-Entwurf aus dieser Mail“). For a pile of material with many decisions, use import-to-odrs instead.
license: Apache-2.0
compatibility: Needs the Rhizome MCP server connected (the setup skill checks it).
---

# Draft an ODR

Someone decided something outside Rhizome and wants it in the register. You
draft the ODR; the person publishes it. A published ODR has a number, can't be
deleted and reaches the whole workspace, so it is theirs to publish, in the
app, after reading it there.

What you create is a draft (the tools: record draft): unnumbered, visible to
the person alone, and nobody is notified. It waits under **Meine Entwürfe** / **My
drafts** in the register until the person publishes or deletes it.

Read these first; this skill doesn't repeat them:

- `references/conventions.md` – draft before
  write, language, mentions, times, markdown for ODR sections, refusals
- `references/vocabulary.md` – *ODR*,
  *gültig* / *valid*, *abgelöst* / *superseded*, *Entwurf* / *draft*

## 1. Take in the decision

Read what the person gives you: their account, pasted text, a file, a link.
Find in it:

- **what was decided** – one decision. If the source holds several, say so and
  ask which one to draft; each rule becomes its own ODR, so each can be
  superseded on its own. Many decisions at once are `import-to-odrs`' job.
- **when it was decided** – the date of the decision, not of the mail that
  reports it, the file's save date or today.
- **why** – the situation that led to it.
- **what follows** – duties, limits, who does what, what changes.
- **what was rejected** – other options that were on the table, and why not.
- **where** – the source. A link counts only if it is `http://` or `https://`.

Is it an ODR at all? An ODR is what could serve as a precedent: a rule, a
standing agreement, a direction. A one-off task, an appointment or an
experiment ("we're trying it until June …") is not – say so and don't draft it,
unless the person insists. An experiment becomes an ODR once a later decision
keeps it.

## 2. Check the register and your drafts

Do both before drafting, and report what you found in one short block before
the draft.

**The register.** Call `list_records` – no status filter, so superseded ODRs
count too – and page on with the `offset` the answer gives until it ends. Read
the titles against the decision, generously: there is no text search. Read
the likely ones in full with `read_record`. Then name each hit as one of:

- **Duplicate** – a valid ODR says the same. Stop and say so, with its number,
  title and link; draft nothing unless the person still wants it. A superseded
  ODR saying the same is no duplicate: the matter was decided again, and the
  draft supersedes whatever holds now.
- **Supersedes** – the new decision supersedes a valid ODR, fully or in part. A
  partial change supersedes too: the register knows only valid and superseded,
  no "amends". The new draft then carries the old ODR's unchanged rules forward
  in its own text, so it holds on its own once published. Name the ODR by
  number in `supersedes`, and say so in the draft.
- **Related** – touches the same matter without changing it. Worth a sentence
  in the context section, not a supersession.

If nothing fits, say so in one line.

**Your drafts.** Call `list_record_drafts` (page on the same way). A draft
whose `from <…>` matches the source link, or whose title says the same, means
this source is drafted already: say so, name the draft, and offer to revise
that one instead of creating a second. A draft of yours that the new one
supersedes goes into `supersedes` by its id.

## 3. Ask for the date if it is missing

`decided_at` dates the ODR. Without it, the record is dated to the moment it is
published – wrong for history, and nobody notices later. So when the source
gives no decision date, **ask**. Never fill in today, the mail's send date or a
file's save date; you may offer a date you found as a hint ("The file was saved
on 14 August – was that the day of the decision?"). Only a date the person
gives or the source states goes into the draft. If the person doesn't know
it either, create the draft without a date only when they say so, and tell
them to set it in the app before publishing.

## 4. Write the draft

Title: what was decided, as one sentence – "Anyone makes purchases up to
€1,000 without asking", not "Purchases".

The sections, keyed as the tools take them:

| Key | DE | EN | |
| --- | --- | --- | --- |
| `context` | Kontext | Context | required |
| `decision` | Entscheidung | Decision | required |
| `consequences` | Konsequenzen | Consequences | required |
| `rejected_options` | Verworfene Optionen | Rejected options | only if the source names some |

- Write only what the source says. Where it says nothing about a required part,
  leave it empty and say so in the draft – the person fills it in the app. Don't
  invent reasons or consequences to make a section look complete.
- `context`: why it was decided, who decided (the body – "the operations circle" –
  rather than a list of names), and where. For a source without an http(s)
  link, name it here: file and passage, or "mail from … of …".
- `decision`: the rule itself, precise – amounts, roles, deadlines as the
  source states them, not rounded.
- `consequences`: what changes, for whom, from when.
- Markdown and language as `conventions.md` says for ODR sections. One
  exception to its mention rule: write names as plain text, no `@[…]` – a
  draft is read by the person alone, and a mention in a published ODR
  notifies for nothing.

## 5. Show the draft, wait for the OK

Show everything that will be written, labelled in the person's language:

```
Title:          <title>
Decided on:     <date>
Source:         <http(s) link> | none (file and passage are in the context)
Replaces:       ODR 4 "…" (partly – takes over …)  | –
Context:        <text>
Decision:       <text>
Consequences:   <text> | empty – please fill in in the app
Rejected:       <text>   (only if there are any)
```

In German the labels are Titel, Entschieden am, Quelle (*keine*), Löst ab
(*teilweise*), and the section names from the table above; an empty section
reads „leer – bitte in der App ergänzen“.

Then ask whether to create the draft. Create it only on a clear yes – "ok",
"yes", "looks good". Anything else is a change: put it in and show the draft again.

## 6. Create the draft

Call `create_record_draft` once, with exactly the approved draft: `title`,
`sections`, `decided_at`, `source_url` only for an http(s) link, `supersedes`
only when step 2 found something.

Report in two or three lines: that the draft exists, visible only to the
person and with nobody notified; the link to the draft from the answer; and
that they review and publish it there, under **My drafts** („Meine
Entwürfe“). If the answer says parts are still empty, name them. If it suggests
a rewrite in the workspace's language, offer it once.

A refusal is passed on as `conventions.md` says, not retried. If the call
fails without a refusal – a timeout, a dropped connection – call
`list_record_drafts` before trying again: it may have landed.

## 7. Afterwards: revise, delete, publish

- **Changes** the person asks for in the chat: show the changed parts, and on
  the OK call `update_record_draft` with only those. Never a second draft for
  the same decision. The tool can't clear a field (a date, a source link); the
  person does that in the app.
- **Rejected** ("discard it", "delete the draft"): `delete_record_draft`,
  and say it is gone.
- **Publish** only when the person explicitly says to publish **this** draft
  ("publish the draft on the mobility rule"). Then
  `publish_record_draft` with `announce=false`: an import is history, and a
  notification to everyone is the person's call – set `announce=true` only
  when they ask for it. Report its number and link. Without such an instruction, the draft stays a draft: "looks good"
  about the draft's text is an OK to create it, not to publish it.

## Never

`create_record`. It publishes straight into the register, numbered and
undeletable, with no draft in between. Not even when the person says "put it
straight into the register": create the draft and offer to publish it with
`publish_record_draft`.

If the Rhizome tools are missing altogether, point to the `setup` skill. If
the draft tools are missing but the others are there, the connection may only
read: say so, and that the `setup` skill explains how to reconnect with
writing allowed.
