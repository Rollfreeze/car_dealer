import sys
#импорты для Дизайера
from PyQt5.QtWidgets import * 
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic
#импорт для сервера БД
import sqlite3 


class Admission(QMainWindow): #Одна из многочисленных форм
    def __init__(self): #Конструктор класса
        super(Admission, self).__init__() #Наследует конструктор от родительского класса

        loadUi('Admission.ui', self) #Прогружается форма из файла, который создается в QT Designer

        self.cancel_button.clicked.connect(self.cancel) # привязывается метод к конкретной кнопке. Self -> аналог указателя this из С++.
        #cancel_button -> название кнопки из QT Designer

        self.show() #Метод открытия формы, который вызывается автоматически во время создания экземпляра класса

    def cancel(self): #Методы класса. Этот метод отвечает за закрывание формы
        self.close() 

class Zero(QMainWindow):
    def __init__(self):
        super(Zero, self).__init__()

        loadUi('zero.ui', self)

        self.cancel_button.clicked.connect(self.cancel)

        self.show()

    def cancel(self):
        self.close()

class Mistake_deleting(QMainWindow):
    def __init__(self):
        super(Mistake_deleting, self).__init__()

        loadUi('mistake_deleting.ui', self)

        self.cancel_button.clicked.connect(self.cancel)

        self.show()

    def cancel(self):
        self.close()

class Mistake_input(QMainWindow):
    def __init__(self):
        super(Mistake_input, self).__init__()

        loadUi('mistake.ui', self)

        self.cancel_button.clicked.connect(self.cancel)

        self.show()

    def cancel(self):
        self.close()

class Addition(QMainWindow):
    def __init__(self):
        super(Addition, self).__init__()

        loadUi('Adding.ui', self)

        self.cancel_button.clicked.connect(self.close_self)

        self.add_button.clicked.connect(self.adding_data)

        self.show()
    
    def close_self(self):
        self.close()

    #Считываешь поля из формы "добавить" и заносишь их в бд, если ввод корректный, иначе окно об ошибке
    #Сценарии предусмотрены
    def adding_data(self, query):
        try:            
            creator = self.comboBox_creator.currentText()

            country = self.comboBox_country.currentText()

            korobka = self.comboBox_korobka.currentText()

            mark = str(self.lineEdit_mark.text())

            year = int(self.lineEdit_year.text())

            v = int(self.lineEdit_v.text())

            probeg = int(self.lineEdit_probeg.text())

            price = int(self.lineEdit_price.text())

            my_bool = True
        except:
            self.mistake_window = Mistake_input()

            self.mistake_window.show() #иначе вызывается окно об ошибке

            my_bool = False

        if (my_bool == True):

            db = SQLClass("cars.db")

            #Занесение в базу данных

            db.edition("""INSERT INTO cars (Производитель, Марка, Страна, Год, Объем, Коробка, Пробег, Цена) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}') """.format(creator, mark, country, year, v, korobka, probeg, price))

            MyCars = CarsTable(True)
            
            MyCars.Data_clear()
            
            MyCars.Data_show()
        else:
            pass
        
        self.close()

#класс помощник, который помогает взаимодействовать с БД SQLite
class SQLClass:
    def __init__ (self, name=None):
        self.conn = None
        self.cursor = None #поля, они же Атрибуты
        if name:
            self.open(name)
        
    def open(self, name): #метод для открытия существующей БД
        try:
            self.conn = sqlite3.connect(name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e: #Ошибка, если БД не найдена
            print("No connection")

    def create_table(self): #Метод создания БД
        curs = self.cursor 

        #Язык SQLite -> создание ТАБЛИЦЫ И СОЗДАНИЕ ЕЕ СТОЛБЦОВ
        create_request = str("""CREATE TABLE cars(id INTEGER PRIMARY KEY AUTOINCREMENT, Производитель TEXT NOT NULL, Марка TEXT NOT NULL, Страна TEXT NOT NULL, Год выпуска INTEGER, Объем двигателя INTEGER, Коробка передач TEXT NOT NULL, Пробег INTEGER, Цена INTEGER)""")

        curs.execute(create_request) #вызов метода, который выполняет запрос составленный и отсылает на сервер БД

    def edition(self,query):
        curs = self.cursor

        curs.execute(query)

        self.conn.commit()

    def selection(self,query):
        curs = self.cursor

        curs.execute(query)

        return curs.fetchall()

#Класс начальной формы
class Greeting(QMainWindow):
    def __init__(self):
        super(Greeting, self).__init__()

        loadUi('Greeting_form.ui', self) #Прогрузка формы

        #Какой функционал к какой кнопке
        self.admin_button.clicked.connect(self.cars_table_open_admin)

        self.user_button.clicked.connect(self.cars_table_open_user)

        self.cancel_button.clicked.connect(self.close_self)

        self.show() 

    def cars_table_open_user(self):
        self.cars_table = CarsTable(False)

        self.close()

        self.cars_table.show()
    
    def cars_table_open_admin(self):
        self.cars_table = CarsTable(True)

        self.close()

        self.cars_table.show()

    def close_self(self):
        self.close()

#Создает вторую форму, в которой мы работаем и видим таблицу, подгруженную из базы данных
class CarsTable(QMainWindow):
    def __init__(self, admin):
        super(CarsTable, self).__init__()
        loadUi('Cars_table.ui', self)

        self.admin = admin

        self.my_request = "SELECT * FROM cars"

        self.tableWidget.setColumnWidth(0,40) #Задаешь размер ширины конкретного столбца

        self.tableWidget.setColumnWidth(4,100)

        self.tableWidget.setColumnWidth(5,150)

        self.tableWidget.setColumnWidth(6,150)

        self.add_button.clicked.connect(self.adding_open)

        self.cancel_button.clicked.connect(self.close_self)

        self.reload_button.clicked.connect(self.Data_show)

        self.creator_button.clicked.connect(self.creater)

        self.country_button.clicked.connect(self.country)

        self.probeg_button.clicked.connect(self.probeg)
        
        self.year_button.clicked.connect(self.year)

        self.delete_button.clicked.connect(self.deleting)

        self.show()
    
    def adding_open(self):
        if (self.admin == True):
            self.addition = Addition()

            self.addition.show()
        else:
            self.access = Admission()

            self.access.show()
    
    def close_self(self):
        self.close()

    def deleting(self): #Метод удаления из БД и соотвественно таблицы
        if (self.admin == True):
            try:
                dele = str(self.lineEdit.text())

                sql = SQLClass("cars.db")

                sql.edition("DELETE FROM cars WHERE id ="+dele) #Создается запрос, в котором ты просишь БД удалить id с введенным номером

                self.Data_show()
            except:
                self.mistake_delete = Mistake_deleting()

                self.mistake_delete.show()
        else:
            self.access = Admission()

            self.access.show()

    def Data_clear(self): #Метод очистки -> Метод для обновления таблицы
        i= self.tableWidget.rowCount()
        while(self.tableWidget.rowCount()>0):
            self.tableWidget.removeRow(i)
            i = i - 1

    def Data_show(self): #Метод для того, чтобы прогрузить столбцы базы данных в table widget главной формы
        self.Data_clear()

        helper = SQLClass("cars.db")
        movies = helper.selection("SELECT * FROM cars")

        for row_number,movies in enumerate(movies):
            self.tableWidget.insertRow(row_number)
            for column_number,data in enumerate(movies):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.tableWidget.setItem(row_number,column_number,cell)

    def creater(self): #Сортировка по создателю
        cars_req = str(self.comboBox_creator.currentText())
        self.Data_clear()

        helper = SQLClass("cars.db")
        movies = helper.selection("""SELECT * FROM cars WHERE Производитель='{}'""".format(cars_req)) #Запрос в БД по создателю

        for row_number,movies in enumerate(movies):
            self.tableWidget.insertRow(row_number)
            for column_number,data in enumerate(movies):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.tableWidget.setItem(row_number,column_number,cell)
    
    def country(self):
        cars_req = str(self.comboBox_country.currentText())
        self.Data_clear()

        helper = SQLClass("cars.db")
        movies = helper.selection("""SELECT * FROM cars WHERE Страна='{}'""".format(cars_req)) #По стране

        for row_number,movies in enumerate(movies):
            self.tableWidget.insertRow(row_number)
            for column_number,data in enumerate(movies):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.tableWidget.setItem(row_number,column_number,cell)

    def probeg(self):
        cars_req = str(self.lineEdit_probeg.text())
        self.Data_clear()

        helper = SQLClass("cars.db")
        movies = helper.selection("""SELECT * FROM cars WHERE Пробег='{}'""".format(cars_req)) #Пробег

        for row_number,movies in enumerate(movies):
            self.tableWidget.insertRow(row_number)
            for column_number,data in enumerate(movies):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.tableWidget.setItem(row_number,column_number,cell)

    def year(self):
        cars_req = str(self.lineEdit_year.text())
        self.Data_clear()

        helper = SQLClass("cars.db")
        movies = helper.selection("""SELECT * FROM cars WHERE Год='{}'""".format(cars_req))  #По году

        for row_number,movies in enumerate(movies):
            self.tableWidget.insertRow(row_number)
            for column_number,data in enumerate(movies):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.tableWidget.setItem(row_number,column_number,cell)