import discord
from discord.ext import commands
from __main__ import send_cmd_help
from .utils import checks
import aiohttp
import requests
import re
import pandas as pd

try: # check if BeautifulSoup4 is installed
    from bs4 import BeautifulSoup
    soupAvailable = True
except:
    soupAvailable = False

class Test:
    """A test cog to practice the discord API and redBot wrapper"""
    
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def punch(self, lol : discord.Member): # call with [p]punch <discord.Member>
        """Incite violence with another user"""
        await self.bot.say("ONE PUNCH! And " + lol.mention + " is out! ლ(ಠ益ಠლ)")

    @commands.group(pass_context=True, no_pm=True) # @ = decorator
    async def defaults(self, ctx):
        """Example function calls"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
    
    @defaults.command(name="dotanow", pass_context=True, no_pm=True)
    @checks.mod_or_permissions(administrator=True) 
    async def _defaults_dotanow(self):
        """Scrape the number of players on DotA2 currently"""
        url = "https://steamdb.info/app/570/graphs/" # build the web address
        async with aiohttp.get(url) as response:
            soupObject = BeautifulSoup(await response.text(), "html.parser")
        try:
            online = soupObject.find(class_='steamspy-stats').find('li').find('strong').get_text()
            await self.bot.say(online + ' players are playing DotA2 at the moment')
        except:
            await self.bot.say("Couldn't load amount of players")
            
    @commands.command()
    @checks.serverowner_or_permissions(administrator=True)
    async def scrape(self):
        """ID"""

        ###########################################################
        # Populate a txt file with the HTML, requires some manual
        # processing to be done (like removing headers)
        ###########################################################
        # url = "https://mee6.xyz/levels/222841664585072641?limit=500"
        # r = requests.get(url)
        # # text = str(r.content, r.encoding)
        # with open('newfile.txt', 'wb') as f:
        #     f.write(r.content)

        ###########################################################
        # Create the Data
        # Needed cols: # userid , currentlvlxp, lvlxp, lvl, totalxp
        # To-do: Some users don't have image, can't fetch ids
        ###########################################################

        with open('newfile.txt', 'rb') as f:
            text = f.read()

        text = text.decode('utf-8')
        df = pd.DataFrame()

        user_pattern = r'<h3>(.+) <small>#(\d+)</small></h3>'
        some_list = re.findall(user_pattern, text)
        list1, list2 = zip(*some_list)
        df['username'] = list1
        df['discriminator'] = list2

        # id_pattern = r'avatars/(\d+)'
        # some_list = re.findall(id_pattern, text)
        # df['userid'] = pd.Series(some_list)

        # print(df)

        xp_pattern = r'<h5>(\d+) / (\d+) <strong>XP</strong> \[(\d+) total'                                                            
        some_list = re.findall(xp_pattern, text)
        list1, list2, list3 = zip(*some_list)
        df['currentlvlxp'] = list1
        df['lvlxp'] = list2
        df['totalxp'] = list3

        lvl_pattern = r'<h3>Level (\d+)'
        some_list = re.findall(lvl_pattern, text)
        df['lvl'] = some_list

        print(df)
        df.to_csv('data.csv', index=False, encoding='utf-8')


    #########################
    #   HELPER FUNCTIONS    #
    #########################

    async def messageListener(self, message):
        """Do something every time a message is (read) in the server/channel"""
        if message.author.bot is True:
            return

        await self.bot.send_message(message.channel, "poi")

            
def setup(bot):
    if soupAvailable:
        new_test = Test(bot)
        bot.add_cog(new_test)
        #bot.add_listener(new_test.messageListener, 'on_message')
    else:
        raise RuntimeError("You need to run 'pip3 install beautifulsoup4'")