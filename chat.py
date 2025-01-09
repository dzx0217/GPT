import requests
import json

# 设置URL和API请求的目标地址
url = "https://xiaoai.plus/v1/chat/completions"

# 从prompt.txt文件中读取system角色的content
with open('prompt.txt', 'r', encoding='utf-8') as f:
    system_content = f.read().strip()  # 读取文件内容并去掉两端的空白字符

# 打印读取到的内容
print(f"Prompt: \n{system_content}")

# 从key.txt文件中读取API密钥
with open('key.txt', 'r', encoding='utf-8') as f:
    api_key = f.read().strip()  # 读取API密钥并去掉两端的空白字符

# 从question.txt文件中读取用户输入的内容
with open('question.txt', 'r', encoding='utf-8') as f:
    user_input = f.read().strip()  # 读取文件内容并去掉两端的空白字符

# 打印用户输入的内容
print(f"User Input: \n{user_input}")

# 构造请求负载，将从文件中读取的内容作为"system"的"content"
payload = json.dumps({
    "messages": [
        {
            "role": "system",
            "content": system_content  # 从prompt.txt读取的内容
        },
        {
            "role": "user",
            "content": user_input
        }
    ],
    "stream": False,
    "model": "gpt-4o",
    "temperature": 0.7,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "top_p": 1
})

# 请求头，包括从key.txt中读取的API密钥
headers = {
    "Content-Type": "application/json",
    'Authorization': f'Bearer {api_key}'  # 使用读取的API密钥
}

# 发送POST请求
response = requests.request("POST", url, headers=headers, data=payload)

# 解析返回的JSON响应
response_data = response.json()

# 提取模型名称
model_name = response_data.get('model', '未知模型')

# 提取并输出返回的内容
if 'choices' in response_data and len(response_data['choices']) > 0:
    message_content = response_data['choices'][0]['message']['content']
    answer = f"{model_name} Answer:\n{message_content}"
    print(answer)  # 打印输出的答案

    # 将答案写入answer.md文件
    with open('answer.md', 'w', encoding='utf-8') as f:
        f.write(answer)
else:
    print("没有找到有效的消息内容")
