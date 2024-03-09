import os
import openai
import requests

def get_openai_api_key():
    try:
        # 从GitHub仓库的.gitignore文件中获取API密钥
        response = requests.get('https://raw.githubusercontent.com/yuancc12/Data-structure/master/.gitignore')

        
        if response.status_code == 200:
            gitignore_content = response.text
            # 在.gitignore文件中查找包含API密钥的行
            for line in gitignore_content.split('\n'):
                if 'OPENAI_API_KEY' in line:
                    # 提取API密钥并返回
                    return line.split('=')[1].strip()
        else:
            print(f"Failed to fetch .gitignore content: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching .gitignore content: {str(e)}")
        return None

def main():
    # 获取OpenAI API密钥
    api_key = get_openai_api_key()
    if api_key:
        openai.api_key = api_key
        print("Successfully fetched OpenAI API key from .gitignore")
    else:
        print("Failed to fetch OpenAI API key from .gitignore")
        exit()

    # 其他代码部分
    # ...

if __name__ == "__main__":
    main()
