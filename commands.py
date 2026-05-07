import datetime
import wikipedia
import requests

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import WEATHER_API_KEY, OPENAI_API_KEY
from openai import AsyncOpenAI

openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)


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
            InlineKeyboardButton("🌦️ Weather", callback_data="weather_info"),
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

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Please provide a city name.\nExample: /weather London"

        )
        return
    
    city = " ".join(context.args)

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "en",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if response.status_code != 200:
            await update.message.reply_text("City not found or weather service error.")
            return

        city_name = data["name"]
        country = data["sys"]["country"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"].title()

        await update.message.reply_text(
            f"🌦️ Weather in {city_name}, {country}\n\n"
            f"Condition: {description}\n"
            f"Temperature: {temp}°C\n"
            f"Feels like: {feels_like}°C\n"
            f"Humidity: {humidity}%"
        )

    except Exception as e:
        print(f"Weather error: {e}")
        await update.message.reply_text("Something went wrong while fetching weather data.")


async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Please ask a question \nExample: /ask What is telegram?"
        )
        return
        
    user_question = " ".join(context.args)

    try: 
        await update.message.reply_text("Thinking...")

        response = await openai_client.responses.create(
            model = "gpt-4.1-mini",
            input=user_question,
            instructions=(
                "You are Sabi41, a helpful and friendly Telegram assistant. "
                "Keep answers concise, clear and beginner-friendly."
            ),
            max_output_tokens=300,
        )

        await update.message.reply_text(response.output_text)
    
    except Exception as e:
        print(f"OpenAI error: {e}")
        await update.message.reply_text(
            "Something went wrong  while generating an answer."
    )
    