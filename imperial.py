#TELEGRAM-PYTHON-BOT FOR HOME AUTOMATION (CONTROLLING LIGHT BULB)

from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
from Adafruit_IO import Client,Feed,Data
import os

ADAFRUIT_IO_USERNAME= os.getenv('ADAFRUIT_IO_USERNAME')         #ADAFRUIT_IO_USERNAME
ADAFRUIT_IO_KEY = os.getenv('ADAFRUIT_IO_KEY')                  #ADAFRUIT_IO_KEY
aio = Client('ADAFRUIT_IO_USERNAME','ADAFRUIT_IO_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

def start(bot,update):   #start command defination
  print(str(update.effective_chat.id))
  bot.send_message(chat_id = update.effective_chat.id, text="Welcome Abhishek! Type either /lighton or 'Trun on Light' to turn on light else type /lightoff or 'Turn Off Light' to turn of the light" )

def unknown(bot,update): #if and command are given apart from start,lighton,lightoff then it prints error
  bot.send_message(chat_id =update.effective_chat.id,text='Error in undertandng your command!Please give proper command')

def value_send(value):
  to_feed=aio.feeds('robot')
  aio.send_data(to_feed.key,value)         #defining a feed variable to give values

def lighton(bot,update):                   # when /lighton is the command value=1 is sent to adafruit 
  chat_id=update.message.chat_id
  bot.send_message(chat_id , text="Light is turned ON")
  bot.send_photo(chat_id=update.effective_chat.id,photo='https://images.squarespace-cdn.com/content/5784e04246c3c41c72bf6305/1468526448115-KB10QTHCWSJ3IHHK7HVP/640px-Bombeta_de_Llum.jpg?content-type=image%2Fjpeg')
  value_send(1)

def lightoff(bot,update):                   # when /lightoff is the command value=0 is sent to adafruit
  chat_id=update.message.chat_id
  bot.send_message(chat_id , text="Light is turned OFF")
  bot.send_photo(chat_id=update.effective_chat.id,photo='https://image.shutterstock.com/image-photo/light-bulb-turned-off-over-260nw-162882104.jpg')
  value_send(0)


def given_message(bot,update):         #defining 'Turn on Light','Turn Off Light' and 'End' commands
  text = update.message.chat_id
  text=update.message.text
  if text == 'Turn on Light':
    lighton(bot,update)
  elif text =='Turn Off Light':
    lightoff(bot,update)
  elif text == 'End':
    print("All the lights are off")
    lightoff(bot,update)

#accessing the tokens and commands using api keys and handling them

u = Updater(TELEGRAM_TOKEN)
dp = u.dispatcher
dp.add_handler(CommandHandler('lighton',lighton))
dp.add_handler(CommandHandler('lightoff',lightoff))
dp.add_handler(CommandHandler('start',start))
dp.add_handler(CommandHandler('exit',exit))
dp.add_handler(MessageHandler(Filters.command,unknown))
dp.add_handler(MessageHandler(Filters.text,given_message))
#dp.add_handler(MessageHandler(Filters.text,exit))
u.start_polling()
u.idle()

