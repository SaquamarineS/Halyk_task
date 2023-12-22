import os
import re
import sqlite3


class Create_DB:
    def __init__(self, db_name='phone_numbers.db'):
        """
        Конструктор класса Create_DB.

        Parameters:
        - db_name (str): Название базы данных. По умолчанию 'phone_numbers.db'.
        """
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        """
        Создает таблицу phone_numbers в базе данных.

        Если таблица уже существует, создание новой таблицы не выполняется.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS phone_numbers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT
            )
        ''')
        self.conn.commit()

    def close_connection(self):
        """
        Закрывает соединение с базой данных.
        """
        self.conn.close()


class PhoneNumbersDatabase:
    def __init__(self, db_name='phone_numbers.db'):
        """
        Конструктор класса PhoneNumbersDatabase.

        Parameters:
        - db_name (str): Название базы данных. По умолчанию 'phone_numbers.db'.
        """
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def read_files_and_insert_numbers(self, directory):
        """
        Считывает номера телефонов из файлов в указанной директории и вставляет их в базу данных.

        Parameters:
        - directory (str): Путь к директории с файлами, содержащими номера телефонов.

        7 — мобильная связь
            700 xxx xx xx — АЛТЕЛ
            701 xxx xx xx — AO «Kcell» (Kcell)
            702 xxx xx xx — AO «Kcell» (Kcell)
            703 xxx xx xx — резерв для сотовых операторов
            704 xxx xx xx — резерв для сотовых операторов
            705 xxx xx xx — ТОО «КаР-Тел» (Beeline)
            706 xxx xx xx — ТОО «КаР-Тел» (izi)
            707 xxx xx xx — ТОО «Мобайл Телеком-Сервис» (Tele2)
            708 xxx xx xx — АЛТЕЛ
            709 xxx xx xx — резерв для сотовых операторов
            747 xxx xx xx — ТОО «Мобайл Телеком-Сервис» (Tele2, FMOBILE)
            750 xxx xx xx — АО «Казахтелеком» (коммутируемый доступ)
            751 xxx xx xx — АО «Казахтелеком» (передача данных)
            760 xxx xx xx — АО «Казахтелеком» (Спутниковая сеть Кулан)
            761 xxx xx xx — АО «Казахтелеком»
            762 xxx xx xx — АО «NURSAT»
            763 xxx xx xx — АО «Арна»
            764 xxx xx xx — АО «2 Day Telecom»
            771 xxx xx xx — ТОО «КаР-Тел»[3] (Beeline)
            775 xxx xx xx — AO «Kcell» (Activ)
            776 xxx xx xx — ТОО «КаР-Тел» (Beeline)
            777 xxx xx xx — ТОО «КаР-Тел» (Beeline)
            778 xxx xx xx — AO «Kcell» (Activ)
        взял за реализацию номера мобильной связи из Википедии
        """

        # Регулярное выражение для извлечения номеров мобильной связи Казахстана
        # phone_pattern = re.compile(r'\b7[01234568]\d{2} \d{3} \d{2} \d{2}\b')   -  этот вариант может учитыввать и номера которые начинаются на 788.. и другие
        phone_pattern = phone_pattern = re.compile(
            r'\b7(?:00|01|02|03|04|05|06|07|08|09|47|50|51|60|61|62|63|64|71|75|76|77|78)\s\d{3}\s\d{2}\s\d{2}\b'
        )

        files = os.listdir(directory)

        for file_name in files:
            file_path = os.path.join(directory, file_name)

            with open(file_path, 'r') as file:
                content = file.read()
                phone_numbers = phone_pattern.findall(content)

                for phone_number in phone_numbers:
                    self.cursor.execute('INSERT INTO phone_numbers (phone_number) VALUES (?)', (phone_number,))

        self.conn.commit()

    def close_connection(self):
        """
        Закрывает соединение с базой данных.
        """
        self.conn.close()
