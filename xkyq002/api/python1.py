import json

def handler(request):
    print("Function called!")  # 调试日志
    input_text = request.args.get("input", "No input")
    return {
        "statusCode": 200,
        "body": json.dumps({"response": f"收到：{input_text}"}),
        "headers": {"Content-Type": "application/json"}
    }