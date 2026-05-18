import fitz
import json


class PdfToTxt:
    def __init__(self, file_name, FILTER):
        self.file_name = file_name
        self.text = ""
        self.words = []
        self.list_words = []
        self.filter = FILTER
        self.author = ""


    def pdf_reader(self):
        doc = fitz.open(self.file_name)
        self.author = doc.metadata.get("author")
        for i in doc:
            self.text += i.get_text()
        self.words = self.text.split()

    def words_lower(self):
        for i in range(len(self.words)):
            self.words[i] = self.words[i].lower()

    def add_filtered_words(self):
        self.list_words += [self.file_name]
        for i_words in self.words:
            for i_filter in self.filter:
                if i_filter in i_words:
                    self.list_words += [i_words]

    def file_writer(self):
        data = {
            "file": self.file_name,
            "author": self.author,
            "words": self.list_words
        }

        with open("words.jsonl", "a", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.write("\n")

    def run(self):
        self.pdf_reader()
        self.words_lower()
        self.add_filtered_words()
        self.file_writer()


file_name = "dataset/elibrary_25309419_24117104.pdf"
FILTER = ['непрервын', 'функци', 'разрыв', 'f(x)', 'гладк', 'дифференцируем']
pdftotxt = PdfToTxt(file_name, FILTER)
pdftotxt.run()









