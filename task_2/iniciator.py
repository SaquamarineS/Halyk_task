from task_2.pdf_reader import PdfReader

if __name__ == "__main__":
    # Относительный путь к файлу PDF внутри репозитория
    pdf_dir_path = 'pdf_files/'

    # Можете вставить свой pdf file и изменить название
    pdf_file_path = 'sample.pdf'

    # Относительный путь к директории для сохранения файла внутри репозитория
    output_directory = 'txt_files'

    # Создание экземпляра класса PdfReader
    pdf_reader = PdfReader(pdf_dir_path+pdf_file_path)


    #Выводит количество страниц в PDF-файле.
    num_pages = pdf_reader.get_number_of_pages()
    print(f"Количество страниц в PDF: {num_pages}")


    #Выводит текст с выбранной страницы PDF-файла.
    num_pages = pdf_reader.get_number_of_pages()  # последняя страница
    text_from_pages = pdf_reader.read_text_from_page(num_pages)
    print(f"Содержимое страницы {num_pages}:\n{text_from_pages}")


    #Сохраняет текст из всей книги в директорию txt_files
    pdf_reader.save_text_to_file(output_directory)



