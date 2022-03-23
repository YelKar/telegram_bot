from time import ctime
from key import TOKEN
from functions import *


def main():
    updater = Updater(
        token=TOKEN,
        use_context=True
    )
    dispatcher = updater.dispatcher
    dispatcher.add_handler(
        CommandHandler("img", img)
    )
    dispatcher.add_handler(
        CommandHandler("info", info)
    )
    dispatcher.add_handler(
        CommandHandler("keyboard", keyboard)
    )
# /r_keyboard -> Удаление клавиатуры
    dispatcher.add_handler(
        CommandHandler("r_keyboard", lambda update, context: update.message.reply_text(
            text="text",
            reply_markup=ReplyKeyboardRemove()
        ))
    )
    dispatcher.add_handler(
        CommandHandler("comm", commands)
    )
    dispatcher.add_handler(
        MessageHandler(Filters.text("Клавиатура"), keyboard)
    )
    dispatcher.add_handler(
        MessageHandler(Filters.all, all_echo)
    )
    updater.start_polling()
    print("Bot had been started")
    updater.idle()


if __name__ == '__main__':
    main()
