import logging
from telegram import InlineQueryResultDocument, InlineQueryResultVideo, InlineQueryResultAudio
from telegram.ext import Updater, InlineQueryHandler, MessageHandler, Filters
import pymongo

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize the Telegram bot
updater = Updater(token='YOUR_TELEGRAM_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher

# Set up the database connection
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']
files_collection = db['files']

def handle_files(update, context):
    if update.message.document or update.message.video or update.message.audio:
        file_info = update.message.document or update.message.video or update.message.audio
        caption = file_info.caption or ''
        file_data = {
            'file_id': file_info.file_id,
            'file_type': file_info.mime_type,
            'caption': caption
        }
        files_collection.insert_one(file_data)

def inline_search(update, context):
    query = update.inline_query.query
    search_results = files_collection.find({'$text': {'$search': query}})
    results = []
    for result in search_results:
        if result['file_type'].startswith('video'):
            results.append(InlineQueryResultVideo(id=result['file_id'], video_url=result['file_id']))
        elif result['file_type'].startswith('audio'):
            results.append(InlineQueryResultAudio(id=result['file_id'], audio_url=result['file_id']))
        else:
            results.append(InlineQueryResultDocument(id=result['file_id'], document_url=result['file_id']))
    update.inline_query.answer(results)

file_handler = MessageHandler(Filters.document | Filters.video | Filters.audio, handle_files)
inline_search_handler = InlineQueryHandler(inline_search)

dispatcher.add_handler(file_handler)
dispatcher.add_handler(inline_search_handler)

updater.start_polling()
