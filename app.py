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
            error = serv.LoadPage(params.url)
        if error == 1:
            error = serv.Process()

        serv.Finish()


if __name__ == '__main__':
    app = Application()
    app.Start()