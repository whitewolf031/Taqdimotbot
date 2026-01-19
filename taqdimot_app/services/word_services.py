# services/word_services.py
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from django.conf import settings
import os

def build_docx(json_data, filename):
    # MEDIA papkasi mavjudligini tekshirish
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    doc = Document()

    # Sarlavha markazlashtirilgan va 16pt
    title = json_data.get("title", "Sarlavha mavjud emas")
    title_paragraph = doc.add_paragraph(title)
    title_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    title_paragraph.runs[0].font.size = Pt(16)
    title_paragraph.runs[0].bold = True

    sections = json_data.get("sections", [])
    for section in sections:
        heading = section.get("heading", "Bo'lim")
        content = section.get("content", "")
        # Bo'lim sarlavhalari
        doc.add_heading(heading, level=2)
        # Matnlarni justify style bilan qo'shish
        para = doc.add_paragraph(content)
        para.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY

    # Fayl saqlash
    path = os.path.join(settings.MEDIA_ROOT, f"{filename}.docx")
    doc.save(path)

    return settings.MEDIA_URL + f"{filename}.docx"