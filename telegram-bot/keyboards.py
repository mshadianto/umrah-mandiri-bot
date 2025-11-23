# -*- coding: utf-8 -*-
"""
Interactive Keyboards for Better UX
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu_keyboard():
    """Main menu with quick access buttons"""
    keyboard = [
        [
            InlineKeyboardButton("🕌 Jadwal Sholat", callback_data="prayer_times"),
            InlineKeyboardButton("📚 Panduan Umrah", callback_data="guide")
        ],
        [
            InlineKeyboardButton("🤲 Doa & Dzikir", callback_data="doa"),
            InlineKeyboardButton("🗺️ Navigasi", callback_data="navigation")
        ],
        [
            InlineKeyboardButton("📊 Progress Saya", callback_data="my_progress"),
            InlineKeyboardButton("💰 Budget", callback_data="budget")
        ],
        [
            InlineKeyboardButton("🆘 Darurat", callback_data="emergency"),
            InlineKeyboardButton("⚙️ Pengaturan", callback_data="settings")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# ============================================================================
# LANGUAGE SELECTION
# ============================================================================

def language_keyboard():
    """Language selection keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("🇮🇩 Bahasa Indonesia", callback_data="lang_id"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
        ],
        [
            InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar"),
            InlineKeyboardButton("« Kembali", callback_data="back_to_main")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# ============================================================================
# MANASIK GUIDE MENU
# ============================================================================

def manasik_keyboard():
    """Manasik guide menu"""
    keyboard = [
        [
            InlineKeyboardButton("🧺 Ihram", callback_data="guide_ihram"),
            InlineKeyboardButton("🕋 Thawaf", callback_data="guide_thawaf")
        ],
        [
            InlineKeyboardButton("🏃 Sa'i", callback_data="guide_sai"),
            InlineKeyboardButton("✂️ Tahalul", callback_data="guide_tahalul")
        ],
        [
            InlineKeyboardButton("📖 Panduan Lengkap", callback_data="guide_full"),
            InlineKeyboardButton("« Kembali", callback_data="back_to_main")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# ============================================================================
# DOA CATEGORIES
# ============================================================================

def doa_keyboard():
    """Doa categories keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("🕌 Doa Ihram", callback_data="doa_ihram"),
            InlineKeyboardButton("🕋 Doa Thawaf", callback_data="doa_thawaf")
        ],
        [
            InlineKeyboardButton("🏃 Doa Sa'i", callback_data="doa_sai"),
            InlineKeyboardButton("💧 Doa Zamzam", callback_data="doa_zamzam")
        ],
        [
            InlineKeyboardButton("🤲 Doa Multazam", callback_data="doa_multazam"),
            InlineKeyboardButton("📿 Talbiyah", callback_data="doa_talbiyah")
        ],
        [
            InlineKeyboardButton("« Kembali", callback_data="back_to_main")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# ============================================================================
# NAVIGATION MENU
# ============================================================================

def navigation_keyboard():
    """Navigation options"""
    keyboard = [
        [
            InlineKeyboardButton("📍 Lokasi Penting", callback_data="nav_locations"),
            InlineKeyboardButton("🗺️ Rute & Jarak", callback_data="nav_routes")
        ],
        [
            InlineKeyboardButton("🏨 Hotel Terdekat", callback_data="nav_hotels"),
            InlineKeyboardButton("🍽️ Tempat Makan", callback_data="nav_food")
        ],
        [
            InlineKeyboardButton("📤 Share Location", callback_data="nav_share"),
            InlineKeyboardButton("« Kembali", callback_data="back_to_main")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# ============================================================================
# EMERGENCY MENU
# ============================================================================

def emergency_keyboard():
    """Emergency quick actions"""
    keyboard = [
        [
            InlineKeyboardButton("🚑 Darurat Medis", callback_data="emerg_medical"),
            InlineKeyboardButton("🔍 Kehilangan", callback_data="emerg_lost_items")
        ],
        [
            InlineKeyboardButton("📍 Tersesat", callback_data="emerg_lost_location"),
            InlineKeyboardButton("🇮🇩 Kontak KJRI", callback_data="emerg_consulate")
        ],
        [
            InlineKeyboardButton("📞 Nomor Darurat", callback_data="emerg_numbers"),
            InlineKeyboardButton("« Kembali", callback_data="back_to_main")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# ============================================================================
# PROGRESS TRACKING
# ============================================================================

def progress_keyboard():
    """Progress tracking options"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Tandai Ihram", callback_data="prog_ihram"),
            InlineKeyboardButton("✅ Tandai Thawaf", callback_data="prog_thawaf")
        ],
        [
            InlineKeyboardButton("✅ Tandai Sa'i", callback_data="prog_sai"),
            InlineKeyboardButton("✅ Tandai Tahalul", callback_data="prog_tahalul")
        ],
        [
            InlineKeyboardButton("📊 Lihat Progress", callback_data="prog_view"),
            InlineKeyboardButton("« Kembali", callback_data="back_to_main")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# ============================================================================
# SETTINGS MENU
# ============================================================================

def settings_keyboard():
    """Settings menu"""
    keyboard = [
        [
            InlineKeyboardButton("🌍 Bahasa", callback_data="settings_language"),
            InlineKeyboardButton("📍 Lokasi", callback_data="settings_location")
        ],
        [
            InlineKeyboardButton("🔔 Notifikasi", callback_data="settings_notifications"),
            InlineKeyboardButton("🗑️ Reset Data", callback_data="settings_reset")
        ],
        [
            InlineKeyboardButton("« Kembali", callback_data="back_to_main")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# ============================================================================
# QUICK REPLY KEYBOARD (Always Visible)
# ============================================================================

def quick_reply_keyboard():
    """Quick reply keyboard at bottom"""
    keyboard = [
        [
            KeyboardButton("🕌 Sholat"),
            KeyboardButton("📚 Panduan"),
            KeyboardButton("🤲 Doa")
        ],
        [
            KeyboardButton("🗺️ Navigasi"),
            KeyboardButton("📊 Progress"),
            KeyboardButton("🆘 Darurat")
        ],
        [
            KeyboardButton("📍 Share Location", request_location=True)
        ]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ============================================================================
# CONFIRMATION KEYBOARDS
# ============================================================================

def confirm_keyboard(action: str):
    """Generic confirmation keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Ya", callback_data=f"confirm_{action}"),
            InlineKeyboardButton("❌ Tidak", callback_data=f"cancel_{action}")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_button():
    """Simple back button"""
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("« Kembali", callback_data="back_to_main")
    ]])