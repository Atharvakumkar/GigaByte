import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def md_to_text(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        return f.read()


def create_pdf(text, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    margin = 50
    y = height - margin
    line_height = 12
    for line in text.splitlines():
        if y < margin:
            c.showPage()
            y = height - margin
        c.drawString(margin, y, line)
        y -= line_height
    c.save()


if __name__ == "__main__":
    md_path = os.path.join(os.path.dirname(__file__), "README.md")
    out_path = os.path.join(os.path.dirname(__file__), "report.pdf")
    text = md_to_text(md_path)
    create_pdf(text, out_path)
    print(f"PDF generated at {out_path}")
