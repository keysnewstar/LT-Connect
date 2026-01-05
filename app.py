import os
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from handlers import start, button_handler

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    port = int(os.environ.get('PORT', 8443))
    webhook_url = os.getenv("WEBHOOK_URL")

    if webhook_url:
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=TELEGRAM_BOT_TOKEN,
            webhook_url=f"{webhook_url}/{TELEGRAM_BOT_TOKEN}"
        )
    else:
        app.run_polling()

if __name__ == "__main__":
    main()