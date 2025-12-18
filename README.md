# 🍽️ Mediterranean Delight - AI Restaurant Agent

> **Hackathon Project**: An intelligent restaurant management system with AI-powered chatbot, dynamic menu, and smart booking features.

## ✨ Features

### 🤖 AI-Powered Chatbot
- Natural language processing for customer queries
- Menu information and recommendations
- Booking retrieval and management
- Operating hours and location info
- Context-aware conversations

### 📋 Interactive Menu System
- Dynamic menu with categories (Appetizers, Main Course, Desserts, Drinks)
- Beautiful card-based UI with images
- Add to cart functionality
- Real-time cart updates

### 🛒 Smart Shopping Cart
- Real-time cart management
- Automatic 10% discount on orders >$500
- Persistent cart (localStorage)
- Toast notifications for better UX

### 📅 Booking Management
- Simple reservation form
- Unique booking ID generation
- Email confirmation system
- Table preference selection
- Date/time validation

### 🌓 Modern UI/UX
- Beautiful gradient hero sections
- Dark/Light theme toggle
- Smooth animations and transitions
- Fully responsive design
- Glassmorphism effects

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ai-restorant-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Visit** `http://localhost:5000`

## 🌐 Deployment

### Quick Deploy (Recommended for Hackathons)

**Deploy on Render** - *Fastest option!*

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Create new Web Service from your repo
4. Add environment variable: `OPENAI_API_KEY`
5. Deploy! ✅

📖 **Full deployment guide:** See [deployment_guide.md](deployment_guide.md)

### Supported Platforms
- ✅ Render (Recommended)
- ✅ Railway
- ✅ Heroku
- ✅ Any platform supporting Python/Flask

## 🛠️ Tech Stack

**Backend:**
- Python 3.11+
- Flask (Web Framework)
- SQLite (Database)
- OpenAI API (AI Chatbot)

**Frontend:**
- HTML5/CSS3
- Vanilla JavaScript
- Responsive Design
- CSS Variables for theming

## 📁 Project Structure

```
ai-restorant-agent/
├── app.py                 # Main Flask application
├── agent.py              # AI chatbot agent logic
├── database.py           # Database operations
├── email_service.py      # Email notifications
├── requirements.txt      # Python dependencies
├── Procfile             # Deployment configuration
├── runtime.txt          # Python version
├── static/              # Frontend files
│   ├── index.html       # Homepage
│   ├── menu.html        # Menu page
│   ├── booking.html     # Booking form
│   ├── styles.css       # Main stylesheet
│   ├── cart.css         # Cart styles
│   ├── chatbot.css      # Chatbot styles
│   ├── app.js           # Theme toggle
│   ├── cart.js          # Cart functionality
│   └── chatbot.js       # Chatbot widget
└── restaurant.db        # SQLite database
```

## 🔑 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for chatbot |
| `FLASK_ENV` | No | Set to `production` for deployment |
| `PORT` | No | Port number (auto-set by platforms) |

## 🎯 Demo Features

### For Hackathon Judges

1. **Homepage** (`/`)
   - Hero section with CTA buttons
   - Feature cards highlighting USPs
   - Opening hours and contact info
   - Theme toggle demonstration

2. **Menu** (`/menu.html`)
   - Dynamic menu loading from database
   - Add to cart functionality
   - Cart sidebar with real-time updates
   - Automatic discount calculation

3. **Booking** (`/booking.html`)
   - Reservation form with validation
   - Unique booking ID generation
   - Email confirmation (if configured)

4. **AI Chatbot** (Click 💬 button)
   - Ask about menu, hours, location
   - Retrieve bookings by ID
   - Natural conversation flow

## 🧪 Testing

### Try These Chatbot Commands:
- "Show me the menu"
- "What are your hours?"
- "Get booking BK001"
- "What's your location?"
- "I need help with a reservation"

## 📊 Database Schema

**Bookings Table:**
- id (Primary Key)
- customer (Name)
- email
- phone
- date
- time
- guests (Number)
- table_pref (Preference)
- status
- created_at

**Menu Table:**
- id (Primary Key)
- name
- description
- price
- category
- image

## 🏆 Hackathon Highlights

- ✅ Modern, professional UI/UX
- ✅ AI integration (OpenAI)
- ✅ Full-stack application
- ✅ Database management
- ✅ Real-time features
- ✅ Email notifications
- ✅ Production-ready deployment
- ✅ Mobile responsive

## 📝 License

MIT License - feel free to use for your projects!

## 🤝 Contributing

This is a hackathon project, but contributions are welcome!

---

**Built with ❤️ for [Hackathon Name]**

🌐 **Live Demo:** [Your deployed URL here]
