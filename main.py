import fitz
import json
import os
from ollama import chat
import re

class PdfToTxt:
    def __init__(self, file_name):
        self.file_name = file_name
        self.all_text = ""
        self.pages_text = []
        self.results = []
        self.article_title = ""
        self.author = ""

    def get_metadata_from_llm(self, first_page_text):
        prompt = f"""извлеки из текста название статьи и автора. верни json:
{{"title": "", "author": ""}}
текст: {first_page_text[:2000]}"""

        try:
            response = chat(model='llama3.1:8b', messages=[
                {'role': 'user', 'content': prompt}
            ])
            answer = response.message.content
            import re
            json_match = re.search(r'\{.*\}', answer, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                self.article_title = data.get("title", "")
                self.author = data.get("author", "")
        except:
            self.article_title = ""
            self.author = ""

    def pdf_reader(self):
        doc = fitz.open(self.file_name)
        global_pos = 0

        first_page_text = doc[0].get_text()
        self.get_metadata_from_llm(first_page_text)

        start_page = 1
        for i in range(start_page, len(doc)):
            page = doc[i]

            page_text_raw = page.get_text()
            page_text_raw = re.sub(r'[-￻-�]', '', page_text_raw)
            lines = page_text_raw.split('\n')
            paragraphs = []
            current_para = []

            for line in lines:
                line = line.strip()
                if not line:
                    if current_para:
                        paragraphs.append(' '.join(current_para))
                        current_para = []
                else:
                    current_para.append(line)

            if current_para:
                paragraphs.append(' '.join(current_para))

            page_text = '\n\n'.join(paragraphs)

            if page_text.strip():
                self.pages_text.append({
                    "page_num": i + 1,
                    "text": page_text.strip(),
                    "start": global_pos,
                    "end": global_pos + len(page_text.strip())
                })
                self.all_text += page_text + "\n\n"
                global_pos += len(page_text.strip()) + 2

        doc.close()

    def find_by_keywords(self):
        keywords = ['непрерывн', 'гладк', 'разрыв', 'дифференцируем']

        all_paragraphs = []

        for page_info in self.pages_text:
            page_text = page_info["text"]
            page_start = page_info["start"]
            page_num = page_info["page_num"]

            paragraphs = page_text.split('\n\n')
            current_pos = page_start

            for para in paragraphs:
                if not para.strip():
                    current_pos += len(para) + 2
                    continue

                found = False
                for kw in keywords:
                    if kw.lower() in para.lower():
                        found = True
                        break

                if found:
                    self.results.append({
                        "text": para,
                        "begin_index": current_pos,
                        "end_index": current_pos + len(para),
                        "page_number": page_num,
                        "summary": "функция"
                    })

                current_pos += len(para) + 2
    def file_writer(self):
        with open("words.jsonl", "a", encoding="utf-8") as f:
            data = {
                "file_name": self.file_name,
                "article_title": self.article_title,
                "author": self.author,
                "text": self.results
            }
            f.write(json.dumps(data, ensure_ascii=False, indent=4) + "\n")

    def run(self):
        self.pdf_reader()

        if not self.all_text.strip():
            self.file_writer()
            return

        self.find_by_keywords()

        if not self.results:
            print("нет функций в файле")

        self.file_writer()

if __name__ == "__main__":
    # path = "dataset/elibrary_49326207_22037942.pdf" # TODO путь до файла
    # parser = PdfToTxt(path)
    # parser.run()

    folder = "dataset"

    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            path = os.path.join(folder, file)
            print(file)
            parser = PdfToTxt(path)
            parser.run()