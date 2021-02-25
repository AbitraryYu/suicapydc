import discord
from discord.ext import commands
from datetime import timedelta
import asyncio
import config


class messageHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.keywords = []
        self.response = {}
        self.portal_id = int(config.getPortal())  # load the portal id from config
        # read the keyword pairs from file
        try:
            with open('keywords.txt', 'r') as data:
                for line in data:
                    (kw, resp) = line.split(':', 1)
                    self.response[kw] = str(resp)
                for (kw, resp) in self.response.items():
                    self.keywords.append(kw)
            data.close()
        except IOError:
            print('keyword file does not exist!')

    @commands.Cog.listener()
    async def on_message(self, message):
        # Keyword respond function###
        if message.content in self.keywords:
            if message.author == self.bot.user:
                return
            else:
                # print('keyword hit')
                msg = self.response[message.content]
                await message.channel.send(msg)
        '''
        if '呼哈' in message.content and message.author != self.bot.user:
            time = message.created_at + timedelta(hours=1)
            msg = '你的下一次呼哈：{:%H:%M:%S}'.format(time)
            await message.channel.send(msg)
        '''
    # portal talking function
        if message.channel.id == self.portal_id:
            await self.bot.get_channel(self.messagedest).send(message.content)

    @classmethod
    def set_destination(self, channel_id):
        self.messagedest = channel_id

    @classmethod
    def get_destination(self):
        return self.messagedest


def setup(bot):
    bot.add_cog(messageHandler(bot))
    print("Message handler loaded.")
