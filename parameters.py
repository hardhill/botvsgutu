import json
from os.path import exists


class Parameters():
    def __init__(self):
        params = {
            'url':'https://portal.esstu.ru/bakalavriat/raspisan.htm'
        }
        if exists('params.json'):
            with open('params.json') as f:
                templates = json.load(f)
            params =json.load(templates)
        else:
            # сохранить параметры
            with open('params.json','w') as f:
                json.dump(params,f)
        self.url = params.get('url')

