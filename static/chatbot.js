// AI Chatbot Widget JavaScript

class Chatbot {
    constructor() {
        this.isOpen = false;
        this.context = [];
        this.init();
    }

    init() {
        this.createChatbotHTML();
        this.attachEventListeners();
        this.addWelcomeMessage();
    }

    createChatbotHTML() {
        const chatbotHTML = `
            <!-- Chatbot Button -->
            <button class="chatbot-button" id="chatbot-button">
                💬
            </button>

            <!-- Chatbot Window -->
            <div class="chatbot-window" id="chatbot-window">
                <div class="chatbot-header">
                    <div class="chatbot-title">
                        <span>🤖</span>
                        <span>AI Assistant</span>
                    </div>
                    <button class="chatbot-close" id="chatbot-close">✕</button>
                </div>

                <div class="chatbot-messages" id="chatbot-messages">
                    <!-- Messages will be added here -->
                </div>

                <div class="chatbot-input-area">
                    <textarea 
                        class="chatbot-input" 
                        id="chatbot-input" 
                        placeholder="Type your message..."
                        rows="1"
                    ></textarea>
                    <button class="chatbot-send" id="chatbot-send">
                        ➤
                    </button>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', chatbotHTML);
    }

    attachEventListeners() {
        const button = document.getElementById('chatbot-button');
        const closeBtn = document.getElementById('chatbot-close');
        const sendBtn = document.getElementById('chatbot-send');
        const input = document.getElementById('chatbot-input');

        button.addEventListener('click', () => this.toggleChat());
        closeBtn.addEventListener('click', () => this.closeChat());
        sendBtn.addEventListener('click', () => this.sendMessage());
        
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Auto-resize textarea
        input.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 100) + 'px';
        });
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        const window = document.getElementById('chatbot-window');
        window.classList.toggle('active');
        
        if (this.isOpen) {
            document.getElementById('chatbot-input').focus();
        }
    }

    closeChat() {
        this.isOpen = false;
        document.getElementById('chatbot-window').classList.remove('active');
    }

    addWelcomeMessage() {
        const messagesContainer = document.getElementById('chatbot-messages');
        const welcomeHTML = `
            <div class="welcome-message">
                <h4>👋 Welcome!</h4>
                <p>I'm your AI assistant. I can help you with:</p>
                <div class="quick-actions">
                    <button class="quick-action" onclick="chatbot.sendQuickMessage('Show me the menu')">📋 Menu</button>
                    <button class="quick-action" onclick="chatbot.sendQuickMessage('What are your hours?')">🕐 Hours</button>
                    <button class="quick-action" onclick="chatbot.sendQuickMessage('Get booking BK001')">🔍 Find Booking</button>
                </div>
            </div>
        `;
        messagesContainer.innerHTML = welcomeHTML;
    }

    sendQuickMessage(message) {
        document.getElementById('chatbot-input').value = message;
        this.sendMessage();
    }

    async sendMessage() {
        const input = document.getElementById('chatbot-input');
        const message = input.value.trim();
        
        if (!message) return;

        // Clear input
        input.value = '';
        input.style.height = 'auto';

        // Add user message to UI
        this.addMessage(message, 'user');

        // Show typing indicator
        this.showTypingIndicator();

        // Send to backend
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    context: this.context
                })
            });

            const data = await response.json();
            
            // Remove typing indicator
            this.hideTypingIndicator();

            if (data.success) {
                const botResponse = data.response;
                
                // Format response message
                let responseText = botResponse.message;
                
                // If there's data, format it nicely
                if (botResponse.data) {
                    if (botResponse.action === 'booking_retrieved') {
                        const booking = botResponse.data;
                        responseText += `\n\n📅 Booking Details:\n` +
                                      `Customer: ${booking.customer}\n` +
                                      `Date: ${booking.date}\n` +
                                      `Time: ${booking.time}\n` +
                                      `Guests: ${booking.guests}\n` +
                                      `Table: ${booking.table_pref || booking.table}\n` +
                                      `Status: ${booking.status}`;
                    }
                }

                this.addMessage(responseText, 'bot');

                // Update context
                this.context.push({
                    user: message,
                    bot: responseText,
                    action: botResponse.action
                });
            } else {
                this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            }
        } catch (error) {
            this.hideTypingIndicator();
            this.addMessage('Sorry, I couldn\'t connect to the server. Please try again later.', 'bot');
            console.error('Chat error:', error);
        }
    }

    addMessage(text, sender) {
        const messagesContainer = document.getElementById('chatbot-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message message-${sender}`;
        
        // Format text (preserve line breaks)
        const formattedText = text.replace(/\n/g, '<br>');
        messageDiv.innerHTML = formattedText;

        messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    showTypingIndicator() {
        const messagesContainer = document.getElementById('chatbot-messages');
        const typingHTML = `
            <div class="typing-indicator" id="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;
        messagesContainer.insertAdjacentHTML('beforeend', typingHTML);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }
}

// Initialize chatbot when page loads
let chatbot;
document.addEventListener('DOMContentLoaded', () => {
    chatbot = new Chatbot();
});
