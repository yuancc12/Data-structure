import openai

openai.api_key = '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'

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
