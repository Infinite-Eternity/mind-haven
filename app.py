from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from pymongo import MongoClient
import os

app = Flask(__name__)

# 简化 CORS 配置 - 允许所有来源
CORS(app)

# MongoDB 连接
uri = os.getenv('MONGODB_URI',
                "mongodb+srv://Infinite_Eternity:Infi_Eternity@mind-haven.ukpo6vf.mongodb.net/?retryWrites=true&w=majority&appName=mind-haven")

try:
    client = MongoClient(uri)
    # 测试连接
    client.admin.command('ping')
    print("成功连接到 MongoDB!")
except Exception as e:
    print(f"连接到 MongoDB 失败: {e}")
    client = None

# 指定数据库和集合
if client:
    db = client['mind_haven_db']
    posts_collection = db['posts']
else:
    posts_collection = None


# 健康检查端点
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


# 根路由
@app.route('/')
def home():
    return jsonify({
        'message': 'Mind Haven API 正在运行!',
        'endpoints': {
            'get_posts': '/api/posts (GET)',
            'create_post': '/api/posts (POST)',
            'health_check': '/health (GET)'
        }
    })


# API 路由 - 获取所有帖子
@app.route('/api/posts', methods=['GET'])
def get_posts():
    if not posts_collection:
        return jsonify({'error': '数据库连接失败'}), 500

    try:
        posts_list = list(posts_collection.find().sort('timestamp', -1))
        for post in posts_list:
            post['_id'] = str(post['_id'])
        return jsonify(posts_list)
    except Exception as e:
        print(f"获取帖子时出错: {e}")
        return jsonify({'error': '内部服务器错误'}), 500


# API 路由 - 创建新帖子
@app.route('/api/posts', methods=['POST'])
def create_post():
    if not posts_collection:
        return jsonify({'error': '数据库连接失败'}), 500

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '无效的 JSON 数据'}), 400

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
        print(f"创建帖子时出错: {e}")
        return jsonify({'error': '内部服务器错误'}), 500


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)