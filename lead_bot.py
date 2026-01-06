from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

TOKEN = "8421338771:AAGLA0N8j2wWEB3iZPLfaDwe7lK_dvNIj-o"
MANAGER_CHAT_ID = 463760724  # сюда свой Telegram ID

NAME, COUNTRY, MODEL, BUDGET, CONTACT = range(5)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте! 👋\n\nКак вас зовут?"
    )
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text

    keyboard = [["Китай 🇨🇳", "Япония 🇯🇵", "Корея 🇰🇷"]]
    await update.message.reply_text(
        "Из какой страны хотите автомобиль?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )
    return COUNTRY


async def get_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["country"] = update.message.text
    await update.message.reply_text("Какую модель рассматриваете?")
    return MODEL


async def get_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["model"] = update.message.text
    await update.message.reply_text("Какой бюджет?")
    return BUDGET


async def get_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["budget"] = update.message.text
    await update.message.reply_text("Контакт для связи (телефон / Telegram)?")
    return CONTACT


async def get_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["contact"] = update.message.text

    text = (
        "🚗 *Новая заявка*\n\n"
        f"👤 Имя: {context.user_data['name']}\n"
        f"🌍 Страна: {context.user_data['country']}\n"
        f"🚘 Модель: {context.user_data['model']}\n"
        f"💰 Бюджет: {context.user_data['budget']}\n"
        f"📞 Контакт: {context.user_data['contact']}"
    )

    await context.bot.send_message(
        chat_id=MANAGER_CHAT_ID,
        text=text,
        parse_mode="Markdown",
    )

    await update.message.reply_text("✅ Заявка отправлена! Мы свяжемся с вами.")
    return ConversationHandler.END


def main():
    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_country)],
            MODEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_model)],
            BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_budget)],
            CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_contact)],
        },
        fallbacks=[],
    )

    app.add_handler(conv)
    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()