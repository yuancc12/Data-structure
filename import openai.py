# import openai.py

def get_openai_key():
    key_file_path = "key.txt"  # 指定金鑰文件的路徑
    try:
        with open(key_file_path, "r") as key_file:
            api_key = key_file.read().strip()  # 讀取並清除任何可能的空白字符
        return api_key
    except FileNotFoundError:
        print("Failed to fetch OpenAI API key from key.txt")
        return None

# 使用示例
openai_key = get_openai_key()
if openai_key:
    # 使用API金鑰進行相應的操作
    print("OpenAI API key:", openai_key)
else:
    # 無法獲取API金鑰，執行相應的錯誤處理邏輯
    print("Error: Unable to fetch OpenAI API key")
