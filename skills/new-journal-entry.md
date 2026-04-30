# Skill: new-journal-entry

**Trigger**: User asks to create a new journal entry for a specific coffee (e.g., "make me an entry for X", "add an entry for Y", "log a brew for Z").

Maintainers fill in tasting notes themselves after brewing. Agents only write the header.

## Step 1: Predict the grind setting

Before writing anything, run the prediction workflow from the `predict-grind` skill (or its equivalent procedure in `AGENT_GUIDE.md` §"Agent Quick-Start"). You need a specific predicted grind value and Day number to write a meaningful header.

## Step 2: Write only the header line

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
