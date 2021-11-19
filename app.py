import telebot
from settings import TOKEN
from extensions import Currency
from extensions import AmountNotDigits, ErrorCurrencyCodes, ErrorCorrectData, ErrorSameCurrency


bot = telebot.TeleBot(TOKEN)
print(bot.get_me())
c = Currency()


@bot.message_handler(commands=['start'])
def welcome(message):
    txt = f'{message.from_user.username} - Добро пожаловать в Конвертер валют\n' \
           'нажмите /help для получения помощи'
    bot.reply_to(message, txt)


@bot.message_handler(commands=['help'])
def help_message(message):
    txt = 'чтобы сконвертировать введите <имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n' \
           '/values - получить список всех доступных валют\n' \
          'допускается ввод: евро, доллар, рубль, золото, серебро, биткоин. Остальные валюты только трехбуквенный код (AUD, ZWL, TWD и т.д.)'
    bot.reply_to(message, txt)


@bot.message_handler(commands=['values'])
def value_message(message):
    txt = f'Доступные валюты:\n'
    dct = c.get_all_currencies()
    for key, value in dct.items():
        txt += f'{key}: {value}\n'
    bot.reply_to(message, txt)


@bot.message_handler(content_types=['text'])
def text(message):
    try:
        lst = message.text.upper().split(' ')
        if len(lst) > 3:
            raise ErrorCorrectData()
        base, quote, amount = lst
        if base == quote:
            raise ErrorSameCurrency
        if not amount.isdigit():
            raise AmountNotDigits()
        req = c.get_price(base, quote, amount)
        txt = f'Цена {amount} {base} в {quote} - {round(req, 4)}'
        bot.reply_to(message, txt)
    except (AmountNotDigits, ErrorCorrectData, ErrorCurrencyCodes, ErrorSameCurrency) as e:
        bot.reply_to(message, e)


bot.polling(none_stop=True)
