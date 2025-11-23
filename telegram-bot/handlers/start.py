from telegram import Update
from telegram.ext import ContextTypes

async def command_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    welcome_text = """
🕌 *Assalamu'alaikum!*

Selamat datang di *Umrah Assistant Bot* 🤖

Saya siap membantu perjalanan umrah Anda dengan fitur:

📚 Panduan Manasik
🤲 Doa & Dzikir  
📍 Navigasi Lokasi
💰 Kalkulator Budget
🆘 Bantuan Darurat

Ketik /help untuk melihat semua perintah.
    """
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown'
    )
