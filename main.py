import json
from src.config import EXCEL_PATH, SHEET_NAME, TABLE_NAME
from src.db import get_engine
from src.generator import generate_db_rows_from_excel
from src.importer import insert_rows
# from src.sql_logger import log_parameterized_inserts
from src.sql_logger_mysql import dump_inserts_mysql

def main():
    engine = get_engine()
    rows = generate_db_rows_from_excel(EXCEL_PATH, SHEET_NAME)

    print("Preview first output row:")
    print(json.dumps(rows[0], ensure_ascii=False, indent=2))

    # log_parameterized_inserts("data/sql/inserts_response_doku.sql", TABLE_NAME, rows)

    dump_inserts_mysql(
        out_path="data/sql/inserts_response_doku.sql",
        table_name=TABLE_NAME,
        rows=rows,
        batch_size=200,
        use_transaction=True
    )

    inserted = insert_rows(engine, TABLE_NAME, rows)
    print(f"Inserted {inserted} rows into {TABLE_NAME}")


if __name__ == "__main__":
    main()
