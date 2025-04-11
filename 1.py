import logging
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, Filters, ConversationHandler, MessageHandler
import sqlite3
from geo_name import get_location_name

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelnames)s - %(massage)s', level=logging.INFO)
conn = sqlite3.connect("users.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users
        (phone_number TEXT PRIMARY KEY, 
        first_name TEXT,
        last_name TEXT,
        age INTEGER,
        gender TEXT,
        address TEXT, 
        latitude REAL,
        longitude REAL, 
        );
""")
conn.commit()

def start(update, context):
    reply_text = 'salom! telefon raqamingizni kiriting:'
    reply_markup = ReplyKeyboardMarkup([
        [KeyboardButton(text="telefon kontaktinizni ulashing", request_contact=True)]
    ], resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_messege(chat_id=update.effective_user.id, text=reply_text, reply_markup=reply_markup)
    return 'PHONE_NUMBER'


def phone_number(update, context):
    phone_number = update.message.text
    context.user_data['phone_number'] = phone_number
    update.message.reply_text('raxmat! Ismingiz nima?')
    return 'FIRST_NAME'


def first_name(update, context):
    phone_number = update.message.text
    context.user_data['first_name'] = first_name()
    update.message.reply_text('raxmat! Familyaniz nima?')
    return 'LAST_NAME'


def last_name(update, context):
    last_name = update.message.text
    context.user_data['last_name'] = last_name()
    update.message.reply_text('raxmat! yoshingiz nechida?')
    return 'AGE'


def age(update, context):
    last_name = update.message.text
    context.user_data['age'] = age()
    update.message.reply_text('raxmat! Jinsinigiz: erkak/ayol?')
    return 'GENDER'


def gender(update, context):
    gender = update.message.text
    context.user_data['age'] = gender()
    update.message.reply_text('raxmat! Jinsinigiz: erkak/ayol?')
    return 'GEOLOCATION'


def geolocation(update, context):
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude
    address = get_location_name(latitude, longitude)
    context.user_data['latitude'] = latitude()
    context.user_data['longitude'] = longitude()
    context.user_data['address'] = address()
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INFO users VALUES (?,?,?,?,?,?,?,?)",(
        context.user_data['phone_number'],
        context.user_data['first_name'],
        context.user_data['last_name'],
        context.user_data['age'],
        context.user_data['gender'],
        context.user_data['address'],
        context.user_data['latitude'],
        context.user_data['longitude'],
    )
              )
    conn.commit()
    conn.close()

    update.message.reply_text("Royhatan otganiz uchun raxmat")
    update.message.reply_text(f"""
        phone: {context.user_data['phone_number']},
        first_name: {context.user_data['first_name']},
        last_name: {context.user_data['last_name']},
        age: {context.user_data['age']},
        gender: {context.user_data['gender']},
        address: {context.user_data['address']},
        """)
    return ConversationHandler.END


def cancel(update, contex):
    update.message.reply_text(text='bekor qilindi')
    return ConversationHandler.END
def main():
    updater = Updater(token="8185283258:AAEXg4ojl1-lM_lB1HqhqvX4DmA6wDcZx2U")
    dispatcher = updater.dispatcher

    cov_handler = ConversationHandler(
    entry_points=[CommandHandler('start',start)],
        states={
            'PHONE_NUMBER': [MessageHandler(Filters.contact & ~Filters.command, phone_number)],
            'FIRST_NAME': [MessageHandler(Filters.text & ~Filters.command, first_name)],
            'LAST_NAME': [MessageHandler(Filters.text & ~Filters.command, last_name)],
            'AGE': [MessageHandler(Filters.text & ~Filters.command, age)],
            'GENDER': [MessageHandler(Filters.text & ~Filters.command, gender)],
            'GEOLOCATION': [MessageHandler(Filters.location & ~Filters.command, geolocation)],

        },
        fallback=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(cov_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()