# ��� Railway Deployment Guide

## Prerequisites

1. ✅ GitHub account
2. ✅ Railway account (sign up at https://railway.app)
3. ✅ Groq API key (from https://console.groq.com)
4. ✅ Telegram bot token (from @BotFather)

## Quick Deploy (5 minutes)

### Step 1: Deploy Backend

1. Go to https://railway.app/new
2. Click **"Deploy from GitHub repo"**
3. Select: `mshadianto/umrah-mandiri-bot`
4. Click **"Add variables"**
```
   GROQ_API_KEY=your-groq-key-here
```
5. Click **"Deploy"**
6. Wait ~2 minutes
7. Copy the deployed URL (e.g., `https://umrah-backend-xxx.up.railway.app`)

### Step 2: Deploy Bot

1. Same project → **"New Service"**
2. **"Deploy from GitHub repo"**
3. Select: `mshadianto/umrah-mandiri-bot`
4. Click **"Add variables"**
```
   TELEGRAM_BOT_TOKEN=your-bot-token
   API_URL=https://umrah-backend-xxx.up.railway.app
   GROQ_API_KEY=your-groq-key-here
```
5. Click **"Deploy"**
6. Wait ~2 minutes

### Step 3: Configure Root Directories

**Backend Service:**
1. Settings → Source
2. Root Directory: `backend`
3. Save

**Bot Service:**
1. Settings → Source
2. Root Directory: `telegram-bot`
3. Save

### Step 4: Test

1. Open Telegram
2. Find your bot
3. Send `/start`
4. Should work! ✅

## Troubleshooting

**Bot not responding:**
- Check Railway logs
- Verify API_URL points to backend
- Test backend: `curl https://your-backend.railway.app/health`

**Backend errors:**
- Check GROQ_API_KEY is set
- View logs in Railway dashboard

## Cost

**Free Tier:**
- $5 monthly credit (new accounts)
- Enough for testing

**After trial:**
- ~$5-10/month for both services

## Support

Issues? Open GitHub issue or contact support.
