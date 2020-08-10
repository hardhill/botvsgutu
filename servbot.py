import json
from datetime import datetime
import mysql.connector
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def _Errcode(codename):
    d = {'None': 0, 'Start': 1, 'LoadPage': 2, "Process": 3, "ProcessTable": 4, "DB":5}
    return d.get(codename)

def _NormalizeDate(param):
    dt = datetime.strptime(param, '%d.%m.%Y').strftime('%Y-%m-%d')
    return dt

def TL():
    return datetime.today().strftime('%H:%M:%S.%f')

class ServBot():
    def __init__(self):
        print(TL(), 'Инициализация сервиса')

    def Start(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs",{})

        try:
            self.driver = webdriver.Chrome(options=options)
            self.wait: WebDriverWait = WebDriverWait(self.driver, 15)
            self.driver.set_window_size(640,900)
            self.driver.set_window_position(1000,10,'current')
            print(TL(), 'Инициализация драйвера')
            return _Errcode("None")
        except Exception as err:
            print(TL(), '(E)Инициализация драйвера',err)
            return _Errcode("Start")

    def LoadPage(self, url):
        try:
            self.driver.get(url)
            self.wait.until(EC.presence_of_element_located((By.XPATH,'//table')))
            print(TL(), 'Открыл страницу', url)
            return _Errcode("None")
        except Exception as err:
            print(TL(), '(E)Открыл страницу', err)
            return _Errcode("LoadPage")

    def Finish(self):
        self.driver.close()
        self.driver.quit()
        print(TL(),'Работа завршена')

    @property
    def Process(self):
        print(TL(), 'Начинаю обработку страницы')
        data_text = self.driver.find_element_by_xpath("/html/body/p[1]").text.rsplit(None, 1)[-1],
        common_table = []
        rows_count = len(self.driver.find_elements_by_xpath('//tr'))-1
        arr_course = []
        el_courses = self.driver.find_elements_by_xpath('//tr[1]/td')
        for el in el_courses:
            arr_course.append(el.text)
        for id_col,course in enumerate(arr_course):
            arr_groups = []
            for id_row in range(rows_count):
                _col = id_col+1;  _row = id_row+2
                el_cell = self.driver.find_element_by_xpath('//tr['+str(_row)+']/td['+str(_col)+']/p/a')
                if el_cell.text != "":
                    arr_groups.append({"grname":el_cell.text,"url":el_cell.get_attribute('href')})
            course_table = {"course": course, "groups": arr_groups}
            common_table.append(course_table)
        print(common_table)
        #обработка всех груп
        for item_course in common_table:
            for item_group in item_course["groups"]:
                url = item_group["url"]
                try:
                    self.driver.get(url)
                    print(TL(),url)
                    self.wait.until(EC.presence_of_element_located((By.XPATH, '//table')))
                    el_table = self.driver.find_element_by_xpath('//table/tbody')
                    table = self._Tabletime(el_table)
                    item_group["table"] = table
                    item_group.pop("url")
                except Exception as err:
                    print(TL(), '(E)Ошибка обработки страниц расписаний', err)
                    return _Errcode("ProcessTable")


        print(common_table)
        print(TL(), 'Обработка страницы завершена')



        with open('timetable.json', 'w',encoding='utf8') as f:
            json.dump(common_table, f,ensure_ascii=False)
        try:
            self._SaveDB(data_text[0],common_table)
            return _Errcode('None')
        except:
            return _Errcode("DB")


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

    def _SaveDB(self,data_text, arr_table):
        try:
            ctx = mysql.connector.connect(user='host1608830_timet',
                                            password='Mer1daCX400',
                                            host='mysql16.hostland.ru',
                                            port='3306',
                                          database='host1608830_timet')
            SQL_CREATE = """
                CREATE TABLE IF NOT EXISTS `timetable` (`id` int(11) NOT NULL AUTO_INCREMENT,
                `datetable` date NOT NULL,`ttable` json NOT NULL, PRIMARY KEY (`id`)) 
                ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
            try:
                cursor = ctx.cursor()
                cursor.execute(SQL_CREATE)
                print(TL(),'Таблица готова')

                SQL_DELETE = "DELETE FROM timetable"
                cursor.execute(SQL_DELETE)
                ctx.commit()
                print(TL(), 'Удалены старые данные (если имелись)')
                try:
                        dt = _NormalizeDate(data_text)
                        tb = arr_table
                        SQL_INSERT = "INSERT INTO timetable (datetable,ttable) VALUES(DATE('"+\
                                     dt+"'),'"+json.dumps(tb,ensure_ascii=False)+"')"
                        cursor.execute(SQL_INSERT)
                        ctx.commit()
                except Exception as err:
                    print(TL(), '(E)Ошибка добавления данных', err)
            except Exception as err:
                print(TL(), '(E)Ошибка создания таблицы',err)
            finally:
                ctx.close()

        except Exception as err:
            print(TL(),'(E)Ошибка работы с БД',err.args)





