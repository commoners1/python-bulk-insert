from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable
from datetime import date, datetime
import math

def _sql_literal(v: Any) -> str:
    """Convert Python value to a MySQL/MariaDB SQL literal."""
    if v is None:
        return "NULL"

    # bool must come before int (because bool is subclass of int)
    if isinstance(v, bool):
        return "1" if v else "0"

    if isinstance(v, (int, float)):
        # Avoid 'nan'/'inf' going into SQL
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            return "NULL"
        return str(v)

    if isinstance(v, (datetime, date)):
        # MariaDB/MySQL accept 'YYYY-MM-DD HH:MM:SS' or 'YYYY-MM-DD'
        if isinstance(v, datetime):
            s = v.strftime("%Y-%m-%d %H:%M:%S")
        else:
            s = v.strftime("%Y-%m-%d")
        return f"'{s}'"

    # treat everything else as string
    s = str(v)

    # Escape for MySQL string literal
    # - Backslash first
    s = s.replace("\\", "\\\\")
    # - Single quotes
    s = s.replace("'", "''")
    # - Newlines / carriage returns / tabs
    s = s.replace("\r", "\\r").replace("\n", "\\n").replace("\t", "\\t")

    return f"'{s}'"


def dump_inserts_mysql(
    out_path: str | Path,
    table_name: str,
    rows: list[dict],
    *,
    batch_size: int = 1,
    use_transaction: bool = True,
    include_columns: list[str] | None = None,
) -> None:
    """
    Write a replayable MySQL/MariaDB .sql file containing INSERT statements.

    - batch_size=1 writes one INSERT per row
    - batch_size>1 writes multi-row INSERT statements
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        out_path.write_text("-- no rows\n", encoding="utf-8")
        return

    cols = include_columns or list(rows[0].keys())
    col_names_sql = ", ".join(f"`{c}`" for c in cols)

    def row_values_sql(r: dict) -> str:
        return "(" + ", ".join(_sql_literal(r.get(c)) for c in cols) + ")"

    with out_path.open("w", encoding="utf-8", newline="\n") as f:
        f.write("-- MySQL/MariaDB insert log\n")
        f.write(f"-- Table: `{table_name}`\n")
        f.write(f"-- Rows: {len(rows)}\n\n")

        if use_transaction:
            f.write("START TRANSACTION;\n\n")

        if batch_size <= 1:
            # One INSERT per row
            for r in rows:
                f.write(
                    f"INSERT INTO `{table_name}` ({col_names_sql}) VALUES {row_values_sql(r)};\n"
                )
        else:
            # Multi-row INSERT batches
            for i in range(0, len(rows), batch_size):
                chunk = rows[i:i + batch_size]
                values = ",\n".join(row_values_sql(r) for r in chunk)
                f.write(
                    f"INSERT INTO `{table_name}` ({col_names_sql}) VALUES\n{values};\n\n"
                )

        if use_transaction:
            f.write("\nCOMMIT;\n")
