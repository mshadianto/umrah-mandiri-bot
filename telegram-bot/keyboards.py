# -*- coding: utf-8 -*-
"""Keyboard layouts"""
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_keyboard():
    """Main menu keyboard"""
    keyboard = [
        ["💬 AI Chat", "🕌 Jadwal Sholat"],
        ["🗺️ Navigasi", "💰 Budget"],
        ["🆘 Emergency", "📚 Tips"],
        ["⚙️ Settings"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def back_keyboard():
    """Back button"""
    keyboard = [["⬅️ Kembali ke Menu"]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def emergency_keyboard():
    """Emergency options"""
    keyboard = [
        [InlineKeyboardButton("🚨 Call Emergency", callback_data="emergency_call")],
        [InlineKeyboardButton("🏥 Nearest Hospital", callback_data="emergency_hospital")],
        [InlineKeyboardButton("👮 Police", callback_data="emergency_police")],
        [InlineKeyboardButton("❌ Cancel", callback_data="emergency_cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)
