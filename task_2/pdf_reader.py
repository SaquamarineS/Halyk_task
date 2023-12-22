import PyPDF2


class PdfReader:
    """Класс для чтения текста из PDF-файлов и сохранения его в текстовый файл."""

    def __init__(self, file_path):
        """
        Инициализация экземпляра класса PdfReader.

        Параметры:
        - file_path (str): Путь к PDF-файлу, из которого будет читаться текст.
        """
        self.file_path = file_path

    def get_number_of_pages(self):
        """
        Получение количества страниц в PDF-файле.

        Возвращает:
        - int: Количество страниц в PDF-файле.
        """
        try:
            with open(self.file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                return pdf_reader.numPages
        except FileNotFoundError:
            print("Файл не найден.")
            return 0

    def read_text_from_page(self, page_number):
        """
        Чтение текста из указанной страницы PDF-файла.

        Параметры:
        - page_number (int): Номер страницы для чтения текста (начиная с 1).

        Возвращает:
        - str: Текст, извлеченный с указанной страницы PDF-файла.
        """
        try:
            with open(self.file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                if 0 < page_number <= pdf_reader.numPages:
                    page = pdf_reader.getPage(page_number - 1)
                    return page.extractText()
                else:
                    print("Некорректный номер страницы.")
                    return ""
        except FileNotFoundError:
            print("Файл не найден.")
            return ""
        except PyPDF2.utils.PdfReadError:
            print("Ошибка при чтении PDF.")
            return ""

    def save_text_to_file(self, output_directory):
        """
        Сохранение текста из всей книги в текстовый файл.

        Параметры:
        - output_directory (str): Директория для сохранения текстового файла.
        """
        output_file = output_directory + '/output.txt'
        try:
            with open(self.file_path, 'rb') as pdf_file, open(output_file, 'w', encoding='utf-8') as output:
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                for page_number in range(pdf_reader.numPages):
                    page = pdf_reader.getPage(page_number)
                    text = page.extractText()

                    # Запись текста страницы в файл
                    output.write(f"Содержимое страницы {page_number + 1}:\n")
                    output.write(text)
                    output.write("\n\n")

                print(f"Текст из PDF сохранен в файл '{output_file}'")
        except FileNotFoundError:
            print("Файл не найден.")
        except PyPDF2.utils.PdfReadError:
            print("Ошибка при чтении PDF.")
