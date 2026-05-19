import fitz
import json
import re

class PdfToTxt:
    def __init__(self, file_name, FILTER):
        self.file_name = file_name
        self.filter = FILTER
        self.paragraphs_to_save = []
        self.paragraphs_data = []


    def clean_word(self, word):
        return re.sub(r'[.,!?;:()\[\]{}\"«»-]', '', word)


    def pdf_reader(self):
        doc = fitz.open(self.file_name)
        global_pos = 0

        for i in range(len(doc)):
            page = doc[i]
            blocks = page.get_text("blocks")

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

                start_idx = global_pos
                end_idx = global_pos + len(cleaned_paragraph)
                self.paragraphs_data.append({
                    "paragraph": cleaned_paragraph,
                    "start_index": start_idx,
                    "end_index": end_idx,
                    "page_number": i + 1
                })
                global_pos += len(cleaned_paragraph) + 2
        doc.close()


    def add_filtered_words(self):
        for i in self.paragraphs_data:
            paragraph_text = i["paragraph"]
            words = paragraph_text.split()
            found = False
            for w in words:
                cleaned = self.clean_word(w)
                lowered = cleaned.lower()
                for root in self.filter:
                    if root in lowered:
                        found = True
                        break
                if found:
                    break
            if found:
                self.paragraphs_to_save.append(i)


    def file_writer(self):
        with open("words.jsonl", "a", encoding="utf-8") as f:
            for para_info in self.paragraphs_to_save:
                data = {
                    "file": self.file_name,
                    "paragraph": para_info["paragraph"],
                    "start_index": para_info["start_index"],
                    "end_index": para_info["end_index"],
                    "page_number": para_info["page_number"]
                }
                f.write(json.dumps(data, ensure_ascii=False, indent=4) + "\n")


    def run(self):
        self.pdf_reader()
        self.add_filtered_words()
        self.file_writer()


file_name = "dataset/elibrary_82514926_23581521.pdf"
FILTER = ['непрервын', 'функци', 'разрыв', 'f(x)', 'гладк', 'дифференцируем']
pdftotxt = PdfToTxt(file_name, FILTER)
pdftotxt.run()