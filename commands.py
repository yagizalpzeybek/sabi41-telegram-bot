import datetime
import wikipedia

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes



async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.first_name
    await update.message.reply_text(f"Hello {user}! I am Sabi41 🤖")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
Commands:
/start - Start the bot
/help - Show help
/about - About bot
/custom - Custom command
        """
    )


async def wiki_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a search term.\nExample: /wiki Python")
        return
    
    query = " ".join(context.args)

    try:
        wikipedia.set_lang("en")

        results =  wikipedia.search(query)

        if not results:
            await update.message.reply_text("No results found.")
            return
        
        page_title = results[0]
        summary = wikipedia.summary(page_title, sentences = 2)

        await update.message.reply_text(
            f"🌐 {page_title}\n\n{summary}"
        )

    except wikipedia.exceptions.DisambiguationError as e:
        options = "\n".join(e.options[:5])
        await update.message.reply_text(f"Too many results. Try one of these:\n\n{options}")

    except wikipedia.exceptions.PageError:
        await update.message.reply_text("No page found for this search.")

    except Exception as e:
        await update.message.reply_text("Something went wrong while searching Wikipedia.")
        print(f"Wikipedia error: {e}")


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am Sabi41, a simple Telegram assistant bot built with Python.")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command!")

async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"Current time: {formatted_time}")

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard= [
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
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🤖 Welcome to Sabi41 Bot!\n\nChoose an option:",
        reply_markup=reply_markup
    )

async def game_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🪨 Rock", callback_data="game_rock"),
            InlineKeyboardButton("📄 Paper", callback_data="game_paper"),
            InlineKeyboardButton("✂️ Scissors", callback_data="game_scissors"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Choose your move:",
        reply_markup=reply_markup
    )