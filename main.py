import os
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("No Telegram token found. Set TELEGRAM_TOKEN as an environment variable.")

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to MathMaster High School Bot!\nUse /help to see what I can do.")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "/start - Welcome message\n"
        "/help - Show this help message\n"
        "/topics - List available math topics\n"
        "/resources - Get PDF notes for Algebra\n"
        "/quiz - Take a short math quiz"
    )

def topics(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Available topics:\n- Algebra\n- Geometry\n- Trigonometry\n- Calculus\n- Probability"
    )

def resources(update: Update, context: CallbackContext):
    pdf_path = "algebra_notes.pdf"
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as pdf_file:
            update.message.reply_document(document=InputFile(pdf_file), filename="Algebra_Notes.pdf")
    else:
        update.message.reply_text("Sorry, the resource is currently unavailable.")

def quiz(update: Update, context: CallbackContext):
    question = "What is the solution to 2x + 3 = 7?"
    update.message.reply_text(f"Quiz Time!\n{question}\nReply with your answer.")
    context.user_data['quiz_answer'] = '2'

def handle_message(update: Update, context: CallbackContext):
    user_answer = update.message.text.strip()
    correct_answer = context.user_data.get('quiz_answer')
    if correct_answer:
        if user_answer == correct_answer:
            update.message.reply_text("Correct! Well done.")
        else:
            update.message.reply_text(f"Oops! The correct answer is {correct_answer}.")
        context.user_data.pop('quiz_answer', None)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(CommandHandler("topics", topics))
dispatcher.add_handler(CommandHandler("resources", resources))
dispatcher.add_handler(CommandHandler("quiz", quiz))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

updater.start_polling()
print("Bot is running...")
updater.idle()
