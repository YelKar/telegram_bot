from time import strftime
from telegram.ext import MessageHandler, Filters, CommandHandler, Updater, CallbackContext
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import json
from base import *


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
    print(update.message.from_user.id, type(update.message.from_user.id))
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


# other messages
def all_echo(update: Update, context: CallbackContext):
    sticker = update.message.sticker
    text = update.message.text
    # print(update.message.from_user.id, type(update.message.from_user.id))

    if text in get_stickers():
        if get_stickers(text)[1]:
            update.message.reply_text(get_stickers(text)[1])
        if get_stickers(text)[0]:
            update.message.reply_sticker(get_stickers(text)[0])


# /keyboard -> Создание клавиатуры
def keyboard(update: Update, context: CallbackContext) -> None:
    buttons = [
        ["Добавить стикер"],
        ["Привет", "Пока"]
    ]
    update.message.reply_text(
        text="Клавиатура выведена",
        reply_markup=ReplyKeyboardMarkup(buttons),

    )


def show_sticker(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text in get_stickers():
        update.message.reply_sticker(get_stickers(text))


# /comm
def commands(update: Update, context: CallbackContext):
    exec(update.message.text[6:])


def stickers(sticker_name: str):
    with open("stickers.json", "r", encoding="UTF-8") as file:
        sticker_dict = json.loads(file.read())["stickers"]
    return sticker_dict[sticker_name]

