import requests
import json
import os
import time
import sys

# 定义一个函数，用于逐个字符输出文本，并在每个字符之间添加延迟
def type_out_text(text, delay=0.05):
    """
    逐字输出文本，模拟打字效果。
    :param text: 需要输出的文本内容
    :param delay: 每个字符输出之间的延迟时间，默认为0.05秒
    """
    # 遍历文本中的每个字符
    for char in text:
        # 将当前字符输出到标准输出
        sys.stdout.write(char)
        # 刷新标准输出缓冲区，确保字符立即显示
        sys.stdout.flush()
        # 暂停一段时间，以模拟打字的延迟
        time.sleep(delay)
    # 输出完所有字符后换行
    print()  

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

while True:
    # 从命令行接收用户输入的内容
    user_input = input("请输入您的问题（输入'exit'结束）：\n")

    # 如果用户输入'exit'，则退出循环
    if user_input.strip().lower() == 'exit':
        print("退出提问...")
        break

    # # 打印用户输入的内容
    # print(f"User Input: \n{user_input}")

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
        answer = f"## {model_name} answer:\n{message_content}"
        type_out_text(answer)

        # 将答案写入answer.md文件
        with open('answer.md', 'w', encoding='utf-8') as f:
            f.write(f"User Input: \n{user_input}")
            f.write(answer)

        # 使用Typora打开answer.md文件
        os.system('start "" "D:\\Typora\\Typora\\Typora.exe" "answer.md"')

        # 等待几秒钟确保Typora能够打开文件
        time.sleep(2)
    else:
        print("没有找到有效的消息内容")
