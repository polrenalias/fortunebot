import random, pyaztro, json
from telegram.ext import Updater, CommandHandler
from telegram import InputMediaPhoto

# Starting condition checker
started = False

# Bot starter function
def start(update, context):
    global started
    username = str(update.message.from_user.first_name)
    context.bot.send_message(update.message.chat_id, 'Welcome, '+username+", I'm FortuneBot.\nYou can use me to consult about your astrological /sign, your /tarot fortune or today's /horoscope.")
    started = True

# Function used to give the user its fortune via tarot card reading
def get_tarot(update, context):
    global started
    theme_list = ['general','work','love','finance','health','spirituality']
    card_meaning = ''
    if started == True:
        if len(context.args) == 1:
            theme = ' '.join(context.args).lower()
            media_group = []
            if theme in theme_list:
                with open('data.json', 'r') as j:
                    data = json.loads(j.read())	
                card_selection = random.sample(range(0,21), 3)
                for num in card_selection:
                    if random.randint(0, 1) == 0:
                        media_group.append(InputMediaPhoto(open('good_cards/%d.jpg' % num, 'rb')))
                        card_meaning += str(data["card_list"][num]["card_name"]+' (straight): '+data["card_list"][num]["straight_info"][theme])
                    else:
                        media_group.append(InputMediaPhoto(open('bad_cards/%d.jpg' % num, 'rb')))
                        card_meaning += str(data["card_list"][num]["card_name"]+' (downward): '+data["card_list"][num]["reverse_info"][theme])
                    card_meaning += '\n\n'
                context.bot.send_media_group(update.message.chat_id, media = media_group)
                context.bot.send_message(update.message.chat_id, card_meaning)
            else:
                context.bot.send_message(update.message.chat_id, 'Your selection needs to match one of the following themes: love, money, work, family')
        elif len(context.args) == 0:
            context.bot.send_message(update.message.chat_id, 'Usage: /tarot theme')
        else:
            context.bot.send_message(update.message.chat_id, 'Too many arguments. Try again or consult /help')

# Function used to give the current day horoscope to the user (based on his astrological sign)
def get_horoscope(update, context):
    global started
    if started == True:
        if len(context.args) == 1:	
            sign = ' '.join(context.args).lower()
            if sign in ['aries','taurus','gemini','leo','cancer','scorpio','pisces','aquarius','virgo','libra','sagittarius','capricorn']:
                horoscope = pyaztro.Aztro(sign)
                context.bot.send_message(update.message.chat_id, 'Horoscope for '+str(horoscope.current_date)+'\n\nDescription: '+horoscope.description+'\n\nMood: '+horoscope.mood+'.\nLucky color: '+horoscope.color+'.\nLucky number: '+str(horoscope.lucky_number)+'.\nLucky time: '+horoscope.lucky_time+'.\nSign compatibility: '+horoscope.compatibility+'.')
            else:
               context.bot.send_message(update.message.chat_id, 'You need to write an astrological sign (ex: Aries).')
        elif len(context.args) == 0:
            context.bot.send_message(update.message.chat_id, 'Usage: /horoscope sign')
        else:
           context.bot.send_message(update.message.chat_id, 'Too many arguments. Try again or consult /help') 

# Function used to discern which astrological sign the user has    
def ask_sign(update, context):
    global started
    day_is_num = False
    day = 0

    if started == True:
        if len(context.args) == 2:
            args = ' '.join(context.args).split(' ')
            month_list = ['january','february','march','april','may','june','july','august','september','october','november','december']
            month = args[0].lower()
            try:
                day = int(args[1])
                day_is_num = True
            except:
                context.bot.send_message(update.message.chat_id, 'The birth day has to be a number.')
            if day_is_num:
                if month in month_list:
                    if 0 < day < 32:
                        if month == month_list[11]:
                            sign = 'Sagittarius ♐' if (day < 22) else 'Capricorn ♑'
                        elif month == month_list[0]:
                            sign = 'Capricorn ♑' if (day < 20) else 'Aquarius ♒'
                        elif month == month_list[1]:
                            sign = 'Aquarius ♒' if (day < 19) else 'Pisces ♓'
                        elif month == month_list[2]:
                            sign = 'Pisces ♓' if (day < 21) else 'Aries ♈'
                        elif month == month_list[3]:
                            sign = 'Aries ♈' if (day < 20) else 'Taurus ♉'
                        elif month == month_list[4]:
                            sign = 'Taurus ♉' if (day < 21) else 'Gemini ♊'
                        elif month == month_list[5]:
                            sign = 'Gemini ♊' if (day < 21) else 'Cancer ♋'
                        elif month == month_list[6]:
                            sign = 'Cancer ♋' if (day < 23) else 'Leo ♌'
                        elif month == month_list[7]:
                            sign = 'Leo ♌' if (day < 23) else 'Virgo ♍'
                        elif month == month_list[8]:
                            sign = 'Virgo ♍' if (day < 23) else 'Libra ♎'
                        elif month == month_list[9]:
                            sign = 'Libra ♎' if (day < 23) else 'Scorpio ♏'
                        elif month == month_list[10]:
                            sign = 'Scorpio ♏' if (day < 22) else 'Sagittarius ♐'
                        context.bot.send_message(update.message.chat_id, 'Your sign is: '+sign)
                    else:
                        context.bot.send_message(update.message.chat_id, 'The day number has to be a valid one (between 1 and 31)')
                else:
                    context.bot.send_message(update.message.chat_id, "You need to write your birth month's name (ex: December).")
        elif len(context.args) == 0:
            context.bot.send_message(update.message.chat_id, 'Usage: /sign birth_month birth_day')
        else:
           context.bot.send_message(update.message.chat_id, 'Too many or too few arguments. Try again or consult /help')

# Function to inform the user of the bot usage        
def help(update, context):
    if started == True:
        context.bot.send_message(update.message.chat_id, "- Initialize the bot with /start\n- Select the tarot reading and its theme with /tarot theme (Themes available: love, health, work)\n- Get your horoscope with /horoscope sign\n- Ask what's your astrological sign with /sign birth_month birth_day (ex: August 13)")

# Main code        
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