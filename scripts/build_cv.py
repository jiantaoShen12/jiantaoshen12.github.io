"""Build the downloadable PDF from the editable cv.html, using ReportLab.

Usage: python scripts/build_cv.py
No network access or front-end build is required.
"""
from pathlib import Path
import re
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape, quoteattr

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "pdf" / "Jiantao_Shen_CV.pdf"
FOREST = colors.HexColor("#203d2d")
MUTED = colors.HexColor("#58685c")


def inline(node):
    """Translate the CV's small, explicit inline vocabulary to PDF markup."""
    result = escape(node.text or "")
    for child in node:
        content = inline(child)
        if child.tag == "a":
            result += f'<link href={quoteattr(child.attrib["href"])} color="#203d2d">{content}</link>'
        elif child.tag in {"strong", "b"}:
            result += f"<b>{content}</b>"
        elif child.tag in {"em", "i"}:
            result += f"<i>{content}</i>"
        elif child.tag == "br":
            result += "<br/>"
        else:
            raise ValueError(f"Unsupported inline element: {child.tag}")
        result += escape(child.tail or "")
    return result.strip()


def build():
    source = (ROOT / "cv.html").read_text(encoding="utf-8")
    match = re.search(r'<main\b[^>]*\bid="cv"[^>]*>.*?</main>', source, re.S)
    if not match:
        raise ValueError('Missing <main id="cv"> in cv.html')
    cv = ET.fromstring(match.group())
    header = cv.find("header")
    name = "".join(header.find("h1").itertext()).strip()
    styles = {
        "name": ParagraphStyle("Name", fontName="Times-Roman", fontSize=29, leading=33, textColor=FOREST, spaceAfter=9),
        "body": ParagraphStyle("Body", fontName="Helvetica", fontSize=9.4, leading=13.5, textColor=colors.HexColor("#25382c"), spaceAfter=2),
        "heading": ParagraphStyle("Heading", fontName="Times-Roman", fontSize=15, leading=18, textColor=FOREST, spaceBefore=13, spaceAfter=5, keepWithNext=True),
        "title": ParagraphStyle("Title", fontName="Helvetica-Bold", fontSize=9.8, leading=13.5, spaceAfter=2, textColor=FOREST),
        "date": ParagraphStyle("Date", fontName="Helvetica", fontSize=8.5, leading=11.5, spaceAfter=2, textColor=MUTED),
        "links": ParagraphStyle("Links", fontName="Helvetica", fontSize=8.3, leading=11.5, spaceAfter=2, textColor=FOREST),
    }
    story = [Paragraph(escape(name), styles["name"])]
    for p in header.findall("p"):
        story.append(Paragraph(inline(p), styles["body"]))
    for section in cv.findall("section"):
        story.append(Paragraph(inline(section.find("h2")), styles["heading"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cad7c8"), spaceAfter=8))
        for entry in section.findall("div"):
            blocks = []
            for node in entry:
                style = "title" if node.tag == "h3" else "body"
                if node.get("class") == "cv-date":
                    style = "date"
                elif node.get("class") == "cv-links":
                    style = "links"
                blocks.append(Paragraph(inline(node), styles[style]))
            blocks.append(Spacer(1, 6))
            story.append(KeepTogether(blocks))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#cad7c8"))
        canvas.setLineWidth(0.5)
        canvas.line(doc.leftMargin, 35, A4[0] - doc.rightMargin, 35)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(doc.leftMargin, 23, f"{name} | Curriculum Vitae")
        canvas.drawRightString(A4[0] - doc.rightMargin, 23, f'Updated {cv.attrib["data-updated"]} | {doc.page}')
        canvas.restoreState()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=46, rightMargin=46, topMargin=38, bottomMargin=47,
                            title=f"{name} - Curriculum Vitae", author=name, subject="Education, research interests, publications and honors")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    build()
