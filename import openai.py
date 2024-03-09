import openai
import os

# 获取当前工作目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 读取文件
with open(os.path.join(current_dir, 'testing.txt'), 'r', encoding='utf-8') as fh:
    tmp = fh.read()
    itemlist = tmp.split(',')

itemlist = str(itemlist)

# 读取API密钥
with open(os.path.join(current_dir, 'key.txt'), "r") as keyfile:
    key = keyfile.readline().strip()

openai.api_key = key

def get_user_input():
    user_input = input("请输入消息内容：")
    return user_input

def construct_message(user_input):
    messages = [
        {"role": "user", "content": user_input}
    ]
    return messages

def main():
    while True:
        user_input = get_user_input()
        messages = construct_message(user_input)
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=300,
            temperature=0.5,
            messages=messages
        )
        
        print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
