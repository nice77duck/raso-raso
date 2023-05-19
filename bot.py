import telegram
from telegram.ext import CommandHandler, Updater
import os

# Define the token for your bot obtained from BotFather
TOKEN = "YOUR_BOT_TOKEN"

# Define a handler function for the /start command
def start(update, context):
    update.message.reply_text("Hi! I'm your file search bot. Use /search to look for files in this channel.")

# Define a handler function for the /help command
def help(update, context):
    update.message.reply_text("To search for a file, use /search followed by the name of the file. For example: /search hello.txt")

# Define a handler function for the /search command
def search_files(update, context):
    # Get the text after the /search command
    query = ' '.join(context.args)

    # Search for files in the private channel directory
    files = []
    for file in os.listdir("private_channel_directory"):
        if query in file:
            files.append(file)

    # Forward the matching files to the user chat
    if len(files) > 0:
        for file in files:
            context.bot.send_document(update.message.chat_id, document=open(os.path.join("private_channel_directory", file), 'rb'))
    else:
        update.message.reply_text("No matching files found.")

# Create an instance of the bot and add handlers for the commands
bot = telegram.Bot(TOKEN)
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help))
dispatcher.add_handler(CommandHandler("search", search_files))

# Start the bot
updater.start_polling()
updater.idle()
