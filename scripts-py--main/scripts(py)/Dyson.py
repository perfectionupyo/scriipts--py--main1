from telegram import *
from telegram.ext import *
import ChatGpt
import messagesDyson
from google.oauth2 import service_account
from googleapiclient.discovery import build

class BigD:
    def __init__(self):
        self.state = None
        self.state_back = {}
        self.user_data = {}
        self.text = messagesDyson.Dyson()
        
    def start_command(self, update, context: CallbackContext):
        self.user_data[] = update.effective_chat.id
        context.bot.send_message(chat_id=id, text = self.text.salam, 
         reply_markup=ReplyKeyboardMarkup(self.text.start, resize_keyboard=True))
        self.state = 0

    def handle_callback(self, update, context):
        query = update.callback_query.data
        id = update.effective_chat.id
        if query == "back":
            self.state = self.state_back[]
        self.handle_all(query, id, context)

    def handle_message(self, update, context):
        text = str(update.message.text)
        id = update.effective_chat.id
        self.handle_all(text, id, context)

    def handle_all(self, text, id, context):
        print(f'state {self.state}')
        if self.state == 0: #Main menu
            context.bot.send_message(chat_id=id, text=self.text.uno,
              reply_markup=ReplyKeyboardRemove())
            self.state = 1
        
        if self.state == 1:
            context.bot.send_message(chat_id=id, text = self.text.dos, 
             reply_markup=self.menu())
            