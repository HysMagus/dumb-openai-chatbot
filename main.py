import logging
from telegram import Update, User
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import os
from dotenv import load_dotenv
import openai
load_dotenv()
openai.api_key = os.getenv('openai')
botkey = os.getenv('botkey')
user = Update.effective_user
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    #   print(repr(user.first_name), repr(user.last_name))
#    print('%s %s' % (user.first_name, user.last_name))
#    print(user.full_name)
    text = "Hello " + user.first_name
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Help Commands Include: " " "
                                                                          "/help - Get this message")
async def change_system_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello Mr.")


async def askgpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    systemrole = "You are a kind helpful assistant. The person you're talking to is named " + str(user.full_name) + " they're your boss"

    messages = [
        {"role": "system", "content": systemrole},
    ]

    message = update.message.text
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

    reply = chat.choices[0].message.content
#    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})
    response = reply
    print(response)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


if __name__ == '__main__':
    application = ApplicationBuilder().token(botkey).build()

    start_handler = CommandHandler('start', start)
    askgpt_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), askgpt)
    help_handler = CommandHandler('help', help)
    application.add_handler(start_handler)
    application.add_handler(askgpt_handler)
    application.add_handler(help_handler)


    application.run_polling()
