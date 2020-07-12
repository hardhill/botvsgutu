from os.path import exists


class Parameters():
    def __init__(self):
        params = {
            'url':'https://portal.esstu.ru/bakalavriat/raspisan.htm'
        }
        if exists('params.json'):
            fp = open('params.json','r')
            w = fp.readlines()
        self.url = params.get('url')
