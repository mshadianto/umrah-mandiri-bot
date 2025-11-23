# -*- coding: utf-8 -*-
"""
Budget Calculator Handler
Simulasi biaya umrah dengan berbagai kategori
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, 
    ConversationHandler, 
    CallbackQueryHandler,
    MessageHandler,
    filters
)
from telegram.constants import ChatAction

# Conversation states
CHOOSING_JAMAAH, CHOOSING_DURATION, CHOOSING_HOTEL, SHOWING_RESULT = range(4)

# Harga base (dalam IDR)
PRICES = {
    "visa": 2500000,
    "flight_jakarta_jeddah": 8500000,
    "transport_local_per_day": 150000,
    "meal_per_day": 200000,
    "hotel_makkah": {
        "bintang_3": 500000,
        "bintang_4": 1000000,
        "bintang_5": 2000000
    },
    "hotel_madinah": {
        "bintang_3": 400000,
        "bintang_4": 800000,
        "bintang_5": 1500000
    },
    "lain_lain": 1000000
}

async def budget_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start budget calculation"""
    # Get message object
    if update.message:
        message = update.message
        chat = message.chat
    elif update.callback_query:
        await update.callback_query.answer()
        message = update.callback_query.message
        chat = message.chat
    else:
        return ConversationHandler.END
    
    await chat.send_action(ChatAction.TYPING)
    
    keyboard = [
        [InlineKeyboardButton("1 Jamaah", callback_data="budget_jamaah_1")],
        [InlineKeyboardButton("2 Jamaah", callback_data="budget_jamaah_2")],
        [InlineKeyboardButton("3-4 Jamaah", callback_data="budget_jamaah_4")],
        [InlineKeyboardButton("5+ Jamaah", callback_data="budget_jamaah_5")],
        [InlineKeyboardButton("❌ Batal", callback_data="budget_cancel")]
    ]
    
    text = (
        "💰 *Simulasi Budget Umrah*\n\n"
        "Mari hitung estimasi biaya umrah Anda!\n\n"
        "*Langkah 1:* Berapa jumlah jamaah?"
    )
    
    if update.callback_query:
        await message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    else:
        await message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    
    return CHOOSING_JAMAAH

async def choose_jamaah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle jamaah selection"""
    query = update.callback_query
    await query.answer()
    
    jamaah_map = {
        "budget_jamaah_1": 1,
        "budget_jamaah_2": 2,
        "budget_jamaah_4": 4,
        "budget_jamaah_5": 5
    }
    
    context.user_data['jamaah'] = jamaah_map.get(query.data, 1)
    
    keyboard = [
        [InlineKeyboardButton("5 Hari", callback_data="budget_duration_5")],
        [InlineKeyboardButton("10 Hari", callback_data="budget_duration_10")],
        [InlineKeyboardButton("15 Hari", callback_data="budget_duration_15")],
        [InlineKeyboardButton("20 Hari", callback_data="budget_duration_20")],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="budget_back_jamaah")]
    ]
    
    await query.edit_message_text(
        f"✅ Jumlah jamaah: *{context.user_data['jamaah']} orang*\n\n"
        "*Langkah 2:* Pilih durasi umrah:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    
    return CHOOSING_DURATION

async def choose_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle duration selection"""
    query = update.callback_query
    await query.answer()
    
    duration_map = {
        "budget_duration_5": 5,
        "budget_duration_10": 10,
        "budget_duration_15": 15,
        "budget_duration_20": 20
    }
    
    context.user_data['duration'] = duration_map.get(query.data, 10)
    
    keyboard = [
        [InlineKeyboardButton("⭐⭐⭐ Bintang 3", callback_data="budget_hotel_3")],
        [InlineKeyboardButton("⭐⭐⭐⭐ Bintang 4", callback_data="budget_hotel_4")],
        [InlineKeyboardButton("⭐⭐⭐⭐⭐ Bintang 5", callback_data="budget_hotel_5")],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="budget_back_duration")]
    ]
    
    await query.edit_message_text(
        f"✅ Durasi: *{context.user_data['duration']} hari*\n\n"
        "*Langkah 3:* Pilih kategori hotel:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    
    return CHOOSING_HOTEL

async def calculate_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calculate and show budget"""
    query = update.callback_query
    await query.answer()
    
    hotel_map = {
        "budget_hotel_3": "bintang_3",
        "budget_hotel_4": "bintang_4",
        "budget_hotel_5": "bintang_5"
    }
    
    context.user_data['hotel_category'] = hotel_map.get(query.data, "bintang_4")
    
    # Calculate costs
    jamaah = context.user_data['jamaah']
    duration = context.user_data['duration']
    hotel_cat = context.user_data['hotel_category']
    
    # Assume split: 60% Makkah, 40% Madinah
    makkah_nights = int(duration * 0.6)
    madinah_nights = duration - makkah_nights
    
    # Calculate each component
    visa_total = PRICES['visa'] * jamaah
    flight_total = PRICES['flight_jakarta_jeddah'] * jamaah
    hotel_makkah_total = PRICES['hotel_makkah'][hotel_cat] * makkah_nights * jamaah
    hotel_madinah_total = PRICES['hotel_madinah'][hotel_cat] * madinah_nights * jamaah
    transport_total = PRICES['transport_local_per_day'] * duration * jamaah
    meal_total = PRICES['meal_per_day'] * duration * jamaah
    misc_total = PRICES['lain_lain'] * jamaah
    
    grand_total = (visa_total + flight_total + hotel_makkah_total + 
                   hotel_madinah_total + transport_total + meal_total + misc_total)
    
    per_person = grand_total / jamaah
    
    # Format message
    hotel_star = "⭐" * int(hotel_cat.split('_')[1])
    
    result = f"""💰 *ESTIMASI BUDGET UMRAH*
━━━━━━━━━━━━━━━━━━━━━━

📊 *Detail Paket:*
👥 Jamaah: {jamaah} orang
📅 Durasi: {duration} hari
🏨 Hotel: {hotel_star}
🕋 Makkah: {makkah_nights} malam
🕌 Madinah: {madinah_nights} malam

━━━━━━━━━━━━━━━━━━━━━━

💵 *Rincian Biaya:*

📋 Visa Umrah
Rp {visa_total:,.0f}

✈️ Tiket Pesawat (PP)
Rp {flight_total:,.0f}

🏨 Hotel Makkah ({makkah_nights} malam)
Rp {hotel_makkah_total:,.0f}

🏨 Hotel Madinah ({madinah_nights} malam)
Rp {hotel_madinah_total:,.0f}

🚗 Transportasi Lokal
Rp {transport_total:,.0f}

🍽️ Konsumsi
Rp {meal_total:,.0f}

💼 Lain-lain
Rp {misc_total:,.0f}

━━━━━━━━━━━━━━━━━━━━━━

💰 *TOTAL BIAYA*
*Rp {grand_total:,.0f}*

👤 *Per Orang*
*Rp {per_person:,.0f}*

━━━━━━━━━━━━━━━━━━━━━━

ℹ️ Catatan:
- Harga estimasi, bisa berubah
- Sudah termasuk hotel & makan
- Belum termasuk belanja pribadi
- Harga tiket tergantung musim"""
    
    keyboard = [
        [InlineKeyboardButton("🔄 Hitung Ulang", callback_data="budget_restart")],
        [InlineKeyboardButton("📱 Hubungi Travel", url="https://wa.me/")],
        [InlineKeyboardButton("❌ Selesai", callback_data="budget_done")]
    ]
    
    await query.edit_message_text(
        result,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    
    context.user_data['last_budget'] = {
        'jamaah': jamaah,
        'duration': duration,
        'hotel': hotel_cat,
        'total': grand_total,
        'per_person': per_person
    }
    
    return SHOWING_RESULT

async def budget_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Finish budget conversation"""
    query = update.callback_query
    await query.answer("Terima kasih!")
    
    await query.edit_message_text(
        "✅ Simulasi budget selesai!\n\n"
        "Ketik /budget untuk menghitung ulang.\n"
        "Ketik /menu untuk kembali ke menu utama.",
        parse_mode="Markdown"
    )
    
    return ConversationHandler.END

async def budget_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel budget conversation"""
    query = update.callback_query
    await query.answer("Dibatalkan")
    
    await query.edit_message_text(
        "❌ Simulasi budget dibatalkan.\n\n"
        "Ketik /budget untuk mulai lagi.",
        parse_mode="Markdown"
    )
    
    return ConversationHandler.END

def get_budget_handler():
    """Get the budget conversation handler"""
    return ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex("^💰 Budget$"), budget_start)
        ],
        states={
            CHOOSING_JAMAAH: [
                CallbackQueryHandler(choose_jamaah, pattern="^budget_jamaah_")
            ],
            CHOOSING_DURATION: [
                CallbackQueryHandler(choose_duration, pattern="^budget_duration_"),
                CallbackQueryHandler(budget_start, pattern="^budget_back_jamaah$")
            ],
            CHOOSING_HOTEL: [
                CallbackQueryHandler(calculate_budget, pattern="^budget_hotel_"),
                CallbackQueryHandler(choose_jamaah, pattern="^budget_back_duration$")
            ],
            SHOWING_RESULT: [
                CallbackQueryHandler(budget_start, pattern="^budget_restart$"),
                CallbackQueryHandler(budget_done, pattern="^budget_done$")
            ]
        },
        fallbacks=[
            CallbackQueryHandler(budget_cancel, pattern="^budget_cancel$")
        ],
        name="budget_conversation",
        persistent=False 
    )
