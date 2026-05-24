import fitz
import json
import os
from ollama import chat

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
            blocks = page.get_text("blocks")
            page_text = ""

            for block in blocks:
                if block[6] != 0:
                    continue
                raw_text = block[4]
                if not raw_text.strip():
                    continue

                cleaned = raw_text.replace('\n', ' ')
                cleaned = cleaned.replace('\r', ' ')
                cleaned = cleaned.replace('\t', ' ')
                cleaned_paragraph = []
                last_was_space = False
                for ch in cleaned:
                    if ch == ' ':
                        if not last_was_space:
                            cleaned_paragraph.append(' ')
                            last_was_space = True
                    else:
                        cleaned_paragraph.append(ch)
                        last_was_space = False
                cleaned_paragraph = ''.join(cleaned_paragraph).strip()
                if not cleaned_paragraph:
                    continue

                page_text += cleaned_paragraph + "  "

            if page_text.strip():
                self.pages_text.append({
                    "page_num": i + 1,
                    "text": page_text.strip(),
                    "start": global_pos,
                    "end": global_pos + len(page_text.strip())
                })
                self.all_text += page_text + "\n"
                global_pos += len(page_text.strip()) + 2

        doc.close()

    def find_by_keywords(self):
        keywords = ['непрерывн', 'гладк', 'разрыв', 'дифференцируем']

        for page_info in self.pages_text:
            page_text = page_info["text"]
            page_start = page_info["start"]
            page_num = page_info["page_num"]

            sentences = page_text.split('. ')

            for sent in sentences:
                if not sent.strip():
                    continue

                found = False
                for kw in keywords:
                    if kw.lower() in sent.lower():
                        found = True
                        break

                if found:
                    sent_with_dot = sent + '.'
                    pos = self.all_text.find(sent_with_dot, page_start, page_start + len(page_text))

                    if pos == -1:
                        pos = self.all_text.find(sent, page_start, page_start + len(page_text))

                    if pos != -1:
                        self.results.append({
                            "text": sent_with_dot,
                            "begin_index": pos,
                            "end_index": pos + len(sent_with_dot),
                            "page_number": page_num,
                            "summary": "функция"
                        })

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
    path = "dataset/" #TODO путь до файла
    parser = PdfToTxt(path)
    parser.run()

    # folder = "dataset"
    #
    # for file in os.listdir(folder):
    #     if file.endswith(".pdf"):
    #         path = os.path.join(folder, file)
    #         print(file)
    #         parser = PdfToTxt(path)
    #         parser.run()