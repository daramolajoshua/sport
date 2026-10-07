import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # e.g., @your_channel_username

# --- Startup Task (Runs immediately upon deployment) ---
async def post_startup_message(application: Application):
    """Sends a message to your channel the exact second the bot deploys and starts."""
    if CHANNEL_ID:
        try:
            startup_text = "🚀 *SportBot is now online and deployed successfully!*\n\nReady to fetch live scores, fixtures, and standings."
            await application.bot.send_message(chat_id=CHANNEL_ID, text=startup_text, parse_mode="Markdown")
            print("Startup notification sent to channel successfully!")
        except Exception as e:
            print(f"Failed to send startup message: {e}")

# --- Commands ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🏆 *Welcome to SportBot!*\n\n"
        "Here are your commands:\n"
        "⚽ /live - View live scores\n"
        "📅 /fixtures - Today's matches\n"
        "📊 /standings - League tables\n"
        "📢 /post - Test channel broadcast"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

async def live_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔴 *Live Matches:*\n\n• Arsenal 2 - 1 Chelsea (78')\n• Lakers 102 - 98 Celtics (Q4)", parse_mode="Markdown")

async def fixtures_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📅 *Today's Fixtures:*\n\n• Real Madrid vs Barcelona - 20:00 UTC", parse_mode="Markdown")

async def standings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 *Top Standings:*\n1. Man City | 64 pts\n2. Arsenal | 62 pts", parse_mode="Markdown")

async def post_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Instantly posts an update to your connected Telegram channel on command"""
    if not CHANNEL_ID:
        await update.message.reply_text("❌ CHANNEL_ID variable is not set on Railway!")
        return
    
    broadcast_msg = "🚨 *SportBot Automated Update*\n\n⚽ Goal! Real Madrid takes the lead! (1-0)"
    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=broadcast_msg, parse_mode="Markdown")
        await update.message.reply_text("✅ Successfully posted to the channel!")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to post: {e}")

def main():
    if not BOT_TOKEN:
        raise ValueError("No BOT_TOKEN environment variable found!")

    # Build application and hook the startup function via post_init
    app = Application.builder().token(BOT_TOKEN).post_init(post_startup_message).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("live", live_command))
    app.add_handler(CommandHandler("fixtures", fixtures_command))
    app.add_handler(CommandHandler("standings", standings_command))
    app.add_handler(CommandHandler("post", post_command))

    print("SportBot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
