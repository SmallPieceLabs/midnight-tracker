# ==========================================================
# PROJECT:     Midnight Tracker Bot
# VERSION:     v1.0.0 (Core Architecture - English)
# AUTHOR:      Mr. Huong | Small Piece Labs
# ECOSYSTEM:   Midnight Network (Cardano Sidechain)
# DESCRIPTION: Professional monitoring tool for NIGHT/DUST rewards.
# LICENSE:     MIT License
# DATE: 2026-02-14
==========================================================

import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# 1. SECURITY CONFIGURATION
# Load environment variables from a hidden .env file
# DO NOT hardcode your token here for public GitHub repositories
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Configure logging to monitor bot performance and errors
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

# 2. MOCK DATA ENGINE (Phase 1.0)
def get_midnight_data(address):
    """
    Simulates fetching unfreezing data from the Midnight Network Indexer.
    Actual on-chain API integration is scheduled for Phase 1.2.
    """
    return {
        "status": "Success",
        "night_balance": "1,250 NIGHT",
        "unfreezing_status": "45/90 days",
        "next_claim": "March 15, 2026"
    }

# 3. USER INTERFACE - MAIN MENU
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Initializes the bot and displays the two core buttons."""
    keyboard = [
        [InlineKeyboardButton("🔍 Check Wallet Status", callback_data='check_night')],
        [InlineKeyboardButton("📖 Detailed User Guide", callback_data='help_info')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_msg = (
        "👋 **Welcome to Midnight Tracker (v1.0)**\n"
        "Developed by **Small Piece Labs**.\n\n"
        "Your automated companion for monitoring NIGHT unfreezing "
        "and DUST accumulation on the Midnight Network.\n\n"
        "Please select an option to begin:"
    )
    await update.message.reply_text(welcome_msg, reply_markup=reply_markup, parse_mode='Markdown')

# 4. INTERACTIVE BUTTON HANDLERS
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes clicks from the inline menu."""
    query = update.callback_query
    await query.answer()

    if query.data == 'check_night':
        await query.edit_message_text(
            text=(
                "🔎 **Wallet Verification**\n\n"
                "Please send your public address using this command:\n"
                "`/check <your_address>`\n\n"
                "*Note:* Only use public addresses. Never share private keys."
            ),
            parse_mode='Markdown'
        )
    
    elif query.data == 'help_info':
        # Comprehensive User Guide
        guide_text = (
            "📖 **Midnight Tracker: Detailed Guide**\n\n"
            "**1. What is NIGHT Unfreezing?**\n"
            "NIGHT tokens are released over a 90-day cycle. This bot tracks "
            "that timeline so you can claim exactly when tokens are ready.\n\n"
            "**2. How to use this Bot?**\n"
            "• Tap 'Check Wallet' to see your current progress.\n"
            "• Copy/Paste your address after the `/check` command.\n\n"
            "**3. Future Updates (v2.0+)**\n"
            "• Multi-wallet monitoring support.\n"
            "• Automatic push notifications for claim windows.\n"
            "• Real-time DUST energy tracking.\n\n"
            "**4. Privacy & Security**\n"
            "Following Midnight Network's privacy standards, we do not store "
            "private keys. All data is fetched from public indexers."
        )
        await query.edit_message_text(text=guide_text, parse_mode='Markdown')

# 5. CORE LOGIC - WALLET QUERY
async def check_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Executes the wallet data lookup command."""
    if not context.args:
        await update.message.reply_text("❌ Error: Missing address.\nFormat: `/check <address>`")
        return
    
    address = context.args[0]
    data = get_midnight_data(address) # Simulate API call
    
    report = (
        f"📊 **Midnight Wallet Report**\n"
        f"Address: `{address[:10]}...` \n\n"
        f"🔹 **NIGHT Balance:** {data['night_balance']}\n"
        f"⏳ **Unfreezing:** {data['unfreezing_status']}\n"
        f"📅 **Next Claim:** {data['next_claim']}\n\n"
        f"_This report uses simulated data for v1.0 Alpha Testing._"
    )
    await update.message.reply_text(report, parse_mode='Markdown')

if __name__ == '__main__':
    # Build and launch the application
    if not TOKEN:
        print("❌ CRITICAL ERROR: TELEGRAM_BOT_TOKEN not found in .env file!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        
        # Register command and callback handlers
        app.add_handler(CommandHandler('start', start))
        app.add_handler(CommandHandler('check', check_wallet))
        app.add_handler(CallbackQueryHandler(button_handler))
        
        print("🚀 Midnight Tracker v1.0 is online. Operational status: GREEN.")
        app.run_polling()
