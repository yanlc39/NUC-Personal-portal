import requests
from OldCAS.LoginCAS import Login


class ExamTimeTable(object):
    def __init__(self, member: Login):

        self.__url = 'http://222.31.49.139/jwglxt/kwgl/kscx_cxXsksxxIndex.html?doType=query&gnmkdm=N358105&su' \
                     '={}'.format(member.getUserID())

        self.__resultDict = {
            'items': []
        }

        self.__header = {
                'Cookie': 'route=cedbb6d83382d4dc66cdc06735dd1eb8; JSESSIONID=28660AA2B69AF2EA7AC862D2AB97C493'
        }

        self.__result = requests.get(url=self.__url, headers=self.__header, timeout=2).text

        print(self.__url)
        print(self.__result)

    def __prossingInformation(self):
        for i in self.__result:
            if '不可查' not in i['kssj']:
                print(i['sjbh'] + ': ' + i['kssj'])
                tmpDict = {
                    'name': i['jxbmc'],
                    'time': i['kssj'],
                    'type': i['ksmc']
                }
                self.__resultDict['items'].append(tmpDict)

    def getDICT(self):
        return self.__resultDict
