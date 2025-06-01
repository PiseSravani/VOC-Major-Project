async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;

    // Add user message
    addMessage('user', message);
    input.value = '';

    // Show typing indicator
    showTypingIndicator();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        hideTypingIndicator();

        if (data.response) {
            addMessage('assistant', data.response);
        } else {
            addMessage('assistant', 'I apologize, but I encountered an error. Please try asking your question again.');
        }
    } catch (error) {
        hideTypingIndicator();
        addMessage('assistant', 'I am having trouble connecting to the server. Please check your connection and try again.');
        console.error('Error:', error);
    }
}

function addMessage(sender, text) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    const time = new Date().toLocaleTimeString();

    if (sender === 'user') {
        messageDiv.innerHTML = `
            <div class="flex items-start space-x-3 flex-row-reverse space-x-reverse mb-4">
                <div class="w-8 h-8 bg-gradient-to-r from-green-500 to-blue-500 rounded-full flex items-center justify-center text-white text-sm">
                    <i class="fas fa-user"></i>
                </div>
                <div class="bg-gradient-to-r from-blue-500 to-purple-500 text-white p-3 rounded-lg chat-bubble">
                    <p class="text-sm">${text}</p>
                    <p class="text-xs text-blue-100 mt-1">${time}</p>
                </div>
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="flex items-start space-x-3 mb-4">
                <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white text-sm">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="bg-gray-100 p-3 rounded-lg chat-bubble">
                    <p class="text-sm">${text}</p>
                    <p class="text-xs text-gray-500 mt-1">${time}</p>
                </div>
            </div>
        `;
    }
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    const chatMessages = document.getElementById('chat-messages');
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = `
        <div class="flex items-start space-x-3 mb-4">
            <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white text-sm">
                <i class="fas fa-robot"></i>
            </div>
            <div class="bg-gray-100 p-3 rounded-lg">
                <div class="flex space-x-1">
                    <div class="w-2 h-2 bg-gray-400 rounded-full typing"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full typing" style="animation-delay: 0.2s;"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full typing" style="animation-delay: 0.4s;"></div>
                </div>
            </div>
        </div>
    `;
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) indicator.remove();
}

function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(content => content.classList.add('hidden'));
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active', 'bg-blue-500', 'text-white');
        button.classList.add('bg-gray-100', 'text-gray-700');
    });
    document.getElementById(tabName + '-content').classList.remove('hidden');
    const activeTab = document.getElementById(tabName + '-tab');
    activeTab.classList.add('active', 'bg-blue-500', 'text-white');
    activeTab.classList.remove('bg-gray-100', 'text-gray-700');
}

function handleQuickAction(action) {
    document.getElementById('chat-input').value = action;
    sendMessage();
    switchTab('chat');
}

document.getElementById('chat-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') sendMessage();
});

document.addEventListener('DOMContentLoaded', function() {
    switchTab('chat');
});
