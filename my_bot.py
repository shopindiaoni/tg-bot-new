from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler,
    ContextTypes, filters
)
import os

# ✅ Replace with your actual file paths later
VIDEO_FILES = [
    "C:/video/video_2025-08-03_08-01-19.mp4",
    "C:/video/video_2025-08-03_08-02-09.mp4",
    "C:/video/video_2025-08-03_08-02-17.mp4"
]

APK_FILE = "C:/TelegramBot/AccessKey.apk"

import os  # Agar upar import nahi hai toh sabse upar likh do

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# 🔹 Store user language choices
user_languages = {}

# 🟢 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ENG 🇬🇧", callback_data='lang_en'),
         InlineKeyboardButton("HI 🇮🇳", callback_data='lang_hi')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choice your language\nअपनी भाषा चुने", reply_markup=reply_markup)

# 🔹 Handle language choice
async def language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user_name = query.from_user.first_name

    language = 'en' if query.data == 'lang_en' else 'hi'
    user_languages[user_id] = language
    await query.answer()

    if language == 'en':
        await query.edit_message_text("You have chosen English. Let's start!")
        await context.bot.send_message(chat_id=user_id, text=f"Hello {user_name}! Here are some files for you.")
    else:
        await query.edit_message_text("आपने हिन्दी चुनी है। चलिए शुरू करते हैं!")
        await context.bot.send_message(chat_id=user_id, text=f"नमस्ते {user_name}! आपके लिए कुछ फाइलें हैं।")

    # 🔸 Send video files
    for video in VIDEO_FILES:
        if os.path.exists(video):
            await context.bot.send_video(chat_id=user_id, video=open(video, 'rb'))
        else:
            await context.bot.send_message(chat_id=user_id, text=f"⚠️ File not found: {video}")

    # 🔸 Send message with "Get App" button
    if language == 'en':
        msg = ("For more Clips 5000+ and daily updates of Viral Clips, tap the button below to get the app and access key.\n"
               "By Paying 1rs for verification join https://t.me/+FFvAI56X8h5kY2Jl")
        button_text = "Get App & Access Key"
    else:
        msg = ("5000+ और अधिक क्लिप्स और Viral Clips की दैनिक अपडेट्स के लिए, नीचे दिए गए बटन पर टैप करें ताकि ऐप और एक्सेस की मिल सके।\n"
               "सिर्फ 1 रुपये भुगतान कर के जॉइन करें: https://t.me/+FFvAI56X8h5kY2Jl")
        button_text = "ऐप और एक्सेस की प्राप्त करें"

    keyboard = [[InlineKeyboardButton(button_text, callback_data='get_app')]]
    await context.bot.send_message(chat_id=user_id, text=msg, reply_markup=InlineKeyboardMarkup(keyboard))

# 🔹 Handle "Get App" button
async def get_app(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    language = user_languages.get(user_id, 'en')
    await query.answer()

    if language == 'en':
        await context.bot.send_message(chat_id=user_id,
            text="Great! To proceed, please download our app. You will find the Access Key inside the app.")
        apk_msg = "Here is the app installer. Please download and install it."
    else:
        await context.bot.send_message(chat_id=user_id,
            text="बहुत बढ़िया! आगे बढ़ने के लिए कृपया हमारा ऐप डाउनलोड करें। आपको एक्सेस की ऐप के अंदर मिल जाएगी।")
        apk_msg = "यह ऐप इंस्टॉलर है। कृपया इसे डाउनलोड और इंस्टॉल करें।"

    # Send APK file
    if os.path.exists(APK_FILE):
        await context.bot.send_document(chat_id=user_id, document=open(APK_FILE, 'rb'), caption=apk_msg)
    else:
        await context.bot.send_message(chat_id=user_id, text=f"⚠️ APK file not found: {APK_FILE}")

    # Ask for Access Key
    if language == 'en':
        await context.bot.send_message(chat_id=user_id, text="Please enter your Access Key below:")
    else:
        await context.bot.send_message(chat_id=user_id, text="कृपया नीचे अपना एक्सेस की दर्ज करें:")

# 🟢 Launch the bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(language_choice, pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(get_app, pattern="^get_app$"))

    print("✅ Bot is running...")
    app.run_polling()