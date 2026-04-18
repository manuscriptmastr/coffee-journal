# Coffee Journal

A repo for dialing in specialty coffees through iterative prediction and measurement. It pairs a universal coffee-prediction methodology with one or more maintainers' calibrated journals.

The **goal**: predict the sweet-spot grind setting for a given coffee at a given age (days since roast). As coffee ages, CO₂ escapes and the cellular structure becomes more porous, shifting the sweet spot coarser at a roaster-specific rate. The methodology here tracks that drift and corrects for it.

## Structure

- **[`AGENT_GUIDE.md`](./AGENT_GUIDE.md)** — universal methodology: drift physics, water chemistry, extraction vocabulary, prediction method.
- **[`CLAUDE.md`](./CLAUDE.md)** — agent loader instructions.
- **Maintainers' journals** — one folder per person, each containing their `profile.md` (parameters) and their raw journal:
  - [`joshua-martin/`](./joshua-martin/) — Joshua Martin (Lagom P64, Z1/Orea, specialty light roast). Drift-based prediction applies.

## Universal illustrations

These apply to any journal:

![Coffee Compass](assets/coffee_compass.png)
![The Sweet Spot Spectrum](assets/sweet_spot_spectrum.png)

The Compass maps taste descriptors to extraction direction; the Spectrum maps the sweet-spot window, its edges, and what lies past the edges on either side.
