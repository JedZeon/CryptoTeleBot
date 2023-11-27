import telebot
from config import TOKEN
from extensions import APIException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_help(message: telebot.types.Message):
    text = ("Бот конвертации валюты в валюту \n"
            "формат ввода (через пробел):\n"
            "<имя валюты, источник> <имя валюты конвертации> <количество первой валюты>\n"
            "_____________________________\n"
            "/start - описание\n"
            "/help - описание\n"
            "/values - информация о всех доступных валютах\n")
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def send_val(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys_val.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров')

        base, quote, amount = values
        itogo = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя \n - {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать \n - {e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {itogo}'
        bot.reply_to(message, text)


bot.polling()
