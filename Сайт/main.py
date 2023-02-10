import threading
import pyttsx3
import pdfplumber
from pathlib import Path
import os
import docx2txt
import langid


def pdf_to_audio(file_path='/'):
    threading.Thread(target=pdf_to_audio_processor(file_path)).start()


def pdf_to_audio_processor(file_path='./'):
    if Path(file_path).is_file() and Path(file_path).suffix == '.pdf':
        print(f'[!] {Path(file_path).stem} is processing...')
        with pdfplumber.PDF(open(file=file_path, mode='rb')) as pdf:
            pages = [pages.extract_text() for pages in pdf.pages]
        doc_text = ''.join(pages).replace('\n', ' ')
        print(doc_text)
        lang = langid.classify(doc_text)
        audio = pyttsx3.init()
        print(lang)

        ru = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0'
        en = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'

        if lang[0] == 'en':
            audio.setProperty('voice', en)
        if lang[0] == 'ru':
            audio.setProperty('voice', ru)
        file_name = Path(file_path).stem
        audio.save_to_file(doc_text, f'files/{file_name}.mp3')
        audio.runAndWait()
        os.remove(file_path)
        return print(f'[+] {file_name} has been converted to audio!')

    elif Path(file_path).is_file() and Path(file_path).suffix == '.docx':
        print(f'[!] {Path(file_path).stem} is processing...')
        doc_text = str(docx2txt.process(file_path)).replace('\n', ' ')
        print(doc_text)
        lang = langid.classify(doc_text)
        audio = pyttsx3.init()
        ru = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0'
        en = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'

        if lang[0] == 'en':
            audio.setProperty('voice', en)
        if lang[0] == 'ru':
            audio.setProperty('voice', ru)
        file_name = Path(file_path).stem
        audio.save_to_file(doc_text, f'files/{file_name}.mp3')
        audio.runAndWait()
        os.remove(file_path)
        return print(f'[+] {file_name} has been converted to audio!')
    else:
        return print('[!] File not found')


if __name__ == "__main__":
    pdf_to_audio('./CV.pdf')
