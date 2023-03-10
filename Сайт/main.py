import pyttsx3  # модуль для озвучки текса (используя голоса операционной системы)
import pdfplumber  # модуль для чтения pdf файлов
from multiprocessing import Process  # модуль для создания отдельных процессов
from pathlib import Path  # модуль для работы с путями в файловой системе
import os  # модуль для взаимодействия с операционной системой
import docx2txt  # модуль для чтения docx файла
import langid  # модуль для определения языка


def pdf_to_audio(file_path='/'):  # Функция для запуска конвертора в отдельном процессе
    p = Process(target=pdf_to_audio_processor(file_path))  # инициализация процесса
    p.start()  # запуск процесса
    p.join()  # завершение процесса


def pdf_to_audio_processor(file_path='./'):  # конвертор
    if Path(file_path).is_file() and Path(file_path).suffix == '.pdf':  # проверка на pdf файл
        print(f'[!] {Path(file_path).stem} is processing...')  # маркер начала конвертации
        with pdfplumber.PDF(open(file=file_path, mode='rb')) as pdf:  # чтение файла
            pages = [pages.extract_text() for pages in pdf.pages]  # переносим все в одну строку
        doc_text = ''.join(pages).replace('\n', '')
        print(doc_text)  # вывод строки
        lang = langid.classify(doc_text)  # определение языка текста
        audio = pyttsx3.init()  # инициализация чтения
        print(lang)  # вывод языка

        ru = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0'  # читалка на русском
        en = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'  # читалка на англ

        if lang[0] == 'en':  # проверка языка текста
            audio.setProperty('voice', en)  # используем соответствующий язык читалки
        if lang[0] == 'ru':
            audio.setProperty('voice', ru)
        file_name = Path(file_path).stem  # получаем название файла
        audio.save_to_file(doc_text, f'files/{file_name}.mp3')  # указываем куда сохранить данные
        audio.runAndWait()  # запускаем читалку
        os.remove(file_path)  # удаляем исходный файл
        return print(f'[+] {file_name} has been converted to audio!')  # маркер готовности файла

    elif Path(file_path).is_file() and Path(file_path).suffix == '.docx':  # проверка на docx файл
        print(f'[!] {Path(file_path).stem} is processing...')  # маркер начала конвертации
        doc_text = str(docx2txt.process(file_path)).replace('\n', '')  # переносим все в одну строку
        print(doc_text)  # выводим текст
        lang = langid.classify(doc_text)  # определяем язык текста
        audio = pyttsx3.init()  # инициализируем читалку
        audio.setProperty('voice', f'{lang[0]}')  # устанавливаем соответствующий язык
        file_name = Path(file_path).stem  # получаем название исходного файла
        print(file_name)  # выводим имя файла для отладки
        audio.save_to_file(doc_text, f'files/{file_name}.mp3')  # указываем место хранения данных
        audio.runAndWait()  # запускаем читалку
        os.remove(file_path)  # удаляем исходный файл
        return print(f'[+] {file_name} has been converted to audio!')  # Маркер завершения конвертации
    else:  # если файл не был найден или не имеет поддерживаемого расширения
        return print('[!] File not found')  # выводим в консоль сообщение


if __name__ == "__main__":  # создаем точку доступа
    p = Process(target=pdf_to_audio_processor('./Возможные вопросы по ПИС.docx'))  # инициализируем процесс для проверки
    p.start()  # запускаем процесс
    p.join()  # завершаем процесс
