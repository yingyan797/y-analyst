import backend.routes as rt

def lambda_handler(event, context):
    path = event.get("path", "")
    method = event.get("httpMethod", "")
    # CORS Preflight
    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "https://yingyan797.github.io",
                "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Requested-With,Accept,Origin",
                "Access-Control-Max-Age": "86400"
            },
            "body": ""
        }
    if path == "/config" and method == "GET":
        return rt.handle_config(event)
    elif path == "/analyze" and method == "POST":
        return rt.handle_analyze_csv(event)
    else:
        return {
            "statusCode": 404,
            "headers": {"Access-Control-Allow-Origin": "https://yingyan797.github.io"},
            "body": '{"error": "Not Found"}'
        }
