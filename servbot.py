from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def _Errcode(codename):
    d = {'None': 1, 'Start': 2, 'LoadPage': 3, "Process": 4, "NotSelect": 5}
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
        for item in list_a:
            self.driver.get(item)
            self.wait.until(EC.presence_of_element_located((By.XPATH,'//table')))
            el_p1 = self.driver.find_element(By.XPATH,"//p[contains(text(),'Расписание обновлено')]")
            print(el_p1.text)
            el_p2 = self.driver.find_element(By.XPATH,'//p[2]')
            print(el_p2.text)
            el_table_rows = self.driver.find_elements_by_xpath('//table/tbody/tr')
            for row in el_table_rows:
                pass
        return _Errcode('None')

