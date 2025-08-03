# AI Orchestrator - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- OpenAI API Key

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd ai-orchestrator
./setup.sh
```

### 2. Configure API Keys
Edit the `.env` file and add your OpenAI API key:
```bash
OPENAI_API_KEY=your-openai-api-key-here
```

### 3. Run with Docker (Recommended)
```bash
docker-compose up -d
```

### 4. Access the Application
- **Web Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🎯 Try Your First Command

1. Open the web dashboard at http://localhost:3000
2. In the command interface, try: `"Go to google.com and search for 'AI automation'"`
3. Watch the task monitor to see your command being processed!

## 📋 Example Commands

### Browser Automation
- `"Go to google.com and search for 'Python tutorials'"`
- `"Take a screenshot of https://example.com"`
- `"Fill out the contact form at https://example.com/contact"`

### Document Management
- `"Create a Google Sheet with sales data for Q1 2024"`
- `"Generate a Google Doc about AI trends"`

### Communication
- `"Make a phone call to +1234567890 and leave a message"`
- `"Send a text message to +1234567890"`

### Media Processing
- `"Transcribe the video at https://example.com/video.mp4"`
- `"Summarize the audio file at https://example.com/audio.mp3"`

### AI Bot Creation
- `"Create a customer service bot for my website"`
- `"Build a sales assistant bot"`

## 🔧 Development Mode

### Backend Development
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

### Frontend Development
```bash
cd frontend/web
npm run dev
```

## 📊 Monitoring

- **Task Queue**: Monitor pending, processing, and completed tasks
- **Service Health**: Check the status of all AI services
- **Real-time Updates**: Dashboard refreshes every 5 seconds

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using the port
   lsof -i :8000
   # Kill the process or change ports in docker-compose.yml
   ```

2. **OpenAI API errors**
   - Verify your API key is correct
   - Check your OpenAI account has sufficient credits

3. **Docker issues**
   ```bash
   # Rebuild containers
   docker-compose down
   docker-compose build --no-cache
   docker-compose up -d
   ```

4. **Database issues**
   ```bash
   # Reset database
   rm backend/ai_orchestrator.db
   docker-compose restart ai-orchestrator
   ```

## 📚 Next Steps

1. **Add More Services**: Configure Google APIs, Twilio, etc.
2. **Custom Commands**: Extend the command parser for your specific needs
3. **Mobile App**: Build the React Native mobile interface
4. **Advanced Features**: Implement conversation history, user management

## 🆘 Support

- Check the logs: `docker-compose logs -f ai-orchestrator`
- API Documentation: http://localhost:8000/docs
- Issues: Create an issue in the repository

---

**Happy automating! 🤖**