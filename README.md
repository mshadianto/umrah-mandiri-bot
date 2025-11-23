# Ìµå Umrah Mandiri Bot

AI-powered Telegram bot untuk panduan umrah mandiri.

## Features

- Ì¥ñ AI Chat dengan RAG
- Ìµå Jadwal Sholat Real-time
- Ì∑∫Ô∏è Navigasi & Lokasi
- Ì∂ò Bantuan Darurat 24/7
- Ì≥ä Progress Tracking
- Ì¥≤ Doa & Dzikir Lengkap

## Tech Stack

- **Backend**: FastAPI
- **Bot**: python-telegram-bot
- **AI**: Groq (Llama 3)
- **Database**: TinyDB
- **Deploy**: Railway + Vercel

## Setup Local
```bash
# Clone
git clone https://github.com/mshadianto/umrah-mandiri-bot.git
cd umrah-mandiri-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install bot dependencies
cd ../telegram-bot
pip install -r requirements.txt

# Create .env files
# backend/.env
GROQ_API_KEY=your-groq-key

# telegram-bot/.env
TELEGRAM_BOT_TOKEN=your-bot-token
API_URL=http://localhost:8000

# Run backend
cd backend
uvicorn app.main:app --reload

# Run bot (new terminal)
cd telegram-bot
python bot.py
```

## Deploy

### Railway (Bot + Backend)

1. Fork this repo
2. Go to [Railway](https://railway.app)
3. New Project ‚Üí Deploy from GitHub
4. Select repo ‚Üí Add services
5. Add environment variables
6. Deploy!

### Vercel (API Only)

1. Install Vercel CLI: `npm install -g vercel`
2. `cd backend && vercel --prod`
3. Add environment variables
4. Done!

## Environment Variables

### Backend
```
GROQ_API_KEY=gsk_...
```

### Bot
```
TELEGRAM_BOT_TOKEN=123456:ABC...
API_URL=https://your-backend.railway.app
GROQ_API_KEY=gsk_...
```

## Author

Created by M Shadianto

## License

MIT
