# Avasev practica

Извлечение смысловых фрагментов из русскоязычных научных статей в формате PDF по заданным корням слов.

## Что делает

- Находит все PDF-файлы в папке assets
- Извлекает текст из PDF
- Через LLM (llama3.1:8b) определяет название статьи и автора
- Ищет абзацы, содержащие заданные корни слов
- Объединяет найденный абзац с соседними (предыдущим и следующим)
- Сохраняет результат в dataset.jsonl

## Как запустить

Установка зависимостей:
```
pip install pymupdf
pip install pymupdf ollama
ollama pull qwen2.5:7b
ollama serve
```


## Для работы с одни файлом:
Заккоментируйте:
```
folder = "dataset"

for file in os.listdir(folder):
    if file.endswith(".pdf"):
        path = os.path.join(folder, file)
        print(file)
        parser = PdfToTxt(path)
        parser.run()
(142-149 строки)
```

Раскомментируйте:
```
# path = "dataset/elibrary_49326207_22037942.pdf" # TODO путь до файла
# parser = PdfToTxt(path)
# parser.run()
```

Вришите путь до файла в переменную path
```
path = "сюда"
```
Запустите main.py, результат запишется в файл words.jsonl


