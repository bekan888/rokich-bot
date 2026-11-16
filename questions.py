# questions.py

TERMINAL_VALUES_UZ = [
    "Faol va mazmunli hayot", "Hayotiy donolik", "Sog'liq", "Qiziqarli ish",
    "Tabiat va san'at go'zalligi", "Sevgi", "Moddiy jihatdan ta'minlangan hayot",
    "Yaxshi va sodiq do'stlarga ega bo'lish", "Jamiyat tomonidan tan olinish",
    "Bilim olish va dunyoni anglash", "Samarali va unumli hayot", "Shaxsiy rivojlanish",
    "Ko'ngilochar hayot", "Erkinlik va mustaqillik", "Baxtli oilaviy hayot",
    "Boshqalarning baxt-saodati", "Ijodkorlik", "O'ziga ishonch va ichki xotirjamlik"
]

TERMINAL_VALUES_RU = [
    "Активная деятельная жизнь", "Жизненная мудрость", "Здоровье", "Интересная работа",
    "Красота природы и искусства", "Любовь", "Материально обеспеченная жизнь",
    "Наличие хороших и верных друзей", "Общественное признание",
    "Познание (образование, кругозор)", "Продуктивная жизнь", "Развитие (самосовершенствование)",
    "Развлечения", "Свобода (самостоятельность)", "Счастливая семейная жизнь",
    "Счастье других", "Творчество", "Уверенность в себе"
]

INSTRUMENTAL_VALUES_UZ = [
    "Ozodalik va tartiblilik", "Odoblilik va tarbiyalilik", "Yuqori talabchanlik",
    "Quvnoqlik va hayotsevarlik", "Ijrochilik va intizomlilik", "Mustaqillik",
    "O'zidagi va boshqalardagi kamchiliklarga murosasiz munosabat", "Bilimdonlik va ma'rifatlilik",
    "Mas'uliyatlilik", "Oqilonalik va mantiqiy fikrlash", "O'zini nazorat qilish",
    "O'z fikrini himoya qilishda jasorat", "Qat'iy iroda", "Bag'rikenglik",
    "Keng dunyoqarash", "Halollik", "Ishda samaradorlik", "Boshqalarga nisbatan sezgirlik va e'tiborlilik"
]

INSTRUMENTAL_VALUES_RU = [
    "Аккуратность, чистоплотность", "Воспитанность", "Высокие запросы",
    "Жизнерадостность", "Исполнительность", "Независимость",
    "Непримиримость к недостаткам в себе и других", "Образованность",
    "Ответственность", "Рационализм", "Самоконтроль",
    "Смелость в отстаивании своего мнения", "Твердая воля", "Терпимость",
    "Широта взглядов", "Честность", "Эффективность в делах", "Чуткость"
]     
import telebot
from telebot import types
import questions

TOKEN = "8924392141:AAF5cADRRC5IbW1VOIeraHObZCUvUa2kbl4"
ADMIN_ID = 8900429870  # твой ID

bot = telebot.TeleBot(TOKEN)
users = {}

def get_user(uid):
    if uid not in users:
        users[uid] = {
            "lang": "uz", "step": "lang",
            "fio": None, "school": None, "class": None,
            "current_list": [], "current_index": 0,
            "terminal_ranks": {}, "instrumental_ranks": {}, "used_ranks": set()
        }
    return users[uid]

# Словари для перевода
TEXTS = {
    "uz": {
        "start": "Assalomu alaykum! Tilni tanlang:",
        "fio": "Iltimos, F.I.Sh.ingizni kiriting (Ruchka bilan yozing):",
        "school": "Maktabingiz raqamini kiriting:",
        "class": "Sinfingizni kiriting (masalan, 9A):",
        "rules": "Endi qadriyatlarni 1 dan 18 gacha tartiblaymiz. 1 - eng muhim, 18 - eng kam muhim.\n\nHar bir qadriyat uchun 1 tadan 18 gacha bo'lgan raqamni yozib yuboring (Ruchka bilan).",
        "ask_rank": "({}/{}) Qaysi o'rinni berasiz?\n\n*{}*\n\nRaqamni yozing (1-18):",
        "err_used": "Bu o'rin allaqachon band qilingan! Boshqa raqam kiriting.",
        "err_num": "Iltimos, 1 dan 18 gacha bo'lgan raqam kiriting.",
        "done": "Barcha qadriyatlar tartiblandi! Rahmat. Natijalar yuborildi.",
        "instr": "Ajoyib! Endi *Instrumental qadriyatlar* ro'yxatiga o'tamiz."
    },
    "ru": {
        "start": "Здравствуйте! Выберите язык:",
        "fio": "Введите ваше ФИО (пишите ручкой):",
        "school": "Введите номер школы:",
        "class": "Введите класс (например, 9А):",
        "rules": "Теперь расставим ценности от 1 до 18. 1 - самое важное, 18 - наименее важное.\n\nДля каждой ценности напишите число от 1 до 18 ручкой.",
        "ask_rank": "({}/{}) Какое место вы дадите?\n\n*{}*\n\nНапишите число (1-18):",
        "err_used": "Это место уже занято! Введите другое число.",
        "err_num": "Пожалуйста, введите число от 1 до 18.",
        "done": "Все ценности расставлены! Спасибо. Результаты отправлены.",
        "instr": "Отлично! Переходим ко второму списку: *Инструментальные ценности*."
    }
}

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    users[uid] = {
        "lang": "uz", "step": "lang", "fio": None, "school": None, "class": None,
        "current_list": [], "current_index": 0,
        "terminal_ranks": {}, "instrumental_ranks": {}, "used_ranks": set()
    }
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="set_lang_uz"),
        types.InlineKeyboardButton("🇷🇺 Русский", callback_data="set_lang_ru")
    )
    bot.send_message(uid, "Tilni tanlang / Выберите язык:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("set_lang_"))
def set_lang(call):
    uid = call.from_user.id
    u = get_user(uid)
    u["lang"] = call.data.split("_")[-1]
    u["step"] = "fio"
    bot.edit_message_text(TEXTS[u["lang"]]["fio"], chat_id=uid, message_id=call.message.message_id, parse_mode="Markdown")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    uid = message.from_user.id
    u = get_user(uid)
    text = message.text.strip()
    lang = u["lang"]

    if u["step"] == "fio":
        u["fio"] = text
        u["step"] = "school"
        bot.send_message(uid, TEXTS[lang]["school"])
    elif u["step"] == "school":
        u["school"] = text
        u["step"] = "class"
        bot.send_message(uid, TEXTS[lang]["class"])
    elif u["step"] == "class":
        u["class"] = text
        u["step"] = "terminal"
        u["current_list"] = questions.TERMINAL_VALUES_UZ if lang == "uz" else questions.TERMINAL_VALUES_RU
        u["current_index"] = 0
        u["used_ranks"] = set()
        bot.send_message(uid, TEXTS[lang]["rules"], parse_mode="Markdown")
        send_value(uid)
    
    elif u["step"] in ["terminal", "instrumental"]:
        # Пользователь вводит число текстом ("Ручкой")
        try:
            rank = int(text)
            if rank < 1 or rank > 18:
                raise ValueError
        except ValueError:
            bot.send_message(uid, TEXTS[lang]["err_num"])
            return

        if rank in u["used_ranks"]:
            bot.send_message(uid, TEXTS[lang]["err_used"])
            return

        # Сохраняем
        value_text = u["current_list"][u["current_index"]]
        if u["step"] == "terminal":
            u["terminal_ranks"][rank] = value_text
        else:
            u["instrumental_ranks"][rank] = value_text

        u["used_ranks"].add(rank)
        u["current_index"] += 1
        send_value(uid)

def send_value(uid):
    u = users[uid]
    idx = u["current_index"]
    total = len(u["current_list"])
    lang = u["lang"]

    if idx >= total:
        if u["step"] == "terminal":
            u["step"] = "instrumental"
            u["current_list"] = questions.INSTRUMENTAL_VALUES_UZ if lang == "uz" else questions.INSTRUMENTAL_VALUES_RU
            u["current_index"] = 0
            u["used_ranks"] = set()
            bot.send_message(uid, TEXTS[lang]["instr"], parse_mode="Markdown")
            send_value(uid)
        else:
            finish_quiz(uid)
        return

    value_text = u["current_list"][idx]
    msg = TEXTS[lang]["ask_rank"].format(idx+1, total, value_text)
    bot.send_message(uid, msg, parse_mode="Markdown")

def finish_quiz(uid):
    u = users[uid]
    u["step"] = "done"
    lang = u["lang"]
    bot.send_message(uid, TEXTS[lang]["done"])

    # Отчет для админа
    lines = [
        "📊 *Yangi natija / Новый результат*",
        f"🌐 Til: {lang.upper()}",
        f"👤 F.I.Sh.: {u['fio']}",
        f"🏫 Maktab: {u['school']}",
        f"📚 Sinf: {u['class']}",
        f"🆔 User ID: {uid}",
        "",
        "📌 *Terminal qadriyatlar (Топ-5):*"
    ]
    for i in range(1, 6):
        if i in u["terminal_ranks"]:
            lines.append(f"{i}. {u['terminal_ranks'][i]}")
            
    lines.append("\n📌 *Instrumental qadriyatlar (Топ-5):*")
    for i in range(1, 6):
        if i in u["instrumental_ranks"]:
            lines.append(f"{i}. {u['instrumental_ranks'][i]}")

    try:
        bot.send_message(ADMIN_ID, "\n".join(lines), parse_mode="Markdown")
    except Exception as e:
        print("Ошибка отправки:", e)

if __name__ == "__main__":
    print("Bot ishga tushdi / Бот запущен...")
    bot.infinity_polling()
