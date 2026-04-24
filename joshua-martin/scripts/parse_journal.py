"""Parse joshua-martin/Coffee Journal.md into a structured DataFrame."""
import re
import json
import sys
from pathlib import Path

import pandas as pd

JOURNAL = Path(__file__).resolve().parents[1] / "Coffee Journal.md"

# Roaster assignments from AGENT_GUIDE / profile (best-effort partial mapping).
# Use the most recent assignment for ambiguous names ("Lasso", "Pena", "Paraiso").
# Order matters: later entries can override.

ROASTER_MAP_DEFAULT = {
    # H&S
    "Pineda": "H&S", "Vista": "H&S", "Lasso Mejorado": "Paix",
    "Lopez": "H&S", "San Antonio": "H&S",
    "La Esperanza 2": "H&S", "La Esperanza": "H&S",
    "Gatomboya": "H&S", "Karani": "H&S", "Iridescence": "H&S",
    "Kiamwangi": "H&S", "Banko Taratu": "H&S", "Placer": "H&S",
    "Birthday Cake": "H&S", "Rumudamo": "H&S",
    "Trujillo": "H&S", "Lasso": "H&S", "Ninco": "H&S", "Chelbessa": "H&S",
    "Karianini": "H&S",
    # Hydrangea
    "Uberrimo": "Hydrangea", "Bolanos": "Hydrangea", "Elida": "Hydrangea",
    "Pena": "Hydrangea", "Paraiso": "Hydrangea",
    "La Isabela": "Hydrangea", "Monteblanco": "Hydrangea",
    # September
    "Morena": "September", "Bermudez": "September", "Velasco": "September",
    "Castillo": "September", "Cuenca": "September", "Ortega": "September",
    "Pintado": "September", "Danche": "September", "Chelbesa": "September",
    "White Honey": "September", "Gingerbread": "September",
    "Putushio": "September", "Tamana": "September", "Tamama": "September",
    "Buttercream": "September", "Sudan Rume": "September",
    "Fajardo": "September", "Martinez": "September", "Rojas": "September",
    # Moonwake
    "Serrato": "Moonwake", "Gomez": "Moonwake",
    "Ramirez": "Moonwake", "Benitez": "Moonwake",
    # SEY
    "Muhito": "Sey", "Dota": "Sey", "Gotiti": "Sey",
    "Botina": "Sey", "Bonita": "Sey",
    # Unknown / multi
    "Norena": "Norena",
    "Rumudamo (natural)": "H&S", "Rumudamo (washed)": "H&S",
    "Antonio": "H&S",
    "Agaro": "Sey",
    "Fazenda": "September",
}

# Per AGENT_GUIDE drift rates (per day):
DRIFT_RATES = {
    "H&S": 0.020,
    "Hydrangea": 0.028,
    "September": 0.018,
    "Moonwake": 0.027,
    "Sey": 0.020,
    "Paix": 0.020,
}

HEADER = re.compile(
    r"^##\s+"
    r"(?P<coffee>[^,]+),\s*"
    r"(?P<brewer>[^,]+),\s*"
    r"(?P<grind>[\d.]+)\s*@\s*"
    r"(?P<temp>\d+)[ºo]?F,\s*"
    r"(?P<dose>[\d.]+)g/(?P<water>[\d.]+)g"
    r"(?:\s+Day\s+(?P<day>\d+))?"
    r"(?:\s+(?P<sentiment>[^,]*?))?"
    r"(?:,\s*Score:\s*(?P<score>\d+))?"
    r"\s*$"
)

def detect_roaster(coffee, prior_roaster):
    if coffee in ROASTER_MAP_DEFAULT:
        return ROASTER_MAP_DEFAULT[coffee]
    return prior_roaster

SHOULD_HAVE_RE = re.compile(r"\*\*([^*]+)\*\*")
SHOULDVE_NUM = re.compile(r"(\d+\.\d+|\d+)")

def parse_should_have(notes):
    """Extract bolded 'should have been' style hints — list of suggested grinds."""
    if not notes:
        return []
    out = []
    for m in SHOULD_HAVE_RE.finditer(notes):
        text = m.group(1)
        # ignore pure sweet-spot / keep / slogans
        nums = SHOULDVE_NUM.findall(text)
        for n in nums:
            try:
                v = float(n)
                if 4.0 <= v <= 8.0:
                    out.append(v)
            except ValueError:
                pass
    return out

def parse():
    text = JOURNAL.read_text()
    lines = text.split("\n")
    entries = []
    cur = None
    note_lines = []
    last_roaster = None
    for line in lines:
        if line.startswith("## "):
            if cur is not None:
                cur["notes"] = "\n".join(note_lines).strip()
                entries.append(cur)
            note_lines = []
            m = HEADER.match(line)
            if not m:
                cur = None
                continue
            d = m.groupdict()
            coffee = d["coffee"].strip()
            roaster = detect_roaster(coffee, None)
            if roaster:
                last_roaster = roaster
            cur = {
                "idx": len(entries),
                "coffee": coffee,
                "brewer": d["brewer"].strip(),
                "grind": float(d["grind"]),
                "temp": int(d["temp"]),
                "dose": float(d["dose"]),
                "water": float(d["water"]),
                "day": int(d["day"]) if d["day"] else None,
                "sentiment": (d["sentiment"] or "").strip() or None,
                "score": int(d["score"]) if d["score"] else None,
                "roaster": roaster,
            }
        else:
            if cur is not None:
                note_lines.append(line)
    if cur is not None:
        cur["notes"] = "\n".join(note_lines).strip()
        entries.append(cur)
    df = pd.DataFrame(entries)
    df["should_be"] = df["notes"].fillna("").map(parse_should_have)
    return df

if __name__ == "__main__":
    df = parse()
    out = Path(__file__).parent / "entries.csv"
    df.to_csv(out, index=False)
    print(f"Parsed {len(df)} entries. Coffees: {df['coffee'].nunique()}. With score: {df['score'].notna().sum()}.")
    print(df["roaster"].value_counts(dropna=False))
    print("\nSample:")
    print(df.tail(8)[["idx","coffee","brewer","grind","day","score","sentiment"]])
