import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import requests

# Replace with your actual API keys
TELEGRAM_BOT_TOKEN = "7855854661:AAEkX7eqtg0nGOF4umWhtcrEtLwc0a8kJK4"
NEWS_API_KEY = "0e82dc76e3f840d2b12bfc39249995be"
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

# Enable logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message when the bot starts."""
    await update.message.reply_text("👋 Hello! I am your News Bot. Use /news to get top headlines.")


async def get_news(update: Update, context: CallbackContext) -> None:
    """Fetches news articles from NewsAPI and sends them to the user."""
    category = context.args[0] if context.args else "technology"
    params = {
        "apiKey": NEWS_API_KEY,
        "country": "us",
        "category": category
    }
    response = requests.get(NEWS_API_URL, params=params)

    if response.status_code == 200:
        articles = response.json().get("articles", [])
        if not articles:
            await update.message.reply_text("No news articles found.")
            return

        news_list = "📰 *Top News Headlines:*\n"
        for index, article in enumerate(articles[:5], start=1):
            news_list += f"{index}. *{article['title']}* ({article['source']['name']})\n   🔗 [Read More]({article['url']})\n\n"

        await update.message.reply_markdown(news_list, disable_web_page_preview=True)
    else:
        await update.message.reply_text("⚠️ Error fetching news.")


# Set up the bot
app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("news", get_news))

if __name__ == "__main__":
    app.run_polling()
