from flask import Flask, request
from telegram.ext import CommandHandler, MessageHandler, Filters, Dispatcher
from telegram import Bot, Update
from helpers import get_user_location, get_weather, get_news, get_reply
import time
import os
import messages

TOKEN = os.environ["BOT_TOKEN"]

app = Flask(__name__)


@app.route("/")
def index():
    """
    To check app is working
    :return:
    """
    return "Hello !"


@app.route(f"/{TOKEN}", methods=["GET", "POST"])
def webhook():
    """Web hook
    :return:
    """
    time.sleep(1.2)
    update = Update.de_json(request.get_json(), bot)
    dp.process_update(update)
    return "ok"


def start(bot, update):
    """To start the bot
    :param bot:
    :param update:
    :return start message:
    """
    bot.send_message(chat_id=update.message.chat_id, text=messages.start_msg)


def weather(bot, update):
    """ To get weather of given location
    :param bot:
    :param update:
    :return weather information of user's location:
    """
    user_location = get_user_location(update.message.from_user.id)

    if user_location:
        bot.send_message(
            chat_id=update.message.chat_id, text=get_weather(user_location[0])
        )
    else:
        bot.send_message(chat_id=update.message.chat_id, text=messages.location_msg)


def news(bot, update):
    """
    To get top 3 news of given location
    :param bot:
    :param update:
    :return top 3 news of user's location:
    """
    user_location = get_user_location(update.message.from_user.id)

    if user_location:
        bot.send_message(
            chat_id=update.message.chat_id, text=get_news(user_location[1])
        )
    else:
        bot.send_message(chat_id=update.message.chat_id, text=messages.location_msg)


def reply_text(bot, update):
    """ All the message given by user except the commands can be handled with this function.
    :param bot:
    :param update:
    :return reply message which are not handled by command handlers:
    """
    reply = get_reply(
        update.message.text, update.message.chat_id, update.message.from_user.id
    )
    bot.send_message(chat_id=update.message.chat_id, text=reply)


bot = Bot(TOKEN)
try:
    time.sleep(1.2)
    bot.set_webhook("LIVE_HEROKU_URL" + TOKEN)
except Exception as e:
    print(e)
dp = Dispatcher(bot, None)
dp.add_handler(CommandHandler("Hi", start))
dp.add_handler(CommandHandler("hi", start))

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("weather", weather))
dp.add_handler(CommandHandler("news", news))
dp.add_handler(MessageHandler(Filters.text, reply_text))

if __name__ == "__main__":
    app.run(port=8443, debug=True)
