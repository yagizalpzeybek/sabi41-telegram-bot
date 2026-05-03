import random
import datetime
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import BOT_USERNAME
from responses import handle_response

logger = logging.getLogger(__name__)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text
    user_id = update.message.from_user.id

    logger.info(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type in ["group", "supergroup"]:
        if BOT_USERNAME and BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, "").strip()
            response = handle_response(new_text, user_id)
        else:
            return
    else:
        response = handle_response(text, user_id)

    print("Bot:", response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Error: {context.error}")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Back button
    back_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅ Back", callback_data="menu")]
    ])

    if query.data == "help":
        await query.edit_message_text(
            "Commands:\n/start - Start\n/help - Help\n/about - About\n/time - Time\n/menu - Menu\n/game - Rock Paper Scissors\n/wiki - Wikipedia Search\n/weather - Weather Search",
            reply_markup=back_markup
        )

    elif query.data == "about":
        await query.edit_message_text(
            "I am Sabi41, a simple Telegram assistant bot.",
            reply_markup=back_markup
        )

    elif query.data == "time":
        import datetime
        now = datetime.datetime.now().strftime("%H:%M:%S")
        await query.edit_message_text(
            f"Current time: {now}",
            reply_markup=back_markup
        )

    elif query.data == "wiki_info":
        await query.edit_message_text(
            "🌐 Wikipedia Search\n\n"
            "Use this command:\n"
            "/wiki search_term\n\n"
            "Example:\n"
            "/wiki Python",
            reply_markup=back_markup
        )

    elif query.data == "weather_info":
        await query.edit_message_text(
            "🌦️ Weather Search\n\n"
            "Use this command:\n"
            "/weather city_name\n\n"
            "Example:\n"
            "/weather London",
            reply_markup=back_markup
        )

    elif query.data == "menu":
        keyboard = [
            [
                InlineKeyboardButton("📘 Help", callback_data="help"),
                InlineKeyboardButton("ℹ️ About", callback_data="about"),
            ],
            [
                InlineKeyboardButton("⏰ Time", callback_data="time"),
                InlineKeyboardButton("🎮 Game", callback_data="game"),
            ],
            [
                InlineKeyboardButton("🌐 Wiki", callback_data="wiki_info"),
                InlineKeyboardButton("🌦️ Weather", callback_data="weather_info"),
            
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
        "Choose an option:",
        reply_markup=reply_markup
        )

    elif query.data == "game_menu":
        
        keyboard = [
            [
            InlineKeyboardButton("🪨 Rock", callback_data="game_rock"),
            InlineKeyboardButton("📄 Paper", callback_data="game_paper"),
            InlineKeyboardButton("✂️ Scissors", callback_data="game_scissors"),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "Choose your move:",
            reply_markup=reply_markup
    )
    
    elif query.data.startswith("game"):
        user_choice = query.data.replace("game_", "")
        bot_choice = random.choice(["rock", "paper", "scissors"])

        if user_choice == bot_choice:
            result = "It's a draw!"
        
        elif(
            user_choice == "rock" and bot_choice == "scissors"
            or user_choice == "paper" and bot_choice == "rock"
            or user_choice == "scissors" and bot_choice == "paper"
        ):
            result = "🎉 You win!"
        else:
            result = "😎 I win!"

        keyboard = [
            [InlineKeyboardButton("🔁 Play Again", callback_data="game_menu")],
            [InlineKeyboardButton("⬅ Back", callback_data="menu")]
        
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"You choose: {user_choice}\n"
            f"I choose: {bot_choice}\n\n"
            f"{result}",
            reply_markup=reply_markup
        )
