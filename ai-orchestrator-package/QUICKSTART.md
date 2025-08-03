# AI Orchestrator - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Prerequisites
- **Python 3.11+** (Download from [python.org](https://python.org))
- **OpenRouter API Key** (Get free key from [openrouter.ai](https://openrouter.ai))

### Step 1: Extract and Navigate
```bash
# Extract the ZIP file
unzip ai-orchestrator.zip
cd ai-orchestrator

# Or on Windows:
# Extract the ZIP file and open the folder
```

### Step 2: Start the Application

#### **Windows Users:**
```bash
# Double-click start.bat
# OR run in Command Prompt:
start.bat
```

#### **Mac/Linux Users:**
```bash
# Run in Terminal:
./start.sh
```

#### **All Platforms (Alternative):**
```bash
# Run the Python startup script:
python start.py
```

### Step 3: Configure and Use
1. **Get your OpenRouter API key** from [openrouter.ai](https://openrouter.ai)
2. **Edit the `.env` file** and add your API key:
   ```bash
   OPENROUTER_API_KEY=your-actual-api-key-here
   ```
3. **Access the application** at [http://localhost:8000](http://localhost:8000)

## 🎯 What You'll See

- **Modern Web Interface** - Works on desktop and mobile
- **Command Input** - Type natural language commands
- **Real-time Monitoring** - Watch tasks process live
- **Task History** - View all completed tasks
- **API Documentation** - Available at `/docs`

## 💡 Example Commands

Try these commands in the interface:

- `"Go to google.com and search for 'AI automation'"`
- `"Create a summary of the latest AI trends"`
- `"Analyze the sentiment of customer reviews"`
- `"Generate a report about machine learning"`

## 🔧 Troubleshooting

### Common Issues:

1. **"Python not found"**
   - Install Python 3.11+ from [python.org](https://python.org)
   - Make sure Python is added to PATH

2. **"Port 8000 already in use"**
   - Stop other applications using port 8000
   - Or change the port in the startup script

3. **"OpenRouter API errors"**
   - Verify your API key is correct
   - Check your OpenRouter account has credits

4. **"Dependencies not found"**
   - Run: `pip install -r backend/requirements.txt`

### Getting Help:
- Check the logs in `backend/logs/`
- Visit the API docs at `http://localhost:8000/docs`
- Review the main README.md file

## 🌟 Features

- ✅ **Responsive Design** - Works on all devices
- ✅ **Real-time Updates** - Live task monitoring
- ✅ **Natural Language** - Type commands in plain English
- ✅ **Modern UI** - Clean, intuitive interface
- ✅ **API Integration** - RESTful API for developers
- ✅ **Error Handling** - Comprehensive error reporting

## 📱 Mobile Usage

The application is fully responsive and works great on mobile devices:
- Open your mobile browser
- Navigate to `http://localhost:8000`
- Use touch-friendly interface
- Submit commands with voice or text

## 🔄 Stopping the Application

- Press `Ctrl+C` in the terminal/command prompt
- The server will shut down gracefully

---

**Need help?** Check the main README.md file for detailed documentation.