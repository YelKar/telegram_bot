from time import strftime
from telegram.ext import MessageHandler, Filters, CommandHandler, Updater, CallbackContext
from telegram import Update


# /info
def info(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    text = update.message.text.replace("/info ", "").replace("/info", "")
    user_id = update.message.chat_id
    update.message.reply_text(text=f"Имя: {user.first_name}\n"
                                   f"Фамилия: {user.last_name}\n"
                                   f"Имя пользователя: {user.username}\n"
                                   f"Текст сообщения: {text if text else None}\n"
                                   f"Время получения: {strftime('%H:%M:%S %d.%m.%Y')}\n"
                                   f"Ваш ID: {user_id}\n"
                              )


# hello
def say_hello(update: Update, context: CallbackContext) -> None:
    name = update.message.from_user.first_name
    update.message.reply_text(text=f"Привет, {name}!")


# /img
def img(update: Update, context: CallbackContext):
    print(update.message.sticker)
    sticker = update.message.sticker
    if sticker:
        thumb_id = sticker.thumb.file_id
        sticker_id = sticker.file_id
        update.message.reply_sticker(sticker_id)
    update.message.reply_text("")


def all_echo(update: Update, context: CallbackContext):
    sticker = update.message.sticker
    if sticker:
        sticker_id = sticker.file_id
        update.message.reply_sticker(sticker_id)
    print(sticker)
    update.message.reply_text(update.message.text)

