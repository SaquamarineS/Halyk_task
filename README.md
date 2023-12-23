# Halyk_task - Техническое задание

## 1. Развертывание среды Python

#### Требования:
- Установка Python на устройство через виртуальное окружение (venv), для GitHub (myenv).


#### Установка

- Клонируйте репозиторий:

```bash
git clone https://github.com/SaquamarineS/Halyk_task.git
cd Halyk_task
```
#### Создайте виртуальное окружение
```bash
python -m venv myenv
```
#### Активируйте виртуальное окружение
- Windovs
```bash
myenv\Scripts\activate 
```
или
- Unix/Mac
```bash
source myenv/bin/activate 
```

#### Установка всех библиотек для заданий через requirements.txt:
  
```bash
pip install -r requirements.txt
```

---

## 2. Чтение данных из PDF файла Python

#### Требования:
- Использование библиотеки PyPDF2 для чтения текста из PDF-файлов через Python.

Реализацию чтения данных совершил через библиотеку PyPDF2
Внутри директории можете вставить свой pdf файл для проверки, и также внутри кода iniciator.py вы можете поменять название файла в 8 строке

```
pdf_file_path = 'sample.pdf'
```

для запуска пропешите в терминале команду:

```bash
cd task_2
python iniciator.py
```

---

## 3. Мини-приложение на C#

#### Требования:
- Создание простого приложения на C# с вводом и выводом данных.


---

## 4. Парсинг текста на SQL

#### Требования:
- Написание скрипта для парсинга текста с целью извлечения номеров телефонов из текста.

Реализацию парсинга данных из текстового данных сделал через регулярные выражения а запись проводил на SQLite3 Казахстанских телефонных номеров операторов связи:

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
            
Взял за реализацию номера мобильной связи из Википедии

Для запуска пропишите команду в терминале:

```bash
cd task_6
python app.py
```



---

## 5. Распознавание наличия живой подписи на скан документах

#### Требования:
- Разработка метода для распознавания наличия подписи на сканах документов.


```bash
cd task_6
python app.py
```


---

## 6. Создание RESTful сервиса на Flask/Django

#### Требования:
- Разработка RESTful сервиса с методом для определения подписи на изображении через Flask.


```bash
cd task_6
python app.py
```


---
