from telegram import *
from telegram.ext import *
import ChatGpt
import messages2
from google.oauth2 import service_account
from googleapiclient.discovery import build

class BigD:
    def __init__(self):
        self.state = None
        self.state_back = {}
        self.user_data = 0
        self.text = messages2
        
    def start_command(self, update, context: CallbackContext):
        self.user_data[] = update.effective_chat.id
        context.bot.send_message(chat_id=id, text = self.text.salam, 
         reply_markup=ReplyKeyboardMarkup(self.text.start))
        self.state = 0

        # Define the menu buttons
        self.button1 = InlineKeyboardButton("Product", callback_data='1')
        self.button2 = InlineKeyboardButton("About", callback_data='2')
        self.button3 = InlineKeyboardButton("Support", callback_data='3')
        self.menu = InlineKeyboardMarkup([[self.button1],[self.button2],[self.button3]])

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
            