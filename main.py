from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is Running 24/7!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
    
import telebot

TOKEN = '8754498485:AAHDc9I_yWLe0IanOoF-NNW7eHxSQWE9PGg'
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 5407896838

@bot.message_handler(commands=['suggestions'])
def start_suggestion(message):
    msg = bot.send_message(message.chat.id, "Send Your Suggestions or Feedback to The Chatbox.")

bot.register_next_step_handler(msg, process_suggestion)

def process_suggestion(message):
    try:
        user_text = message.text
        user_first_name = message.from_user.first_name
        user_username = f"@{message.from_user.username}" if message.from_user.username else "NONE"
        user_id = message.from_user.id
        
        admin_alert = (
            f"📩 **New Suggestion has Arrived!**\n\n"
            f"💬 **Suggestion:** {user_text}\n\n"
            f"👤 **Name** {user_first_name}\n"
            f"🆔 **Username:** {user_username}\n"
            f"🔢 **User ID:** {user_id}"
        )
        bot.send_message(ADMIN_ID, admin_alert)
        
        bot.send_message(message.chat.id, "Thank You! Your Message Has Been Send to ADMIN.")
        
    except Exception as e:
        bot.send_message(message.chat.id, "There was an Error. Please Try Again.")
        
CHANNEL_ID = -1003842909353

items_database = {
    "vizard mask": 4,
    "onikiri eren": 7,
    "forsaken": 6,
    "deus ex machina": 8,
    "jõtunn": 9,
    "equinox moon": 10,
    "moai": 11,
    "grumpy": 12
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_msg = (
        "👋 Welcome to Hikari Value Bot!\n\n"
        "Type `/value [item name]` to see the value of items.\n"
        "Type `/suggestions` to Give a Suggestions to The ADMIN."
    )
    bot.send_message(message.chat.id, welcome_msg, parse_mode='Markdown')

@bot.message_handler(commands=['value'])
def copy_value(message):
    try:
        input_parts = message.text.split(maxsplit=1)

        if len(input_parts) < 2:
            bot.send_message(message.chat.id, "💡 Usage: `/value [item name]`", parse_mode='Markdown')
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

if __name__ == "__main__":
    keep_alive()
print("--- Bot is Running ---")
bot.infinity_polling()
