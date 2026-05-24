# AvasevFunctions
<<<<<<< HEAD
pip install pymupdf ollama
ollama: ollama pull llama3.1:8b
pip install fitz

1 положите pdf файл в папку dataset
2 (147) path = "dataset/..." <- пкть до файла
3 запустите main.py
4 откройте words.jsonl, результат в самом низу

для того, чтобы проверить всю папку datasrt:
1 (147-149)
Закоментировать
    path = "dataset/" #TODO путь до файла
    parser = PdfToTxt(path)
    parser.run()

2 (151-158)
Раскоментировать
    # folder = "dataset"
    #
    # for file in os.listdir(folder):
    #     if file.endswith(".pdf"):
    #         path = os.path.join(folder, file)
    #         print(file)
    #         parser = PdfToTxt(path)
    #         parser.run()



clean_word - чистит знаки препинания
pdf_reader - читает pdf, разбивает на страницы и блоки
find_by_keywords - ищет нужные абзацы по ключевым словам
file_writer - сохраняет в jsonl
run - запускает всё по порядку
=======
file_name - переменная, хранящая имя файла, который используется в программе
FILTER - корни слов для фильтра
для работы с этой программой достаточно этих двух переменных

__init__ - хранит объкты класса
clean_word - удаляет знаки препинания
pdf_reader - читает и разбивает pdf файл
add_filtered_words - разбивает на абзацы
file_writer - запись в файл jsonl
run - запуск кдасса
>>>>>>> origin/main
