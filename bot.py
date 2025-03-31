from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Ganti dengan token botmu
TOKEN = '8061966528:AAGeOKTUi49qA3x98blJQKE53bqdq-xZbU8'

# Fungsi untuk memulai bot
def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info(f"User {user.first_name} dengan ID {user.id} telah memulai bot.")
    update.message.reply_text(
        f"Halo {user.first_name}! Selamat datang di bot saya. Ketik /help untuk bantuan lebih lanjut."
    )

# Fungsi untuk menampilkan bantuan
def help(update: Update, context: CallbackContext):
    update.message.reply_text("Ini adalah bot sederhana. Gunakan /start untuk memulai.")

# Fungsi utama untuk memulai bot
def main():
    # Inisialisasi updater dan dispatcher
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Menambahkan handler untuk perintah /start dan /help
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))

    # Start polling untuk menerima update
    updater.start_polling()

    # Menjaga bot tetap berjalan
    updater.idle()

if __name__ == '__main__':
    main()