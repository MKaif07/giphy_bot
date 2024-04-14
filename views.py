import pytz
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext
from req import get_views_from_Id
import datetime
import database

import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''
                                    Welcome to the Giphy View Tracker Bot! \nType /help for available commands.
                                    ''')
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''
                                    Available commands:
/views <project url>: Get current views for the specified Giphy post.
/track <project url>: Save the Giphy post to track its views.
/untrack <project url>: Remove the Giphy post from tracking.
/list: List all tracked Giphy posts.
                                    ''')
 
async def views_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if len(update.message.text.split(" ")) == 1:
        await update.message.reply_text(f'TRY: /view <project_url> ')
        
    else:
        url = update.message.text.split(" ")[1].split("/")[-1].split("-")[-1]
        
        response, status_code = get_views_from_Id(url)
        if(status_code == 200):
            await update.message.reply_text(f'Current views for the specified Giphy post: {response} views')

        else:
            await update.message.reply_text(f'No views to track')
            
async def track_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    if len(update.message.text.split(" ")) == 1:
        await update.message.reply_text(f'TRY: /track <project_url> ')
        return
    
    userId = update.message.chat.id
    url = update.message.text.split(" ")[1]
    url_id = url.split("/")[-1].split("-")[-1]

    if(database.search_with_userId('project_url', url, '=', userId) == []):
        view_count, status_code = get_views_from_Id(url_id)
        if(status_code == 200):
            try:
                database.add_one(userId, url, url_id, datetime.datetime.now(), datetime.datetime.now(),view_count)
                await update.message.reply_text(f'Giphy post successfully saved for tracking. 🔍')
            except:
                print('error in database')
        else:
            await update.message.reply_text(f'No views to track')
    else:
            await update.message.reply_text(f'Already tracking this project')
        
async def untrack_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    if len(update.message.text.split(" ")) == 1:
        await update.message.reply_text(f'TRY: /untrack <project_url> ')
        return

    userId = update.message.chat.id
    url = update.message.text.split(" ")[1]
    database.delete_record('project_url', url, '=', userId)
    await update.message.reply_text('Giphy post successfully removed from tracking. ✅')
    pass

async def list_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    userId = update.message.chat.id
    items = database.search('userId', userId, '=')
    if len(items) == 0:
        await update.message.reply_text(f'You aren\'t tracking any projects')
        return 
    
    await update.message.reply_text(f'List of all tracked projects:')
    count = 1 
    for item in items:
        added_obj = datetime.datetime.strptime(item[3], "%Y-%m-%d %H:%M:%S.%f") 
        updated_obj = datetime.datetime.strptime(item[4], "%Y-%m-%d %H:%M:%S.%f")
        current_views, status_code = get_views_from_Id(item[2])
        await update.message.reply_text(f'#{count} \n{item[1]} \nAdded On: {added_obj.strftime("%B %d, %Y %I:%M %p")} \nUpdated On: {updated_obj.strftime("%B %d, %Y %I:%M %p")} \nViews Today: {current_views - item[5]} \nTotal views: {current_views}')
        count+=1

async def update_database(context: CallbackContext):
    result = database.update_all()

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

def main():
    print('Starting bot...')
    app = Application.builder().token(BOT_TOKEN).build()
    context = ContextTypes.DEFAULT_TYPE

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('views', views_command))
    app.add_handler(CommandHandler('track', track_command))
    app.add_handler(CommandHandler('untrack', untrack_command))
    app.add_handler(CommandHandler('list', list_command))

    # Error
    app.add_error_handler(error)

    # UPDATES database at 5 AM UTC +5:30
    app.job_queue.run_daily(update_database, datetime.time(hour=5, minute=00, tzinfo=pytz.timezone('Asia/Kolkata')), days=(0, 1, 2, 3, 4, 5, 6))

    # Polls the bot
    print('Polling...')
    app.run_polling(allowed_updates=Update.ALL_TYPES, poll_interval=3)
