from flask import Flask, request, jsonify
import os
import requests
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/api/python1', methods=['GET'])
def joke_handler():
    # 获取用户输入
    input_text = request.args.get('input', '').strip()
    if not input_text:
        return jsonify({"response": "请输入点啥吧！"}), 400

    # 获取环境变量
    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
    api_url = os.getenv("DASHSCOPE_API_URL")

    # 检查环境变量
    if not dashscope_api_key or not api_url:
        logger.error("环境变量未配置：DASHSCOPE_API_KEY 或 DASHSCOPE_API_URL")
        return jsonify({"response": "服务配置错误，请联系管理员"}), 500

    # 构建提示词
    prompt = f"""
    首先你是各个行业的专业顶级教育家，其次你是一个毒舌喜剧家，同时也是一个创新创意思考家，用50字内回复用户，要求：
    1. 你是具有创新创意的爱思考的毒舌喜剧家，你要从出其不意的角度回复用户，给用户带来启发和顿悟
    2. 要结合网络上，现实中的热梗，来回复用户的问题，要有笑点和启发性
    3. 给出的答案及建议要保证具有实用性，思考性，以及启发和娱乐性，答案和建议具有广泛传播的潜力
    4. 引导用户说出自己的热梗，问题或者困惑以及新思想来进行互动
    3. 结尾加🤡/🐶表情
    用户输入：{input_text}
    """

    try:
        # 调用 DashScope API
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

        # 解析 API 响应
        response_data = response.json()
        result = response_data.get('output', {}).get('choices', [{}])[0].get('message', {}).get('content', "回复解析失败")
        return jsonify({"response": result})

    except requests.exceptions.RequestException as e:
        logger.error(f"API 请求失败: {str(e)}")
        return jsonify({"response": f"API 请求失败: {str(e)}"}), 500
    except Exception as e:
        logger.error(f"未知错误: {str(e)}")
        return jsonify({"response": f"未知错误: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)