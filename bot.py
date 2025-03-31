from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging
import os
from flask import Flask, request

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Ganti dengan token botmu
TOKEN = '8061966528:AAGeOKTUi49qA3x98blJQKE53bqdq-xZbU8'

# Ganti dengan username channelmu
CHANNEL_USERNAME = '@vibemeetch'
# Ganti dengan link Traktir atau instruksi pembayaran lainnya
PAYMENT_INSTRUCTION = 'Silakan bayar melalui link berikut: https://trakteer.id/yourprofile'

app = Flask(__name__)

# Fungsi untuk memulai bot
def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    update.message.reply_text(
        f"Halo {user.first_name}! Sebelum melanjutkan, silakan bergabung ke channel kami di {CHANNEL_USERNAME}. Setelah itu, lanjutkan untuk melakukan pembayaran.",
        parse_mode='Markdown'
    )
    update.message.reply_text(
        "Setelah kamu bergabung, lanjutkan dengan pembayaran di Traktir. Silakan klik link berikut untuk membayar: \n" + PAYMENT_INSTRUCTION
    )

# Fungsi untuk memverifikasi pengguna telah bergabung dengan channel
def check_channel_membership(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = user.id

    try:
        member = context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            update.message.reply_text("Terima kasih telah bergabung! Sekarang, silakan lakukan pembayaran untuk melanjutkan.")
            update.message.reply_text(PAYMENT_INSTRUCTION)
        else:
            update.message.reply_text(f"Silakan bergabung dengan channel {CHANNEL_USERNAME} terlebih dahulu.")
    except Exception as e:
        logger.error(f"Error: {e}")
        update.message.reply_text("Terjadi kesalahan dalam memverifikasi status channel. Coba lagi nanti.")

# Flask route untuk menerima webhook
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = Update.de_json(json_str, updater.bot)
    updater.dispatcher.process_update(update)
    return 'OK'

# Fungsi untuk mengatur webhook dan menjalankan bot
def main():
    global updater
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_channel_membership))

    # Set webhook untuk bot
    webhook_url = os.environ.get("WEBHOOK_URL")  # Railway akan menambahkannya secara otomatis
    if webhook_url:
        updater.bot.set_webhook(url=f"{webhook_url}/{TOKEN}")
        logger.info(f"Webhook successfully set to {webhook_url}/{TOKEN}")
    else:
        logger.error("Webhook URL not found!")

if __name__ == '__main__':
    main()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))