import json
from src.config import EXCEL_PATH, SHEET_NAME, TABLE_NAME
from src.db import get_engine
from src.generator import generate_db_rows_from_excel
from src.importer import insert_rows

def main():
    engine = get_engine()
    rows = generate_db_rows_from_excel(EXCEL_PATH, SHEET_NAME)

    print("Preview first output row:")
    print(json.dumps(rows[0], ensure_ascii=False, indent=2))

    inserted = insert_rows(engine, TABLE_NAME, rows)
    print(f"Inserted {inserted} rows into {TABLE_NAME}")

if __name__ == "__main__":
    main()
