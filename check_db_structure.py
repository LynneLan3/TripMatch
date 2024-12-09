import mysql.connector
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 数据库配置
db_config = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

def get_table_structure(cursor, table_name):
    # 获取表结构
    cursor.execute(f"DESCRIBE {table_name}")
    columns = cursor.fetchall()
    print(f"\n表名: {table_name}")
    print("列名\t\t数据类型\t\t可空\t\t键\t\t默认值\t\t额外信息")
    print("-" * 100)
    for column in columns:
        print(f"{column[0]}\t\t{column[1]}\t\t{column[2]}\t\t{column[3]}\t\t{column[4]}\t\t{column[5]}")

try:
    # 连接数据库
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # 获取所有表名
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    print("数据库中的所有表：")
    for table in tables:
        table_name = table[0]
        get_table_structure(cursor, table_name)

    cursor.close()
    conn.close()

except Exception as e:
    print(f"Error: {str(e)}")
