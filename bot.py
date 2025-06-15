import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# יצירת תיקיית thumbs אם לא קיימת
if not os.path.exists("thumbs"):
    os.makedirs("thumbs")

# שמירת מצב התמונה הנוכחית
DEFAULT_THUMB_PATH = "thumbs/default.jpg"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("היי! שלח לי תמונה עם /setthumb כדי להגדיר thumbnail, ואז שלח קובץ PDF או EPUB.")

def set_thumbnail(update: Update, context: CallbackContext):
    if update.message.photo:
        photo = update.message.photo[-1]
        photo_file = photo.get_file()
        photo_file.download(DEFAULT_THUMB_PATH)
        update.message.reply_text("תמונה נשמרה כ-thumbnail ברירת מחדל.")
    else:
        update.message.reply_text("שלח תמונה עם הפקודה הזו.")

def handle_document(update: Update, context: CallbackContext):
    document = update.message.document
    if not document.file_name.lower().endswith((".pdf", ".epub")):
        update.message.reply_text("רק קבצי PDF או EPUB נתמכים.")
        return

    if not os.path.exists(DEFAULT_THUMB_PATH):
        update.message.reply_text("לא הוגדרה תמונה. שלח תמונה עם /setthumb קודם.")
        return

    file = document.get_file()
    file_path = f"thumbs/{document.file_name}"
    file.download(file_path)

    with open(DEFAULT_THUMB_PATH, "rb") as thumb:
        context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=open(file_path, "rb"),
            thumb=thumb,
            caption="הנה הקובץ שלך עם ה-thumbnail 🎯"
        )

def main():
    TOKEN = os.getenv("BOT_TOKEN") or "YOUR_TELEGRAM_BOT_TOKEN_HERE"
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("setthumb", set_thumbnail))
    dp.add_handler(MessageHandler(Filters.document, handle_document))
    dp.add_handler(MessageHandler(Filters.photo & Filters.caption_regex("^/setthumb$"), set_thumbnail))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
