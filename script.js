// 用于存储树洞帖子的数组
let posts = [];

// 发布新帖子
function publishPost() {
    const postContent = document.getElementById('post-content').value.trim();
    
    if (!postContent) {
        alert('写点什么再发布吧~');
        return;
    }
    
    // 创建新帖子对象
    const newPost = {
        content: postContent,
        timestamp: new Date().toLocaleString('zh-CN')
    };
    
    // 添加到帖子数组
    posts.unshift(newPost); // 新帖子放在最前面
    
    // 清空输入框
    document.getElementById('post-content').value = '';
    
    // 更新页面显示
    renderPosts();
}

// 渲染帖子列表
function renderPosts() {
    const postsList = document.getElementById('posts-list');
    
    if (posts.length === 0) {
        postsList.innerHTML = '<p class="empty-tip">树洞里还没有声音... 成为第一个分享的人吧！</p>';
        return;
    }
    
    // 生成帖子HTML
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
    else {
        // 默认回复
        const defaultResponses = [
            "谢谢分享你的感受。有时候把心事说出来本身就能让人轻松一些。",
            "我在这里倾听。如果你想聊聊更多，我随时都在。",
            "我理解这种感觉。生活中总会有起起落落，这都是成长的一部分。",
            "你的感受很重要。记住，照顾好自己的情绪健康是勇敢的表现。",
            "不确定该怎么帮你，但我真的很关心你的感受。想多聊一些吗？"
        ];
        return defaultResponses[Math.floor(Math.random() * defaultResponses.length)];
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    renderPosts();
});