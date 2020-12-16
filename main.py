from Cars import * #импорт Cars.py в main.py


#main функция
def main():
    db = SQLClass("cars.db") #Создание (db) экземпляра класса SQLClass на основе базы данных созданной
    
    try:
        db.create_table()
    except:
        pass

    project = QApplication(sys.argv) #Создание приложения

    window = Greeting() #Создание первого GUI окна

    try:
        sys.exit(project.exec_())
    except:
        pass

if __name__ == '__main__':
    main() #вызов main()