import telebot, bs4, requests, random
from telebot import formatting

bot = telebot.TeleBot('Token') #Your bot token

@bot.message_handler(commands=['start'])
def welcome_message(message):
    bot.send_message(message.chat.id, 'Welcome to the random quote bot.\ntype /quote to get a random quote.')

@bot.message_handler(commands=['quote'])
def random_quote(message):
    page = requests.get('https://www.quotationspage.com/random.php')
    soup = bs4.BeautifulSoup(page.text, 'html.parser')

    quotes = [str(i)[str(i).find('>')+1:-4] for i in soup.find_all('a', attrs={'title': 'Click for further information about this quotation'})]

    authors = list()

    for j in soup.find_all('b'):
        author = str(j).split('>')[2][:-3]
        if str(j) != '</b':
            author += str(j).split('>')[-2][:-3]
        authors.append(author)
    rand = random.randint(0,len(quotes)-1)

    quote = formatting.hbold(f'"{quotes[rand]}"')

    name = formatting.hitalic(f'\n\t\t-{authors[rand]}')

    bot.send_message(message.chat.id, quote+name, parse_mode='HTML')

bot.infinity_polling()