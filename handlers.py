from telegram import Update
from telegram.ext import ContextTypes
from keyboards import main_menu_keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я помогу тебе с жизнью в Литве. Выбери, что тебе нужно:",
        reply_markup=main_menu_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "medicine":
        await query.edit_message_text(text="🏥 Выбрана категория: Медицина")
    elif query.data == "beauty":
        await query.edit_message_text(text="✂️ Выбрана категория: Красота")
    elif query.data == "lawyer":
        await query.edit_message_text(text="⚖️ Выбрана категория: Юрист")
    elif query.data == "housing":
        await query.edit_message_text(text="🏠 Выбрана категория: ЖКХ")
    elif query.data == "food":
        await query.edit_message_text(text="🍽️ Выбрана категория: Кафе")
    elif query.data == "education":
        await query.edit_message_text(text="📚 Выбрана категория: Образование")
    elif query.data == "documents":
        await query.edit_message_text(text="🧾 Выбрана категория: Документы")