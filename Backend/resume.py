import fitz  # PyMuPDF

class Resume:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = self.read_pdf()

    def read_pdf(self):
        doc = fitz.open(self.file_path)
        return "".join([page.get_text() for page in doc])

    def get_text(self):
        return self.text
