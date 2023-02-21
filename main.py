import telebot
from config import symbols, keys, TOKEN
from extension import ConvertionException, CryptoConverter
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Format of commands: \n <current coins>  <change coins>  <amount>  \n List of currency /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Active currency:'
    for k in keys.keys():
        text = f'\n {symbols[k]}   {k}'.join((text,'   ', ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('So much parameters')
        quote, base, amount = message.text.split(' ')
        total_base = CryptoConverter.convert(quote, base, amount) * float(amount)
    except ConvertionException as e:
        bot.reply_to(message, f"User's fault \n{e}")

    except Exception as e:
        bot.reply_to(message, f'Something wrong\n{e}')
    else:
        text = f'Coast {amount} {quote} in {base} - {total_base:.7f}'
        bot.send_message(message.chat.id, text)

bot.polling()




