import datetime
import wikipedia
import requests

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import WEATHER_API_KEY, GROQ_API_KEY
from groq import Groq
from budget import set_budget, get_balance, spend_money, reset_budget
from calories import set_calories, get_calories, take_calories, reset_calories, reset_to_initial_calories


groq_client = Groq(api_key=GROQ_API_KEY)




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
            "Please ask a question.\nExample: /ask What is Telegram??"
        )
        return

    user_question = " ".join(context.args)

    try:
        await update.message.reply_text("Thinking...")

        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are Sabi41, a helpful Telegram assistant. Keep answers short and clear."
                },
                {
                    "role": "user",
                    "content": user_question
                }
            ],
            temperature=0.7,
            max_tokens=300,
        )

        answer = completion.choices[0].message.content
        await update.message.reply_text(answer.strip())

    except Exception as e:
        print(f"Groq error: {e}")
        await update.message.reply_text("AI service is currently unavailable.")


async def set_budget_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Please enter a budget amount.\nExample: /setbudget 20000"
        )
        return
        
    try:
        amount = float(context.args[0].replace(",","."))
    except ValueError:
        await update.message.reply_text("Please enter a valid number.")
        return
    
    if amount <= 0:
        await update.message.reply_text("Budget must be greater than 0")
        return
        
    user_id = update.message.from_user.id
    budget = set_budget(user_id, amount)

    await update.message.reply_text(
        f"Budget set: {budget:,.2f} TL"
    )
        
async def spend_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Please enter an amount.\nExample: /spend 150"

        )

        return
        
    try: 
        amount = float(context.args[0].replace(",","."))
    except ValueError:
        await update.message.reply_text("Please enter a valid number")
        return
        
    if amount <= 0:
        await update.message.reply_text("Amount must be greater than 0.")
        return
        
    user_id = update.message.from_user.id
    remaining_balance = spend_money(user_id, amount)

    if remaining_balance is None:
        await update.message.reply_text(
            "You don't have a budget yet.\nSet one with: /setbudget"
        )
        return
        
    await update.message.reply_text(
        f"Expense recorded: {amount:,.2f} TL\n"
        f"Remaining balance: {remaining_balance:,.2f} TL"
    )

async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    balance = get_balance(user_id)

    if balance is None:
        await update.message.reply_text(
            "You don't have a budget yet.\n Set one with: /setbudget"
        )
        return
        
    await update.message.reply_text(
        f"Your remaining balance is {balance:,.2f} TL"
    )

async def reset_budget_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    reset_budget(user_id)

    await update.message.reply_text(
        "Budget reset. Set a new budget with: /setbudget"
    )

async def balance_tracker_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💰 Balance Tracker Commands\n\n"
        "/setbudget - Set your budget\n"
        "/spend - Record an expense\n"
        "/balance - Show remaining balance\n"
        "/resetbudget - Reset your budget"
    )

async def set_calories_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Please enter a calorie amount.\nExample: /setcalories 2500"
        )
        return
        
    try:
        amount = float(context.args[0].replace(",","."))
    except ValueError:
        await update.message.reply_text("Please enter a valid number.")
        return
    
    if amount <= 0:
        await update.message.reply_text("Calorie amount must be greater than 0")
        return
        
    user_id = update.message.from_user.id
    calories = set_calories(user_id, amount)

    await update.message.reply_text(
        f"Initial calories: {calories['initial_calories']:,.2f} kcal\n"
        f"Current calories: {calories['current_calories']:,.2f} kcal"
    )
        
async def take_calories_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Please enter an amount.\nExample: /take 150"

        )

        return
        
    try: 
        amount = float(context.args[0].replace(",","."))
    except ValueError:
        await update.message.reply_text("Please enter a valid number")
        return
        
    if amount <= 0:
        await update.message.reply_text("Amount must be greater than 0.")
        return
        
    user_id = update.message.from_user.id
    remaining_calories = take_calories(user_id, amount)

    if remaining_calories is None:
        await update.message.reply_text(
            "You didn't enter a calorie amount yet.\nSet one with: /setcalories"
        )
        return
        
    await update.message.reply_text(
        f"Calories recorded: {amount:,.2f} kcal\n"
        f"Remaining calories: {remaining_calories['current_calories']:,.2f} kcal"
    )

async def calories_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    calories = get_calories(user_id)

    if calories is None:
        await update.message.reply_text(
            "You didn't enter a calorie amount yet.\n Set one with: /setcalories"
        )
        return
        
    await update.message.reply_text(
        f"Initial calories: {calories['initial_calories']:,.2f} kcal\n"
        f"Current calories: {calories['current_calories']:,.2f} kcal"
    )

async def reset_calories_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    reset_calories(user_id)

    await update.message.reply_text(
        "Calories reset. Set a new calorie amount with: /setcalories"
    )

async def reset_calories_to_initial_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    calories = reset_to_initial_calories(user_id)

    if calories is None:
        await update.message.reply_text(
            "You don't have a calorie amount yet.\n Set one with: /setcalories"
        )
        return
    
    await update.message.reply_text(
        f"Calories reset to initial amount.\n"
        f"Current calories: {calories['current_calories']:,.2f} kcal"
    )

async def calorie_tracker_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Calorie Tracker Commands\n\n"
        "/setcalories - Set your daily calorie amount\n"
        "/take - Record the calories taken\n"
        "/calories - Show remaining calories\n"
        "/resetnew - Reset to your new daily calorie amount\n"
        "/resetcalories - Reset you calories to initial amount"
    )







