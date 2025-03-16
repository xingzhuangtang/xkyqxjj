from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)


@app.route('/api/python1', methods=['GET'])
def joke_handler():
    input_text = request.args.get('input', '')
    if not input_text:
        return jsonify({"response": "请输入点啥吧！"}), 400

    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
    api_url = os.getenv("DASHSCOPE_API_URL")  # 新增环境变量

    prompt = f"""你的提示模板内容..."""

    try:
        response = requests.post(
            api_url,
            headers={"Authorization": f"Bearer {dashscope_api_key}"},
            json={
                "model": "deepseek-v3",
                "input": {
                    "messages": [{
                        "role": "user",
                        "content": prompt
                    }]
                }
            },
            timeout=10
        )
        response.raise_for_status()

        # 根据实际API响应结构调整解析逻辑
        result = response.json()['output']['choices'][0]['message']['content']

    except Exception as e:
        return jsonify({"response": f"服务异常: {str(e)}"}), 500

    return jsonify({"response": result})


if __name__ == '__main__':
    app.run()