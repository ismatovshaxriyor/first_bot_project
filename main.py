from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

from admin import *

from users import get_movie_handler
import logging

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

ADMIN_ID = "ADMIN ID"

""" ------------------------ START COMMAND ------------------------ """
def start_handler(update, context):
    update.message.reply_text(f"Assalomu alaykum {update.message.from_user.first_name}")
    context.bot.send_message(chat_id=ADMIN_ID, text=f"user: {update.message.from_user.first_name} \nid: {update.message.from_user.id}")
    update.message.reply_text("Marhamat, kino kodini kiriting:")



""" ------------------------ MAIN FUNCTIONS ------------------------ """
def error_handler(update, context: CallbackContext):
    logging.error(f"Update '{update}' caused error '{context.error}'")

def main():
    updater = Updater(token="TOKEN", use_context=True, request_kwargs={'read_timeout': 10, 'connect_timeout': 10})
    dispatcher = updater.dispatcher

    # =====> FOR USERS
    dispatcher.add_handler(CommandHandler("start", start_handler))
    dispatcher.add_handler(MessageHandler(Filters.regex(r"^\d+$"), get_movie_handler))

    # =====> FOR ADMINS
    dispatcher.add_handler(CommandHandler("admin", admin_menu))

    add_movie_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("Kino qo'shish"), add_movie)],
        states={
            ADD_MOVIE: [MessageHandler(Filters.text & ~Filters.command, add_genre)],
            ADD_GENRE: [MessageHandler(Filters.text & ~Filters.command, add_duration)],
            ADD_DURATION: [MessageHandler(Filters.text & ~Filters.command, add_country)],
            ADD_COUNTRY: [MessageHandler(Filters.text & ~Filters.command, add_code)],
            ADD_CODE: [MessageHandler(Filters.text & ~Filters.command, ask_for_movie)],
            UPLOAD_MOVIE: [MessageHandler(Filters.video, save_movie_file)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_user=True
    )

    update_movie_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("Kinoni tahrirlash"), update)],
        states={
            UPDATE: [MessageHandler(Filters.text & ~Filters.command, check_code)],
            CHECK_CODE: [MessageHandler(Filters.text, update_genre)],
            UPDATE_GENRE: [MessageHandler(Filters.text & ~Filters.command, update_duration)],  # Bu yerda tuzatdim
            UPDATE_DURATION: [MessageHandler(Filters.text & ~Filters.command, update_country)],
            UPDATE_COUNTRY: [MessageHandler(Filters.text & ~Filters.command, update_movie)],
            UPDATE_MOVIE: [MessageHandler(Filters.all, save_update)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_user=True
    )

    delete_movie_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("Kinoni o'chirish"), get_code)],
        states={
            DELETE: [MessageHandler(Filters.text, delete_movie)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_user=True
    )


    # =====> CRUD
    dispatcher.add_handler(add_movie_conv_handler)
    dispatcher.add_handler(update_movie_conv_handler)
    dispatcher.add_handler(delete_movie_conv_handler)
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.regex(r"^Kinolar ro'yxati$"), get_movies))

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
