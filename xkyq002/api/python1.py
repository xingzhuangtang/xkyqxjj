import json
import os
import requests
from dotenv import load_dotenv

load_dotenv(".env")


def joke_generator(input_text):
    debug = os.getenv("DEBUG", "False").lower() == "true"  # 检查 DEBUG 变量，默认 False
    if debug:
        print(f"DEBUG: Received input: {input_text}")

    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
    if not dashscope_api_key:
        if debug:
            print("DEBUG: DASHSCOPE_API_KEY is not set")
        return "API Key 未设置，请检查环境变量！"

    prompt = f"""
    首先你是各个行业的专业顶级教育家，其次你是一个毒舌喜剧家，同时也是一个创新创意思考家，用50字内回复用户，要求：
    1. 你是具有创新创意的爱思考的毒舌喜剧家，你要从出其不意的角度回复用户，给用户带来启发和顿悟
    2. 要结合网络上，现实中的热梗，来回复用户的问题，要有笑点和启发性
    3. 给出的答案及建议要保证具有实用性，思考性，以及启发和娱乐性，答案和建议具有广泛传播的潜力
    4. 引导用户说出自己的热梗，问题或者困惑以及新思想来进行互动
    3. 结尾加🤡/🐶表情
    用户输入：{input_text}
    """

    url = os.getenv("DATABASE_URL")
    headers = {"Authorization": f"Bearer {dashscope_api_key}", "Content-Type": "application/json"}

    try:
        if debug:
            print(f"DEBUG: Sending request to {url} with prompt: {prompt[:50]}...")
        response = requests.post(
            url,
            headers=headers,
            json={"model": "deepseek-v3", "input": {"messages": [{"role": "user", "content": prompt}]}},
            timeout=10
        )
        response.raise_for_status()
        response_data = response.json()
        if debug:
            print(f"DEBUG: API response: {response_data}")
        return response_data["output"]["choices"][0]["message"]["content"]
    except Exception as e:
        if debug:
            print(f"DEBUG: Error occurred: {str(e)}")
        return f"出错啦：{str(e)}，稍后再试吧！"


def handler(request):
    debug = os.getenv("DEBUG", "False").lower() == "true"  # 检查 DEBUG 变量，默认 False
    if debug:
        print("DEBUG: Function handler called")

    input_text = request.args.get("input", "")
    if debug:
        print(f"DEBUG: Input received: {input_text}")
    if not input_text:
        if debug:
            print("DEBUG: No input provided, returning 400")
        return {"statusCode": 400, "body": json.dumps({"response": "请输入点啥吧！"})}

    result = joke_generator(input_text)
    if debug:
        print(f"DEBUG: Result generated: {result}")
    return {
        "statusCode": 200,
        "body": json.dumps({"response": result}),
        "headers": {"Content-Type": "application/json"}
    }