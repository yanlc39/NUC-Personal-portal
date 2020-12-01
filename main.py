from OldCAS.LoginCAS import Login as Lg
from OldCAS.getExamTime import ExamTimeTable as ett
from NewCAS.LoginCAS import Login as nLg
from NewCAS.getExamTime import GetTestTime as gtt

if __name__ == '__main__':
    # 密码为 http://zhzb.nuc.edu.cn/cas/login 门户密码
    a = nLg('学号', '密码')
    print(gtt(a).getResult())

