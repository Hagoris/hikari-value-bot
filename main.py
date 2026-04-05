from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is Running 24/7!"

# ၂။ အဲ့ဒီ Website ကို Port 8080 မှာ ဖွင့်ပေးတာ
def run():
    app.run(host='0.0.0.0', port=8080)

# ၃။ Bot အလုပ်လုပ်နေတုန်း ဒီ Website လေးကို နောက်ကွယ်ကနေ မောင်းပေးတာ
def keep_alive():
    t = Thread(target=run)
    t.start()
    
import telebot

# --- ၁။ BOT TOKEN ထည့်သွင်းခြင်း ---
TOKEN = '8754498485:AAGBuerMGoPT5tFk9ydTyX69nUAnC-9CJnU'
bot = telebot.TeleBot(TOKEN)

# --- ၂။ CHANNEL ID ထည့်သွင်းခြင်း ---
# အရှေ့က -100 ကစပြီး ဂဏန်းအကုန် ထည့်ပါ
CHANNEL_ID = -1003842909353

# --- ၃။ ITEM DATABASE ---
# "ခေါ်မယ့်နာမည်": Channel ထဲက Message ID
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
        "Type `/value [item name]` to see the value of items."
    )
    bot.send_message(message.chat.id, welcome_msg, parse_mode='Markdown')

@bot.message_handler(commands=['value'])
def copy_value(message):
    try:
        # User ရိုက်လိုက်တဲ့စာသားကို ခွဲထုတ်ခြင်း
        input_parts = message.text.split(maxsplit=1)

        if len(input_parts) < 2:
            bot.send_message(message.chat.id, "💡 Usage: `/value [item name]`", parse_mode='Markdown')
            return

        item_name = input_parts[1].lower().strip()

        if item_name in items_database:
            msg_id = items_database[item_name]

            # Channel ထဲက Message ကို ပုံ၊ စာ၊ Format အကုန်လုံး အတူတူအတိုင်း ကူးပေးတာပါ
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
    keep_alive()  # Website လေးကို စနှိုးလိုက်တာ
print("--- Bot is Running ---")
bot.infinity_polling()
