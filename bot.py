from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
import logging
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Ganti dengan token botmu
TOKEN = '8061966528:AAGeOKTUi49qA3x98blJQKE53bqdq-xZbU8'

# Ganti dengan username channelmu
CHANNEL_USERNAME = '@vibemeetch'  # Nama Channelmu di Telegram
# Ganti dengan link Traktir atau instruksi pembayaran lainnya
PAYMENT_INSTRUCTION = 'Silakan bayar melalui link berikut: https://trakteer.id/yourprofile'

# Fungsi untuk memulai bot
async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    await update.message.reply_text(
        f"Halo {user.first_name}! Sebelum melanjutkan, silakan bergabung ke channel kami di {CHANNEL_USERNAME}. Setelah itu, lanjutkan untuk melakukan pembayaran.",
        parse_mode='Markdown'
    )
    await update.message.reply_text(
        "Setelah kamu bergabung, lanjutkan dengan pembayaran di Traktir. Silakan klik link berikut untuk membayar: \n" + PAYMENT_INSTRUCTION
    )

# Fungsi untuk memverifikasi apakah pengguna sudah bergabung dengan channel
async def check_channel_membership(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = user.id

    try:
        # Mengecek apakah pengguna sudah menjadi anggota channel
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        
        if member.status in ['member', 'administrator', 'creator']:
            # Jika sudah menjadi anggota, kirimkan instruksi pembayaran
            await update.message.reply_text("Terima kasih telah bergabung! Sekarang, silakan lakukan pembayaran untuk melanjutkan.")
            await update.message.reply_text(PAYMENT_INSTRUCTION)
        else:
            # Jika belum menjadi anggota, minta pengguna bergabung terlebih dahulu
            await update.message.reply_text(f"Silakan bergabung dengan channel {CHANNEL_USERNAME} terlebih dahulu.")
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("Terjadi kesalahan dalam memverifikasi status channel. Coba lagi nanti.")

# Fungsi utama untuk memulai bot
def main():
    # Membuat aplikasi bot
    application = Application.builder().token(TOKEN).build()

    # Menambahkan handler untuk perintah /start
    application.add_handler(CommandHandler("start", start))

    # Menambahkan handler untuk memeriksa status channel dan pembayaran
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_channel_membership))

    # Memulai bot
    application.run_polling()

if __name__ == '__main__':
    main()