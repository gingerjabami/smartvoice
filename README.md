# 🎙️ SmartVoice 

An intelligent voice assistant with real-time sentiment analysis and adaptive responses.

---

## 📦 Installation Guide

### 🖥️ System Requirements

- Python 3.8 or higher  
- Operating System: Windows  
- Microphone hardware (for voice input)

---
###🔧 1. Set Up Virtual Environment (Windows)

```bash

python -m venv .venv
.venv\Scripts\activate
```

## 🎧 Hardware Setup

### 🎤 Microphone Configuration
Set your microphone as the default input device.

Test it using system sound settings.

### 🔊 Speaker Setup
Default output device will be used for spoken responses.

### 🧠 Speech Recognition Failures
Ensure you're connected to the internet (Google API requires it)
Minimize background noise

## 📁 File Structure

```bash
├── requirements.txt        # Complete dependency list
├── smartvoice.py           # Core voice assistant
├── app.py                  # Flask web server
├── README.md               # Project documentation
├── .venv/                  # Virtual environment
└── templates/
    └── index.html          # Web interface template
```
### 📄 License
This project is licensed under the MIT License.

**Note:** All dependencies are pinned in *requirements.txt* to ensure reproducible builds.