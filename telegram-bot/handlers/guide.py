from telegram import Update
from telegram.ext import ContextTypes

async def command_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /guide command"""
    guide_text = """
📖 *Panduan Umrah*

Pilih tahapan:
1️⃣ Ihram & Miqat
2️⃣ Thawaf
3️⃣ Sa'i
4️⃣ Tahallul

Contoh: ketik "Cara thawaf" atau "Doa sa'i"
    """
    
    await update.message.reply_text(
        guide_text,
        parse_mode='Markdown'
    )
