import backend.routes as rt

def lambda_handler(event, context):
    path = event.get("path", "")
    method = event.get("httpMethod", "")

    if path == "/config" and method == "GET":
        return rt.handle_config(event)
    elif path == "/analyze" and method == "POST":
        return rt.handle_analyze_csv(event)
    else:
        return {
            "statusCode": 404,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": '{"error": "Not Found"}'
        }
