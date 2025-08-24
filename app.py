from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from pymongo import MongoClient
import os

app = Flask(__name__)

# 简化 CORS 配置
CORS(app)

# MongoDB 连接
uri = os.getenv('MONGODB_URI',
                "mongodb+srv://Infinite_Eternity:Infi_Eternity@mind-haven.ukpo6vf.mongodb.net/?retryWrites=true&w=majority&appName=mind-haven")

client = MongoClient(uri)

# 尝试连接并检查是否成功
try:
    db_names = client.list_database_names()
    print("Successfully connected to MongoDB! Available databases:", db_names)
except Exception as e:
    print("Failed to connect to MongoDB:", e)

# 指定数据库和集合
db = client['mind_haven_db']
posts_collection = db['posts']

# 健康检查端点
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

# 根路由
@app.route('/')
def home():
    return jsonify({
        'message': 'Mind Haven API is running!',
        'endpoints': {
            'get_posts': '/api/posts (GET)',
            'create_post': '/api/posts (POST)'
        }
    })

@app.route('/api/posts', methods=['GET'])
def get_posts():
    try:
        posts_list = list(posts_collection.find().sort('timestamp', -1))
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

        result = posts_collection.insert_one(new_post)
        new_post['_id'] = str(result.inserted_id)

        return jsonify(new_post), 201
    except Exception as e:
        print("Error in POST /api/posts:", e)
        return jsonify({'error': 'Internal server error'}), 500

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)