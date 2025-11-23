# -*- coding: utf-8 -*-
"""Umrah Assistant Bot - Clean Version"""
import logging
import sys
from datetime import datetime

import httpx
from telegram import Update, BotCommand
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
    
    welcome = f"""Assalamualaikum {user.first_name}!

Selamat datang di Umrah Assistant Bot v3.0

Fitur tersedia:
- AI Chat
- Jadwal Sholat
- Navigasi
- Emergency
- Tips

Pilih menu di bawah atau tanya langsung!"""
    
    await update.message.reply_text(welcome, reply_markup=main_menu_keyboard())

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu command"""
    await update.message.reply_text("Menu Utama", reply_markup=main_menu_keyboard())

async def sholat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prayer times"""
    await update.message.chat.send_action(ChatAction.TYPING)
    
    result = await api.call_api("/api/v1/advanced/prayer-times", "POST", {"location": "Makkah"})
    
    if result:
        await update.message.reply_text(result.get("response", "Error"))
    else:
        await update.message.reply_text("Tidak dapat mengambil jadwal sholat")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle buttons"""
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    user_id = update.effective_user.id
    
    await query.message.chat.send_action(ChatAction.TYPING)
    
    if callback_data == "prayer_times":
        result = await api.call_api("/api/v1/advanced/prayer-times", "POST", {"location": "Makkah"})
        if result:
            await query.edit_message_text(result.get("response", "Error"), reply_markup=back_button())
    
    elif callback_data == "guide":
        await query.edit_message_text("Panduan Manasik Umrah", reply_markup=manasik_keyboard())
    
    elif callback_data == "doa":
        await query.edit_message_text("Doa dan Dzikir", reply_markup=doa_keyboard())
    
    elif callback_data == "navigation":
        await query.edit_message_text("Navigasi dan Lokasi", reply_markup=navigation_keyboard())
    
    elif callback_data.startswith("nav_"):
        nav_query = callback_data.replace("nav_", "").replace("_", " ")
        result = await api.call_api("/api/v1/advanced/navigation", "POST", {"query": nav_query})
        if result:
            await query.edit_message_text(result.get("response", "Error"), reply_markup=navigation_keyboard())
    
    elif callback_data == "emergency":
        await query.edit_message_text("Bantuan Darurat", reply_markup=emergency_keyboard())
    
    elif callback_data.startswith("emerg_"):
        emerg_type = callback_data.replace("emerg_", "")
        result = await api.call_api("/api/v1/advanced/emergency", "POST", {"query": "bantuan", "type": emerg_type})
        if result:
            await query.edit_message_text(result.get("response", "Error"), reply_markup=emergency_keyboard())
    
    elif callback_data == "budget":
        result = await api.call_api("/api/v1/advanced/tips/budget", "GET")
        if result:
            tips_list = result.get("tips", [])
            tips_text = "Tips Budget:\n\n" + "\n".join(f"- {tip}" for tip in tips_list)
            await query.edit_message_text(tips_text, reply_markup=back_button())
    
    elif callback_data.startswith("guide_"):
        topic = callback_data.replace("guide_", "")
        result = await api.call_api("/api/v1/chat/message", "POST", {"message": f"Jelaskan {topic}", "user_id": str(user_id)})
        if result:
            await query.edit_message_text(result.get("response", "Error"), reply_markup=manasik_keyboard())
    
    elif callback_data.startswith("doa_"):
        doa_type = callback_data.replace("doa_", "")
        result = await api.call_api("/api/v1/chat/message", "POST", {"message": f"Doa {doa_type}", "user_id": str(user_id)})
        if result:
            await query.edit_message_text(result.get("response", "Error"), reply_markup=doa_keyboard())
    
    elif callback_data == "back_to_main":
        await query.edit_message_text("Menu Utama", reply_markup=main_menu_keyboard())
    
    elif callback_data == "settings":
        await query.edit_message_text("Pengaturan", reply_markup=settings_keyboard())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle messages"""
    user_id = update.effective_user.id
    message = update.message.text
    
    if message in ["Sholat", "Panduan", "Doa", "Navigasi", "Darurat"]:
        await menu_command(update, context)
        return
    
    await update.message.chat.send_action(ChatAction.TYPING)
    
    result = await api.call_api("/api/v1/chat/message", "POST", {"message": message, "user_id": str(user_id)})
    
    if result:
        await update.message.reply_text(result.get("response", "Error"))
    else:
        await update.message.reply_text("Sistem offline. Gunakan menu.", reply_markup=main_menu_keyboard())

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle location"""
    user_id = update.effective_user.id
    location = update.message.location
    user_manager.set_user_location(user_id, "Makkah")
    await update.message.reply_text("Lokasi diterima!")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Error handler"""
    logger.error(f"Error: {context.error}")

async def post_init(application: Application):
    """Post init"""
    try:
        commands = [
            BotCommand("start", "Mulai bot"),
            BotCommand("menu", "Menu utama"),
            BotCommand("sholat", "Jadwal sholat"),
        ]
        await application.bot.set_my_commands(commands)
        logger.info("Bot commands set")
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{API_URL}/health")
                if response.status_code == 200:
                    logger.info(f"Backend connected: {API_URL}")
        except:
            logger.warning("Backend not reachable")
            
    except Exception as e:
        logger.error(f"Error: {e}")

def main():
    """Main"""
    
    if not BOT_TOKEN:
        print("ERROR: BOT TOKEN NOT SET!")
        return
    
    try:
        app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
        
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("menu", menu_command))
        app.add_handler(CommandHandler("sholat", sholat_command))
        
        app.add_handler(CallbackQueryHandler(button_callback))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        app.add_handler(MessageHandler(filters.LOCATION, handle_location))
        
        app.add_error_handler(error_handler)
        
        print("=" * 60)
        print("UMRAH ASSISTANT BOT v3.0")
        print("=" * 60)
        print("Bot is running!")
        print(f"Backend: {API_URL}")
        print("=" * 60)
        
        app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
        
    except Exception as e:
        logger.error(f"Fatal: {e}")
        raise

if __name__ == '__main__':
    main()
