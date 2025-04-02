from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import ConversationHandler
from control_db import set_movie_items, get_movie_code, update_item, delete_item, get_movies_info
import re

ADMIN_ID_list = [2048383791, 808511625]

ADD_MOVIE, ADD_GENRE, ADD_DURATION, ADD_COUNTRY, ADD_CODE, UPLOAD_MOVIE = range(6)
UPDATE, CHECK_CODE, UPDATE_GENRE, UPDATE_DURATION, UPDATE_COUNTRY, UPDATE_MOVIE = range(6)
DELETE = 1

buttons = [
            [KeyboardButton(text="Kino qo'shish"), KeyboardButton(text="Kinoni tahrirlash")],
            [KeyboardButton(text="Kinoni o'chirish"), KeyboardButton(text="Kinolar ro'yxati")]
        ]

def admin_menu(update, context):
    if update.message.from_user.id in ADMIN_ID_list:
        update.message.reply_text("Xush kelibsiz ADMIN", reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
    else:
        update.message.reply_text("Siz ADMIN emassiz!")


""" ---------------------- KINO QO'SHISH ---------------------- """
def add_movie(update, context):
    update.message.reply_text("Kino nomini kiriting:", reply_markup=ReplyKeyboardRemove())
    return ADD_MOVIE

def add_genre(update, context):
    movie_name = update.message.text
    context.user_data["movie_name"] = movie_name
    update.message.reply_text("Kino janrini kiriting:")
    return ADD_GENRE

def add_duration(update, context):
    movie_genre = update.message.text
    context.user_data["movie_genre"] = movie_genre
    update.message.reply_text("Kino davomiyligini kiriting:")
    return ADD_DURATION

def add_country(update, context):
    movie_duration = update.message.text
    context.user_data["movie_duration"] = movie_duration
    update.message.reply_text("Kino davlatini kiriting: ")
    return ADD_COUNTRY

def add_code(update, context):
    movie_country = update.message.text
    context.user_data["movie_country"] = movie_country
    update.message.reply_text("Kino kodini kiriting (Masalan _123): ")
    return ADD_CODE

def ask_for_movie(update, context):
    movie_code_input = update.message.text.strip() 

    match = re.match(r'^_(\d+)$', movie_code_input)
    if not match:
        update.message.reply_text("Iltimos, kino kodini _ bilan boshlanadigan va faqat raqamlardan iborat formatda kiriting (masalan, _123)!")
        return ADD_CODE

    movie_code = match.group(1)  
    context.user_data["movie_code"] = movie_code
    update.message.reply_text(f"Kino kodi qabul qilindi: {movie_code}\nEndi filmini yuboring 🎥")
    return UPLOAD_MOVIE

def save_movie_file(update, context):
    try:
        movie_name = context.user_data.get("movie_name")
        movie_genre = context.user_data.get("movie_genre")
        movie_duration = context.user_data.get("movie_duration")
        movie_country = context.user_data.get("movie_country")
        movie_code = int(context.user_data.get("movie_code"))
        movie_file = update.message.video

        if not movie_file:
            update.message.reply_text("❌ Kino fayli topilmadi. Iltimos, video fayl yuboring!")
            return UPLOAD_MOVIE

        file_id = movie_file.file_id

        result = set_movie_items(movie_code, movie_name, movie_genre, movie_duration, movie_country, file_id)
        update.message.reply_text(f"Kino '{movie_name}' yuklandi! \n{result}")
        return ConversationHandler.END

    except Exception as e:
        update.message.reply_text(f"❌ Xatolik yuz berdi: {e}")
        return UPLOAD_MOVIE

""" ---------------------- KINO TAHRIRLASH ---------------------- """
def update(update, context):
    update.message.reply_text("Tahrirlanayotgan kino kodini kiriting (oldida * belgisi bilan, masalan *123):", reply_markup=ReplyKeyboardRemove())
    return UPDATE

def check_code(update, context):
    movie_code_input = update.message.text.strip() 

    match = re.match(r'^\*(\d+)$', movie_code_input)
    if not match:
        update.message.reply_text("Iltimos, kino kodini * bilan boshlanadigan va faqat raqamlardan iborat formatda kiriting (masalan, *123)!")
        return UPDATE
    movie_code = int(match.group(1)) 
    context.user_data["movie_code"] = movie_code
    movie_codes = list(get_movie_code())

    if movie_code in movie_codes:
        update.message.reply_text("Kino nomini kiriting:")
        return CHECK_CODE
    else:
        update.message.reply_text("Bu koddagi kino topilmadi", reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True))
        return ConversationHandler.END

def update_genre(update, context):
    update_name = update.message.text
    context.user_data["update_name"] = update_name
    update.message.reply_text("Janrni kiriting:")
    return UPDATE_GENRE

def update_duration(update, context):
    update_genre = update.message.text
    context.user_data["update_genre"] = update_genre
    update.message.reply_text("Davomiyligini kiriting:")
    return UPDATE_DURATION

def update_country(update, context):
    update_duration = update.message.text
    context.user_data["update_duration"] = update_duration
    update.message.reply_text("Davlatini kiriting:")
    return UPDATE_COUNTRY

def update_movie(update, context):
    update_country = update.message.text
    context.user_data["update_country"] = update_country
    update.message.reply_text("Yangi kinoni yuboring:")
    return UPDATE_MOVIE

def save_update(update, context):
    movie_code = int(context.user_data["movie_code"])
    update_name = context.user_data["update_name"]
    update_genre = context.user_data["update_genre"]
    update_duration = context.user_data["update_duration"]
    update_country = context.user_data["update_country"]

    if update.message.video:
        try:
            movie_file = update.message.video
            if not movie_file:
                update.message.reply_text("❌ Kino fayli topilmadi. Iltimos, video fayl yuboring!")
                return UPDATE_MOVIE
            
            file_id = movie_file.file_id
            update_item("kino_id", str(file_id), movie_code)

            if update_name != ".":
                update_item("kino_nomi", update_name, movie_code)
            if update_genre != ".":
                update_item("janri", update_genre, movie_code)
            if update_duration != ".":
                update_item("davomiyligi", update_duration, movie_code)
            if update_country != ".":
                update_item("davlati", update_country, movie_code)

            update.message.reply_text("✅ Kino muvaffaqiyatli yangilandi!")
            return ConversationHandler.END

        except Exception as e:
            update.message.reply_text(f"❌ Xatolik yuz berdi: {e}")
            return UPDATE_MOVIE
    elif update.message.text and update.message.text == ".":
        if update_name != ".":
            update_item("kino_nomi", update_name, movie_code)
        if update_genre != ".":
            update_item("janri", update_genre, movie_code)
        if update_duration != ".":
            update_item("davomiyligi", update_duration, movie_code)
        if update_country != ".":
            update_item("davlati", update_country, movie_code)
        update.message.reply_text("✅ Kino ma'lumotlari muvaffaqiyatli yangilandi!")
    else:
        update.message.reply_text("❌ Noto'g'ri format! Kino videosini yoki '.' belgisi yuboring.")
        return UPDATE_MOVIE

def cancel(update, context):
    update.message.reply_text("Jarayon to'xtatildi.", reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
    return ConversationHandler.END

""" ---------------------- KINONI O'CHIRISH ---------------------- """
def get_code(update, context):
    update.message.reply_text("O'chirilayotgan kino kodini kiriting:", reply_markup=ReplyKeyboardRemove())
    return DELETE

def delete_movie(update, context):
    delete_movie_code = update.message.text.strip()

    match = re.match(r'^\!(\d+)$', delete_movie_code)
    if not match:
        update.message.reply_text("Iltimos, kino kodini ! bilan boshlanadigan va faqat raqamlardan iborat formatda kiriting (masalan, !123):")
        return DELETE
    movie_codes = list(get_movie_code())
    movie_code = int(match.group(1))

    if movie_code in movie_codes:
        delete_item(movie_code)
        update.message.reply_text("Kino o'chirildi.")
    else:
        update.message.reply_text("Bu kodda kino mavjud emas!")
    return ConversationHandler.END

""" ---------------------- KINOLAR RO'YXATI ---------------------- """
def get_movies(update, context):
    movie_names, movie_codes = get_movies_info()
    
    message = "\n".join([f"Kino kodi: {j},   Kino nomi: {i}" for i, j in zip(movie_names, movie_codes)])

    update.message.reply_text(message if message else "Hech qanday kino topilmadi.")
