import telebot
from config import TOKEN, CURRENCY_NAMES
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    msg = "Чтобы начать работу введите комманду боту в формате:\n" \
          "<имя валюты> <в какую валюту перевести> " \
          "<количество переводимой валюты>" \
          "\n\nУвидеть список всех доступных валют: /values"
    bot.reply_to(message, msg)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    msg = "Доступные валюты:"
    for name in CURRENCY_NAMES.keys():
        msg = '\n'.join((msg, name,))
    bot.reply_to(message, msg)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров')

        quote, base, amount = values
        price = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        msg = f'Цена {amount} {quote} в {base} = {price:.2f}'
        bot.send_message((message.chat.id), msg)


bot.polling()
