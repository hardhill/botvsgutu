from parameters import Parameters
from servbot import ServBot


class Application(object):
    def __init__(self):
        print('=====================================================================')
        print('             Timetable bot VSGUTU ver. 2.5                           ')
        print('=====================================================================')
    def Start(self):
        params = Parameters()
        serv = ServBot()
        error = serv.Start()
        if error == 0:
            erCount = 0
            while True and erCount<6:
                erCount+=1

                error = serv.LoadPage(params.url_bakal)
                if error == 0:
                    error = serv.Process("bakalavriat")
                if error == 0:
                    break
                error = serv.LoadPage(params.url_spec)
                if error == 0:
                    error = serv.Process("magistratura")
                if error == 0:
                    break
            print('Число ошибок',erCount-1)
        serv.Finish()


if __name__ == '__main__':
    app = Application()
    app.Start()