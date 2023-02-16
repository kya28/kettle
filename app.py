import os
import time
from datetime import datetime
import sqlite3
from dotenv import load_dotenv

# подключение к бд
try:
    con = sqlite3.connect('sqlite.db')
    cursor = con.cursor()
    cursor.close()
except sqlite3.Error as error:
    print('Error connection sqlite', error)


# функция добавления в бд аргументов
def db_insert(state, amount_of_water, temperature):
    con = sqlite3.connect('sqlite.db')
    cursor = con.cursor()
    cursor.execute("INSERT INTO kettle (state, amount_of_water, temperature) VALUES ( ?, ?, ?)",
                   [state, amount_of_water, temperature])
    con.commit()
    cursor.close()


# класс Чайник
class Kettle:
    def __init__(self, amount_of_water):
        self.amount_of_water = amount_of_water # количество залитой воды в чайнике
        self.date = datetime.now().time() # текущая дата со временем (начальная)
        self.state = 'Kettle off' # текущее состояние чайника
        self.temperature = 0 # (начальная температура воды в чайнике)

    def working(self, num_of_secs, temp): # функция работы чайника
        db_insert(self.state, self.amount_of_water, self.temperature) # добавляем начальное состояние чайника в бд
        try:
            while num_of_secs: # пока есть время
                if self.temperature < temp: # если текущая температура меньше температуры, до которой нужно кипятить чайник
                    self.temperature = self.temperature + 10 # тогда температуру увеличиваем
                    time.sleep(1) # ждем секунду
                    num_of_secs -= 1 # вычитаем одну секунду из основного времени
                    db_insert('Working', self.amount_of_water, self.temperature)  # добавляем текущее состояние чайника в бд
                    print(
                        str(self.temperature) + ' ' + str(datetime.now().time()) +
                        ' ' + 'Working' + ' ' + str(self.amount_of_water)) # выводим текущее состояние чайника на консоль
                else:
                    break # не удовлетворяет условию, то не продолжаем
        except:
            db_insert('Stop', self.amount_of_water, self.temperature) # если нажали на кнопку выключения, то сохраняем сотояние в бд
        db_insert('Boiled', self.amount_of_water, self.temperature) # если чайник проработал до конца, то он вскипитился, значит записываем состояние в бд


load_dotenv() # загружаем конфигуративный файл
vertek = Kettle(int(os.getenv('AMOUNT_OF_WATER')))  # создаем класс vertek
vertek.working(int(os.getenv('TIME_WORKING')), int(os.getenv('TEMP_OFF'))) # вызываем функцию включить кнопку с параметрами время работы чайника и до какой температуры греть
