# AI Orchestrator - Central AI Management System

A comprehensive AI-powered orchestration platform that manages multiple services through natural language commands.

## 🚀 Features

### Core Services
- **Central AI Orchestrator**: Natural language processing and task routing
- **Browser Automation**: Web interactions, Make.com workflows, Canva design creation
- **Document Management**: Google Sheets/Docs integration
- **Communication Service**: Voice calls, speech recognition, conversation management
- **Media Processing**: Video transcription, content summarization
- **AI Bot Builder**: Automated bot creation and deployment

### Interfaces
- **Web Dashboard**: React/Next.js with Tailwind CSS
- **Mobile App**: React Native for mobile control

## 🛠️ Tech Stack

### Backend
- **Python 3.11+** with FastAPI
- **SQLAlchemy** for database management
- **OpenAI GPT-4** for natural language processing
- **Playwright** for browser automation
- **Google APIs** for document management
- **Twilio** for communication
- **OpenAI Whisper** for media processing

### Frontend
- **React/Next.js** for web interface
- **Tailwind CSS** for styling
- **React Native** for mobile app

## 📁 Project Structure

```
ai-orchestrator/
├── backend/
│   ├── app/
│   │   ├── core/           # Core orchestrator
│   │   ├── services/       # Individual services
│   │   ├── models/         # Database models
│   │   └── api/           # API routes
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── web/               # React web dashboard
│   └── mobile/            # React Native app
├── docker-compose.yml
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-orchestrator
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend/web
   npm install
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run the Application**
   ```bash
   # Backend
   cd backend
   uvicorn main:app --reload
   
   # Frontend (in another terminal)
   cd frontend/web
   npm run dev
   ```

## 🔧 Configuration

### Required API Keys
- OpenAI API Key
- Google Cloud API Key
- Twilio Account SID & Auth Token
- ElevenLabs API Key (optional)

### Environment Variables
See `.env.example` for all required environment variables.

## 📚 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.