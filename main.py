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
import sqlite3

TOKEN = '8754498485:AAHDc9I_yWLe0IanOoF-NNW7eHxSQWE9PGg'
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 5407896838
CHANNEL_ID = -1003842909353

def log_user(user_id):
    conn = sqlite3.connect('bot_users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)''')
    c.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def count_users():
    conn = sqlite3.connect('bot_users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)''')
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]
    conn.close()
    return count

@bot.message_handler(commands=['start'])
def send_welcome(message):
    log_user(message.from_user.id)
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

@bot.message_handler(commands=['users'])
def show_user_count(message):
    if message.from_user.id == ADMIN_ID:
        total = count_users()
        bot.reply_to(message, f"📊 Users: {total} People")
    else:
        bot.reply_to(message, "❌ This Command Can Be Only Use by Admin")

@bot.message_handler(commands=['message'])
def start_broadcast(message):
    if message.from_user.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "Write the Sentences or Announcement that You Want to Sent to the Users.")
        bot.register_next_step_handler(msg, send_broadcast_to_all)
    else:
        bot.reply_to(message, "❌ This Command Can Be Only Use by Admin")

def send_broadcast_to_all(message):
    broadcast_text = message.text
    conn = sqlite3.connect('bot_users.db')
    c = conn.cursor()
    c.execute("SELECT user_id FROM users")
    users = c.fetchall()
    conn.close()

    success_count = 0
    fail_count = 0

    bot.send_message(ADMIN_ID, f"🚀 Sending to the Users")

    for user in users:
        try:
            bot.send_message(user[0], broadcast_text)
            success_count += 1
        except Exception:
            fail_count += 1
    
    bot.send_message(ADMIN_ID, f"✅ Sending Finished!\n\nSucceed: {success_count}\nFailed: {fail_count}")

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
    "riess": 27
}

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
