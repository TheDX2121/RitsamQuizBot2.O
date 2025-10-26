import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB setup
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['quiz_bot_db']  # Database name
questions_collection = db['questions']  # Collection for questions
scores_collection = db['scores']  # Collection for user scores

# Test DB connection
try:
    client.admin.command('ping')
    logger.info("MongoDB connected successfully.")
except ConnectionFailure:
    logger.error("MongoDB connection failed.")

# Sample questions (seed these into DB manually or via a script)
# Example: questions_collection.insert_many([
#     {"question": "What is 2+2?", "options": ["3", "4", "5"], "correct": "4"},
#     {"question": "Capital of France?", "options": ["London", "Paris", "Berlin"], "correct": "Paris"}
# ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome to the Quiz Bot! Use /quiz to start a quiz."
    )

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    # Fetch questions from DB
    questions = list(questions_collection.find())
    if not questions:
        await update.message.reply_text("No questions available. Please contact admin.")
        return
    
    # Initialize user quiz state
    context.user_data['questions'] = questions
    context.user_data['current_question'] = 0
    context.user_data['score'] = 0
    
    await send_question(update, context)

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    questions = context.user_data['questions']
    current = context.user_data['current_question']
    
    if current >= len(questions):
        score = context.user_data['score']
        total = len(questions)
        user_id = update.effective_user.id
        # Save score to DB
        scores_collection.update_one(
            {"user_id": user_id},
            {"$set": {"score": score, "total": total}},
            upsert=True
        )
        await update.callback_query.edit_message_text(f"Quiz complete! Your score: {score}/{total}")
        return
    
    question = questions[current]
    keyboard = [[InlineKeyboardButton(opt, callback_data=f"answer_{opt}")] for opt in question['options']]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            f"Question {current + 1}: {question['question']}", reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            f"Question {current + 1}: {question['question']}", reply_markup=reply_markup
        )

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    selected = query.data.split('_')[1]
    questions = context.user_data['questions']
    current = context.user_data['current_question']
    correct = questions[current]['correct']
    
    if selected == correct:
        context.user_data['score'] += 1
        await query.edit_message_text(f"Correct! {query.message.text}")
    else:
        await query.edit_message_text(f"Wrong! Correct answer: {correct}. {query.message.text}")
    
    context.user_data['current_question'] += 1
    await send_question(update, context)

def main() -> None:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(CallbackQueryHandler(handle_answer, pattern="^answer_"))
    
    # For webhook mode, we'll set it up in server.py
    return application