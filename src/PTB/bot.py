from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters)

from botModule import *

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

KEY, COUNT, QUERY = range(3)


async def find(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    reply_keyboard = [['music or title', 'artist or performer']]

    await update.message.reply_text(
        '<b>Welcome to the fakyoos bot!\n'
        'Let\'s find your favourite playlist.\n'
        'Which category you want to look for?</b>',
        parse_mode='HTML',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )

    return KEY


async def key(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    if update.message.text == 'music or title':
        context.user_data['key'] = 'title'
    else:
        context.user_data['key'] = 'performer'
    logger.info('key of %s: %s', user.first_name, context.user_data['key'])

    await update.message.reply_text(
        f'<b>You selected the category {update.message.text}.\n'
        f'How many results you want to recive?</b>',
        parse_mode='HTML',
        reply_markup=ReplyKeyboardRemove(),
    )
    keyboard = [
        [InlineKeyboardButton('5', callback_data=5)],
        [InlineKeyboardButton('10', callback_data=10)],
        [InlineKeyboardButton('20', callback_data=20)],
        [InlineKeyboardButton('40', callback_data=40)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('<b>Please choose:</b>', parse_mode='HTML', reply_markup=reply_markup)

    return COUNT


async def count(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    query = update.callback_query
    await query.answer()
    context.user_data['count'] = query.data
    logger.info('count: %s', context.user_data['count'])

    await query.edit_message_text(
        f'<b>Your playlist will contain exactly {query.data} musics.\nFeel free to say what are you looking for</b>',
        parse_mode='HTML'
    )

    return QUERY


async def query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    context.user_data['query'] = update.message.text
    logger.info('query: %s', context.user_data['query'])

    await update.message.reply_text('<b>query noted.\n'
                                    'Next messages are the result for matching musics.</b>',
                                    parse_mode='HTML')

    find_fwrd, find_txt = result(
        context.user_data['key'],
        context.user_data['count'],
        context.user_data['query'],
        update.effective_chat.id
    )
    logger.info('musics result: %s', find_fwrd)
    logger.info('playlist result: %s', find_txt)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Bye! Hope to talk to you again soon.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Send /find to make your delighted playlist")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Sorry, I didn't understand that command. Use /help or /start to continue")


if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()  # .context_types(context_types).read_timeout(read_timeout)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('find', find)],
        states={
            KEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, key)],
            COUNT: [CallbackQueryHandler(count)],
            QUERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, query)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    start_handler = CommandHandler('start', start)
    caps_handler = CommandHandler('caps', caps)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(conv_handler)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
