### **File 2: `telegram-bot/bot.py`**
**Path:** `telegram-bot/bot.py`  
**Action:** Replace - Remove duplicate budget handling

<details>
<summary>Click to expand - bot.py (FIXED)</summary>
```python
# -*- coding: utf-8 -*-
"""Umrah Assistant Bot - Clean Version"""
import logging
import sys
from datetime import datetime
import httpx
from telegram import Update, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction, ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)
from config import BOT_TOKEN, API_URL
from user_manager import user_manager
from keyboards import *

# Import budget handler
from handlers.budget_handler import get_budget_handler

# Logging
from loguru import logger
logger.remove()
logger.add(sys.stdout, level="INFO")

class APIClient:
    """API Client"""
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.timeout = 30.0
    
    async def call_api(self, endpoint: str, method: str = "POST", data: dict = None):
        """Make API call"""
        url = f"{self.base_url}{endpoint}"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                if method == "POST":
                    response = await client.post(url, json=data or {})
                else:
                    response = await client.get(url, params=data)
                
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            logger.error(f"API error: {e}")
            return None

api = APIClient(API_URL)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    user = update.effective_user
    user_manager.create_or_update_user(user.id, {
        'username': user.username,
        'first_name': user.first_name
    })
    
    welcome = f"""Assalamualaikum {user.first_name}! 👋

🕋 Selamat datang di *Umrah Assistant Bot v3.0*

*Fitur tersedia:*
💬 AI Chat - Tanya apa saja
🕌 Jadwal Sholat - Waktu sholat real-time
🗺️ Navigasi - Petunjuk lokasi
💰 Budget - Simulasi biaya umrah
🆘 Emergency - Bantuan darurat
📚 Tips - Panduan umrah

Pilih menu di bawah atau tanya langsung!"""
    
    await update.message.reply_text(
        welcome, 
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown"
    )

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu command"""
    await update.message.reply_text(
        "📋 *Menu Utama*\n\nPilih fitur yang Anda butuhkan:", 
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown"
    )

async def sholat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prayer times"""
    await update.message.chat.send_action(ChatAction.TYPING)
    
    result = await api.call_api(
        "/api/v1/advanced/prayer-times", 
        "POST", 
        {"location": "Makkah"}
    )
    
    if result:
        await update.message.reply_text(result.get("response", "Error"))
    else:
        await update.message.reply_text("❌ Tidak dapat mengambil jadwal sholat")

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages"""
    text = update.message.text
    
    # Handle menu buttons (except Budget - handled by ConversationHandler)
    if text == "💬 AI Chat":
        await update.message.reply_text(
            "💬 *AI Chat Mode*\n\n"
            "Tanyakan apa saja tentang umrah!\n"
            "Contoh: 'Bagaimana cara umroh mandiri?'",
            parse_mode="Markdown"
        )
    
    elif text == "🕌 Jadwal Sholat":
        await sholat_command(update, context)
    
    elif text == "🗺️ Navigasi":
        await update.message.reply_text(
            "🗺️ *Navigasi*\n\n"
            "Kirim lokasi Anda untuk mendapat petunjuk arah ke:\n"
            "• Masjidil Haram\n"
            "• Masjid Nabawi\n"
            "• Hotel terdekat\n"
            "• Restoran halal",
            parse_mode="Markdown"
        )
    
    elif text == "🆘 Emergency":
        keyboard = [
            [InlineKeyboardButton("🚨 Call Emergency", url="tel:911")],
            [InlineKeyboardButton("🏥 Nearest Hospital", callback_data="emergency_hospital")],
            [InlineKeyboardButton("🇸🇦 Saudi Emergency (997)", url="tel:997")],
            [InlineKeyboardButton("🇮🇩 KBRI Jeddah", url="tel:+966126603000")]
        ]
        await update.message.reply_text(
            "🆘 *Emergency Contacts*\n\n"
            "Pilih kontak darurat:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    
    elif text == "📚 Tips":
        tips = """📚 *Tips Umrah Mandiri*

✅ *Sebelum Berangkat:*
- Cek syarat visa umrah
- Booking hotel dekat Haram
- Download app navigasi offline
- Siapkan budget lebih

✅ *Di Makkah:*
- Ibadah di jam sepi (pagi/malam)
- Jaga kesehatan & istirahat
- Pakai sepatu nyaman
- Bawa air minum

✅ *Tips Hemat:*
- Makan di warung lokal
- Jalan kaki kalau dekat
- Beli oleh-oleh di pasar

Ketik /tips untuk tips lengkap!"""
        await update.message.reply_text(tips, parse_mode="Markdown")
    
    elif text == "⚙️ Settings":
        await update.message.reply_text(
            "⚙️ *Settings*\n\n"
            "• /language - Ganti bahasa\n"
            "• /notifications - Atur notifikasi\n"
            "• /help - Bantuan",
            parse_mode="Markdown"
        )
    
    elif text == "⬅️ Kembali ke Menu":
        await menu_command(update, context)
    
    else:
        # Send to AI Chat API
        await update.message.chat.send_action(ChatAction.TYPING)
        
        result = await api.call_api(
            "/api/v1/chat", 
            "POST", 
            {
                "message": text,
                "user_id": str(update.effective_user.id)
            }
        )
        
        if result:
            await update.message.reply_text(result.get("response", "Maaf, saya tidak mengerti."))
        else:
            await update.message.reply_text("❌ Maaf, terjadi kesalahan. Coba lagi nanti.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "emergency_hospital":
        await query.edit_message_text(
            "🏥 *Rumah Sakit Terdekat*\n\n"
            "📍 Kirim lokasi Anda untuk mencari RS terdekat",
            parse_mode="Markdown"
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot"""
    try:
        # Create application
        app = Application.builder().token(BOT_TOKEN).build()
        
        # IMPORTANT: Add budget conversation handler FIRST
        app.add_handler(get_budget_handler())
        
        # Add command handlers
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("menu", menu_command))
        app.add_handler(CommandHandler("sholat", sholat_command))
        
        # Add message and callback handlers
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
        app.add_handler(CallbackQueryHandler(button_callback))
        
        # Error handler
        app.add_error_handler(error_handler)
        
        # Set bot commands
        async def post_init(application: Application):
            await application.bot.set_my_commands([
                BotCommand("start", "Mulai bot"),
                BotCommand("menu", "Tampilkan menu"),
                BotCommand("sholat", "Jadwal sholat"),
                BotCommand("budget", "Simulasi budget umrah"),
                BotCommand("help", "Bantuan")
            ])
        
        app.post_init = post_init
        
        # Start bot
        logger.info("🚀 Bot started successfully!")
        logger.info(f"🔗 Backend API: {API_URL}")
        app.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
