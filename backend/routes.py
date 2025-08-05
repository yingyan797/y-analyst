import json, os, csv, io
from backend.utils import parse_body

def handle_config(event):
    return _response(200, {
        "GREETING": os.environ.get("GREETING", "Hello"),
        "STAGE": os.environ.get("STAGE", "dev")
    })

def handle_analyze_csv(event):
    body = parse_body(event)
    csv_text = body.get("csv", "")
    if not csv_text.strip():
        return _response(400, {"error": "No CSV data received"})

    try:
        reader = csv.DictReader(io.StringIO(csv_text))
        rows = list(reader)
        sample = rows[:5]
        return _response(200, {
            "columns": reader.fieldnames,
            "num_rows": len(rows),
            "sample_rows": sample
        })
    except Exception as e:
        return _response(500, {"error": f"Failed to parse CSV: {str(e)}"})

def _response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "https://yingyan797.github.io/y-analyst",  # Allow all origins
            "Access-Control-Allow-Headers": "*",  # Allow all headers
            "Access-Control-Allow-Methods": "*"   # Allow all methods
        },
        "body": json.dumps(body)
    }
