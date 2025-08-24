// API的基础URL，指向你本地运行的Flask服务器
const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:5000/api'
    : 'https://mind-haven-production.up.railway.app/api'; // 添加了 https://

// 用于存储树洞帖子的数组 (现在将从后端获取)
let posts = [];

// 页面加载完成后，自动加载帖子
document.addEventListener('DOMContentLoaded', function() {
    loadPosts();
});

// 从后端加载帖子
async function loadPosts() {
    try {
        const response = await fetch(`${API_BASE_URL}/posts`);
        posts = await response.json();
        renderPosts();
    } catch (error) {
        console.error('获取帖子失败:', error);
        // 如果后端不可用，显示错误信息但仍然保留页面其他功能
        document.getElementById('posts-list').innerHTML = 
            '<p class="empty-tip">暂时无法加载树洞内容，请检查后端服务器是否运行。</p>';
    }
}

// 发布新帖子
async function publishPost() {
    const postContent = document.getElementById('post-content').value.trim();
    
    if (!postContent) {
        alert('写点什么再发布吧~');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/posts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content: postContent })
        });
        
        if (response.ok) {
            // 发布成功，清空输入框并重新加载帖子列表
            document.getElementById('post-content').value = '';
            loadPosts(); // 重新从服务器获取最新列表
        } else {
            alert('发布失败！');
        }
    } catch (error) {
        console.error('发布帖子失败:', error);
        alert('发布失败，请检查网络连接和后端服务器。');
    }
}

// 渲染帖子列表
function renderPosts() {
    const postsList = document.getElementById('posts-list');
    
    if (posts.length === 0) {
        postsList.innerHTML = '<p class="empty-tip">树洞里还没有声音... 成为第一个分享的人吧！</p>';
        return;
    }
    
    // 生成帖子HTML (新帖子在前)
    postsList.innerHTML = posts.map(post => `
        <div class="post">
            <p>${post.content}</p>
            <small>发布时间: ${post.timestamp}</small>
        </div>
    `).join('');
}

// 发送消息到AI伙伴
function sendMessage() {
    const userInput = document.getElementById('user-input').value.trim();
    const chatMessages = document.getElementById('chat-messages');
    
    if (!userInput) return;
    
    // 添加用户消息
    addMessage(userInput, 'user');
    
    // 清空输入框
    document.getElementById('user-input').value = '';
    
    // 模拟AI思考并回复（简单版）
    setTimeout(() => {
        let aiResponse = generateAIResponse(userInput);
        addMessage(aiResponse, 'ai');
        
        // 自动滚动到底部
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 1000);
}

// 添加消息到聊天窗口
function addMessage(text, sender) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const messageP = document.createElement('p');
    messageP.textContent = text;
    
    messageDiv.appendChild(messageP);
    chatMessages.appendChild(messageDiv);
    
    // 自动滚动到底部
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 生成AI回复（简易规则库）
function generateAIResponse(userInput) {
    userInput = userInput.toLowerCase();
    
    // 关键词匹配回复
    if (userInput.includes('压力') || userInput.includes('焦虑') || userInput.includes('紧张')) {
        return "听起来你最近压力有些大。试试深呼吸：用4秒吸气，屏住呼吸7秒，然后用8秒慢慢呼气。重复几次，可能会让你感觉平静一些。";
    }
    else if (userInput.includes('开心') || userInput.includes('高兴') || userInput.includes('幸福')) {
        return "真为你感到高兴！记住这种感觉，生活中总会有这样的美好时刻。";
    }
    else if (userInput.includes('朋友') || userInput.includes('人际') || userInput.includes('交往')) {
        return "人际关系有时确实会带来烦恼。做真实的自己，找到那些能让你感到轻松自在的人，真诚的友谊需要时间培养。";
    }
    else if (userInput.includes('学习') || userInput.includes('考试') || userInput.includes('成绩')) {
        return "学习是成长的一部分，但不要忘记平衡休息。尝试制定一个合理的学习计划，每次完成一个小目标就奖励自己一下。";
    }
    else if (userInput.includes('父母') || userInput.includes('家长') || userInput.includes('家庭')) {
        return "和家人相处有时不容易。试着找一个平静的时刻，真诚地分享你的感受，倾听他们的想法，沟通是理解的桥梁。";
    }
    else if (userInput.includes('无聊') || userInput.includes('没意思') || userInput.includes('无趣')) {
        return "有时候感到无聊是尝试新事物的好机会！有没有一直想学但没时间尝试的技能或爱好？现在可能就是开始的好时机。";
    }
    else if (userInput.includes('谢谢') || userInput.includes('感谢')) {
        return "不用客气！我很高兴能陪伴你。记住，你并不孤单。";
    }
    else if (userInput.includes('你好') || userInput.includes('嗨') || userInput.includes('hello')) {
        return "你好！我是你的AI伙伴小港湾。如果你感到压力大、迷茫或者只是想聊聊天，我随时都在这里。今天有什么想分享的吗？";
    }
    else if (userInput.includes('失眠') || userInput.includes('睡不着')) {
        return "失眠确实令人困扰。试着睡前一小时避免使用电子设备，喝杯温热的牛奶，或者听一些轻柔的音乐可能会有帮助。";
    }
    else if (userInput.includes('未来') || userInput.includes('迷茫')) {
        return "对未来感到迷茫是很正常的，每个人都会经历这个阶段。试着从小事做起，专注于当下，未来的道路会慢慢清晰起来的。";
    }
    else {
        // 默认回复
        const defaultResponses = [
            "谢谢分享你的感受。有时候把心事说出来本身就能让人轻松一些。",
            "我在这里倾听。如果你想聊聊更多，我随时都在。",
            "我理解这种感觉。生活中总会有起起落落，这都是成长的一部分。",
            "你的感受很重要。记住，照顾好自己的情绪健康是勇敢的表现。",
            "不确定该怎么帮你，但我真的很关心你的感受。想多聊一些吗？",
            "感谢你愿意分享这些。有时候，仅仅是表达出来就能减轻内心的负担。",
            "我明白这不容易。你正在经历的事情，很多人也都曾经历过，你并不孤单。"
        ];
        return defaultResponses[Math.floor(Math.random() * defaultResponses.length)];
    }
}