from bs4 import BeautifulSoup
import discord
import requests,webbrowser
from urllib import parse
from discord.ext import tasks

#Discord channel's id
DISC_CH = 906241457139109919;
#web page to scrape 
LINK = "https://www.di.univr.it/?ent=avviso"
#first part of the page to use for later manipulations
PRE_LINK = "https://www.di.univr.it"

#Creation of client obj
client = discord.Client()

#When the bot is ready
@client.event
async def on_ready():
  #Get channel in wich to write
  channel = client.get_channel(DISC_CH)
  #write on the channel, just to let you know is running
  await channel.send("Hello!")
  #call func send
  send.start()

#change "minutes" to change looping period
#i.e.: minutes = 60, means send is called every 60 minutes
@tasks.loop(minutes=3)
async def send():
  channel = client.get_channel(DISC_CH)
  #open file to the id of the last message sent
  fd = open("id.txt", "r+")
  #read last id
  max_id = int(fd.read())

  #SCRAPING
  response = requests.get(LINK)
  response.raise_for_status()
  soup = BeautifulSoup(response.text, 'html.parser')
  div_avvisi = soup.find('table', class_='table table-striped')
  a_avvisi = div_avvisi.find_all('a')
  
  #For every link found send a message to the channel
  for a_avviso in reversed(a_avvisi):
    link_avviso = str(a_avviso.get('href'))
    link_avviso = PRE_LINK + link_avviso
    parsed_url = parse.urlsplit(link_avviso)
    dic_ = dict(parse.parse_qsl(parsed_url.query))
    id_ = int( dic_["id"])
    if max_id < id_:
      await channel.send(str(link_avviso))
      max_id = id_

  #reset file pointer
  fd.seek(0)
  #write id on file
  fd.write(str(max_id))
  


client.run('OTA2MTg0OTQ3Njk2NTQ1ODIz.YYU8fw.gCnQEt-QjVRODa5WvlMRlkbgObk')