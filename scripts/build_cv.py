"""Build the industry research resume PDF from editable cv.html.

Usage: python scripts/build_cv.py
Dependencies: ReportLab. No network access or front-end build is required.
"""
from pathlib import Path
import os
import re
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape, quoteattr

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Flowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "pdf" / "Jiantao_Shen_CV.pdf"
INK = colors.HexColor("#111111")
MUTED = colors.HexColor("#484848")
LINK = "#203d2d"


def register_fonts():
    """Embed a complete Arial-compatible family for consistent PDF rendering."""
    arial = ("arial.ttf", "arialbd.ttf", "ariali.ttf", "arialbi.ttf")
    liberation = ("LiberationSans-Regular.ttf", "LiberationSans-Bold.ttf",
                  "LiberationSans-Italic.ttf", "LiberationSans-BoldItalic.ttf")
    candidates = [
        (Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts", arial),
        (Path("/System/Library/Fonts/Supplemental"),
         ("Arial.ttf", "Arial Bold.ttf", "Arial Italic.ttf", "Arial Bold Italic.ttf")),
        (Path("/usr/share/fonts/truetype/liberation2"), liberation),
        (Path("/usr/share/fonts/truetype/liberation"), liberation),
    ]
    for directory, filenames in candidates:
        paths = [directory / filename for filename in filenames]
        if all(path.is_file() for path in paths):
            for suffix, path in zip(("", "-Bold", "-Italic", "-BoldItalic"), paths):
                pdfmetrics.registerFont(TTFont("ResumeSans" + suffix, str(path)))
            pdfmetrics.registerFontFamily("ResumeSans", normal="ResumeSans", bold="ResumeSans-Bold",
                                          italic="ResumeSans-Italic", boldItalic="ResumeSans-BoldItalic")
            return
    raise RuntimeError("Install Arial or Liberation Sans to build the PDF with embedded fonts.")


def inline(node, link_color=LINK):
    """Translate the CV's explicit inline vocabulary into ReportLab markup."""
    result = escape(node.text or "")
    for child in node:
        content = inline(child, link_color)
        if child.tag == "a":
            result += f'<link href={quoteattr(child.attrib["href"])} color="{link_color}">{content}</link>'
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


class TitleWithDate(Flowable):
    """Keep an entry title and its date on one line without a layout table."""
    def __init__(self, title, date, style):
        super().__init__()
        self.title = Paragraph(title, style)
        self.date = date
        self.date_style = ParagraphStyle("EntryDate", fontName="ResumeSans", fontSize=10,
                                         leading=12.7, textColor=MUTED, alignment=2)
        self.date_p = Paragraph(escape(date), self.date_style)

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        self.date_width = 106 if len(self.date) > 10 else 70
        _, h1 = self.title.wrap(availWidth - self.date_width - 12, availHeight)
        _, h2 = self.date_p.wrap(self.date_width, availHeight)
        self.height = max(h1, h2)
        return self.width, self.height

    def draw(self):
        self.title.drawOn(self.canv, 0, self.height - self.title.height)
        self.date_p.drawOn(self.canv, self.width - self.date_width, self.height - self.date_p.height)


def build():
    register_fonts()
    source = (ROOT / "cv.html").read_text(encoding="utf-8")
    match = re.search(r'<main\b[^>]*\bid="cv"[^>]*>.*?</main>', source, re.S)
    if not match:
        raise ValueError('Missing <main id="cv"> in cv.html')
    cv = ET.fromstring(match.group())
    header = cv.find("header")
    name = "".join(header.find("h1").itertext()).strip()
    styles = {
        "name": ParagraphStyle("Name", fontName="ResumeSans-Bold", fontSize=25, leading=28,
                               textColor=colors.black, spaceAfter=3),
        "role": ParagraphStyle("Role", fontName="ResumeSans", fontSize=11, leading=13.5,
                               textColor=colors.black, spaceAfter=4),
        "contact": ParagraphStyle("Contact", fontName="ResumeSans", fontSize=10, leading=12.5,
                                  textColor=INK, spaceAfter=0.5),
        "profile": ParagraphStyle("Profile", fontName="ResumeSans", fontSize=10.5, leading=13.2,
                                  textColor=INK, spaceBefore=7, spaceAfter=1),
        "heading": ParagraphStyle("Heading", fontName="ResumeSans-Bold", fontSize=10.5, leading=13,
                                  textColor=colors.black, spaceBefore=7, spaceAfter=3, keepWithNext=True),
        "title": ParagraphStyle("Title", fontName="ResumeSans-Bold", fontSize=10.5, leading=13.2,
                                textColor=colors.black, spaceAfter=0.5),
        "body": ParagraphStyle("Body", fontName="ResumeSans", fontSize=10.5, leading=13.2,
                               textColor=INK, spaceAfter=1),
        "meta": ParagraphStyle("Meta", fontName="ResumeSans", fontSize=10, leading=12,
                               textColor=MUTED, spaceAfter=2),
        "bullet": ParagraphStyle("Bullet", fontName="ResumeSans", fontSize=10.5, leading=13.2,
                                 textColor=INK, leftIndent=10, firstLineIndent=0, bulletIndent=0,
                                 bulletFontName="ResumeSans", bulletFontSize=9, spaceAfter=1.8),
        "pubtitle": ParagraphStyle("PubTitle", fontName="ResumeSans-Bold", fontSize=10.2, leading=12.5,
                                   textColor=colors.black, spaceAfter=0.4),
        "pubbody": ParagraphStyle("PubBody", fontName="ResumeSans", fontSize=10, leading=12,
                                  textColor=INK, spaceAfter=0.4),
    }
    story = [Paragraph(escape(name), styles["name"])]
    for p in header.findall("p"):
        key = {"cv-role": "role", "cv-profile": "profile"}.get(p.get("class"), "contact")
        story.append(Paragraph(inline(p), styles[key]))

    for section in cv.findall("section"):
        story.append(Paragraph(inline(section.find("h2")).upper(), styles["heading"]))
        entries = section.findall("div")
        for idx, entry in enumerate(entries):
            blocks = []
            is_pub = "cv-publication" in entry.get("class", "")
            title = entry.find("h3")
            date = entry.get("data-date")
            if title is not None:
                if date:
                    blocks.append(TitleWithDate(inline(title, "#000000"), date, styles["title"]))
                else:
                    blocks.append(Paragraph(inline(title, "#000000"), styles["pubtitle" if is_pub else "title"]))
            for node in entry:
                if node.tag == "h3" or node.get("class") == "cv-date":
                    continue
                if node.tag == "ul":
                    for li in node.findall("li"):
                        blocks.append(Paragraph(inline(li), styles["bullet"], bulletText="\u2022"))
                elif node.tag == "p":
                    key = "pubbody" if is_pub else ("meta" if node.get("class") == "cv-project-meta" else "body")
                    blocks.append(Paragraph(inline(node), styles[key]))
                else:
                    raise ValueError(f"Unsupported CV block: {node.tag}")
            if idx < len(entries) - 1:
                blocks.append(Spacer(1, 3 if is_pub else 4))
            story.append(KeepTogether(blocks))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(MUTED)
        canvas.setFont("ResumeSans", 8)
        canvas.drawRightString(letter[0] - doc.rightMargin, 20, f'Updated {cv.attrib["data-updated"]}')
        canvas.restoreState()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=letter, leftMargin=42, rightMargin=42,
                            topMargin=30, bottomMargin=34, title=f"{name} Resume", author=name,
                            subject="Multimodal learning, dynamical modeling, flow matching and LLM agent interests")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    build()

