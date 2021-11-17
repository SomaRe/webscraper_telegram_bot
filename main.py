from bs4 import BeautifulSoup
import requests
import keys
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler,  CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
# logging End


url = "https://www.canadacomputers.com/search/results_details.php?language=en&keywords=3070+ti+%2B"
interval = 43200

TOKEN = keys.TELE_TOKEN

def scrape(context: CallbackContext):
    job = context.job
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    productTag = soup.find(id = "product-list")
    children = productTag.findChildren("div",recursive=False)
    flag = False
    for child in children:
        if "Bundle Code:" in str(child):
            flag = True

    if(flag == True):
        context.bot.send_message(job.context, text ="Bundle's available")
        context.bot.send_message(job.context, text ="https://www.canadacomputers.com/search/results_details.php?language=en&keywords=3070+ti+%2B")    
    else:
        context.bot.send_message(job.context, text ="No Bundles Found")

def start(update: Update, _: CallbackContext):
    update.message.reply_text('Hi! give use command /search to start bot')

def search(update:Update, context: CallbackContext):
    update.message.reply_text("Job started!")
    chat_id = update.message.chat_id
    context.job_queue.run_repeating(scrape, interval, first=5,context=chat_id)

def stop(update:Update, context: CallbackContext):
    update.message.reply_text( 'Stopping the search!')
    context.job_queue.jobs()[0].schedule_removal()


def main():
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start",start))
    dispatcher.add_handler(CommandHandler("search",search))
    dispatcher.add_handler(CommandHandler("stop", stop))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()