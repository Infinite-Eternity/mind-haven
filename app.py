from flask import Flask, request, jsonify
from flask_cors import CORS  # 导入CORS包
import datetime

# 创建一个Flask应用实例
app = Flask(__name__)
CORS(app)  # 为整个应用启用CORS，允许前端跨域访问

# 用一个全局列表在内存中模拟数据库（重启服务器数据会丢失，下一步会换成真数据库）
posts = []

# 定义API路由：获取所有帖子
@app.route('/api/posts', methods=['GET'])
def get_posts():
    # 直接返回posts列表，jsonify会将其转换为JSON格式
    return jsonify(posts)

# 定义API路由：创建新帖子
@app.route('/api/posts', methods=['POST'])
def create_post():
    # 从前端发送的JSON数据中获取内容
    data = request.get_json()
    post_content = data.get('content')

    if not post_content:
        return jsonify({'error': '内容不能为空'}), 400

    # 创建一个新的帖子对象
    new_post = {
        'id': len(posts) + 1, # 简单模拟一个ID
        'content': post_content,
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    posts.append(new_post)
    posts.reverse() # 新的放在前面
    # 返回成功信息和新建的帖子
    return jsonify(new_post), 201

# 启动Flask开发服务器
if __name__ == '__main__':
    app.run(debug=True, port=5000) # 在5000端口运行，debug模式方便调试