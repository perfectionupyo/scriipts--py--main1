import openai
from translate import Translator

def gpt_query(query):
    openai.api_key = "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"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role":"user", "content": query}])
    return str(response.choices[0].message.content)

def create_beginner(age, bad, minus):
    translator = Translator(to_lang="en")
    minus = translator.translate(minus)
    openai.api_key = "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"
    if bad:
        prompt = "Design me a full body workout for a beginner with sets and reps. I'm " +age+ " years old. Keep in mind i have" + minus + ". I have already consulted with a medical proffesional and have clearence to exercise. Dont talk about your inexperience in designing workouts"
    else:
        prompt = "Design me a full body workout for a beginner with sets and reps. I'm " +age+ " years old. Dont talk about your inexperience in designing workouts."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role":"user", "content": prompt}])
    return splitus_and_translatus(response.choices[0].message.content)

def create_final(age, bad, minus, gender, weight, height, goal, new):
    tranlator = Translator(to_lang='en')
    minus = tranlator.translate(minus)
    openai.api_key = "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"
    fnew = ""
    fgender = "I'm female"
    fgoal = "My goal is to lose weight"
    if new: fnew = "I'm new to the gym"
    if gender: fgender = "I'm male"
    if goal: fgoal = "My goal is to gain mass"  

    if bad:
        prompt = f"Design me a 3 day training program, I'm {age} years old, keep in mind: i have {minus} but have already consulted a medical proffesional and have clearence to exercise, {fgender}, I weigh {weight}kg, My height is {height}m, {fgoal}, {fnew}."
    else:
        prompt = f"Design me a 3 day training program, I'm {age} years old, keep in mind: {fgender}, I weigh {weight}kg, My height is {height}cm, {fgoal}, {fnew}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role":"user", "content": prompt}])
    return splitus_and_translatus(response.choices[0].message.content)

def splitus_and_translatus(stringus):
    translator = Translator(to_lang="ru")
    ret = []
    for i in stringus.split("\n"):
        if not i.isspace() and i!="":
            if "�" in i:
                i.replace("�", "-")
            ret.append(translator.translate(i))
    return ret

if __name__ == "__main__":
    print(gpt_query("how do i use the yandex translator in my python code"))
    #print(create_beginner("18",False, "Да").encode("utf-8"))
    #sys.stdout.reconfigure(encoding='utf-8')
    #translator = Translator(to_lang="en")
    #translator_ru = Translator(to_lang="ru")
    #print(create_beginner(True, translator.translate("колени болят")))
    pass