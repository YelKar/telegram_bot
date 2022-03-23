from telegram.ext import MessageHandler, Filters, CommandHandler, Updater, CallbackContext
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from key import TOKEN
from base import DB


db = DB()


def main():
    updater = Updater(
        token=TOKEN,
        use_context=True
    )
    dispatcher = updater.dispatcher

    updater.start_polling()
    print("Bot had been started")
    updater.idle()


# start
def meet(update: Update, context: CallbackContext):
    """Start dialog and check is user in db

    if id in db, go to exit
    if id not in db, go to:
        ask_name
        ask_sex
        ask_grade
    :param update: Update
    :param context: CallbackContext
    :return: None
    """
    user_id = update.message.from_user.id
    if user_id in db.users():
        pass
    ask_name(update, context)


def ask_name(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Здравствуйте!\n"
        "Как вас зовут?"
    )


def ask_sex(update: Update, context: CallbackContext):  # key_board
    pass


def ask_grade(update: Update, context: CallbackContext):  # key_board
    pass


def get_id(update: Update):
    return update.message.from_user.id


def validate_name(name: str) -> bool:
    return True


if __name__ == '__main__':
    main()
