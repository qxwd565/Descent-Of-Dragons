#!/usr/bin/env python3
"""Normalize display-text line breaks without changing JSON structural newlines."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_KEYS = {"text", "nativeRawText", "rawText", "flavor", "name"}

def normalize(value, key=None):
    if isinstance(value, str) and key in TEXT_KEYS:
        return (value.replace("\r\n", "<br></br>")
                     .replace("\r", "<br></br>")
                     .replace("\n", "<br></br>")
                     .replace("\\n", "<br></br>")
                     .replace("/n", "<br></br>"))
    if isinstance(value, list):
        return [normalize(item, key) for item in value]
    if isinstance(value, dict):
        return {name: normalize(item, name) for name, item in value.items()}
    return value

def main():
    changed = 0
    for path in [ROOT / "cards.json", *sorted((ROOT / "data").glob("*.json"))]:
        original = json.loads(path.read_text(encoding="utf-8"))
        normalized = normalize(original)
        if normalized != original:
            path.write_text(json.dumps(normalized, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8", newline="\n")
            changed += 1
    print(json.dumps({"normalizedDisplayTextFiles": changed}))

if __name__ == "__main__":
    main()
