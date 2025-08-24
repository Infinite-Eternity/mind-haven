from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from pymongo import MongoClient
import os

app = Flask(__name__)

# 更明确的 CORS 配置
cors = CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:5000",
            "http://localhost:8000",
            "https://*.netlify.app",  # 允许所有 Netlify 子域名
            "https://your-netlify-site.netlify.app"  # 替换为你的实际 Netlify 域名
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

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
db = client['mind_haven_db']
posts_collection = db['posts']


# 添加一个健康检查端点
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


@app.route('/api/posts', methods=['GET', 'OPTIONS'])
def get_posts():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    try:
        # 从数据库查找所有帖子，按时间倒序排列
        posts_list = list(posts_collection.find().sort('timestamp', -1))
        # 将ObjectId转换为字符串
        for post in posts_list:
            post['_id'] = str(post['_id'])
        return _corsify_actual_response(jsonify(posts_list))
    except Exception as e:
        print("Error in GET /api/posts:", e)
        return _corsify_actual_response(jsonify({'error': 'Internal server error'}), 500)


@app.route('/api/posts', methods=['POST', 'OPTIONS'])
def create_post():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    try:
        data = request.get_json()
        post_content = data.get('content')

        if not post_content:
            return _corsify_actual_response(jsonify({'error': '内容不能为空'}), 400)

        new_post = {
            'content': post_content,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # 插入新帖子
        result = posts_collection.insert_one(new_post)
        # 将插入后生成的ObjectId也返回给前端
        new_post['_id'] = str(result.inserted_id)

        return _corsify_actual_response(jsonify(new_post), 201)
    except Exception as e:
        print("Error in POST /api/posts:", e)
        return _corsify_actual_response(jsonify({'error': 'Internal server error'}), 500)


# CORS 预检请求处理
def _build_cors_preflight_response():
    response = jsonify()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


# 为实际响应添加 CORS 头
def _corsify_actual_response(response, status_code=200):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


port = int(os.environ.get('PORT', 5000))
# 启动应用，监听所有网络接口（'0.0.0.0'），并端口
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)