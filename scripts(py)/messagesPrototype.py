from telegram import *
from telegram.ext import *

class BigM:
    def __init__(self):
#=========State=0====================================================================================================================================================#
        self.greeting = "Привет!\n\nЯ твой личный тренер-бот DaddyGains,\nкоторый поможет тебе достичь целей и полностью раскрыть свой потенциал 💪.\nЕсли ты хочешь освоить новые навыки, выработать привычку или просто нуждаешься в мотивации, я здесь, чтобы помочь в этом. 🏋‍♂️\n🦾С помощью искуственного интеллекта и современных технологий я моментально составляю индивидуальные программы тренировок!🦿\nИ так, чего мы ждем? Начнем путь к успеху вместе! 🏃"
        
        self.age = "Сколько тебе лет?🤔\nНапиши цифру. Пример: 18"
        self.injury = "Any injuries?"
        self.injury1 = "What is your injury?"
        self.start = "💊Расскажи, есть ли у тебя противопоказания?👨‍🦽"
        self.finito = "The trial version of this bot is finished, you will now proceed "
        self.minus = "💉Напиши свои противопоказания или прошлые травмы словами.🩹\n\nПример: Грыжа, ломал запястье"
        self.infoo = "Is ur info correctus?"
#====================================================================================================================================================================#       
        self.firstweek = "🏅Первая неделя тренировок - фулбади.🏅 \nНеделя «активного восстановления» помогает организму приспособиться и адаптироваться к новым физическим требованиям, которые будут предъявляться к нему во время более интенсивных тренировок."
#==========State=2=================================================================================================================================================#
        self.main_start = "Добро пожаловать в (полную\платную версию) бота!\n❓Я задам тебе парочку вопросов, чтобы узнать тебя лучше и сгенерировать индивидуальные тренировки. Ответы должны быть честными, врать нельзя 🤗"
        self.gender = "🧍‍♂Выбери свой пол🧍‍♀"
        self.weight = "⚖Сколько ты весишь в киллограммах?⚖ \n(вводи только число)\n пример: 70"
        self.height = "📏Какой у тебя рост в сантиметрах?📏\n пример: 175"
        self.BMI = "Твой индекс массы тела (BMI)\nОн рассчитывается по формуле: масса/рост^2 и измеряется в кг/м^2."
        self.goal = "Определимся с целью... 🧐"
        self.new = "🔍Ты в зале…🔍"
        self.loading = "🎉Мне достаточно этой информации, вопросы закончились!🎉\n⚙Составляю тренировку...⚙\n⏲Это может занять более 10 секунд секунд⏲"
        self.options = "where yall wanna train nigg"
#=========Errors====================================================================================================================================================#
        self.error = "Ошибка ввода бля. Отправь сообщение заново, \nВнимательнее в этот раз!!!"
        self.numerror = "Error: please enter a number"
        self.use_button = "Пожалуйста используй предоставленные кнопки!"
        self.bad_input = "Fuck u, write ok"
        self.primer = "Введите значение как в примере"
#=========Menus+Buttons====================================================================================================================================================#
        self.back = [[InlineKeyboardButton("⏪", callback_data='Назад')]]
        self.answ_back = [["Назад"]]
        self.menu = [['Составить тренировку','Составить диету','Техника выполнения'],['Моя Информация','О боте','Стоимость услуг']]
        self.answ_1 = [["Давай начнем! 💪"]]
        self.answ_2 = [["😖Да"], ["☺Нет"], ["Назад"]]
        self.answ_3 = [[InlineKeyboardButton("⏪", callback_data='Назад'),InlineKeyboardButton("👩Женский", callback_data='female'),InlineKeyboardButton("👱‍♂Мужской", callback_data='male')]]
        self.answ_4 = [["Набрать массу 💪"],["Похудеть 🏃"],["maintain weight"],["Назад"]]
        self.answ_5 = [["Новичок👶"],["Опытный👦"],["Давно хожу👨‍🦳"], ["Назад"]]
        self.yesno = [[InlineKeyboardButton("⏪", callback_data='Назад'),InlineKeyboardButton("Yes", callback_data='yes'),InlineKeyboardButton("No", callback_data='no')]]
        self.range = [[InlineKeyboardButton("⏪", callback_data='Назад'),InlineKeyboardButton("Менее 3", callback_data='less'),InlineKeyboardButton("3", callback_data='3'), InlineKeyboardButton("Более 3", callback_data='more')]]
#=========Stage=3=====Diet=Bullshit========================================================================================================================================#
        self.allergies = "Do you have any food allergies or intolerances?"
        self.allergy = "What is ur allergy nigger?"
        self.gas = "Are you currently experiencing any gastrointestinal issues such as bloating, gas, or constipation?"
        self.preference = "Is there any food you do not eat cuz of personal preferences?"
        self.eat = "How often do you usually eat a day?"
#=========Stage=4=====Техника=========================================================================================================================================#        
        self.tech = "Какое упражнение вас интересует?"

    def bmi(self, weight, height):
        x = int(weight)
        y = float(height)
        z = y * y
        bmi = x/z
        ret = round(bmi, 1)

        if ret < 18.5:
            message = "Недостаточная"
        elif 18.5 <= ret <= 24.9:
            message = "Нормальная"
        elif 25.0 <= ret <= 29.9:
            message = "Избыточная"
        elif 30.0 <= ret <= 34.9:
            message = "Ожирение 1 степени"
        elif 35.0 <= ret <= 39.9:
            message = "Ожирение 2 степени"
        elif 40 <= ret:
            message = "Ожирение 3 степени"
        return str(ret), message
    
    def info(self, dicus, nigga_name):
        if dicus['bad']: message = f"{nigga_name}, проверь все ли правильно,\nТебе {dicus['age']} лет.\nТвои недуги: {dicus['minus']}\nВсе ли верно?"
        else: message = f"{nigga_name}, проверь все ли правильно,\nТебе {dicus['age']} лет.\nУ тебя нет недугов.\nВсе ли верно?"
        return message