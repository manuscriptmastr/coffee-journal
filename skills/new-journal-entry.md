# Skill: new-journal-entry

**Trigger**: User asks to create a new journal entry for a specific coffee (e.g., "make me an entry for X", "add an entry for Y", "log a brew for Z").

Maintainers fill in tasting notes themselves after brewing. Agents only write the header.

## Step 2: Re-read the journal tail immediately before appending

**Mandatory and non-skippable, even if you just read the file earlier in the same session.**

Before writing the new header:

1. **Read the last ~20 lines of the target journal file** with a fresh Read call (offset = file length − 20 or thereabouts). Don't trust your in-memory model of the tail from earlier in the conversation; the user may have edited the file, added notes, or you may have appended an earlier header that you've since forgotten about.
2. **Verify the file ends with either** (a) a fully-noted, fully-scored prior entry, or (b) a still-blank header from a prior turn that the user has not yet brewed. Both states are normal; both require different append behavior.
3. **Choose the insertion point**:
   - If the file ends with a fully-noted prior entry → append the new header at end-of-file (after a blank line separator).
   - **If the file ends with one or more still-blank headers** → STOP. Do NOT append a new header above them. Either:
     - Ask the user which still-pending header takes priority and whether the new one should replace or follow it; or
     - Append the new header strictly **after** the trailing blank headers so the chronological-append invariant holds.
4. **Construct the Edit `oldString` from the literal trailing N lines of the file you just re-read**, not from memory of an earlier file state. The `oldString` must reflect the file's current tail exactly. If your `oldString` includes prose body text from an earlier entry but the file has since gained a blank header below that text, the Edit will silently insert in the wrong place.

**Failure mode this guards against**: a still-unbrewed header from a prior turn becomes a "trapped" header sitting above the new insertion. The user then writes notes assuming the latest header is the one they brewed, but the notes end up attached to whichever header the file actually placed at the bottom. The notes-to-coffee mapping breaks, and recovery requires asking the user which coffee they actually brewed — contaminating both the journal and the calibration data.

## Step 3: Predict the grind setting

Before writing anything, run the prediction workflow from the `predict-grind` skill (or its equivalent procedure in `AGENT_GUIDE.md` §"Agent Quick-Start"). You need a specific predicted grind value and Day number to write a meaningful header.

**Always look up the current date programmatically — every time, no exceptions.** Run `date` (or your environment's equivalent shell call) before deriving Day N. Do **not** trust the "Today's date" line in your system prompt / environment block, your own arithmetic from earlier in the conversation, or the date implied by the most recent journal entry. Multi-turn sessions can cross midnight; environment dates can be stale or wrong.

**Day N is always `(today − roast_date)` in calendar days** — never copied from the Day label of the most recent sibling entry sitting above your insertion point. Sibling labels can be off-by-one from a prior mislabeled session; if they disagree with the calendar math, the calendar wins and the new entry uses the correct Day N even when it doesn't match the siblings immediately above. The roast date is in the journal's `profile.md` (per-batch) or can be back-derived: `roast_date = entry_calendar_date − entry_Day_N` from any prior batch-mate whose calendar date is known.

## Step 4: Write only the header line

Append a single header line to the journal file (e.g., `joshua-martin/Coffee Journal.md`), matching the journal's format. For Joshua's journal:

```
## CoffeeName, Brewer, GrindSetting @ Temp, Dose/Water Day X, Score:
```

- Leave the **Score blank** (the user hasn't brewed it yet).
- Leave the **body empty** — **do not** write tasting notes, prediction rationale, bracket plans, or commentary in the entry body. The body is the maintainer's space for their own notes after they brew.
- Preserve existing entries; append at the end (or in date order if the journal is strictly chronological — check the neighboring entries).

## Step 3: Share reasoning in chat, not in the file

Your prediction rationale — drift math, anchors, guardrails, what vocabulary would confirm or falsify the call — goes in the **chat response**, not in the entry body.

## Why this convention

- The journal is the maintainer's record of _their own_ sensory experience. Agent commentary in the body contaminates that signal and skews later calibration (holdout tests, vocabulary lift analyses, drift fits).
- Reasoning in chat remains available to the user for discussion but doesn't leak into the data.
- Future agents reading the journal for pattern-mining treat every non-header line as maintainer-authored; mixing in agent-authored prose breaks that assumption.

## Cross-journal note

This convention is universal across this repo's journals, but entry-header formats differ per journal (some use prose Markdown headers; others use CSV rows). Check the journal's existing entries before writing the first line, and match its format exactly.
