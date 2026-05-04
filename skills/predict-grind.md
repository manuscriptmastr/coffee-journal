# Skill: predict-grind

**Trigger**: User asks for a grind-setting prediction for a specific coffee (e.g., "what grind for X today", "predict setting for Y", "dial in Z").

This skill executes the grind-setting prediction workflow for a coffee in a maintainer's journal.

## Context to load

Before predicting, load **both**:

1. `AGENT_GUIDE.md` at the repo root — universal methodology (drift physics, vocabulary, prediction method, spiral diagnosis).
2. The `profile.md` of the journal you're predicting for (e.g., `joshua-martin/profile.md`) — that journal's numeric calibration, roaster drift rates, failure modes.

If the user hasn't named the journal, infer from context (whose coffee is it / which folder contains recent entries for this coffee) or ask.

## Prediction procedure

Follow the "Agent Quick-Start" in `AGENT_GUIDE.md` §"Agent Quick-Start: Predicting in Under a Minute". Summarized:

0. **Always look up the current date programmatically — every time, no exceptions.** Run `date` (or your environment's equivalent shell call) at the start of every prediction. Do **not** rely on:
   - The "Today's date" line in your system prompt or environment block (it can be stale across turns or initialized to a wrong value).
   - Your own date arithmetic from a remembered "yesterday" or earlier turn.
   - The date implied by the most recent journal entry.
   - The date you used earlier in the same conversation (a multi-turn session can cross midnight).

   After getting the current date, compute Day N as `(today − roast_date)` in calendar days. The roast date lives in the journal's `profile.md` (per-batch) or can be back-derived from any prior batch-mate entry whose calendar date is known: `roast_date = entry_calendar_date − entry_Day_N`. **Day N is a function of the calendar, not of sibling-entry labels.** If today's sibling entries disagree with the calendar math, the calendar wins — the siblings are mislabeled and this new entry should still use the correct Day N. Same calendar day always shares the same Day N across all batch-mates of the same roast date. Do **not** copy Day N from the most recent sibling header without verifying it against the roast date, and do **not** increment Day X blindly from the previous entry of this same coffee (gaps of multiple days are common).
1. **Find the 1–3 most recent entries for this coffee.** Any Score 5 or `**Sweet spot**` markers are anchors.
2. **Find the most recent sibling** (same roaster/batch) at a comparable or same age. A sibling cup from today at the same Day N is the strongest anchor.
3. **Apply drift** using the profile's drift table (or default ~0.020/day if unlisted; flag the assumption). If the profile disables drift-based prediction (see §"Does drift-based prediction apply to this journal?" in the guide), use the profile's static-grind strategy instead.
4. **Round to the grinder step** from the profile. On ties, round coarser **only if the last brew for this coffee was Score ≥ 4** (per profile correction-bias table); if the last was Score ≤ 3, diagnosis matters more than the coarser default.
5. **Sanity-check** against the profile's "Known failure modes" section and the guide's spiral / reference-anchor / coarse-tolerance cautions.

## Output format

Respond in chat with:

- **The prediction header line**, in the journal's format (e.g., `CoffeeName, Z, 5.825 @ 211°F, 12.5g/250g Day 24`).
- **Brief reasoning** — Day calculation, anchor(s), drift math, tiebreaker.
- **Guardrails** — what vocabulary in the resulting cup would confirm vs. falsify the prediction, and the next-step response.

## Do NOT automatically write the entry into the journal file

Writing a prediction entry into `Coffee Journal.md` (or equivalent) is a **separate** action governed by the `new-journal-entry` skill. Only do it if the user explicitly asks ("make me an entry", "add it to the journal"). When writing, follow that skill's header-only convention.

## Common pitfalls

- **Auto-incrementing Day N from the previous entry of the same coffee.** Always compute from `(today − roast_date)`.
- **Copying Day N from today's sibling-entry labels without verifying against the calendar.** Sibling labels can be wrong (carried forward from a prior session that was itself off-by-one). The roast date + today's calendar date is the source of truth; siblings are a cross-check, not the authority. If they disagree, the calendar wins and the new entry uses the correct Day N even if it doesn't match the siblings sitting just above it.
- **Using a pooled drift rate across drift regimes.** CO₂ phase, mid-life, and late-life acceleration can differ 3–5×. Identify the regime first.
- **Over-trusting the user's extraction-direction diagnosis.** Per the guide, direction calls are only ~55–70% accurate; trust descriptors and sibling data more than the direction label.
- **Treating a Score 5 setting as a "this week's" anchor.** Per Joshua's profile §10: 86% of Score-5 follow-ups within 3 days go coarser, 0% go finer. Default to "tomorrow ≈ today + one drift-step."
- **Applying drift to a journal where it doesn't apply.** Check the profile's drift-applicability verdict before reaching for the drift math.
