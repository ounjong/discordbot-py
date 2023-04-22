from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
load_dotenv()

import requests
import json
import re
import os
import time

class WAO:

    # 변수
    user = {}
    language = 'en'
    translation = {
        'en' : {
            'gameID' : 'Please input your User ID',
            'confirm' : 'Confirm',
            'change' : 'Switch Account',
            'level' : 'Castle Level',
            'kingdom' : 'Realm',
            'name' : 'User Name',
            'error1' : 'Server error!',
            'error3' : 'Parameter error!',
            'error5' : 'Result is null!',
            'error11' : 'This user couldn’t be found. Please input the accurate User ID.'
        },
        
        'ko_KR' : {
            'gameID' : '사용자 ID를 입력해 주십시오',
             'confirm' : '확인',
            'change' : '계정 변경',
            'level' : '성 레벨',
            'kingdom' : '왕국',
            'name' : '이름',
            'error1' : '서버 오류',
            'error3' : '변수 오류',
            'error5' : '결과 없음',
            'error11' : '이 사용자를 찾을 수 없었습니다. 정확한 사용자 ID를 입력해 주십시오.'
        }
    }; t = translation[language]

    # 검색
    def search(self, uid):
        self.uid = uid
        self.Initialization()
        return self.response()

    # 초기화
    def Initialization(self):
        url = 'https://pay-service.camelgames-wao.com/pay/gameInfo/getUserInfoById'
        headers = {'Content-type' : 'application/json; charset=utf-8'}
        data = {'uid' : str(self.uid), 'projectId' : 'wao_us'}
        self.post = requests.post(url, headers = headers, data = json.dumps(data))

    # 응답
    def response(self):
        result = self.post.text
        result = result.replace('{', '\r\n')
        result = result.replace('}', '\r\n')
        result = result.replace(',', '\r\n')
        result = result.replace('"', '')
        regex = re.compile('(.+?)\r\n')
        for i in regex.findall(result):
            a = self.change(i.split(':'))
            try:
                self.user[a[0]] = a[1]
            except:
                self.user[a[0]] = 'error'
        if self.user['success']:
            print('true')
            print(self.result())
            return True
        else:
            print('false')
            print(self.result())
            return False

    # 변경
    def change(self, data):
        match data[0]:
            case 'success' :
                if data[1] == "true":
                    data[1] = True
                else:
                    data[1] = False
            case 'data' :
                match data[1]:
                    case '服务器错误' :
                        data[1] = self.t['error1']
                    case '参数错误' :
                        data[1] = self.t['error3']
                    case '返回结果为空' :
                        data[1] = self.t['error5']
                    case '没有找到该用户，请重新输入正确的用户ID' :
                        data[1] = self.t['error11']
            case 'userInfo' :
                pass
            case 'server' :
                data[1] = int(data[1])
            case 'cus_icon' :
                data[1] = int(data[1])
            case 'city_lvl' :
                data[1] = int(data[1])
            case 'err' :
                data[1] = int(data[1])
            case 'channel' :
                pass
            case 'sys_icon' :
                if data[1] == '-1':
                    data[1] = 1
                elif data[1] == '0':
                    data[1] = 1
                else:
                    data[1] = int(data[1])
            case 'language' :
                pass
            case 'uid' :
                data[1] = int(data[1])
            case 'country_code' :
                pass
            case 'down_icon' :
                data[1] += ':' + data[2]
                del data[-1]
                pass
            case 'succ' :
                pass
            case 'name' :
                pass
            case 'action' :
                data[1] = int(data[1])
            case 'err_t' :
                data[1] = int(data[1])
            case 'paymentItemInfo' :
                pass
            case 'errorCode' :
                pass
        return data

    # 이미지
    def image(self):
        if self.user['cus_icon'] < 0:
            icon = 'images/' + str(self.user['sys_icon']) + '.png'
            return icon
        start = time.time()
        try:
            file = self.user['down_icon'] + str(self.user['cus_icon']) + '.jpg'
            icon = 'images/' + str(self.user['uid']) + '.jpg'
            os.system('curl ' + file + ' > ' + icon)
            print(time.time() - start)
            return icon
        except:
            icon = 'images/' + str(self.user['sys_icon']) + '.png'
            return icon

    # 결과
    def result(self):
        result = self.t['kingdom'] + ' : ', self.user['server']
        result += 'cus_icon :', self.user['cus_icon']
        result += self.t['level'] + ' : ', self.user['city_lvl']
        result += 'channel :', self.user['channel']
        result += 'sys_icon :', self.user['sys_icon']
        result += 'language :', self.user['language']
        result += 'uid :', self.user['uid']
        result += 'country_code :', self.user['country_code']
        result += 'down_icon :', self.user['down_icon']
        result += 'succ :', self.user['succ']
        result += self.t['name'] + ' : ', self.user['name']
        result += 'action :', self.user['action']
        return result

from googletrans import Translator

class Google_Translator:
    def __init__(self):
        self.translator = Translator()
        self.result = {'src_text': '', 'src_lang': '', 'tgt_text': '', 'tgt_lang': ''}
 
    def translate(self, text, lang='en'):
        translated = self.translator.translate(text, dest=lang)
        self.result['src_text'] = translated.origin
        self.result['src_lang'] = translated.src
        self.result['tgt_text'] = translated.text
        self.result['tgt_lang'] = translated.dest
 
        return self.result
 
    def translate_file(self, file_path, lang='en'):
        with open(file_path, 'r') as f:
            text = f.read()
        return self.translate(text, lang)


PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']

class MyClient(discord.Client):

    # 준비
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        status = discord.Status.online
        activity = discord.Game("WarAndOrder")
        await self.change_presence(status = status, activity = activity)
        print("준비 @1")

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
