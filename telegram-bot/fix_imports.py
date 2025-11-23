# -*- coding: utf-8 -*-
"""Fix imports in bot.py"""

# Read file
with open('bot.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix ChatAction import
old_import = "from telegram import Update, BotCommand, ChatAction"
new_import = "from telegram import Update, BotCommand\nfrom telegram.constants import ChatAction, ParseMode"

content = content.replace(old_import, new_import)

# Remove duplicate ParseMode import if exists
content = content.replace("from telegram.constants import ParseMode\n", "")

# Write back
with open('bot.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Imports fixed!")