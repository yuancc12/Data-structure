from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from openai import OpenAI
import mysql.connector
import pandas as pd
from sentence_transformers import SentenceTransformer
import os
import json

model = SentenceTransformer('distiluse-base-multilingual-cased-v1')
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def handle_message():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid JSON format"}), 400

        data = request.get_json()
        if 'message' not in data:
            return jsonify({"error": "Missing 'message' key in request data"}), 400

        message = data['message']
        
        # 数据库连接
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # 更新为你的MySQL密码
            database="ehrsystem"
        )
        cursor = db.cursor(dictionary=True)  # 使用字典游标
        
        # 执行查询
        query = """
        SELECT TimeEvents.*, employees.Firstname 
        FROM TimeEvents 
        JOIN employees ON TimeEvents.EmployeeID = employees.EmployeeID;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # 提取名字
        sentences = [row['Firstname'] for row in rows]
        sentence_embeddings = model.encode(sentences).tolist()  # 将嵌入转换为列表
        
        # 创建DataFrame
        dataframe = pd.DataFrame(rows)
        
        # 打印调试信息
        print(f"DataFrame: {dataframe}")
     
        # 将嵌入转化为字符串格式
        embeddings_str = json.dumps(sentence_embeddings)

        data_for_ai = {
            "dataframe": dataframe.to_json(),
            "embeddings": embeddings_str,  # 转化为JSON字符串
            "message": message
        }
        

        # 调用OpenAI API
        completion = client.chat.completions.create(
            model="model-identifier",
            messages=[{"role": "user", "content": f"请根据以下数据回答：{json.dumps(data_for_ai)}"}],
            temperature=0.7,
        )
        
        # 提取API响应内容
        if completion.choices:
            chat_message = completion.choices[0].message
            response_text = chat_message.content if chat_message else "No message found"
        else:
            response_text = "No completion found"
            
        return jsonify({"status": "success", "message": response_text}), 200
    except KeyError as e:
        print(f"KeyError: {str(e)}")
        return jsonify({"error": f"Missing key: {str(e)}"}), 400
    except TypeError as e:
        print(f"TypeError: {str(e)}")
        return jsonify({"error": f"Type error: {str(e)}"}), 400
    except Exception as e:
        # 捕捉其它异常并返回通用错误信息，并记录详细的错误信息
        print(f"Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
