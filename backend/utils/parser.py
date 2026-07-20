import fitz
import pytesseract 
from PIL import Image
from docx import Document
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
def extract_text_from_pdf(pdf_path):
    text = ""
    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        extracted = page.get_text()
        text+=extracted
    return text

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text=""
    for para in doc.paragraphs:
        text+=para.text+"\n"
    return text

def extract_text_using_ocr(pdf_path):
    images = convert_from_path(
        pdf_path,
        first_page=1,
        last_page=1,
        dpi=100,
        poppler_path= r"C:\poppler\poppler-26.02.0\Library\bin"
    )
    text=""
    for image in images:
        extracted = pytesseract.image_to_string(image,config="--psm 6")
        text+= extracted+"\n"
    
    return text