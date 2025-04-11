from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Main menu layout
main_menu = ReplyKeyboardMarkup(
    [["Form 1", "Form 2"], ["Form 3", "Form 4"],
     ["Mock Exams", "KCSE Past Papers", "Termly Exams"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to MathMaster Bot! Please choose what you'd like to revise:",
        reply_markup=main_menu
    )

async def menu_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    await update.message.reply_text(f"You chose: {user_choice}\n(More coming soon!)")

if __name__ == '__main__':
    import os
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_response))

    print("Bot is running...")
    app.run_polling()
