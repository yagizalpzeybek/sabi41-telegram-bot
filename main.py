import logging

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

from config import TOKEN
from commands import (start_command, help_command, about_command, custom_command, time_command, menu_command, game_command, wiki_command, weather_command, ask_command,
set_budget_command, spend_command, balance_command, reset_budget_command, balance_tracker_command, set_calories_command, take_calories_command, calories_command, reset_calories_command, 
reset_calories_to_initial_command, calorie_tracker_command
)
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
    app.add_handler(CommandHandler("setbudget", set_budget_command))
    app.add_handler(CommandHandler("spend", spend_command))
    app.add_handler(CommandHandler("balance", balance_command))
    app.add_handler(CommandHandler("resetbudget", reset_budget_command))
    app.add_handler(CommandHandler("balancetracker", balance_tracker_command))
    app.add_handler(CommandHandler("setcalories", set_calories_command))
    app.add_handler(CommandHandler("calories", calories_command))
    app.add_handler(CommandHandler("take", take_calories_command))
    app.add_handler(CommandHandler("reset", reset_calories_command))
    app.add_handler(CommandHandler("resettoinitial", reset_calories_to_initial_command))
    app.add_handler(CommandHandler("calorietracker", calorie_tracker_command))
                    

    app.add_error_handler(error)

    print("Polling...")
    app.run_polling()