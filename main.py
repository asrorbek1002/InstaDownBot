
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import instaloader
import os
import shutil

# Telegram token
TELEGRAM_TOKEN = '7400870136:AAHiXJts8p2CwJph5n3wx2qtVf2fAno2h14'

# Initialize Instaloader
loader = instaloader.Instaloader(
    filename_pattern="{shortcode}"  # Use shortcode as the filename
)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Salom, videoni yuklab olish uchun Instagram ssilkasini botga yuboring!\nBot hozircha faqat reels videolarni yuklaydi')

def download_video(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text.startswith('http'):
        url = text
        try:
            shortcode = url.split('/')[-2]
            post = instaloader.Post.from_shortcode(loader.context, shortcode)

            if post.is_video:
                temp_dir = f'temp_{shortcode}'
                os.makedirs(temp_dir, exist_ok=True)  # Create temp directory
                loader.download_post(post, target=temp_dir)
                video_file = f'{temp_dir}/{shortcode}.mp4'
                txt_file = f'{temp_dir}/{shortcode}.txt'
                thumb_file = f'{temp_dir}/{shortcode}.jpg'

                if os.path.exists(video_file):
                    caption_text = ''
                    if os.path.exists(txt_file):
                        with open(txt_file, 'r') as caption_file:
                            caption_text = caption_file.read()

                    with open(video_file, 'rb') as video:
                        thumb = open(thumb_file, 'rb') if os.path.exists(thumb_file) else None
                        try:
                            update.message.reply_video(video=video, caption=caption_text, thumb=thumb)
                        except Exception as e:
                            update.message.reply_text(f'Video yuborishda xatolik yuz berdi: {e}')
                        finally:
                            if thumb:
                                thumb.close()

                    # Clean up the temporary directory
                    shutil.rmtree(temp_dir)
                else:
                    update.message.reply_text('Video faylini topib bo\'lmadi.')
            else:
                update.message.reply_text('Bu ssilka videoga olib bormaydi!')
        except Exception as e:
            update.message.reply_text(f'Muammo yuzaga keldi: {e}')
    else:
        update.message.reply_text('Iltimos videoni ssilkasini yuboring!')

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, download_video))
    dispatcher.add_handler(MessageHandler(Filters.all, start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
