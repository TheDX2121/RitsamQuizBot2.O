
RitsamQuizBot - README
======================

Files:
- quiz_bot.py       -> main bot source
- questions.json    -> sample questions (bilingual)

Requirements:
- Python 3.10+
- Install dependencies:
    pip install python-telegram-bot==13.19 pymongo openai requests

Environment variables:https://github.com/TheDX2121/RitsamQuizBot2.O/blob/main/.env.example

How to run locally:
1. Create a virtualenv and install requirements.
2. Set environment variables (BOT_TOKEN at minimum).
3. Place your questions.json next to quiz_bot.py or set QUESTIONS_FILE to point to it.
4. Run:
    python quiz_bot.py

Commands (overview):
- /start             - Greeting message
- /mode              - Choose Practice or Test (buttons)
- /source            - Choose source for questions (AI/JSON/Sheet)
- /practice          - Start practice mode (continuous, up to 20 non-repeating)
- /test n t source   - Start test mode with n questions, t seconds per question, source (json/ai/sheet)
                     Example: /test 10 20 json
- /set_sheet <url>   - Save a Google Sheet CSV-export URL for your session
- /stop              - Stop current session
- /score             - Show current score (if in test)
- /upload            - Reply with a JSON array to replace questions.json (anyone can upload in this build)
- /ritsam            - Admin-only: show summarized user data (requires MongoDB)

Google Sheet format:
The CSV should have headers like:
question_en,question_hi,option1_en,option2_en,option3_en,option4_en,option1_hi,option2_hi,option3_hi,option4_hi,correct_index,explanation_en,explanation_hi

Notes & caveats:
- This implementation is a practical MVP matching requested features. It sends questions as messages with inline buttons.
- Timers are per-user using threading.Timer and cancel on answer. Timer must be 5-40 seconds.
- Practice mode chooses random questions without repeating during that session.
- For AI generation the OpenAI key is required; model used is gpt-3.5-turbo by default.
- MongoDB is optional but recommended for saving user history and admin features.
- You can host on Render / Koyeb / Railway. Make sure to set env variables in the hosting panel.

Credits:
Powered by Rɪᴛsᴀᴍ✨ (http://t.me/RitsamHub)
# RitsamQuizBot2.O