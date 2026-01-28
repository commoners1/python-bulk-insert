import pandas as pd

def normalize_columns(cols):
    return [c.strip().lower().replace(" ", "_") for c in cols]

def excel_to_json_rows(excel_path: str, sheet_name=0, column_map: dict | None = None) -> list[dict]:
    """
    Reads Excel and returns rows as JSON-like objects (list of dicts).
    - Normalizes Excel headers to lowercase_with_underscores
    - Applies column_map if provided (excel_col -> db_col)
    - Converts NaN to None (so DB inserts NULL)
    """
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    df.columns = normalize_columns(df.columns)

    if column_map:
        missing = [c for c in column_map.keys() if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns in Excel: {missing}")

        df = df[list(column_map.keys())].rename(columns=column_map)

    df = df.where(pd.notnull(df), None)

    # Optional: make datetime columns JSON friendly
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime("%Y-%m-%d %H:%M:%S")

    return df.to_dict(orient="records")
