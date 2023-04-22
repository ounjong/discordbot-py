from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
load_dotenv()

from WAO import WAO
from translator import Google_Translator

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']

class MyClient(discord.Client):

    # 준비
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        status = discord.Status.online
        activity = discord.Game("WarAndOrder")
        await self.change_presence(status = status, activity = activity)

    # 메시지
    async def on_message(self, message):
        print(message)
        if message.author == self.user:
            return
        if message.content.startswith('/search'):
            a = message.content.split(' ')
            wao = WAO()
            if wao.search(a[1]):
                image = discord.File(wao.image(), filename = 'image.png')
                translator = Google_Translator()
                result = translator.translate(wao.t['level'], "en")
                wao.t['level'] = result['tgt_text']
                result = translator.translate(wao.t['kingdom'], "en")
                wao.t['kingdom'] = result['tgt_text']
                title = wao.user['name']
                description = wao.t['level'] + ' : {}\r\n'.format(wao.user['city_lvl'])
                description += wao.t['kingdom'] + ' : {}'.format(wao.user['server'])
                embed = discord.Embed(title = title, description = description)
                embed.set_thumbnail(url = 'attachment://image.png')
                await message.channel.send(embed = embed, file = image)
            else:
                await message.channel.send('{}'.format(wao.t['error11']))
            return
        if message.content.startswith('/검색'):
            a = message.content.split(' ')
            wao = WAO()
            if wao.search(a[1]):
                image = discord.File(wao.image(), filename = 'image.png')
                translator = Google_Translator()
                result = translator.translate(wao.t['level'], "ko")
                wao.t['level'] = result['tgt_text']
                result = translator.translate(wao.t['kingdom'], "ko")
                wao.t['kingdom'] = result['tgt_text']
                title = wao.user['name']
                description = wao.t['level'] + ' : {}\r\n'.format(wao.user['city_lvl'])
                description += wao.t['kingdom'] + ' : {}'.format(wao.user['server'])
                embed = discord.Embed(title = title, description = description)
                embed.set_thumbnail(url = 'attachment://image.png')
                await message.channel.send(embed = embed, file = image)
            else:
                await message.channel.send('{}'.format(wao.t['error11']))

            return
        if message.content.startswith('/s'):
            a = message.content.split(' ')
            wao = WAO()
            if a[2] == '':
                a[2] = 'en'
            if wao.search(a[1]):
                print("통과")
                image = discord.File(wao.image(), filename = 'image.png')
                translator = Google_Translator()
                try:
                    result = translator.translate(wao.t['level'], a[2])
                    wao.t['level'] = result['tgt_text']
                    result = translator.translate(wao.t['kingdom'], a[2])
                    wao.t['kingdom'] = result['tgt_text']
                except:
                    result = translator.translate(wao.t['level'], 'en')
                    wao.t['level'] = result['tgt_text']
                    result = translator.translate(wao.t['kingdom'], 'en')
                    wao.t['kingdom'] = result['tgt_text']
                title = wao.user['name']
                description = wao.t['level'] + ' : {}\r\n'.format(wao.user['city_lvl'])
                description += wao.t['kingdom'] + ' : {}'.format(wao.user['server'])
                embed = discord.Embed(title = title, description = description)
                embed.set_thumbnail(url = 'attachment://image.png')
                await message.channel.send(embed = embed, file = image)
            else:
                await message.channel.send('{}'.format(wao.t['error11']))
            return

    # 메시지 삭제
    async def on_message_delete(self, message):
        if message.author == self.user:
            return
        message.channel.id = 1096771452142878850
        await message.channel.send('message delete (' + str(message.author) + '): ' + message.content)
        return

    # 가입
    async def on_member_join(self, member):
        if message.author == self.user:
            return
        await member.guild.get_channel(1096759823900606484).send(member.mention + ' join!')

    # 유저 갱신
    async def on_user_update(self, before, after):
        if message.author == self.user:
            return
        await member.guild.get_channel(1096759823900606484).send('user update : ' + before + " | " + after)
        return

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(command_prefix = '/', intents = intents)
client.run(TOKEN)
