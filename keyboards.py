from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🏥 Медицина", callback_data="medicine")],
        [InlineKeyboardButton("✂️ Красота", callback_data="beauty")],
        [InlineKeyboardButton("⚖️ Юрист", callback_data="lawyer")],
        [InlineKeyboardButton("🏠 ЖКХ", callback_data="housing")],
        [InlineKeyboardButton("🍽️ Кафе", callback_data="food")],
        [InlineKeyboardButton("📚 Образование", callback_data="education")],
        [InlineKeyboardButton("🧾 Документы", callback_data="documents")],
    ]
    return InlineKeyboardMarkup(keyboard)