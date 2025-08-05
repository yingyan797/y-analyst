def parse_body(event):
    import json
    if "body" in event and event["body"]:
        try:
            return json.loads(event["body"])
        except Exception:
            return {}
    return {}
