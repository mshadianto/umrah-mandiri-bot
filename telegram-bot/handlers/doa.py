from telegram import Update
from telegram.ext import ContextTypes

async def command_doa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /doa command"""
    doa_text = """
🤲 *Doa & Dzikir*

Pilih kategori:
- Doa Ihram
- Doa Thawaf
- Doa Sa'i
- Doa Multazam
- Doa Umum

Contoh: ketik "Doa thawaf"
    """
    
    await update.message.reply_text(
        doa_text,
        parse_mode='Markdown'
    )
