from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from queue import Queue
from time import sleep

from camera import camera

# Замените токеном вашего бота
TOKEN = '6927500986:AAG_PFfTm3kT_Pldu9ZeyGCc4dMjsbkv4jA'

def take_photo(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    camera.read_cam()
    sleep(5)
    with open('/test.png', 'rb') as f:
        context.bot.send_photo(chat_id=chat_id, photo=f)

def main() -> None:
    update_queue = Queue()
    updater = Updater(TOKEN, update_queue=update_queue)
    # dispatcher = updater.dispatcher
    # dispatcher.add_handler(CommandHandler('photo', take_photo))
    updater.start_polling()
    #updater.idle()

if __name__ == '__main__':
    main()