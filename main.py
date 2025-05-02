import feedparser
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext

# البودكاستات العربية
arabic_podcasts = {
    "فنجان": "https://anchor.fm/s/1fbb7d24/podcast/rss",
    "أبجورة": "https://anchor.fm/s/3c3e920/podcast/rss",
    # إضافة المزيد من البودكاستات
}

# البودكاستات لتعلم اللغات
language_podcasts = {
    "إنجليزية": "https://www.englishclass101.com/podcast/feed.xml",
    "فرنسية": "https://coffee-break-french.com/rss",
    "ألمانية": "https://slowgerman.com/feed/",
    # إضافة المزيد
}

# دالة لتحميل الحلقات من RSS
def get_podcast_episode(rss_url):
    feed = feedparser.parse(rss_url)
    episode = feed.entries[0]  # الحصول على الحلقة الأخيرة
    mp3_url = episode.enclosures[0].url  # رابط الـ MP3
    return episode.title, mp3_url

# دالة للتعامل مع أمر "/start"
def start(update: Update, context: CallbackContext):
    # أزرار مدمجة مع الرسالة
    keyboard = [
        [InlineKeyboardButton("🎧 بودكاست عشوائي", callback_data='random_podcast')],
        [InlineKeyboardButton("📚 بودكاستات عربية", callback_data='arabic_podcasts')],
        [InlineKeyboardButton("🌍 تعلم اللغات", callback_data='language_podcasts')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        "مرحبًا! اختر نوع البودكاست:\n\n"
        "يمكنك اختيار بودكاست عشوائي أو بودكاستات باللغة العربية أو تعلم اللغات.",
        reply_markup=reply_markup
    )

# دالة لعرض البودكاستات العربية
def arabic_podcasts_list(update: Update, context: CallbackContext):
    buttons = [InlineKeyboardButton(key, callback_data=f"podcast_{key}") for key in arabic_podcasts]
    keyboard = [buttons]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("اختر بودكاست عربي:", reply_markup=reply_markup)

# دالة لعرض بودكاستات تعلم اللغات
def language_podcasts_list(update: Update, context: CallbackContext):
    buttons = [InlineKeyboardButton(key, callback_data=f"podcast_{key}") for key in language_podcasts]
    keyboard = [buttons]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("اختر بودكاست تعلم لغة:", reply_markup=reply_markup)

# دالة لتحميل الحلقة من RSS وإرسالها
def send_episode(update: Update, context: CallbackContext):
    podcast_name = update.callback_query.data.split("_")[1]  # استخراج اسم البودكاست
    podcast_type = 'arabic_podcasts' if 'arabic' in update.callback_query.data else 'language_podcasts'
    
    if podcast_type == 'arabic_podcasts':
        rss_url = arabic_podcasts.get(podcast_name)
    else:
        rss_url = language_podcasts.get(podcast_name)
    
    if rss_url:
        title, mp3_url = get_podcast_episode(rss_url)
        update.callback_query.answer()
        update.callback_query.message.reply_text(f"الـ حلقة: {title}")
        update.callback_query.message.reply_audio(mp3_url)
    else:
        update.callback_query.answer()
        update.callback_query.message.reply_text("لم أتمكن من العثور على هذا البودكاست.")

# دالة لعرض بودكاست عشوائي
def random_podcast(update: Update, context: CallbackContext):
    all_podcasts = list(arabic_podcasts.values()) + list(language_podcasts.values())
    import random
    random_podcast_url = random.choice(all_podcasts)
    title, mp3_url = get_podcast_episode(random_podcast_url)
    update.callback_query.answer()
    update.callback_query.message.reply_text(f"الـ حلقة العشوائية: {title}")
    update.callback_query.message.reply_audio(mp3_url)

# إعداد البوت
def main():
    updater = Updater('YOUR_BOT_TOKEN', use_context=True)
    dispatcher = updater.dispatcher

    # إضافة الأوامر
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("arabic_podcasts", arabic_podcasts_list))
    dispatcher.add_handler(CommandHandler("language_podcasts", language_podcasts_list))
    dispatcher.add_handler(CommandHandler("random_podcast", random_podcast))

    # معالجة الأزرار
    dispatcher.add_handler(CallbackQueryHandler(send_episode, pattern="^podcast_"))
    dispatcher.add_handler(CallbackQueryHandler(random_podcast, pattern="^random_podcast$"))

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
