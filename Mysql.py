import mysql.connector
import pandas as pd

def fetch_data():
    try:
        # 创建数据库连接
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # 将"your_password"替换为您的MySQL密码
            database="ehrsystem"
        )

        # 定义SQL查询语句
        query = "SELECT * FROM timeevents"

        # 使用pandas读取数据
        dataframe = pd.read_sql_query(query, connection)
        print(dataframe)

    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)

    finally:
        # 关闭数据库连接
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

if __name__ == '__main__':
    fetch_data()
