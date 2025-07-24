import telebot
import requests
import config
from flask import Flask, request

BOT_TOKEN = config.TOKEN
CRYPTOBOT_TOKEN = config.CRYPTOBOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Створення рахунку (Invoice)
def create_invoice(user_id):
    url = "https://pay.crypt.bot/createInvoice"
    payload = {
        "asset": "USDT",
        "amount": 5,
        "description": "Доступ до каналу",
        "hidden_message": "Дякуємо за оплату! Ось доступ: t.me/твій_канал",
        "paid_btn_name": "openChannel",
        "paid_btn_url": "https://t.me/твій_канал",
        "payload": str(user_id)
    }
    headers = {"Crypto-Pay-API-Token": CRYPTOBOT_TOKEN}
    response = requests.post(url, json=payload, headers=headers)
    return response.json().get("result", {}).get("pay_url", None)

@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

@app.route('/')
def index():
    return 'CryptoBot is running'

@bot.message_handler(commands=['start', 'buy'])
def send_invoice(message):
    url = create_invoice(message.from_user.id)
    if url:
        bot.send_message(message.chat.id, f"Оплатіть, будь ласка: {url}")
    else:
        bot.send_message(message.chat.id, "Сталася помилка. Спробуйте пізніше.")

# Установи webhook перед запуском
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url='https://твоє_доменне_ім’я/' + BOT_TOKEN)
    app.run(host='0.0.0.0', port=8443)
