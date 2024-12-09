from flask import Flask, jsonify, request, send_from_directory
import mysql.connector
from dotenv import load_dotenv
import os
from flask_cors import CORS

# 加载环境变量
load_dotenv()

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:8000", "http://localhost:8081", "http://localhost:8082", "http://localhost"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})

# 数据库配置
db_config = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def make_response(code=200, message="success", data=None):
    return jsonify({
        "code": code,
        "message": message,
        "data": data if data is not None else {}
    })

@app.route('/')
def root():
    return send_from_directory('.', 'index.html')

@app.route('/questions', methods=['GET'])
def get_questions():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, content FROM questions')
        questions = cursor.fetchall()
        cursor.close()
        conn.close()
        return make_response(data=questions)
    except Exception as e:
        return make_response(code=500, message=str(e), data={})

@app.route('/questionnaires', methods=['GET'])
def get_questionnaires():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 查询所有问卷信息
        cursor.execute('''
            SELECT id, title, level, description
            FROM questionnaires
            ORDER BY level ASC, id ASC
        ''')
        questionnaires = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return make_response(data=questionnaires)
    except Exception as e:
        return make_response(code=500, message=str(e), data={})

@app.route('/questionnaire/<int:questionnaire_id>', methods=['GET'])
def get_questionnaire_with_questions(questionnaire_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 查询问卷信息
        cursor.execute('''
            SELECT id, title, level, description
            FROM questionnaires 
            WHERE id = %s
        ''', (questionnaire_id,))
        questionnaire = cursor.fetchone()
        
        if not questionnaire:
            return make_response(code=404, message="问卷不存在", data={})
        
        # 查询关联的问题
        cursor.execute('''
            SELECT q.id, q.content, q.category
            FROM questions q
            JOIN questionnaire_questions qq ON q.id = qq.question_id
            WHERE qq.questionnaire_id = %s
            ORDER BY q.id ASC
        ''', (questionnaire_id,))
        questions = cursor.fetchall()
        
        # 为每个问题获取选项
        for question in questions:
            cursor.execute('''
                SELECT id, content
                FROM options
                WHERE question_id = %s
                ORDER BY id ASC
            ''', (question['id'],))
            question['options'] = cursor.fetchall()

        # 将questions添加到questionnaire结构中
        questionnaire['questions'] = questions
        
        cursor.close()
        conn.close()
        return make_response(data=questionnaire)
    except Exception as e:
        return make_response(code=500, message=str(e), data={})

# 用户登录
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')
        
        if not phone_number:
            return make_response(code=400, message="手机号不能为空", data={})
            
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 查找用户
        cursor.execute('SELECT id, phone_number FROM users WHERE phone_number = %s', (phone_number,))
        user = cursor.fetchone()
        
        if not user:
            # 如果用户不存在，创建新用户
            username = f'user_{phone_number}'  # 使用手机号作为用户名的一部分
            cursor.execute('INSERT INTO users (phone_number, username) VALUES (%s, %s)', (phone_number, username))
            conn.commit()
            user_id = cursor.lastrowid
            user = {'id': user_id, 'phone_number': phone_number, 'username': username}
            
        cursor.close()
        conn.close()
        return make_response(data=user)
        
    except Exception as e:
        return make_response(code=500, message=str(e), data={})

# 保存用户答题记录
@app.route('/save_answers', methods=['POST'])
def save_answers():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        questionnaire_id = data.get('questionnaire_id')
        answers = data.get('answers')

        if not all([user_id, questionnaire_id, answers]):
            return make_response(code=400, message="缺少必要参数", data={})

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 先删除该用户对该问卷的旧答案
        cursor.execute('''
            DELETE FROM user_answers 
            WHERE user_id = %s AND questionnaire_id = %s
        ''', (user_id, questionnaire_id))

        # 插入新的答案
        for answer in answers:
            cursor.execute('''
                INSERT INTO user_answers 
                (user_id, questionnaire_id, question_id, option_id) 
                VALUES (%s, %s, %s, %s)
            ''', (user_id, questionnaire_id, answer['question_id'], answer['option_id']))

        conn.commit()
        cursor.close()
        conn.close()

        return make_response(message="答案保存成功")
    except Exception as e:
        return make_response(code=500, message=str(e), data={})

# 获取用户答题记录
@app.route('/user_answers/<int:user_id>/<int:questionnaire_id>', methods=['GET'])
def get_user_answers(user_id, questionnaire_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 获取用户在特定问卷的答题记录
        cursor.execute('''
            SELECT ua.question_id, ua.option_id as selected_option_id
            FROM user_answers ua
            JOIN questionnaire_questions qq ON ua.question_id = qq.question_id
            WHERE ua.user_id = %s AND qq.questionnaire_id = %s
        ''', (user_id, questionnaire_id))
        
        answers = {}
        for row in cursor.fetchall():
            answers[row['question_id']] = row['selected_option_id']
            
        cursor.close()
        conn.close()
        return make_response(data=answers)
        
    except Exception as e:
        return make_response(code=500, message=str(e), data={})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
