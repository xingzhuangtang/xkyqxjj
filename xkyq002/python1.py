import gradio as gr
import requests
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv(".env")

def joke_generator(input_text):
    # 从环境变量中读取 API Key
    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
    if not dashscope_api_key:
        return "API Key 未设置，请检查 .env 文件！"

    # 预设搞笑Prompt（可修改）
    prompt = f"""
    首先你是各个行业的专业顶级教育家，其次你是一个毒舌喜剧家，同时也是一个创新创意思考家，用50字内回复用户，要求：
    1. 你是具有创新创意的爱思考的毒舌喜剧家，你要从出其不意的角度回复用户，给用户带来启发和顿悟
    2. 要结合网络上，现实中的热梗，来回复用户的问题，要有笑点和启发性
    3. 给出的答案及建议要保证具有实用性，思考性，以及启发和娱乐性，答案和建议具有广泛传播的潜力
    4. 引导用户说出自己的热梗，问题或者困惑以及新思想来进行互动
    3. 结尾加🤡/🐶表情
    用户输入：{input_text}
    """

    # 调用 DashScope API
    url = os.getenv("DATABASE_URL")
    headers = {
        "Authorization": f"Bearer {dashscope_api_key}",
        "Content-Type": "application/json"
    }

    try:
        print("Sending request to DashScope API...")
        print("Request URL:", url)
        print("Request Headers:", headers)
        print("Request Body:", {
            "model": "deepseek-v3",
            "input": {
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        })

        response = requests.post(
            url,
            headers=headers,
            json={
                "model": "deepseek-v3",
                "input": {
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }
            },
            timeout=10
        )
        response.raise_for_status()
        response_data = response.json()
        print("Response:", response_data)

        # 检查 API 返回格式并提取内容
        if "output" in response_data and "choices" in response_data["output"]:
            return response_data["output"]["choices"][0]["message"]["content"]
        else:
            print("API 返回格式异常:", response_data)
            return "API 返回格式异常，请检查日志！"
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return "请求失败，请稍后重试！"
    except KeyError:
        print("解析响应失败，请检查 API 返回格式")
        return "解析响应失败，请检查 API 返回格式！"


# 创建网页界面
demo = gr.Interface(
    fn=joke_generator,
    inputs="text",
    outputs="text",
    title="引擎喜剧家🤡",
    description="输入你的烦恼，获得毒舌回复！",
    examples=["我今天心情不好", "我考试没考好"]
)

# 启动 Gradio 应用
demo.launch(server_name="0.0.0.0", server_port=8080, share=False)  # 禁用 share 功能用 False