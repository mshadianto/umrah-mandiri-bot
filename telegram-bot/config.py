# -*- coding: utf-8 -*-
"""
Enhanced Bot Configuration
"""
import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
API_URL = os.getenv('BACKEND_URL', 'https://umrah-mandiri-bot-production.up.railway.app')

# Feature Flags
FEATURES = {
    "ai_chat": True,
    "prayer_times": True,
    "navigation": True,
    "emergency": True,
    "progress_tracking": True,
    "voice_messages": True,
    "image_recognition": True,
    "scheduled_reminders": True,
    "group_support": True,
    "multilingual": True
}

# Supported Languages
LANGUAGES = {
    "id": "🇮🇩 Bahasa Indonesia",
    "en": "🇬🇧 English",
    "ar": "🇸🇦 العربية"
}

# Admin User IDs (for monitoring/management)
ADMIN_IDS = [
    # Add your Telegram ID here for admin features
]

# Rate Limiting
RATE_LIMIT = {
    "messages_per_minute": 20,
    "messages_per_hour": 100
}

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = 'bot.log'

# Database (TinyDB for local storage)
DB_PATH = 'user_data.json'

# API Configuration
API_TIMEOUT = 30.0
API_RETRY_ATTEMPTS = 3

# Notifications
PRAYER_TIME_REMINDER_MINUTES = 15  # Remind 15 mins before prayer

# Validate configuration
if not BOT_TOKEN or BOT_TOKEN == "8132751045:AAHPTRwRzUfJM2Q_rPFuAbpqsuyedF1cX9Q":
    raise ValueError("TELEGRAM_BOT_TOKEN not set in .env file!")

print("✅ Configuration loaded successfully")
print(f"🔗 API URL: {API_URL}")
print(f"🌍 Languages: {', '.join(LANGUAGES.keys())}")
print(f"⚡ Features enabled: {sum(FEATURES.values())}/{len(FEATURES)}")
