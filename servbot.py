import json
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def _Errcode(codename):
    d = {'None': 1, 'Start': 2, 'LoadPage': 3, "Process": 4, "ProcessTable": 5}
    return d.get(codename)




class ServBot():
    def __init__(self):
        print(self._TL(), 'Инициализация сервиса')
    def _TL(self):
        return datetime.today().strftime('%H:%M:%S.%f')
    def Start(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs",{})

        try:
            self.driver = webdriver.Chrome(options=options)
            self.wait: WebDriverWait = WebDriverWait(self.driver, 15)
            self.driver.set_window_size(640,1000)
            self.driver.set_window_position(1000,10,'current')
            print(self._TL(), 'Инициализация драйвера')
            return _Errcode("None")
        except Exception as err:
            print(self._TL(), '(E)Инициализация драйвера',err)
            return _Errcode("Start")

    def LoadPage(self, url):
        try:
            self.driver.get(url)
            self.wait.until(EC.presence_of_element_located((By.XPATH,'//table')))
            print(self._TL(), 'Открыл страницу', url)
            return _Errcode("None")
        except Exception as err:
            print(self._TL(), '(E)Открыл страницу', err)
            return _Errcode("LoadPage")

    def Finish(self):
        self.driver.close()
        self.driver.quit()
        print(self._TL(),'Работа завршена')

    def Process(self):
        elements = self.driver.find_elements_by_xpath('//a')
        list_a = []
        print(self._TL(),'Начинаю обработку страницы')
        for el_anchor in elements:
            el =el_anchor.find_element_by_tag_name('font')
            if el.text!='':
                list_a.append(el_anchor.get_attribute('href'))

        print(list_a)
        print(self._TL(), 'Обработка страницы завершена')
        #массив расписаний
        arr_tables = []
        for item in list_a:
            try:
                self.driver.get(item)
                print(self._TL(),item)
                self.wait.until(EC.presence_of_element_located((By.XPATH,'//table')))
                el_p1 = self.driver.find_element(By.XPATH,"//p[contains(text(),'Расписание обновлено')]")
                el_p2 = self.driver.find_element(By.XPATH,'/html[1]/body[1]/p[2]/font[2]')
                el_table = self.driver.find_element_by_xpath('//table/tbody')
                table = self._Tabletime(el_table)
                tabletime = {
                    'group':el_p2.text.strip(),
                    'date':el_p1.text.rsplit(None, 1)[-1],
                    'table': table
                }
                arr_tables.append(tabletime)
            except Exception as err:
                print(self._TL(),'(E)Ошибка обработки страниц расписаний',err)
                return _Errcode("ProcessTable")
            finally:
                pass
        print(arr_tables)
        with open('timetable.json', 'w') as f:
            json.dump(arr_tables, f,ensure_ascii=True)


        return _Errcode('None')

    def _Tabletime(self,inptable):
        self.table = {
            'week1': {
                'mon': [
                    inptable.find_element_by_xpath('//tr[3]//td[2]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[3]//td[3]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[3]//td[4]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[3]//td[5]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[3]//td[6]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[3]//td[7]//p[1]//font[1]').text,
                ],
                'tue': [
                    inptable.find_element_by_xpath('//tr[4]//td[2]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[4]//td[3]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[4]//td[4]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[4]//td[5]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[4]//td[6]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[4]//td[7]//p[1]//font[1]').text,
                ],
                'wed': [
                    inptable.find_element_by_xpath('//tr[5]//td[2]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[5]//td[3]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[5]//td[4]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[5]//td[5]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[5]//td[6]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[5]//td[7]//p[1]//font[1]').text,
                ],
                'thu': [
                    inptable.find_element_by_xpath('//tr[6]//td[2]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[6]//td[3]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[6]//td[4]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[6]//td[5]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[6]//td[6]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[6]//td[7]//p[1]//font[1]').text,
                ],
                'fri': [
                    inptable.find_element_by_xpath('//tr[7]//td[2]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[7]//td[3]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[7]//td[4]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[7]//td[5]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[7]//td[6]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[7]//td[7]//p[1]//font[1]').text,
                ],
                'sat': [
                    inptable.find_element_by_xpath('//tr[8]//td[2]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[8]//td[3]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[8]//td[4]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[8]//td[5]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[8]//td[6]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[8]//td[7]//p[1]//font[1]').text,
                ],
                'sun': []
            },
            'week2': {
                'mon': [
                    inptable.find_element_by_xpath('//tr[9]//td[2]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[9]//td[3]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[9]//td[4]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[9]//td[5]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[9]//td[6]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[9]//td[7]//p[1]//font[1]').text,
                ],
                'tue': [
                    inptable.find_element_by_xpath('//tr[10]//td[2]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[10]//td[3]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[10]//td[4]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[10]//td[5]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[10]//td[6]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[10]//td[7]//p[1]//font[1]').text,
                ],
                'wed': [
                    inptable.find_element_by_xpath('//tr[11]//td[2]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[11]//td[3]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[11]//td[4]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[11]//td[5]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[11]//td[6]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[11]//td[7]//p[1]//font[1]').text,
                ],
                'thu': [
                    inptable.find_element_by_xpath('//tr[12]//td[2]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[12]//td[3]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[12]//td[4]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[12]//td[5]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[12]//td[6]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[12]//td[7]//p[1]//font[1]').text,
                ],
                'fri': [
                    inptable.find_element_by_xpath('//tr[7]//td[2]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[7]//td[3]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[7]//td[4]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[7]//td[5]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[7]//td[6]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[7]//td[7]//p[1]//font[1]').text,
                ],
                'sat': [
                    inptable.find_element_by_xpath('//tr[8]//td[2]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[8]//td[3]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[8]//td[4]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[8]//td[5]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[8]//td[6]//p[1]//font[1]').text,
                    inptable.find_element_by_xpath('//tr[8]//td[7]//p[1]//font[1]').text,
                ],
                'sun': []
            }
        }
        return self.table



