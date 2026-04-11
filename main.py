import telebot
import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "OK", 200

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

TOKEN = '8754498485:AAHDc9I_yWLe0IanOoF-NNW7eHxSQWE9PGg'
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 5407896838
CHANNEL_ID = -1003842909353

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_msg = (
        "👋 Welcome to Hikari Value Bot!\n\n"
        "Type `/value [item name]` to see the value of items.\n"
        "Type `/suggestions` to Give a Suggestions to The ADMIN."
    )
    bot.send_message(message.chat.id, welcome_msg, parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def check_status(message):
    # Bot က အသက်ရှိကြောင်း ပြန်ပြောမယ့်စာ
    status_text = "✅ Bot Status: Online\n\nEverything is working perfectly! I am ready to help you."
    bot.reply_to(message, status_text, parse_mode='Markdown')

@bot.message_handler(commands=['suggestions'])
def start_suggestion(message):
    msg = bot.send_message(message.chat.id, "Send Your Suggestions or Feedback in Here")
    
    bot.register_next_step_handler(msg, process_suggestion)

def process_suggestion(message):
    try:
        
        user_first_name = message.from_user.first_name
        user_username = f"@{message.from_user.username}" if message.from_user.username else "NONE"
        user_id = message.from_user.id
        user_text = message.text
        
        admin_alert = (
            f"📩 New Suggestion has Arrived!\n\n"
            f"👤 Name {user_first_name}\n"
            f"🆔 Username: {user_username}\n"
            f"🔢 User ID: {user_id}"
            f"💬 Suggestion:\n\n {user_text}\n\n"
        )
        bot.send_message(ADMIN_ID, admin_alert)
        
        bot.send_message(message.chat.id, "Thank You! Your Message Has Been Send to ADMIN.")
        
    except Exception as e:
        bot.send_message(message.chat.id, "There was an Error. Please Try Again.")

items_database = {
    "vizard mask": 4,
    "viz": 4,
    "onikiri eren": 7,
    "oni eren": 7,
    "forsaken": 6,
    "deus ex machina": 8,
    "jõtunn": 9,
    "jotnn": 9,
    "jothnn": 9,
    "equinox moon": 10,
    "moai": 11,
    "grumpy": 12,
    "attack serum": 13,
    "att serum": 13,
    "armour serum": 14,
    "armoured serum": 14,
    "female serum": 15,
    "colossal serum": 16,
    "collosal serum": 16,
    "giyu attire": 17,
    "giyu": 17,
    "titanstrike":18,
    "tengen attire": 19,
    "tengen": 19,
    "sorcerer attire": 20,
    "soucerer attire": 20,
    "socerer attire": 20,
    "soul reaper attire": 21,
    "sra": 21,
    "black flash aura": 22,
    "bf aura": 22,
    "fritz": 23,
    "helos": 24,
    "yeager": 25,
    "ackerman": 26,
    "ack": 26,
    "reiss": 27,
    "riss": 27,
    "riess": 27,
    "leonhart": 29,
    "loenhert": 29,
    "leonheart": 29,
    "leoheart": 29,
    "arlert": 30,
    "arlett": 30
}

builds_database = {
    "leonhart female": 28,
    "leonhart fem": 28,
    "leonhert female": 28,
    "leonhert fem": 28
}

@bot.message_handler(commands=['value', 'val'])
def copy_value(message):
    try:
        input_parts = message.text.split(maxsplit=1)

        if len(input_parts) < 2:
            bot.send_message(message.chat.id, "💡 Usage:\n`/value [item name]`\n`/val [item name]`", parse_mode='Markdown')
            return

        item_name = input_parts[1].lower().strip()

        if item_name in items_database:
            msg_id = items_database[item_name]

            bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id=CHANNEL_ID,
                message_id=msg_id
            )
        else:
            bot.send_message(message.chat.id, f"❌ Item '{item_name}' not found.")

    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Error: Make sure the Bot is an Admin in your Channel and the IDs are correct.")

@bot.message_handler(commands=['build'])
def send_build(message):
    try:
        input_parts = message.text.split(maxsplit=1)

        if len(input_parts) < 2:
            bot.send_message(message.chat.id, "💡 Usage:\n`/build [family_name] [build_name]`\nExample `/build leonhart female` ", parse_mode='Markdown')
            return

        build_name = input_parts[1].lower().strip()

        if build_name in builds_database:
            msg_id = builds_database[build_name]

            bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id=CHANNEL_ID,
                message_id=msg_id
            )
        else:
            bot.send_message(message.chat.id, f"❌ Build '{build_name}' not found.")

    except Exception as e:
        print(f"Build Error: {e}")
        bot.send_message(message.chat.id, "⚠️ Error: Something went wrong while fetching the build.")
        
if __name__ == "__main__":
    keep_alive()
    print("--- Bot is Running ---")
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Error: {e}")
