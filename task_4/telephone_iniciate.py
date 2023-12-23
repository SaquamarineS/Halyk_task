from telephone_re import *
from text_generator import *

if __name__ == "__main__":
    # Сперва сгенерировал номера, после убрал в комментарий чтобы код смог пройтись по всем файлам и считать номера телефонов
    '''
    n = random.randint(10, 30)
    for i in range(n):
        file_path = f'phone_numbers_in_file/generated_file_{i}.txt'
        generate_phone_numbers_file(file_path, random.randint(10, 500))
        '''

    # Создаем БД содержащая таблицу phone_numbers которая содержит столбцы id, phone number
    create_db = Create_DB()
    create_db.create_table()
    create_db.close_connection()

    # Считываем из директории phone_numbers_in_file все текстовые файлы и записываем в наш БД
    phone_db = PhoneNumbersDatabase()
    directory_path = r'phone_numbers_in_file'
    phone_db.read_files_and_insert_numbers(directory_path)
    phone_db.close_connection()
