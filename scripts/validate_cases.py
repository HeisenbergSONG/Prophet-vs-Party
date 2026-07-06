"""Validate all entries in cases.json against case_schema."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.case_schema import validate_case


def main() -> int:
    path = ROOT / "cases.json"
    cases = json.loads(path.read_text(encoding="utf-8"))
    failed = 0
    for case in cases:
        errors = validate_case(case)
        if errors:
            failed += 1
            print(f"{case.get('id', '?')}: {errors}")
    if failed:
        print(f"\n{failed}/{len(cases)} cases failed validation", file=sys.stderr)
        return 1
    print(f"OK — {len(cases)} cases passed validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())