# ==========================================================
# PROJECT:     Midnight Tracker Bot
# VERSION:     v1.1.0 (UX Enhancement - English)
# AUTHOR:      Mr. Huong | Small Piece Labs
# DESCRIPTION: Simplified 2-button UI with Emoji Icons.
#              Auto-wallet detection (No /check command needed).
# SECURITY:    Token hidden via environment variables.
# DATE:        2026-02-22
# ==========================================================

import os
import logging
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# 1. SECURITY CONFIGURATION (Sanitized)
load_dotenv()
# This will search for 'TELEGRAM_BOT_TOKEN' in your local .env file
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Configure logging for monitoring
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

# 2. MOCK DATA ENGINE (v1.1 Simulation)
def get_midnight_data(address):
    return {
        "status": "Success",
        "night_balance": "1,250 NIGHT",
        "unfreezing_status": "45/90 days",
        "next_claim": "March 15, 2026"
    }

# 3. KEYBOARD DEFINITION (2 Buttons with Icons)
def main_menu_keyboard():
    keyboard = [
        [KeyboardButton("🔍 Check Status")],
        [KeyboardButton("📖 Help Guide")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# 4. COMMAND HANDLERS
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        f"Hello {user_name}! 🤖\n\n"
        f"Welcome to **Midnight Tracker (v1.1)**.\n\n"
        f"**How to use:**\n"
        f"• Paste your wallet address directly into the chat.\n"
        f"• Or use the menu buttons below."
    )
    await update.message.reply_text(
        welcome_text, 
        reply_markup=main_menu_keyboard(),
        parse_mode='Markdown'
    )

# 5. MESSAGE HANDLER (Auto-wallet detection logic)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # Button Logic (Exact match)
    if text == "🔍 Check Status":
        await update.message.reply_text("Please **Paste** your Midnight wallet address below:")
        
    elif text == "📖 Help Guide":
        guide_text = (
            "📖 **User Guide**\n\n"
            "1. **Check Wallet:** No commands needed. Just paste your address.\n"
            "2. **Claiming:** We monitor the 90-day unfreezing cycle.\n"
            "3. **Security:** We never store private keys.\n\n"
            "*Real-time API integration coming in v1.2!*"
        )
        await update.message.reply_text(guide_text, parse_mode='Markdown')
        
    # AUTO-DETECTION: Long strings are assumed to be wallet addresses
    elif len(text) > 20: 
        data = get_midnight_data(text)
        report = (
            f"📊 **Wallet Status Report**\n"
            f"Address: `{text[:10]}...` \n\n"
            f"🔹 **Balance:** {data['night_balance']}\n"
            f"⏳ **Progress:** {data['unfreezing_status']}\n"
            f"📅 **Estimated Claim:** {data['next_claim']}\n\n"
            f"_Simulated data for v1.1 testing._"
        )
        await update.message.reply_text(report, parse_mode='Markdown')
    
    else:
        await update.message.reply_text(
            "I didn't recognize that. Please paste a valid address or select 'Help Guide'.",
            reply_markup=main_menu_keyboard()
        )

if __name__ == '__main__':
    if not TOKEN:
        print("❌ CRITICAL ERROR: TELEGRAM_BOT_TOKEN not found in .env file!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler('start', start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        
        print("🚀 Midnight Tracker v1.1 is Live & Secure!")
        app.run_polling()
