from telegram.ext import MessageHandler, Filters, Updater, CallbackContext, ConversationHandler, CommandHandler
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.parsemode import ParseMode
from key import TOKEN
from base import DB
from colorama import Fore, Style

db = DB()
NAME, SEX, GRADE = range(3)


def main():
    updater = Updater(
        token=TOKEN
    )
    dispatcher = updater.dispatcher
    test_regex = MessageHandler(Filters.regex(r"^([5-9]|10|11)(н|о|п)$"), echo)

    meet_handler = ConversationHandler(
        entry_points=[CommandHandler("start", meet)],

        states={
            NAME: [
                MessageHandler(Filters.regex(r"^[А-ЯA-z][а-яa-z]{1,30}$"), get_name),
                invalid_value("Неверное имя!\nПовторите, пожалуйста!\nПример: <b>И</b><u>ван</u>", NAME)
            ],
            SEX: [
                MessageHandler(Filters.regex(r"(?i)Мужской|Женский"), get_sex),
                invalid_value("Неверный пол!\nПовторите, пожалуйста!", SEX)
            ],
            GRADE: [
                MessageHandler(Filters.regex(r"^([5-9]|10|11)(н|о|п)$"), get_grade),
                invalid_value("Неверный Класс!\nПовторите, пожалуйста!", GRADE)
            ],
        },

        fallbacks=[MessageHandler(Filters.text("Отмена"), cancel), CommandHandler("cancel", cancel)]
    )

    dispatcher.add_handler(meet_handler)
    dispatcher.add_handler(test_regex)

    updater.start_polling()
    print("Bot had been started")
    updater.idle()


grades_keyboard = [
    [f"{grade}н", f"{grade}о", f"{grade}п"]
    if grade > 8
    else [f"{grade}н", f"{grade}о"]
    for grade in range(5, 12)
]


def echo(update: Update, context: CallbackContext):
    update.message.reply_text(update.message.text)


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
        "Здравствуйте!", reply_markup=ReplyKeyboardRemove()
    )
    user_id = update.message.from_user.id
    if user_id in db.users():
        update.message.reply_text("Вы уже зарегистрированы")
        return ConversationHandler.END

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


def get_sex(update: Update, context: CallbackContext):  # key_board
    """Валидация имени и запрос пола

    :param update:
    :param context:
    :return:
    """
    sex = update.message.text

    context.user_data["user"].append(sex)
    update.message.reply_text(
        "Выберите ваш класс",
        reply_markup=ReplyKeyboardMarkup(grades_keyboard, one_time_keyboard=True)
    )
    return GRADE


def get_grade(update: Update, context: CallbackContext):  # key_board
    """Валидация пола и запрос класса

    :param update:
    :param context:
    :return:
    """
    grade = update.message.text
    context.user_data["user"].append(grade)
    db.new_user(context.user_data["user"])
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT)
    print(f'User was register')
    print("_" * 50)
    print(*context.user_data["user"], sep="\n")
    print("_" * 50)
    print(Style.RESET_ALL)
    update.message.reply_text("<b><u>Вы зарегистрированы</u></b>",
                              parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("/start - зарегистрироваться", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def get_id(update: Update):
    return update.message.from_user.id


def invalid_value(text: str, next):
    def answer(update: Update, context: CallbackContext):
        message_text = update.message.text
        if message_text == "Отмена" or message_text == "/cancel":
            return cancel(update, context)
        update.message.reply_text(text, parse_mode=ParseMode.HTML)
        return next
    return MessageHandler(Filters.text, answer)


if __name__ == '__main__':
    main()
