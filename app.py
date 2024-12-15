from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN = '7885506138:AAGBJ5ctgVwXomnRoJiSZAsgfTezLqvB70c'
GROUP_CHAT_ID = '-1002276126546'

REQUEST_TYPE, ENTER_NAME, ENTER_TEXT = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [['Пересылка сообщения']]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text('Выберите кнопку:', reply_markup=reply_markup)
    return REQUEST_TYPE


async def handle_complaints_ideas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['request_type'] = 'пересылка сообщения'
    await update.message.reply_text('Введите ваше имя:')
    return ENTER_NAME


async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['name'] = update.message.text
    await update.message.reply_text('Введите ваш текст:')
    return ENTER_TEXT


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    name = context.user_data.get('name')
    request_type = context.user_data.get('request_type')

    if request_type and name:
        await context.bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=f'[{request_type.capitalize()}] от {name}: {text}'
        )
        await update.message.reply_text('Ваше сообщение успешно отправлено!')
        context.user_data.clear()
        return ConversationHandler.END
    else:
        await update.message.reply_text('Произошла ошибка. Пожалуйста, начните заново с /start.')
        return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Действие отменено. Вы можете начать заново, отправив /start.')
    return ConversationHandler.END


def main():
    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            REQUEST_TYPE: [
                MessageHandler(filters.TEXT & filters.Regex(
                    '^Пересылка сообщения$'), handle_complaints_ideas)
            ],
            ENTER_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)
            ],
            ENTER_TEXT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    print('bot started')
    main()
