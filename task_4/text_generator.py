import random
import re

def generate_phone_numbers_file(file_path, number_of_lines):
    '''
    Генерирует также различные файлы внутри которых будет содержаться номера телефонов различные
    :param file_path:
    :param number_of_lines:
    :return:
    '''
    with open(file_path, 'w') as file:
        phone_pattern = re.compile(
            r'\b7(?:00|01|02|03|04|05|06|07|08|09|47|50|51|60|61|62|63|64|71|75|76|77|78)\s\d{3}\s\d{2}\s\d{2}\b'
        )

        for _ in range(number_of_lines):
            rand_value = random.choice([str(random.random()), '!', '@', '#', '$', '%', '^', '&', '*', '?'])
            phone_number = '7' + ''.join(random.choices('0123456789', k=2)) + ' '  + ''.join(random.choices('0123456789', k=3)) + ' '   + ''.join(random.choices('0123456789', k=3)) + ' '  + ''.join(random.choices('0123456789', k=2))

            line = f"This is random text: {rand_value}. Phone number: {phone_number}\n"
            file.write(line)
