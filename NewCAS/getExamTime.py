from .LoginCAS import Login
import requests


class GetTestTime(object):
    def __init__(self, member: Login):
        self.__url = 'http://222.31.49.139/jwglxt/kwgl/kscx_cxXsksxxIndex.html?doType=query&gnmkdm=N358105&su=' + str(
            member.getUserID())

        self.__result = requests.get(url=self.__url, cookies=member.getCookies()).text

    def getResult(self):
        return self.__result
