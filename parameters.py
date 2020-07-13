import json
from os.path import exists


class Parameters():
    def __init__(self):
        params = {
            'url':'https://portal.esstu.ru/bakalavriat/raspisan.htm'
        }
        if exists('params.json'):
            with open('params.json','r') as f:
                params = json.load(f)
        else:
            # сохранить параметры
            with open('params.json','w') as f:
                json.dump(params,f)
        self.url = params.get('url')

