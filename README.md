# AI Orchestrator

A fully functional AI-powered orchestration platform that processes natural language commands using OpenRouter AI. The application runs on both PC and mobile browsers with a modern, responsive interface.

## 🚀 Features

- **Natural Language Processing**: Submit commands in plain English
- **Real-time Task Monitoring**: Track task status and progress
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Modern UI**: Clean, intuitive interface built with TailwindCSS
- **API Integration**: RESTful API with comprehensive endpoints
- **Task Queue Management**: Monitor pending, processing, and completed tasks
- **Conversation History**: Track all interactions
- **Error Handling**: Comprehensive error reporting and logging

## 🏗️ Architecture

- **Backend**: FastAPI with SQLAlchemy for database management
- **Frontend**: Modern HTML/CSS/JavaScript with TailwindCSS
- **AI Integration**: OpenRouter API for natural language processing
- **Database**: SQLite (can be easily switched to PostgreSQL/MySQL)
- **Task Queue**: Built-in queue management system

## 📁 Project Structure

```
ai-orchestrator/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py          # API endpoints
│   │   ├── core/
│   │   │   ├── command_parser.py  # Command parsing logic
│   │   │   └── orchestrator.py    # Main orchestration logic
│   │   ├── models/
│   │   │   ├── database.py        # Database models
│   │   │   ├── task.py           # Task model
│   │   │   ├── user.py           # User model
│   │   │   └── conversation.py   # Conversation model
│   │   └── services/
│   │       └── llm_service.py    # OpenRouter integration
│   ├── main.py                   # FastAPI application entry point
│   └── requirements.txt          # Python dependencies
├── frontend/
│   └── static/
│       ├── index.html            # Main HTML file
│       ├── styles.css            # Custom CSS styles
│       └── app.js               # Frontend JavaScript
├── .env.example                  # Environment variables template
├── README.md                     # This file
└── setup.sh                      # Setup script
```

## 🛠️ Quick Start

### Prerequisites

- Python 3.11+
- OpenRouter API key (get one at [openrouter.ai](https://openrouter.ai))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-orchestrator
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenRouter API key
   ```

3. **Install Python dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the application**
   - **Web Interface**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/health

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```bash
# Required
OPENROUTER_API_KEY=your-openrouter-api-key-here
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet

# Optional
HOST=0.0.0.0
PORT=8000
DEBUG=True
DATABASE_URL=sqlite:///./ai_orchestrator.db
```

### OpenRouter Setup

1. Visit [openrouter.ai](https://openrouter.ai)
2. Create an account and get your API key
3. Add the API key to your `.env` file
4. Choose your preferred model (default: `anthropic/claude-3.5-sonnet`)

## 📱 Usage

### Web Interface

1. Open your browser and navigate to `http://localhost:8000`
2. Enter a natural language command in the text area
3. Click "Submit Command" or press `Ctrl+Enter`
4. Monitor the task status in real-time
5. View results and conversation history

### Example Commands

- `"Go to google.com and search for 'AI automation'"`
- `"Create a summary of the latest AI trends"`
- `"Send an email to john@example.com about the meeting"`
- `"Analyze the sentiment of customer reviews"`

### API Endpoints

- `POST /api/v1/command` - Submit a new command
- `GET /api/v1/task/{task_id}` - Get task status
- `GET /api/v1/queue/status` - Get queue status
- `GET /api/v1/tasks` - List recent tasks
- `DELETE /api/v1/task/{task_id}` - Cancel a task
- `GET /api/v1/health` - Health check

## 🎨 Frontend Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Updates**: Automatic polling for status updates
- **Keyboard Shortcuts**: 
  - `Ctrl+Enter`: Submit command
  - `Escape`: Clear command input
- **Toast Notifications**: Success/error feedback
- **Loading States**: Visual feedback during processing
- **API Log**: Real-time API interaction logging

## 🔌 API Integration

The application exposes a RESTful API that can be integrated with other systems:

```bash
# Submit a command
curl -X POST "http://localhost:8000/api/v1/command" \
  -H "Content-Type: application/json" \
  -d '{"command": "Go to google.com and search for AI", "user_id": 1}'

# Get task status
curl "http://localhost:8000/api/v1/task/1"

# Get queue status
curl "http://localhost:8000/api/v1/queue/status"
```

## 🚀 Deployment

### Local Development

```bash
# Run with auto-reload
uvicorn backend.main:app --reload

# Run in production mode
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### Docker Deployment

```bash
# Build and run with Docker
docker build -t ai-orchestrator .
docker run -p 8000:8000 --env-file .env ai-orchestrator
```

### Production Considerations

- Use a production WSGI server like Gunicorn
- Set up a reverse proxy (Nginx/Apache)
- Configure SSL/TLS certificates
- Use a production database (PostgreSQL/MySQL)
- Set up proper logging and monitoring

## 🐛 Troubleshooting

### Common Issues

1. **Connection Error**
   - Check if the server is running
   - Verify the port is not in use
   - Check firewall settings

2. **OpenRouter API Errors**
   - Verify your API key is correct
   - Check your OpenRouter account has sufficient credits
   - Ensure the model name is valid

3. **Database Errors**
   - Check database file permissions
   - Verify DATABASE_URL in .env file
   - Ensure the logs directory exists

### Logs

Check the application logs at `backend/logs/ai_orchestrator.log` for detailed error information.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [OpenRouter](https://openrouter.ai) for AI model access
- [FastAPI](https://fastapi.tiangolo.com) for the web framework
- [TailwindCSS](https://tailwindcss.com) for styling
- [SQLAlchemy](https://sqlalchemy.org) for database ORM

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the API documentation at `/docs`
- Review the troubleshooting section above