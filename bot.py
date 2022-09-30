import random, pyaztro
from telegram.ext import (Updater, CommandHandler)
from telegram import InputMediaPhoto

started = False

def start(update, context):
    global started
    username = str(update.message.from_user.first_name)
    context.bot.send_message(update.message.chat_id, 'Welcome, '+username+", I'm FortuneBot.")
    context.bot.send_message(update.message.chat_id, 'Select the theme (love, friendship, money, work, family) you want to consult about with /select theme')
    started = True

def get_tarot(update, context):
    global started
    if started == True:	
        user_selection = ' '.join(context.args)
        themes = ['love','money','friendship','work','family']
        media_group = []
        if user_selection in themes:
            card_selection = random.sample(range(0,21), 3)
            for num in card_selection:
                if random.randint(0, 1) == 0:
                    media_group.append(InputMediaPhoto(open('good_cards/%d.jpg' % num, 'rb'), caption = 'cards' if num == 0 else ''))
                else:
                    media_group.append(InputMediaPhoto(open('bad_cards/%d.jpg' % num, 'rb'), caption = 'cards' if num == 0 else ''))
            context.bot.send_media_group(update.message.chat_id, media = media_group)  

def get_horoscope(update, context):
    sign = ' '.join(context.args)
    horoscope = pyaztro.Aztro(sign)
    
    context.bot.send_message(update.message.chat_id, 'Description: '+horoscope.description)
    context.bot.send_message(update.message.chat_id, 'Mood: '+horoscope.mood)
    context.bot.send_message(update.message.chat_id, 'Lucky color: '+horoscope.color)
    context.bot.send_message(update.message.chat_id, 'Lucky number: '+str(horoscope.lucky_number))
    context.bot.send_message(update.message.chat_id, 'Lucky time: '+horoscope.lucky_time)
    context.bot.send_message(update.message.chat_id, 'Sign compatibility: '+horoscope.compatibility)
    context.bot.send_message(update.message.chat_id, 'Horoscope valid until: '+str(horoscope.current_date))
    
def ask_sign(update, context):
    correct = True
    args = ' '.join(context.args).split(' ')
    month = args[0]
    day = int(args[1])
    if month == 12:
        sign = 'Sagittarius' if (day < 22) else 'Capricorn'
    elif month == 'january':
        sign = 'Capricorn' if (day < 20) else 'Aquarius'
    elif month == 'february':
        sign = 'Aquarius' if (day < 19) else 'Pisces'
    elif month == 'march':
        sign = 'Pisces' if (day < 21) else 'Aries'
    elif month == 'april':
        sign = 'Aries' if (day < 20) else 'Taurus'
    elif month == 'may':
        sign = 'Taurus' if (day < 21) else 'Gemini'
    elif month == 'june':
        sign = 'Gemini' if (day < 21) else 'Cancer'
    elif month == 'july':
        sign = 'Cancer' if (day < 23) else 'Leo'
    elif month == 'august':
        sign = 'Leo' if (day < 23) else 'Virgo'
    elif month == 'september':
        sign = 'Virgo' if (day < 23) else 'Libra'
    elif month == 'october':
        sign = 'Libra' if (day < 23) else 'Scorpio'
    elif month == 'november':
        sign = 'scorpio' if (day < 22) else 'Sagittarius'
    else:
        correct = False
    print('aaaa')

    if correct == True:
    	context.bot.send_message(update.message.chat_id, sign)

def help(update, context):
    context.bot.send_message(update.message.chat_id, 'Initialize the bot with /start')
    context.bot.send_message(update.message.chat_id, "Select the tarot reading and its theme with /tarot theme")
    context.bot.send_message(update.message.chat_id, "Get your horoscope with /horoscope sign")
    context.bot.send_message(update.message.chat_id, "Ask what's your astrological sign with /sign month day")
        
def main():
	TOKEN = "5692200430:AAH5CitxWYf5fAAUj97pzusUnh0Sk-4egl0"
	updater = Updater(TOKEN, use_context=True)
	dp = updater.dispatcher

	dp.add_handler(CommandHandler('start',  start))
	dp.add_handler(CommandHandler('tarot',  get_tarot))
	dp.add_handler(CommandHandler('help',   help))
	dp.add_handler(CommandHandler('sign',   ask_sign))
	dp.add_handler(CommandHandler('horoscope',  get_horoscope))
 	
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()