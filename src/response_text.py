def build_response_text(status: str, row: dict, date_now: str = "") -> dict:
    """
    Return a dict (will be json.dumps() later).
    Change fields to match exactly your required JSON.
    """

    if status == "REG_SUCCESS":
        return {
            "customer_id": row.get("email"),
            "bill_number": (row.get('bill_number')).replace("TRX_", "BILL_"),
            "words": row.get("words", ""),          # if you have it
            "mallid": row.get("mallid", "2508"),
            "chain_merchant": row.get("chain_merchant", "NA"),
            "card_number": row.get("card_number"),
            "status": "SUCCESS",
            "error_code": "",
            "message": emphasized("Registration Success"),
            "status_type": "G",
        }

    if status == "REDIRECT":
        return {
            "trans_id_merchant": row.get("bill_number"),
            "payment_channel": row.get("payment_channel", "17"),
            "bill_number": (row.get('bill_number')).replace("TRX_", "BILL_"),
            "amount": str(row.get("amount")),
            "words": row.get("words", ""),
            "session_id": row.get("session_id", ""),
            "customer_id": row.get("email"),
        }

    if status == "PAID":
        return {
            "result_message": "SUCCESS",
            "mallid": row.get("mallid", "1709"),
            "chain_merchant": row.get("chain_merchant", ""),
            "words": row.get("words", ""),
            "customer_id": row.get("email"),
            "token_id": row.get("token_id", ""),
            "card_number": row.get("card_number"),
            "bill_number": (row.get('bill_number')).replace("TRX_", "BILL_"),
            "trans_id_merchant": row.get("trans_id_merchant_paid", ""),
            "amount": str(row.get("amount")),
            "currency": row.get("currency"),
            "response_code": "00",
            "approval_code": row.get("approval_code", ""),
            "verify_id": "",
            "verify_score": "",
            "verify_status": "REVIEW",
            "payment_datetime": row.get("payment_datetime", date_now),
        }

    return {}

def emphasized(s: str) -> str:
    # helper if later you want formatting rules; keep simple for now
    return s
