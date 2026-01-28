from sqlalchemy import text

def insert_rows(engine, table_name: str, rows: list[dict]) -> int:
    if not rows:
        return 0

    # remove id if your DB auto-increments and you don't want to insert it
    clean = []
    for r in rows:
        rr = dict(r)
        rr.pop("id", None)
        clean.append(rr)

    cols = list(clean[0].keys())
    col_names = ", ".join(f"`{c}`" for c in cols)
    placeholders = ", ".join(f":{c}" for c in cols)

    sql = text(f"INSERT INTO `{table_name}` ({col_names}) VALUES ({placeholders})")

    with engine.begin() as conn:
        conn.execute(sql, clean)

    return len(clean)
