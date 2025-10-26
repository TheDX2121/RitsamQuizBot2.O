import os
from flask import Flask, request
from quiz_bot import main as bot_main
from telegram import Update

app = Flask(__name__)
application = bot_main()  # Initialize the bot application

@app.route('/')
def home():
    return "Quiz Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.process_update(update)
    return 'OK'

if __name__ == '__main__':
    # Set webhook on startup
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    if WEBHOOK_URL:
        application.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
        print(f"Webhook set to {WEBHOOK_URL}/webhook")
    else:
        print("WEBHOOK_URL not set. Webhook not configured.")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)