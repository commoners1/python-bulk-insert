import json
import pandas as pd
from datetime import datetime, date
from src.response_text import build_response_text
from src.config import PAYMENT_GATEWAY, RESPONSE_TYPE, FLAG_DEFAULT, CALLBACK_SLUG

def normalize_columns(cols):
    return [str(c).strip().lower().replace(" ", "_") for c in cols]

def first_day_of_current_month() -> datetime:
    today = date.today()
    return datetime(today.year, today.month, 1, 8, 0, 0)

def first_day_next_month(d: datetime) -> datetime:
    y, m = d.year, d.month
    if m == 12:
        return datetime(y + 1, 1, 1, 8, 0, 0)
    return datetime(y, m + 1, 1, 8, 0, 0)

def parse_register_date(value) -> datetime:
    """
    Your register_date looks like: '16-03-2022 10:36:47'
    """
    if isinstance(value, datetime):
        return value
    s = str(value).strip()
    # adjust if your excel format differs
    # dt = datetime.strptime(s, "%d-%m-%Y %H:%M:%S")
    # return dt.date()
    return datetime.strptime(s, "%d-%m-%Y %H:%M:%S")

def generate_db_rows_from_excel(excel_path: str, sheet_name=0) -> list[dict]:
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    df.columns = normalize_columns(df.columns)
    df = df.where(pd.notnull(df), None)

    rows = df.to_dict(orient="records")
    out = []

    end_date = first_day_of_current_month()

    for r in rows:
        ref_id = r["bill_number"]
        register_dt = parse_register_date(r["register_date"])

        # 1) REG_SUCCESS row (same date as start/register date)
        for status in ("REDIRECT", "REG_SUCCESS"):
            response_obj = build_response_text(status, r)
            out.append({
                "id": None,
                "refId": ref_id,
                "responseRefId": ref_id,
                "status": status,
                "dateCreated": register_dt.strftime("%Y/%m/%d %H:%M:%S"),
                "responseType": RESPONSE_TYPE,
                "callbackSlug": CALLBACK_SLUG.get(status, None),
                "paymentGateway": PAYMENT_GATEWAY,
                "responseText": json.dumps(response_obj, ensure_ascii=False),
                "flag": FLAG_DEFAULT,
                "payload": None,
            })

        # 2) PAID rows monthly: from first day of next month after register date → first day of current month
        paid_date = first_day_next_month(register_dt)

        while paid_date <= end_date:
            response_obj = build_response_text("PAID", r, paid_date.strftime("%Y%m%d%H%M%S"))
            out.append({
                "id": None,
                "refId": ref_id,
                "responseRefId": ref_id,
                "status": "PAID",
                "dateCreated": paid_date.strftime("%Y/%m/%d %H:%M:%S"),
                "responseType": RESPONSE_TYPE,
                "callbackSlug": CALLBACK_SLUG.get("PAID", None),
                "paymentGateway": PAYMENT_GATEWAY,
                "responseText": json.dumps(response_obj, ensure_ascii=False),
                "flag": FLAG_DEFAULT,
                "payload": None,
            })

            paid_date = first_day_next_month(paid_date)

    return out
