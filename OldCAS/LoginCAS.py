import base64
import requests
from lxml import etree
import rsa
import time


class Login(object):
    def __init__(self, userID: str, password: str):
        self.__id = userID
        self.__pwd = password.encode()
        self.__csrfToken = None
        self.__rq = requests.Session()
        self.__result = None

        self.__baseURL = 'http://222.31.49.139/jwglxt/xtgl/login_slogin.html'
        self.__keyURL = 'http://222.31.49.139/jwglxt/xtgl/login_getPublicKey.html'
        self.__testURL = 'http://222.31.49.139/jwglxt/xtgl/index_cxBczjsygnmk.html'

        self.__csrfToken = self.__getCSRFTOKEN(1)

        self.__cookies = self.__loginCAS()

    def __getCSRFTOKEN(self, num: int):
        while True:
            print(str(num) + '次重试中...')
            num += 1
            self.__result = self.__rq.get(url=self.__baseURL)
            result = etree.HTML(self.__result.text).xpath(
                '/html/body/div[1]/div[2]/div[2]/form/input/@value')
            try:
                return result[0]
            except:
                print('连接失败!5s后重试...')
                time.sleep(5)
                self.__rq = requests.Session()
                self.__getCSRFTOKEN(num)

    def __loginCAS(self):
        tmpCookies = self.__result.cookies.get_dict()
        pbk = self.__getPublicKey(tmpCookies)
        print(self.__rq.cookies.get_dict())
        print(pbk)
        self.__pwd = base64.b64encode(rsa.encrypt(self.__pwd, self.__getEncodePWD(pbk['modulus'], pbk['exponent']))).decode()
        self.__data = {
            'csrftoken': self.__csrfToken,
            'yhm': self.__id,
            'mm': self.__pwd,
        }
        self.__loginResult = self.__rq.post(url=self.__baseURL, data=self.__data, cookies=tmpCookies)

        tmpCookies['JSESSIONID'] = self.__loginResult.cookies.get('JSESSIONID')

        self.__loginResult = self.__rq.get(url=self.__testURL, cookies=tmpCookies)

        print(self.__loginResult.text)

        if '密码' in self.__loginResult.text:
            print("Bad Connection")
        else:
            print("Good Connection")
            print(self.__loginResult.text)
        print(self.__data)
        return self.__loginResult.cookies

    def __getEncodePWD(self, modulus: str, exponent: str) -> int:
        return rsa.PublicKey(int.from_bytes(base64.b64decode(modulus), 'big'), int.from_bytes(base64.b64decode(exponent), 'big'))

    def __getPublicKey(self, cookies: str):
        return self.__rq.get(url=self.__keyURL).json()

    def getCookies(self):
        return '; '.join([item.name + '=' + item.value for item in self.__cookies])

    def getUserID(self):
        return self.__id
