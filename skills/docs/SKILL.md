---
name: docs
description: Answer how Rhizome works – topics, decisions and the eight decision modes, proposals, tasks, documents, groups, notifications, settings, integrations, the API – from the current Rhizome documentation, with links to the exact sections. Use whenever someone asks how something in Rhizome works, what a Rhizome term means, which decision mode fits, or where a setting is – also in German („Wie funktioniert … in Rhizome?“, „Was ist ein Konsent?“, „Wo stelle ich … ein?“, „Was bedeutet Widerstandsabfrage?“) – even if they don't mention the docs.
license: Apache-2.0
compatibility: Python 3 and network access to docs.get-rhizome.app.
---

# Rhizome docs

Answer from the **current** documentation at docs.get-rhizome.app, and link
every claim to the section it comes from. No copy of the docs ships with this
plugin: the script below reads the live search index.

## 1. Pick the language

The German docs (`/de`) are the original; the English ones (`/en`) are a
translation of them. Search in the language the person writes in: German
question → `--lang de`, English question → `--lang en`. Any other language →
search the German docs and answer in the person's language.

## 2. Search

The script is `scripts/search.py`, relative to this skill's folder. It needs
Python 3, standard library only.

```bash
python3 scripts/search.py "Wie funktioniert Konsent?" --lang de
```

It prints the best sections, each with its anchor URL, breadcrumb and text.
The docs server can take half a minute to answer; wait for it rather than
retrying.

- Search with the question's subject words in the docs' language – the German
  UI terms (`references/vocabulary.md`) find German sections: „Punkteverteilung“,
  not "dot poll", in `/de`.
- If the top hits miss, search once or twice more with other words (the
  concept's German name, a broader term) before concluding the docs don't say.
- `--limit` shows more sections, `--chars` more of each.

## 3. Answer

- Answer in a few sentences from the sections' text, in the docs' own terms,
  and link each section you used: `[Konsent](https://docs.get-rhizome.app/de/funktionen/entscheidungsmodi/konsent/)`.
  Use the printed URLs verbatim; never build one yourself.
- The English docs are a translation and sometimes use other words than the
  app ("resolved" for what the app calls *Settled*). Name things as the app
  does (`references/vocabulary.md`), so the person finds the button.
- Say only what the sections say. If none covers the question, say that the
  docs don't answer it and link the nearest section. ODRs are not in the docs
  yet: explain them from `references/vocabulary.md`, and say that this comes
  from the plugin, not the docs.
- A question about the person's own workspace – "which topics are waiting on
  me?" – is not a docs question. Use the Rhizome tools for it.

If the script fails to reach the docs, say so and give
https://docs.get-rhizome.app/de/ (or `/en/`) as the place to look. Don't answer
from memory as if it were the docs.

`python3 scripts/search.py check` is the
script's self-check: known questions in both languages must find their pages.

## Shared references

This skill also carries the references every Rhizome skill writes by. Every
other skill carries its own copy in its `references/` folder:

| File | What's in it |
| --- | --- |
| `references/vocabulary.md` | German ↔ English terms, and the value the tools use, including ODR, gültig / in force and abgelöst / superseded |
| `references/conventions.md` | Draft before write, `@[Full Name]`, local time, markdown that fits the editor, refusals |
| `references/decision-modes.md` | The eight decision modes: when each fits, how many options, what people respond with |
