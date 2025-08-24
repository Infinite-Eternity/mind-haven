from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from pymongo import MongoClient  # 修改导入方式
import os

app = Flask(__name__)
CORS(app)

# 注意：请将 <your-real-password> 替换为你的真实密码，并确保密码已进行URL编码
uri = os.getenv('MONGODB_URI',
                "mongodb+srv://Infinite_Eternity:Infi_Eternity@mind-haven.ukpo6vf.mongodb.net/?retryWrites=true&w=majority&appName=mind-haven")

# 创建MongoDB客户端
client = MongoClient(uri)

# 尝试连接并检查是否成功
try:
    # 列出数据库名是一个简单的连接测试方法
    db_names = client.list_database_names()
    print("Successfully connected to MongoDB! Available databases:", db_names)
except Exception as e:
    print("Failed to connect to MongoDB:", e)

# 指定数据库和集合
db = client['mind_haven_db']  # 使用下标语法
posts_collection = db['posts']


@app.route('/api/posts', methods=['GET'])
def get_posts():
    try:
        # 从数据库查找所有帖子，按时间倒序排列
        posts_list = list(posts_collection.find().sort('timestamp', -1))
        # 将ObjectId转换为字符串
        for post in posts_list:
            post['_id'] = str(post['_id'])
        return jsonify(posts_list)
    except Exception as e:
        print("Error in GET /api/posts:", e)
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/posts', methods=['POST'])
def create_post():
    try:
        data = request.get_json()
        post_content = data.get('content')

        if not post_content:
            return jsonify({'error': '内容不能为空'}), 400

        new_post = {
            'content': post_content,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # 插入新帖子
        result = posts_collection.insert_one(new_post)
        # 将插入后生成的ObjectId也返回给前端
        new_post['_id'] = str(result.inserted_id)

        return jsonify(new_post), 201
    except Exception as e:
        print("Error in POST /api/posts:", e)
        return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)