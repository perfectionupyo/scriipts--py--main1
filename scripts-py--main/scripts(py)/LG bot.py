from telegram import *
from telegram.ext import *
import ChatGpt

def start_command(update, context: CallbackContext):
    print('bot is running away')
    context.bot.send_message(chat_id=update.effective_chat.id, text="I use chat gpt, send shit and imma answer it")

def handle_message(update, context):
    text = str(update.message.text)
    print("User input:", text)
    response = ChatGpt.gpt_query(text)
    print("ChatGpt response:", response)
    context.bot.send_message(chat_id=update.effective_chat.id, text=ChatGpt.gpt_query(text))

def run_bot(token):
    updater = Updater(token, use_context=True)
    
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command)) 
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    run_bot("5934499305:AAEI_0sJe1PUTzIxTz8DDmnD84bJ03fR65A")