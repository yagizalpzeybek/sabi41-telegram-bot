import logging

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

from config import TOKEN
from commands import start_command, help_command, about_command, custom_command, time_command, menu_command, game_command, wiki_command, weather_command, ask_command
from handlers import handle_message, button_handler, error


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO

)

    

if __name__ == "__main__":
    print("Starting bot...")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("custom", custom_command))
    app.add_handler(CommandHandler("time", time_command))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("game", game_command))
    app.add_handler(CommandHandler("wiki", wiki_command))
    app.add_handler(CommandHandler("weather", weather_command))
    app.add_handler(CommandHandler("ask", ask_command))

    # ❗ önemli
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_error_handler(error)

    print("Polling...")
    app.run_polling()