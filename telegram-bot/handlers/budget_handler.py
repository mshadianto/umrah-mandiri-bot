# -*- coding: utf-8 -*-
"""
AI-Powered Budget Calculator Handler
Uses RAG + Agentic AI for optimal recommendations
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
import httpx
from config import API_URL

# Conversation states
CHOOSING_JAMAAH, CHOOSING_DURATION, CHOOSING_BUDGET, SHOWING_RESULTS = range(4)

async def budget_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start budget optimization"""
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
        "🤖 *AI Budget Optimizer - Powered by RAG*\n\n"
        "Saya akan analisis & cari paket umrah TERBAIK untuk Anda!\n\n"
        "💡 AI akan analyze 50+ hotel & airlines\n"
        "📊 Dapat 3 rekomendasi optimal\n\n"
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
        [InlineKeyboardButton("💰 Ekonomis (Budget Terbatas)", callback_data="budget_pref_ekonomis")],
        [InlineKeyboardButton("⭐ Standar (Balance)", callback_data="budget_pref_standar")],
        [InlineKeyboardButton("👑 Premium (Luxury)", callback_data="budget_pref_premium")],
        [InlineKeyboardButton("🎯 Semua Opsi (Recommended)", callback_data="budget_pref_all")],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="budget_back_duration")]
    ]
    
    await query.edit_message_text(
        f"✅ Durasi: *{context.user_data['duration']} hari*\n\n"
        "*Langkah 3:* Pilih preferensi budget:\n\n"
        "💡 Pilih 'Semua Opsi' untuk dapat 3 rekomendasi!",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    
    return CHOOSING_BUDGET

async def analyze_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Call AI to analyze and recommend packages"""
    query = update.callback_query
    await query.answer()
    
    preference_map = {
        "budget_pref_ekonomis": "ekonomis",
        "budget_pref_standar": "standar",
        "budget_pref_premium": "premium",
        "budget_pref_all": "all"
    }
    
    context.user_data['preference'] = preference_map.get(query.data, "all")
    
    # Show loading message
    await query.edit_message_text(
        "🤖 *AI sedang menganalisis...*\n\n"
        "⏳ Mencari kombinasi terbaik dari:\n"
        "• 50+ hotel options\n"
        "• 10+ airlines\n"
        "• Real-time prices\n\n"
        "Mohon tunggu 5-10 detik...",
        parse_mode="Markdown"
    )
    
    # Call backend API
    jamaah = context.user_data['jamaah']
    duration = context.user_data['duration']
    preference = context.user_data['preference']
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{API_URL}/api/v1/budget/optimize",
                json={
                    "jamaah": jamaah,
                    "duration": duration,
                    "preferences": {"type": preference}
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                packages = data['data']['packages']
                
                # Format recommendations
                result_text = await format_recommendations(packages, jamaah, duration, preference)
                
                keyboard = [
                    [InlineKeyboardButton("📊 Detail Paket 1", callback_data="budget_detail_0")],
                    [InlineKeyboardButton("📊 Detail Paket 2", callback_data="budget_detail_1")],
                    [InlineKeyboardButton("📊 Detail Paket 3", callback_data="budget_detail_2")],
                    [InlineKeyboardButton("🔄 Hitung Ulang", callback_data="budget_restart")],
                    [InlineKeyboardButton("❌ Selesai", callback_data="budget_done")]
                ]
                
                await query.edit_message_text(
                    result_text,
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode="Markdown"
                )
                
                # Save packages for detail view
                context.user_data['packages'] = packages
                
                return SHOWING_RESULTS
            else:
                raise Exception("API Error")
                
    except Exception as e:
        await query.edit_message_text(
            f"❌ Maaf, terjadi kesalahan saat menganalisis.\n\n"
            f"Error: {str(e)}\n\n"
            "Silakan coba lagi atau hubungi admin.",
            parse_mode="Markdown"
        )
        return ConversationHandler.END

async def format_recommendations(packages, jamaah, duration, preference):
    """Format AI recommendations into readable message"""
    
    if preference != "all" and len(packages) == 1:
        # Show only selected preference
        pkg = packages[0]
        text = f"""🎯 *REKOMENDASI AI: {pkg['name'].upper()}*
━━━━━━━━━━━━━━━━━━━━━━

👥 {jamaah} Jamaah | 📅 {duration} Hari

💰 *TOTAL: Rp {pkg['total']:,.0f}*
👤 *Per Orang: Rp {pkg['per_person']:,.0f}*

✨ *Keunggulan:*
{chr(10).join(f'• {h}' for h in pkg['highlights'][:3])}

🧠 *AI Reasoning:*
{pkg['reasoning'][:200]}...

━━━━━━━━━━━━━━━━━━━━━━
Gunakan button di bawah untuk melihat detail lengkap!"""
    else:
        # Show all 3 packages summary
        text = f"""🤖 *AI BUDGET OPTIMIZER RESULTS*
━━━━━━━━━━━━━━━━━━━━━━

👥 {jamaah} Jamaah | 📅 {duration} Hari

AI menemukan 3 paket optimal untuk Anda:

"""
        for i, pkg in enumerate(packages[:3], 1):
            emoji = "💰" if pkg['category'] == "ekonomis" else "⭐" if pkg['category'] == "standar" else "👑"
            text += f"""{emoji} *{pkg['name']}*
Total: Rp {pkg['total']:,.0f}
Per Orang: Rp {pkg['per_person']:,.0f}
{pkg['highlights'][0] if pkg['highlights'] else 'Best value'}

"""
        
        text += """━━━━━━━━━━━━━━━━━━━━━━
💡 Klik 'Detail Paket' untuk breakdown lengkap!"""
    
    return text

async def show_package_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show detailed breakdown of selected package"""
    query = update.callback_query
    await query.answer()
    
    # Get package index from callback data
    pkg_idx = int(query.data.split("_")[-1])
    packages = context.user_data.get('packages', [])
    
    if pkg_idx >= len(packages):
        await query.answer("Paket tidak ditemukan")
        return SHOWING_RESULTS
    
    pkg = packages[pkg_idx]
    
    # Format detailed breakdown
    detail = f"""📊 *DETAIL: {pkg['name'].upper()}*
━━━━━━━━━━━━━━━━━━━━━━

🏨 *HOTEL MAKKAH*
{pkg['hotels']['makkah']['name']}
{"⭐" * pkg['hotels']['makkah']['stars']} - {pkg['hotels']['makkah']['distance']}
{pkg['hotels']['makkah']['nights']} malam × Rp {pkg['hotels']['makkah']['price_per_night']:,.0f}
Subtotal: Rp {pkg['hotels']['makkah']['subtotal']:,.0f}

🕌 *HOTEL MADINAH*
{pkg['hotels']['madinah']['name']}
{"⭐" * pkg['hotels']['madinah']['stars']} - {pkg['hotels']['madinah']['distance']}
{pkg['hotels']['madinah']['nights']} malam × Rp {pkg['hotels']['madinah']['price_per_night']:,.0f}
Subtotal: Rp {pkg['hotels']['madinah']['subtotal']:,.0f}

✈️ *PENERBANGAN*
{pkg['flight']['airline']} ({pkg['flight']['type']})
{context.user_data['jamaah']} pax × Rp {pkg['flight']['price_per_person']:,.0f}
Subtotal: Rp {pkg['flight']['subtotal']:,.0f}

💵 *BIAYA LAIN*
📋 Visa: Rp {pkg['costs']['visa']:,.0f}
🛡️ Asuransi: Rp {pkg['costs']['insurance']:,.0f}
🚗 Transport: Rp {pkg['costs']['transport']:,.0f}
🍽️ Makan: Rp {pkg['costs']['meals']:,.0f}
💼 Lain-lain: Rp {pkg['costs']['misc']:,.0f}

━━━━━━━━━━━━━━━━━━━━━━

💰 *TOTAL: Rp {pkg['total']:,.0f}*
👤 *Per Orang: Rp {pkg['per_person']:,.0f}*

🧠 *Kenapa Paket Ini?*
{pkg['reasoning']}"""
    
    # Add tips if available
    if 'tips' in pkg and pkg['tips']:
        detail += f"\n\n💡 *Tips Khusus:*\n"
        detail += chr(10).join(f'• {t}' for t in pkg['tips'][:3])
    
    keyboard = [
        [InlineKeyboardButton("⬅️ Kembali ke Summary", callback_data="budget_back_summary")],
        [InlineKeyboardButton("📱 Hubungi Travel", url="https://wa.me/")],
        [InlineKeyboardButton("❌ Selesai", callback_data="budget_done")]
    ]
    
    await query.edit_message_text(
        detail,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    
    return SHOWING_RESULTS

async def back_to_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Go back to summary view"""
    query = update.callback_query
    await query.answer()
    
    jamaah = context.user_data['jamaah']
    duration = context.user_data['duration']
    preference = context.user_data['preference']
    packages = context.user_data['packages']
    
    result_text = await format_recommendations(packages, jamaah, duration, preference)
    
    keyboard = [
        [InlineKeyboardButton("📊 Detail Paket 1", callback_data="budget_detail_0")],
        [InlineKeyboardButton("📊 Detail Paket 2", callback_data="budget_detail_1")],
        [InlineKeyboardButton("📊 Detail Paket 3", callback_data="budget_detail_2")],
        [InlineKeyboardButton("🔄 Hitung Ulang", callback_data="budget_restart")],
        [InlineKeyboardButton("❌ Selesai", callback_data="budget_done")]
    ]
    
    await query.edit_message_text(
        result_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    
    return SHOWING_RESULTS

async def budget_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Finish budget conversation"""
    query = update.callback_query
    await query.answer("Terima kasih!")
    
    await query.edit_message_text(
        "✅ Analisis budget selesai!\n\n"
        "💾 Hasil sudah tersimpan di chat history.\n"
        "🔄 Ketik /budget untuk analisis ulang.\n"
        "📋 Ketik /menu untuk menu utama.",
        parse_mode="Markdown"
    )
    
    return ConversationHandler.END

async def budget_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel budget conversation"""
    query = update.callback_query
    await query.answer("Dibatalkan")
    
    await query.edit_message_text(
        "❌ Analisis budget dibatalkan.\n\n"
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
            CHOOSING_BUDGET: [
                CallbackQueryHandler(analyze_budget, pattern="^budget_pref_"),
                CallbackQueryHandler(choose_jamaah, pattern="^budget_back_duration$")
            ],
            SHOWING_RESULTS: [
                CallbackQueryHandler(show_package_detail, pattern="^budget_detail_"),
                CallbackQueryHandler(back_to_summary, pattern="^budget_back_summary$"),
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
