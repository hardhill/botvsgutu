from parameters import Parameters
from servbot import ServBot


class Application(object):
    def __init__(self):
        print('=====================================================================')
        print('             Timetable bot VSGUTU ver. 1.0                           ')
        print('=====================================================================')
    def Start(self):
        params = Parameters()
        serv = ServBot()
        error = serv.Start()
        if error == 1:
            erCount = 0
            while True and erCount<6:
                erCount+=1
                error = serv.LoadPage(params.url)
                if error == 1:
                    error = serv.Process()
                if error == 1:
                    break
            print('Число ошибок',erCount)
        serv.Finish()


if __name__ == '__main__':
    app = Application()
    app.Start()