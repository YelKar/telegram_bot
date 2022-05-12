from telegram.ext import MessageHandler, Filters, Updater, CallbackContext, ConversationHandler, CommandHandler
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from key import TOKEN
from base import DB
from colorama import Fore, Style


db = DB()
NAME, SEX, GRADE, GREED = range(4)


def main():
    updater = Updater(
        token=TOKEN,
        use_context=True
    )
    dispatcher = updater.dispatcher

    meet_handler = ConversationHandler(
        entry_points=[CommandHandler("start", meet)],

        states={
            NAME: [MessageHandler(Filters.text, get_name)],
            SEX: [MessageHandler(Filters.text, get_sex)],
            GRADE: [MessageHandler(Filters.text, get_grade)],
        },

        fallbacks=[]
    )

    dispatcher.add_handler(meet_handler)

    updater.start_polling()
    print("Bot had been started")
    updater.idle()


grades_keyboard = [
    [f"{grade}н", f"{grade}о", f"{grade}п"]
    if grade > 8
    else [f"{grade}н", f"{grade}о"]
    for grade in range(5, 12)
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
    update.message.reply_text(
        "Здравствуйте!"
    )
    user_id = update.message.from_user.id
    if user_id in db.users():
        return

    update.message.reply_text(
        "Представьтесь, пожалуйста.\n"
        "Как вас зовут?"
    )
    context.user_data["user"] = [get_id(update)]
    return NAME


def get_name(update: Update, context: CallbackContext):
    """Запрос имени

    :param update:
    :param context:
    :return:
    """

    name = update.message.text

    if validate_name(name):
        context.user_data["user"].append(name)
        update.message.reply_text(
            f"Приятно познакомиться, {name}!\n"
            "Выберите ваш пол",

            reply_markup=ReplyKeyboardMarkup(  # Создание клавиатуры
                [["Мужской"], ["Женский"]],
                one_time_keyboard=True
            )
        )
        return SEX
    update.message.reply_text(
        "Неверное имя!\n"
        "Повторите, пожалуйста!"
    )
    return NAME


def get_sex(update: Update, context: CallbackContext):  # key_board
    """Валидация имени и запрос пола

    :param update:
    :param context:
    :return:
    """
    sex = update.message.text

    if validate_sex(sex):
        context.user_data["user"].append(sex)
        update.message.reply_text(
            "Выберите ваш класс",
            reply_markup=ReplyKeyboardMarkup(grades_keyboard, one_time_keyboard=True)
        )
        return GRADE
    update.message.reply_text(
        "Неверный пол!\n"
        "Повторите, пожалуйста!"
    )
    return SEX


def get_grade(update: Update, context: CallbackContext):  # key_board
    """Валидация пола и запрос класса

    :param update:
    :param context:
    :return:
    """
    ReplyKeyboardRemove()
    grade = update.message.text
    if not validate_grade(grade):
        update.message.reply_text(
            "Неверный Класс!\n"
            "Повторите, пожалуйста!"
        )
        return GRADE
    context.user_data["user"].append(grade)
    db.new_user(context.user_data["user"])
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT)
    print(f'User was register')
    print("_" * 50)
    print(*context.user_data["user"], sep="\n")
    print("_" * 50)
    print(Style.RESET_ALL)
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    return ConversationHandler.END


def get_id(update: Update):
    return update.message.from_user.id


def validate_name(name: str) -> bool:
    return name.isalpha() and name[0].isupper() and name[1:].islower()


def validate_sex(sex: str) -> bool:
    return True


def validate_grade(grade: str) -> bool:
    return any(map(lambda x: grade in x, grades_keyboard))


if __name__ == '__main__':
    main()
