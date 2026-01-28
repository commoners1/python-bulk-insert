from __future__ import annotations
from pathlib import Path
import json
from datetime import date, datetime
from typing import Any

def _json_default(o: Any):
    if isinstance(o, (datetime, date)):
        return o.isoformat()
    return str(o)

def log_parameterized_inserts(
    out_path: str | Path,
    table_name: str,
    rows: list[dict],
) -> None:
    """
    Writes:
      - the INSERT template (parameterized)
      - one JSON line of values per row
    This is the safest way to log queries.
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        out_path.write_text("-- no rows\n", encoding="utf-8")
        return

    cols = list(rows[0].keys())
    col_names = ", ".join(f"`{c}`" for c in cols)
    placeholders = ", ".join(f":{c}" for c in cols)

    template = f"INSERT INTO `{table_name}` ({col_names}) VALUES ({placeholders});"

    with out_path.open("w", encoding="utf-8") as f:
        f.write("-- SQL template (parameterized)\n")
        f.write(template + "\n\n")
        f.write("-- Values (one JSON object per row)\n")
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, default=_json_default) + "\n")
