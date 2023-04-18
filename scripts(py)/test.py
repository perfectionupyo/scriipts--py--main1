from telegram import *
from telegram.ext import *
import ChatGpt
import messages1
from google.oauth2 import service_account
from googleapiclient.discovery import build

class BigT:
    def __init__(self):
        self.state = None
        self.state_back = {0:0, 2:0, 3:1, 4:1, 5:1, 6:4, 7:5, 8:6, 9:7, 10:8}
        self.user_data = {'user_id':None, 'age':None, 'bad':None, 'minus':None, 'gender':None, 'weight':0, 'height':0, 'BMI':0, 'goal':None, 'new':None, 'gym':None}
        self.text = messages1.BigM()
        # create button objects
        self.option1 = KeyboardButton('Составить тренировку')
        self.option2 = KeyboardButton('Обо мне')
        self.option3 = KeyboardButton('Моя инфа')
        # create keyboard layout and add buttons
        menu = [[self.option1], [self.option2], [self.option3]]
        self.reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True)


    def start_command(self, update, context: CallbackContext):
        self.user_data['user_id'] = update.effective_chat.id
        context.bot.send_message(chat_id=update.effective_chat.id, text=self.text.greeting,
            reply_markup=self.reply_markup)
        self.state = 0

    def handle_callback(self, update, context):
        query = update.callback_query.data
        id = update.effective_chat.id
        if query == "back":
            self.state = self.state_back[self.state]
        self.handle_all(query, id, context)

    def handle_message(self, update, context):
        text = str(update.message.text)
        id = update.effective_chat.id
        if text == "Назад": self.state = self.state_back[self.state]
        if text == "Составить тренировку": self.state = 0
        self.handle_all(text, id, context)
        
        
                
    def handle_all(self, text, id, context):
        print(f'state {self.state}')
        if self.state == 0: #age bish
            context.bot.send_message(chat_id=id, text=self.text.age, reply_markup=ReplyKeyboardRemove())
            self.state = 1
        
        elif self.state == 1: #do u have injury
            if not self.is_number(text) and text != "back":
                return context.bot.send_message(chat_id=id, text="Error: please enter a number")
            context.bot.send_message(chat_id=id, text="Any injuries?",
             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏪", callback_data='back'),InlineKeyboardButton("Yes", callback_data='yes'),InlineKeyboardButton("No", callback_data='no')]]))
            self.user_data['age'] = text
            self.state = 2
        
        elif self.state == 2: #what injury?
            if text == 'yes':
                self.user_data['bad'] = True
                context.bot.send_message(chat_id=id, text="What is your injury?", 
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏪", callback_data='back')]]))
                self.state = 3
                return
            elif text == "no":
                self.user_data['bad'] = False
                self.state = 3
            else: context.bot.send_message(chat_id=id, text="fuck u use the fucking buttons")

        if self.state == 3: #create program
            if self.user_data['bad']:
                if len(text) > 50: return context.bot.send_message("Лимит в 50 символов превышен, пожалуйста напиши покороче.")
                self.user_data['minus'] = text
            context.bot.send_message(chat_id=id, text="creating program...")
            context.bot.send_message(chat_id=id, text="🥊 Ты готов двигаться дальше?🥊",
             reply_markup=ReplyKeyboardMarkup([["⚡Погнали!⚡"]]))
            self.state = 4

        elif self.state == 4: #gender
            context.bot.send_message(chat_id=id, text = "imma ask u questions nigga be honest", reply_markup=ReplyKeyboardRemove())
            context.bot.send_message(chat_id=id, text = "what is ur gender nigg", 
             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏪", callback_data='back'),InlineKeyboardButton("👩Женский", callback_data='female'),InlineKeyboardButton("👱‍♂Мужской", callback_data='male')]]))
            self.state = 5
            return
            
        elif self.state == 5: #weight
            if text not in ["female","male","back"]:
                return context.bot.send_message(chat_id=id, text = "use the fucking buttons!") 
            elif text == "male":
                self.user_data['gender'] = True
            elif text == "female":
                self.user_data['gender'] = False
            context.bot.send_message(chat_id=id, text="how much u weight negroni",
             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏪", callback_data='back')]])) 
            self.state = 6

        elif self.state == 6: #height
            if not self.is_number(text) and text !="back" and text !="Назад" or len(text) > 50:
                context.bot.send_message(chat_id=id, text="Введите значение как в примере", reply_markup = ReplyKeyboardRemove())
                return
            if text != "back": self.user_data['weight'] = text
            context.bot.send_message(chat_id=id, text="what ur height bitch?", 
             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏪", callback_data='back')]]))
            self.state = 7

        elif self.state == 7:
            if not self.is_number(text) and text != "Назад" and text != "back" or len(text) > 50:
                context.bot.send_message("vvedy kak v primere")
                return
            if text != "Назад":
                self.user_data['height'] = str(int(text)/100)
            self.user_data['BMI'], message = self.text.bmi(self.user_data['weight'], self.user_data['height'])
            context.bot.send_message(chat_id=id, text=self.text.BMI)
            context.bot.sendMediaGroup(chat_id=id,
                media=[InputMediaPhoto("http://www.yamalcmp.ru/images/cms/data/darya/1.png", caption="")])
            context.bot.send_message(chat_id=id, text=f"Твой индекс тела: {self.user_data['BMI']}\n Твоя масса тела : {message}")
            context.bot.send_message(chat_id=id, text="opredelimsya s goal bitch",
                reply_markup=ReplyKeyboardMarkup(self.text.answ_4))
            self.state = 8

        elif self.state == 8:
            if text != "Набрать массу 💪" and text != "Похудеть 🏃" and text != "maintain weight"  and text !="Назад" and text !="back":
                return context.bot.send_message(chat_id=id, text = self.text.use_button)
            elif text == "Набрать массу 💪":
                self.user_data['goal'] = True
            elif text == "Похудеть 🏃":
                self.user_data['goal'] = False
            context.bot.send_message(chat_id=id, text=self.text.new, reply_markup=ReplyKeyboardMarkup(self.text.answ_5))
            self.state = 9

        elif self.state == 9:
            if text != "Новичок👶" and text != "Опытный👦" and text != "Давно хожу👨‍🦳" and text !="Назад": 
                if text == "Новичок👶":
                    self.user_data['new'] = True
            context.bot.send_message(chat_id=id, text='i removed the keyboard', reply_markup=ReplyKeyboardRemove())
            context.bot.send_message(chat_id=id, text=self.text.options, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏪", callback_data='back'),InlineKeyboardButton("Home", callback_data='home'),InlineKeyboardButton("Gym", callback_data='gym'),InlineKeyboardButton("Outside", callback_data='out')]]))
            self.state = 10

        elif self.state == 10:
            if text == "home":
                self.user_data['gym'] = False
            elif text == "out":
                self.user_data['gym'] = True
            context.bot.send_message(chat_id=id, text=self.text.loading, reply_markup=ReplyKeyboardRemove())
            

    
    

    
    def main(self):                 #call all the functions, create the bot
        updater = Updater("5827934954:AAFm1Xvs9pkseN_Ehp0IWdTEHnglIpqzdHM", use_context=True)
        
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", self.start_command)) 
        dp.add_handler(MessageHandler(Filters.text, self.handle_message))
        dp.add_handler(CallbackQueryHandler(self.handle_callback))
        updater.start_polling()
        updater.idle()

    def is_number(self, s):#check if something is a number
        try:
            int(s)
            return True
        except ValueError:
            return False


if __name__ == '__main__':
    print("bot is running")
    bot = BigT()
    bot.main()