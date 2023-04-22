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
