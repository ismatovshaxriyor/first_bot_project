from control_db import get_movie_items

def get_movie_handler(update, context):
    try:
        chat_id = update.message.from_user.id
        name, duration, genre, country, movie_id = get_movie_items(int(update.message.text))
        context.bot.send_video(chat_id=chat_id, video=movie_id, caption=f"Kino nomi: {name} \nJanri: {genre} \nDavlati: {country} \nDavomiyligi: {duration}")
    except Exception:
        update.message.reply_text(get_movie_items(int(update.message.text)))