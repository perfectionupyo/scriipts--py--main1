from telegram import *
from telegram.ext import *
import ChatGpt
import messagesPrototype
from google.oauth2 import service_account
from googleapiclient.discovery import build

class BigT:
    def __init__(self):
        self.state = None
        self.section = 0
        self.state_back = {0:0, 1:0, 2:0,3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8} #[['Составить тренировку','Составить диету','Техника выполнения'],['Моя Информация','О боте','Стоимость услуг']]
        self.section_dic = {'Составить тренировку':2, 'Составить диету':3, 'Техника выполнения':4, 'Моя Информация':5, 'О боте':6, 'Стоимость услуг':7}
        self.user_data = {'user_id':None, 'age':None, 'bad':None, 'minus':None, 'gender':None, 'weight':0, 'height':0, 'BMI':0,
                          'goal':None, 'new':None, 'gym':None, 'have_allergy':None, 'allergy':None, 'has_gas':None, 'gas':None, 'has_pre':None, 'preferences':None, 'eat':None}
        self.user_name = None
        self.text = messagesPrototype.BigM()
        self.reply_markup = ReplyKeyboardMarkup(self.text.menu,resize_keyboard=True)

        self.context = None
        self.update = None

    def start_command(self, update, context: CallbackContext):
        self.user_data['user_id'] = update.effective_chat.id
        self.user_name = update.effective_user.username
        context.bot.send_message(chat_id=update.effective_chat.id, text=self.text.greeting,
            reply_markup=ReplyKeyboardMarkup(self.text.answ_1, resize_keyboard=True))
        self.state = 0

    def handle_callback(self, update, context):
        self.context = context
        self.update = update
        query = update.callback_query.data
        if query == "Назад": 
            if self.state == 1: self.section = 1
            self.state = self.state_back[self.state]
            
        #context.bot.edit_message_reply_markup(chat_id=id, message_id=update.callback_query.message.message_id, reply_markup=InlineKeyboardMarkup([]))
        self.handle_all(query)

    def handle_message(self, update, context):
        self.context = context
        self.update = update
        text = str(update.message.text)
        if text == "Назад": 
            if self.state == 1:self.section = 1
            self.state = self.state_back[self.state]
        self.handle_all(text)
        #context.bot.edit_message_reply_markup(chat_id=id, message_id=update.callback_query.message.message_id, reply_markup=InlineKeyboardMarkup([]))
                
    def handle_all(self, text):
        print(f'section {self.section}')
        print(f'state {self.state}')
        if self.section == 0:
            if self.state == 0: #age bish
                self.zero_state_0()
            elif self.state == 1: #do u have injury
                self.zero_state_1(text)
            elif self.state == 2: #what injury?
                self.zero_state_2(text)
            elif self.state == 3: #create program
                self.zero_state_3(text)
            elif self.state == 4:
                self.zero_state_4(text)

        elif self.section == 1:
            if self.state == 0: self.one_state_0()    
            elif self.state == 1:self.one_state_1(text)
        
        elif self.section == 2:
            if self.state == 0: self.two_state_0()
            elif self.state == 1: self.two_state_1(text)
            elif self.state == 2: self.two_state_2(text)
            elif self.state == 3: self.two_state_3(text)
            elif self.state == 4: self.two_state_4(text)
            elif self.state == 5: self.two_state_5(text)
            elif self.state == 6: self.two_state_6(text)
            elif self.state == 7: self.two_state_7(text)

        elif self.section == 3:
            if self.state == 0: self.three_state_0()
            elif self.state == 1: self.three_state_1(text)
            elif self.state == 2: self.three_state_2(text)
            elif self.state == 3: self.three_state_3(text)
            elif self.state == 4: self.three_state_4(text)
            elif self.state == 5: self.three_state_5(text)
        else:
            self.context.bot.send_message(chat_id=self.update.effective_chat.id, text="Not ready yet")
            self.section = 1
        
#====SECTION 0===================================================================================================================#
    def zero_state_0(self):
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.age, reply_markup=ReplyKeyboardRemove())
        self.state = 1

    def zero_state_1(self, text):
        if not self.is_number(text) and text != "Назад":
            return self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.numerror)
        if text != "Назад": self.user_data['age'] = text
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.injury,
         reply_markup=InlineKeyboardMarkup(self.text.yesno))
        self.state = 2

    def zero_state_2(self, text):
        if text == 'yes':
                self.user_data['bad'] = True
                self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.injury1, 
                    reply_markup=InlineKeyboardMarkup(self.text.back))
                self.state = 3
                return
        elif text == "no":
            self.user_data['bad'] = False
            self.zero_state_3(text)
        else: self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.use_button)

    def zero_state_3(self, text):
        if self.user_data['bad']:
            if len(text) > 50 or self.is_number(text): return self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.bad_input)
            self.user_data['minus'] = text
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.info(self.user_data, self.user_name), 
         reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Yes", callback_data='yes'),InlineKeyboardButton("No", callback_data='no')]]))
        self.state = 4        

    def zero_state_4(self, text):
        if text == "no": return self.zero_state_0()
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text="creating program...")
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.finito,
         reply_markup=ReplyKeyboardMarkup([["⚡Startuem!⚡"]], resize_keyboard=True))
        self.state = 0
        self.section = 1
        

#====SECTION 1===============Меню==================================================================================================#
    def one_state_0(self):
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text="Главное меню",
         reply_markup=ReplyKeyboardMarkup(self.text.menu, resize_keyboard=True))
        self.state = 1
    
    def one_state_1(self, text):
        self.section = self.section_dic[text]
        self.state = 0
        self.handle_all(text)
#====SECTION 2===============Составить=Тренировку==================================================================================#
    def two_state_0(self):
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text = self.text.main_start, reply_markup=ReplyKeyboardRemove())
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text = self.text.gender, 
         reply_markup=InlineKeyboardMarkup(self.text.answ_3))
        self.state = 1
    
    def two_state_1(self, text): 
        if text == "male": self.user_data['gender'] = True
        elif text == "female": self.user_data['gender'] = False
        elif text !="Назад": return self.context.bot.send_message(chat_id=self.update.effective_chat.id, text = "use the fucking buttons!")
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.weight,
            reply_markup=InlineKeyboardMarkup(self.text.back)) 
        self.state = 2

    def two_state_2(self, text):
        if not self.is_number(text) and text !="Назад" or len(text) > 50: return self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.primer)
        if text != "Назад": self.user_data['weight'] = text
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.height, reply_markup=ReplyKeyboardRemove())
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text="Пример: 177", 
         reply_markup=InlineKeyboardMarkup(self.text.back))
        self.state = 3

    def two_state_3(self, text):
        if not self.is_number(text) and text != "Назад" or len(text) > 50: return self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.primer)
        if text != "Назад": self.user_data['height'] = str(int(text)/100)
        self.user_data['BMI'], message = self.text.bmi(self.user_data['weight'], self.user_data['height'])
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.BMI)
        self.context.bot.sendMediaGroup(chat_id=self.update.effective_chat.id,
         media=[InputMediaPhoto("http://www.yamalcmp.ru/images/cms/data/darya/1.png", caption="")])
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=f"Твой индекс тела: {self.user_data['BMI']}\n Твоя масса тела : {message}")
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.goal,
         reply_markup=ReplyKeyboardMarkup(self.text.answ_4, resize_keyboard=True))
        self.state = 4

    def two_state_4(self, text):
        if text not in ["Набрать массу 💪","Похудеть 🏃","maintain weight","Назад"]: return self.context.bot.send_message(chat_id=self.update.effective_chat.id, text = self.text.use_button)
        elif text == "Набрать массу 💪": self.user_data['goal'] = True
        elif text == "Похудеть 🏃": self.user_data['goal'] = False
        elif text == "maintain weight": self.user_data['goal'] = None
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.new, reply_markup=ReplyKeyboardMarkup(self.text.answ_5, resize_keyboard=True))
        self.state = 5

    def two_state_5(self, text):
        if text not in ["Новичок👶","Опытный👦","Давно хожу👨‍🦳","Назад"]: return self.context.bot.send_message(chat_id=self.update.effective_chat.id, text = self.text.use_button)
        if text == "Новичок👶": self.user_data['new'] = True
        elif text == "Опытный👦" or text == "Давно хожу👨‍🦳": self.user_data['new'] = False
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.options, reply_markup=ReplyKeyboardRemove())
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text="Please choose from options below bish",
          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏪", callback_data='Назад'),InlineKeyboardButton("Home", callback_data='home'),InlineKeyboardButton("Gym", callback_data='gym'),InlineKeyboardButton("Outside", callback_data='out')]]))
        self.state = 6

    def two_state_6(self, text):
        if text == "home": self.user_data['gym'] = False
        elif text == "out": self.user_data['gym'] = True
        elif text == "gym": self.user_data['gym'] = None
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.loading, reply_markup=ReplyKeyboardRemove())
        self.section = 1
        self.state = 0
        self.handle_all(text)
#====SECTION 3================Составить=диету=====================================================================================#
    def three_state_0(self):
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text = "Imma create a coolass dietplan nig, be honest", reply_markup=ReplyKeyboardRemove())
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text = self.text.allergies, 
         reply_markup=InlineKeyboardMarkup(self.text.yesno))
        self.state = 1
        
    def three_state_1(self, text):
        if text == 'yes':
            self.user_data['have_allergy'] = True
            self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.allergy,
             reply_markup=InlineKeyboardMarkup(self.text.back))
            self.state = 2
            return
        elif text == "no":
            self.user_data['have_allergy'] = False
            self.three_state_2(text)
        else: self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.use_button)
  
    def three_state_2(self, text):
        if self.user_data['have_allergy']:
            if len(text) > 50 or self.is_number(text): return self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.bad_input)
            self.user_data['allergy'] = text
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.gas, reply_markup=InlineKeyboardMarkup(self.text.yesno))
        self.state = 3

    def three_state_3(self, text):
        if text not in ["yes","no","Назад"]: return self.context.bot.send_message(chat_id=self.update.effective_chat.id, text = self.text.use_button)
        elif text == "yes": 
            self.user_data['has_gas'] = True
            self.context.bot.send_message(chat_id=self.update.effective_chat.id, text="what is ur problem specifically?", reply_markup=InlineKeyboardMarkup(self.text.back))
            self.state = 4
            return
        elif text == "no": 
            self.user_data['has_gas'] = False
            self.three_state_4(text)
        else: self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.use_button)
        
    def three_state_4(self, text):
        if self.user_data['has_gas']:
            if len(text) > 50 or self.is_number(text): return self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.bad_input)
            self.user_data['gas'] = text
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.preference, reply_markup=InlineKeyboardMarkup(self.text.yesno))
        self.state = 5

    def three_state_5(self, text):
        if text not in ["yes","no","Назад"]: return self.context.bot.send_message(chat_id=self.update.effective_chat.id, text = self.text.use_button)
        elif text == "yes": 
            self.user_data['has_pre'] = True
            self.context.bot.send_message(chat_id=self.update.effective_chat.id, text="what is ur problem specifically?", reply_markup=InlineKeyboardMarkup(self.text.back))
            self.state = 6
            return
        elif text == "no": 
            self.user_data['has_pre'] = False
            self.three_state_6(text)
        else: self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.use_button)

    def three_state_6(self, text):
        if self.user_data['has_pre']:
            if len(text) > 50 or self.is_number(text): return self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.bad_input)
            self.user_data['preferences'] = text
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.eat, reply_markup=InlineKeyboardMarkup(self.text.range))
        self.state = 7
    
    def three_state_7(self, text):
        if text not in ["Назад","less","3","more"]: return self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=self.text.bad_input)
        elif text == "less":self.user_data['eat'] = False
        elif text == "more":self.user_data["eat"] = True
        elif text == "3": self.user_data['eat'] = None
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text='im creating a diet moment bitte blyat', reply_markup=InlineKeyboardMarkup(self.text.back))
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text='Is all ur info correct?')

        
#====SECTION 4====================================================================================================================#
    def four_state_0(self):
        self.context.bot.send_message(chat_id=self.update.effective_chat.id, text = self.text.tech, reply_markup=ReplyKeyboardRemove())
        self.state = 1

#====SECTION 5====================================================================================================================#

#====SECTION 6====================================================================================================================#

#====SECTION 7====================================================================================================================#







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