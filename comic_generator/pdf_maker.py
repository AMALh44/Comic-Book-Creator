from fpdf import FPDF
import os
import unicodedata

def sanitize_text(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

def build_comic_pdf(panels, output_dir, title="AI Comic", subtitle="A Comic by AI"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Cover page
    pdf.add_page()
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(255, 255, 255)
    pdf.set_fill_color(0, 0, 0)
    pdf.cell(0, 40, "", ln=True)
    pdf.cell(0, 20, title, ln=True, align="C", fill=True)
    pdf.set_font("Arial", '', 16)
    pdf.cell(0, 20, subtitle, ln=True, align="C", fill=True)

    # Panels
    for i, (scene, image_path) in enumerate(panels):
        if i % 2 == 0:
            pdf.add_page()
        y = 20 if i % 2 == 0 else 150
        pdf.image(image_path, x=10, y=y, w=190)
        pdf.set_xy(10, y + 90)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(190, 10, sanitize_text(scene))

    pdf_path = os.path.join(output_dir, "comic_book.pdf")
    pdf.output(pdf_path)
    return pdf_path
