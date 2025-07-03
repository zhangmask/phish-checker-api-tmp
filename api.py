from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = "sk-fsuatntmfrvlhipveykhrbvkuqeurtdpepblhdoljkjvkcog"
API_URL = "https://api.siliconflow.cn/v1/chat/completions"

@app.route("/check", methods=["POST"])
def check_url():
    data = request.json
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "请输入内容！"}), 400

    payload = {
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,  # 确保足够长度
        "temperature": 0.7  # 可选，控制生成随机性
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(API_URL, json=payload, headers=headers)
        r.raise_for_status()
        print("🧠 SiliconFlow 返回状态码:", r.status_code)
        print("🧠 SiliconFlow 返回内容:", r.text)
        return r.text, 200, {'Content-Type': 'application/json'}
    except requests.exceptions.RequestException as e:
        print("❌ 请求失败详情:", str(e))
        return jsonify({"error": "请求失败，请检查 API 配置或网络"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)