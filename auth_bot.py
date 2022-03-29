from telegram.ext import MessageHandler, Filters, Updater, CallbackContext
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

    meet_handler = MessageHandler(Filters.text, meet)

    dispatcher.add_handler(meet_handler)

    updater.start_polling()
    print("Bot had been started")
    updater.idle()


grades_keyboard = [
    [f"{grade}н", f"{grade}о", f"{grade}п"]
    if grade > 8
    else [f"{grade}н", f"{grade}о"]
    for grade in range(1, 12)
]


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
    """Запрос имени

    :param update:
    :param context:
    :return:
    """
    update.message.reply_text(
        "Здравствуйте!\n"
        "Как вас зовут?"
    )


def ask_sex(update: Update, context: CallbackContext):  # key_board
    """Валидация имени и запрос пола

    :param update:
    :param context:
    :return:
    """
    name = update.message.text

    if validate_name(name):
        context.user_data["name"] = name
        update.message.reply_text(
            f"Приятно познакомиться, {name}!\n"
            "Выберите ваш пол",

            reply_markup=ReplyKeyboardMarkup(       # Создание клавиатуры
                [["Мужской"], ["Женский"]]
            )
        )
    else:
        ask_name(update, context)


def ask_grade(update: Update, context: CallbackContext):  # key_board
    """Валидация пола и запрос класса

    :param update:
    :param context:
    :return:
    """
    sex = update.message.text

    if validate_sex(sex):
        ReplyKeyboardRemove()

        update.message.reply_text(
            "Выберите ваш класс",
            reply_markup=ReplyKeyboardMarkup(grades_keyboard)
        )
    else:
        ask_sex(update, context)


def get_id(update: Update):
    return update.message.from_user.id


def validate_name(name: str) -> bool:
    return True


def validate_sex(sex: str) -> bool:
    return True


def validate_grade(grade: str) -> bool:
    return True


if __name__ == '__main__':
    main()
