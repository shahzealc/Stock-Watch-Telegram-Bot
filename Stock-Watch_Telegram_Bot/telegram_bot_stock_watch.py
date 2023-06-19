import os
from bs4 import BeautifulSoup
import requests
import re
import telebot

API_Key = "apikeywhichicantputhere"

bot = telebot.TeleBot(API_Key)

@bot.message_handler(commands=['start'])
def start(message):
  bot.reply_to(message,"Hey,this is Stock Watch\nTo Know the functionality just type /help")


@bot.message_handler(commands=['help'])
def help(message):
  bot.reply_to(message,"Here are some commands that you can use : \nTo know the price and detail of particular Stock just enter the name of Stock after /getprice\nTo know Top Gainer Stocks type /gainer \nTo know Top Loser Stocks type /loser \nTo know price and info of Cryptocurrencies type /crypto \nTo know price price of indian rupees type /currency")

  
# For stocks details
@bot.message_handler(commands=['getprice'])
def getprice(message):
  bot.reply_to(message,"Enter Stock name")
  @bot.message_handler(func=lambda m: True)
  def stock_price(message):
    
    try:
        weblink = "https://www.google.com/finance/quote/{0}"
        
        stock_weblink = weblink.format(message.text)
        
        html_text = requests.get(stock_weblink).text
        
        soup = BeautifulSoup(html_text,'html.parser')
        
        stock_ul = soup.find('ul',class_='sbnBtf xJvDsc ANokyb')
    
        
        # Getting the proper Stock Name here
        proper_name = stock_ul.a['href']
        stock_weblink_updated = weblink.format(proper_name[8::])

        html_text = requests.get(stock_weblink_updated).text

        soup = BeautifulSoup(html_text,'html.parser')

        # getting stock price here
        stock_price = soup.find('div',class_='YMlKec fxKbKc').text
        sp = "Stock Price : {}".format(stock_price)

            
        #getting stock's today's status
        stock_status_percentage = soup.find('div',class_="JwB6zf").text
        ssp = "Today Percentage : {}".format(stock_status_percentage)
        a = [sp,ssp]


        # getting stock's additional info.
        stock_detail_info = soup.find_all('div',class_="gyFHrc")
        i=0
        for  stock in stock_detail_info:
            stock_detail_name = stock.find('div',class_="mfs7Fc")
            stock_detail_value = stock.find('div',class_="P6K39c")
            a.append(stock_detail_name.text + " : " + stock_detail_value.text)
            i = i+1
            if(i==7):
                break

        str = ""
        for i in a:
            str += i
            str += "\n\n"
    except:
        str = " Please enter proper Stock name"

    bot.reply_to(message,str)

#for top gainers
@bot.message_handler(commands=['gainer'])
def gainer(message):  
  weblink_2 = "https://www.google.com/finance/markets/gainers"
  
  html_text_2 = requests.get(weblink_2).text
  
  soup_2 = BeautifulSoup(html_text_2,'html.parser')
  
  gainer_ul = soup_2.find("ul",class_="sbnBtf")
  
  gainer_li = gainer_ul.find_all('li')    
  sp = "Top Gainers are : "
  a = [sp]
  i=0
  for temp in gainer_li:
      gainer_name = temp.find('div',class_="ZvmM7").text
      gainer_price = temp.find('div',class_="YMlKec").text
      gainer_today_value = temp.find('span',class_="P2Luy Ez2Ioe").text
      gainer_today_percentage = temp.find('span',class_="NydbP nZQ6l").text
      a.append(gainer_name+"   "+gainer_price+"   "+gainer_today_value+"   "+gainer_today_percentage+"↑")
      i=i+1
      if i>10:
          break

  str = ""
  for i in a:
    str += i
    str += "\n\n"
  bot.reply_to(message,str)



# getting top losers

@bot.message_handler(commands=['loser'])
def loser(message):
  weblink_2 = "https://www.google.com/finance/markets/losers"
  
  html_text_2 = requests.get(weblink_2).text
  
  soup_2 = BeautifulSoup(html_text_2,'html.parser')
  
  loser_ul = soup_2.find("ul",class_="sbnBtf")
  
  loser_li = loser_ul.find_all('li')
  sp = "Top losers are : "
  a = [sp]
  i=0
  for temp in loser_li:
      loser_name = temp.find('div',class_="ZvmM7").text
      loser_price = temp.find('div',class_="YMlKec").text
      loser_today_value = temp.find('span',class_="P2Luy Ebnabc").text
      loser_today_percentage = temp.find('span',class_="NydbP VOXKNe").text
      a.append(loser_name+"   "+loser_price+"   "+loser_today_value+"   "+loser_today_percentage+"↓")
      i=i+1
      if i>10:
          break
  str = ""
  for i in a:
    str += i
    str += "\n\n"
  bot.reply_to(message,str)


# getting Cryptocurrencies

@bot.message_handler(commands=['crypto'])
def crypto(message):
  
  weblink_2 = "https://www.google.com/finance/markets/cryptocurrencies"
  
  html_text_2 = requests.get(weblink_2).text
  
  soup_2 = BeautifulSoup(html_text_2,'html.parser')
  
  crypto_ul = soup_2.find("ul",class_="sbnBtf")
  
  crypto_li = crypto_ul.find_all('li')  
  sp = "Crypto-Currencies are : "
  a = [sp]
  i=0
  for temp in crypto_li:
      crypto_name = temp.find('div',class_="ZvmM7").text
      crypto_price = temp.find('div',class_="YMlKec").text
      crypto_today_value = temp.find('div',class_="BAftM").text
      crypto_today_percentage = temp.find('div',class_="zWwE1").text
      a.append(crypto_name+"   "+crypto_price+"   "+crypto_today_value+"   "+crypto_today_percentage)
      i=i+1
      if i>10:
          break

  str = ""
  for i in a:
    str += i
    str += "\n\n"
    
  bot.reply_to(message,str)



# getting Currencies

@bot.message_handler(commands=['currency'])
def currency(message):
  
  weblink_2 = "https://www.google.com/finance/markets/currencies"
  
  html_text_2 = requests.get(weblink_2).text
  
  soup_2 = BeautifulSoup(html_text_2,'html.parser')
  
  currency_ul = soup_2.find("ul",class_="sbnBtf")
  
  currency_li = currency_ul.find_all('li')  
  sp = "Currencies in term of Indian Rupee are : "
  a = [sp]
  i=0
  for temp in currency_li:
      currency_name = temp.find('div',class_="ZvmM7").text
      currency_price = temp.find('div',class_="YMlKec").text
      currency_today_value = temp.find('div',class_="BAftM").text
      currency_today_percentage = temp.find('div',class_="zWwE1").text
      a.append(currency_name+"   "+currency_price+"   "+currency_today_value+"   "+currency_today_percentage)
      i=i+1
      if i>10:
          break

  str = ""
  for i in a:
    str += i
    str += "\n\n"
    
  bot.reply_to(message,str)


bot.polling()
