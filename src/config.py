import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def env_str(name: str, default: str | None = None) -> str | None:
    v = os.getenv(name)
    if v is None:
        return default
    v = v.strip()
    if v == "" or v.lower() == "none":
        return default
    return v

def env_int(name: str, default: int) -> int:
    v = env_str(name)
    if v is None:
        return default
    try:
        return int(v)
    except ValueError:
        raise ValueError(f"{name} must be an integer, got {v!r}")

DB_USER = env_str("DB_USER")
DB_PASS = env_str("DB_PASS")
DB_HOST = env_str("DB_HOST")
DB_PORT = env_int("DB_PORT", 3306)
DB_NAME = env_str("DB_NAME")

TABLE_NAME = env_str("DB_TABLE_NAME")

BASE_DIR = Path(__file__).resolve().parent.parent 
EXCEL_PATH = BASE_DIR / "data" / "excel" / "DOKU Transaction List 26 January 2026.xlsx"
# SHEET_NAME = "na_transaction_dataset"
SHEET_NAME = "na_test"

PAYMENT_GATEWAY = "doku"
RESPONSE_TYPE = 2
FLAG_DEFAULT = 0

# callbackSlug per status (edit to match yours)
CALLBACK_SLUG = {
    "REG_SUCCESS": "doku_rcrreg_notify",
    "REDIRECT": "doku_rcrreg_redirect",
    "PAID": "doku_rcr_notify",
}
