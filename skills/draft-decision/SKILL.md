---
name: draft-decision
description: Prepare a decision in a Rhizome topic – check the ODR register first, read the topic, suggest the decision mode that fits with a one-line reason, phrase the options from the discussion and its proposals, and open the decision only after the person approves the draft. Use when someone wants to decide something in Rhizome, start or set up a decision, a vote, a consent or a poll in a topic, or asks which mode fits a topic – also in German („Entscheidung vorbereiten“, „Lass uns darüber abstimmen“, „Starte einen Konsent in Thema X“, „Welcher Entscheidungsmodus passt?“, „Mach daraus eine Entscheidung“).
license: Apache-2.0
compatibility: Needs the Rhizome MCP server connected (the setup skill checks it).
---

# Draft a decision

Turn a topic's discussion into a decision the person approves and opens. You
draft; the person decides whether it opens, because it opens in their name and
notifies everybody in the topic.

Read these first; this skill doesn't repeat them:

- `references/decision-modes.md` – the modes,
  their option counts, what each fits
- `references/conventions.md` – draft before
  write, language, mentions, times, markdown, refusals
- `references/vocabulary.md` – the words, in
  both languages

## 0. Sparring or ready?

Make the sparring offer (`conventions.md`, *Sparring offer*) as your first
answer – before any Rhizome tool, not even a lookup of the topic or the
register; those come after the person's answer. The mirror's
entry point is "an important decision in a topic".

## 1. Find the topic

Take the topic the person names or links. If it is only described, look it up
with `list_topics`, and ask when more than one fits: a decision in the wrong
topic notifies the wrong people.

## 2. Check the register

Call `list_records` with `status=in_force` and read the titles against the
question. Read the likely ones in full with `read_record`. Page on with the
`offset` the answer gives until the register ends.

If a valid ODR already settles the question, **stop and say so before
drafting**: its number, its title and what it says in one sentence. The
register is what the workspace has settled; a parallel decision would
contradict it without anyone noticing. Ask whether they want to revisit it.
Only on a yes go on, and name the ODR in the draft so everybody sees what is
at stake. An ODR that merely touches the question is worth a line in the
draft, not a stop.

If nothing in the register fits, say so in one line.

## 3. Read the topic

Call `read_topic`. If the conversation goes further back than the answer shows
and the older posts may matter, read on with `read_posts`. Note:

- the proposals, and the question (`proposal_collection`) they answer – the
  options' first source;
- what people argued for and against, and who;
- the topic's groups – they are who will be asked to take part;
- decisions on the topic already. A decision still running on the same
  question means there is nothing to draft: point to it. Adding options to it
  would change what people are already responding to.

If the topic is settled or archived, say that a decision can't open there.

## 4. Choose the mode

Pick from `decision-modes.md`: **the question first, the number of options
second** – a mode that fits the count but not the question is wrong. Give the
reason in one sentence that names what in this topic makes the mode fit:

> Consent, because it is about a process you can try out and change later,
> and there is a worked-out proposal.

If two modes fit, name the other and when it would be better. If the person
names a mode, use it; object only when it breaks a hard limit or clearly
misfits.

## 5. Phrase the options

- Build them from the proposals and the discussion, in the words people used,
  and say where each comes from ("from Mara's proposal"). Mark an option
  nobody raised as yours, so the person doesn't mistake it for the group's.
- Keep to the mode's option count in `decision-modes.md`. Consent and
  consensus carry **exactly one** option: if several proposals compete, merge
  them into the one the discussion supports, or suggest a mode with several
  options and say why. Equally, a voting mode needs at least two options:
  with one there is nothing to choose.
- Consent, consensus, Insight process (`advice`) and role-based carry one
  option: the proposal, or what the decider is asked to decide.
- An option's title is one short line; detail goes in its description.
- The title says what is being decided, usually as a question. Consent and
  consensus take no title: theirs is their option's.

## 6. Name who decides

The Insight process (`advice`) and role-based need a decider. **Ask the person
who it is**; suggest someone only when the topic says whose remit it is, and
say why. Without a decider nobody can conclude these modes, so never open one
without. The decider must be able to work in the topic, or the tool refuses.

A role-based decision the person takes themselves is a decision already made,
not one to open, and the tools can't record it. Tell them to post it in the
app as a decision they take, or to choose the Insight process to hear others
first.

## 7. End date

Set `end_at` **only when the person gives a date** – a date they didn't choose
closes the decision on people unexpectedly. Otherwise leave it out and say that
the decision runs until it is closed.

## 8. Show the draft, wait for the OK

Show everything that will be written, labelled in the draft's language:

```
Topic:        <title of the topic>
Groups:       <the topic's groups>
Method:       Consent – <the reason>
Title:        <title>                (not for consent and consensus)
Option 1:     <title>
              <description>
Decides:      @[Full Name]           (Insight process and role-based)
Ends:         <date> | open
ODR:          puts ODR 12 "…" up for review   (only if step 2 found one)
```

In German the labels are Thema, Gruppen, Methode, Titel, Option, Entscheidet,
Ende (*offen*), and the ODR line reads `stellt ODR 12 „…“ zur Prüfung`; the
method takes its German name from `references/decision-modes.md`.

Then ask plainly whether to open it. Open it only on an explicit yes – "ok",
"yes, start it", "go". Anything else is a change: put it into the draft and show
it again. Settings the tools can't carry (binding or pulse check, experiment,
together or on behalf, a rationale) are set in the app afterwards; say so if
the person asks for them.

## 9. Open it

Call `create_decision` once, with exactly the approved draft, and give the
person the link from the answer.

If the call fails, follow the refusal rules in `conventions.md`. Before any
second attempt, `read_topic` and look for the decision: a failed write may
have landed, and a second one would open it twice.

## Not this skill's job

Voting, adding an option to a decision, raising an objection, veto or step
aside – not after opening the decision either. They speak for the person, and
the person does that themselves. Nor `create_record`: an ODR comes out of a
finished decision in the app.
