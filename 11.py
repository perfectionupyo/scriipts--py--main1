import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, Updater

bot = telegram.Bot(token='5801282633:AAFj2usoiVPdlVdnP-MeyxPDh5fJky_weDs')

def button(update: Update, context: telegram.ext.CallbackContext):
    query = update.callback_query
    query.answer()
    # Get the data from the button that was pressed
    button_data = query.data
    # Send a new message based on which button was pressed
    if button_data == '1':
        query.message.reply_text('You pressed button 1')
    elif button_data == '2':
        query.message.reply_text('You pressed button 2')

def start(update: Update, context: telegram.ext.CallbackContext):
    message = "Choose an option:"
    inline_keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                        InlineKeyboardButton("Option 2", callback_data='2')]]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    update.message.reply_text(message, reply_markup=reply_markup)

updater = Updater(token='5801282633:AAFj2usoiVPdlVdnP-MeyxPDh5fJky_weDs')
updater.dispatcher.add_handler(CommandHandler('start', start)) 
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.start_polling()
