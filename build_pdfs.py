"""
build_pdfs.py
Converts PROJECT_ANALYSIS.md and IMPLEMENTATION_PLAN.md into beautifully typeset,
executive-ready PDFs with Devanagari (Hindi) and English font support, tables,
callouts, and custom header/footer numbering.
"""

import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# Register Fonts
FONT_NAME = "Nirmala"
FONT_BOLD = "NirmalaBold"

try:
    pdfmetrics.registerFont(TTFont("Nirmala", "C:/Windows/Fonts/Nirmala.ttc", subfontIndex=0))
    # Nirmala bold in ttc or fallback to arialbd / Nirmala
    pdfmetrics.registerFont(TTFont("NirmalaBold", "C:/Windows/Fonts/Nirmala.ttc", subfontIndex=0))
except Exception as e:
    print(f"Font registration fallback: {e}")
    FONT_NAME = "Helvetica"
    FONT_BOLD = "Helvetica-Bold"

class NumberedCanvas(canvas.Canvas):
    """Adds running headers and page numbers like 'Page X of Y'"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_header_footer(self, total_pages):
        self.saveState()
        self.setFont(FONT_NAME, 8)
        self.setFillColor(colors.HexColor("#555555"))

        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "KrishiMitra (कृषिमित्र) — AI Agriculture Assistant")
            self.setStrokeColor(colors.HexColor("#D0D7CC"))
            self.setLineWidth(0.5)
            self.line(54, 744, 612 - 54, 744)

        # Footer
        page_text = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(612 - 54, 36, page_text)
        self.drawString(54, 36, "Smart India Hackathon (SIH) Innovation Project • Confidential & Proprietary")
        self.setStrokeColor(colors.HexColor("#D0D7CC"))
        self.setLineWidth(0.5)
        self.line(54, 48, 612 - 54, 48)

        self.restoreState()

def clean_inline_markdown(text):
    # Remove file links [text](url) -> <u>text</u>
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<b>\1</b>', text)
    # Bold **text**
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Italic *text*
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    # Inline code `code`
    text = re.sub(r'`(.*?)`', r'<font face="Courier" color="#1B5E20"><b>\1</b></font>', text)
    # HTML escapes
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Re-allow safe tags
    text = text.replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
    text = text.replace("&lt;i&gt;", "<i>").replace("&lt;/i&gt;", "</i>")
    text = text.replace("&lt;u&gt;", "<u>").replace("&lt;/u&gt;", "</u>")
    text = text.replace("&lt;font", "<font").replace("&lt;/font&gt;", "</font>").replace("&gt;", ">")
    return text

def parse_markdown_to_flowables(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        fontName=FONT_BOLD,
        fontSize=20,
        leading=25,
        textColor=colors.HexColor("#1B5E20"),
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'DocH1',
        fontName=FONT_BOLD,
        fontSize=15,
        leading=20,
        textColor=colors.HexColor("#004D20"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'DocH2',
        fontName=FONT_BOLD,
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1E3A1E"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'DocH3',
        fontName=FONT_BOLD,
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#2C4C2C"),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'DocBody',
        fontName=FONT_NAME,
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#222222"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'DocBullet',
        fontName=FONT_NAME,
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#222222"),
        leftIndent=14,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'DocCallout',
        fontName=FONT_NAME,
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1A3A1A")
    )

    code_style = ParagraphStyle(
        'DocCode',
        fontName="Courier",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0D3813")
    )

    flowables = []
    in_code_block = False
    code_lines = []
    in_table = False
    table_rows = []

    for line in lines:
        raw = line.rstrip()

        # Code block fence
        if raw.startswith("```"):
            if in_code_block:
                # End code block
                in_code_block = False
                # Chunk code lines into blocks of at most 25 lines so they fit on pages
                chunk_size = 25
                for i in range(0, len(code_lines), chunk_size):
                    chunk = code_lines[i:i + chunk_size]
                    code_text = "<br/>".join([clean_inline_markdown(l) for l in chunk])
                    p = Paragraph(code_text, code_style)
                    t = Table([[p]], colWidths=[504])
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F8F1")),
                        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#C8E6C9")),
                        ('PADDING', (0, 0), (-1, -1), 5),
                    ]))
                    flowables.append(Spacer(1, 2))
                    flowables.append(t)
                flowables.append(Spacer(1, 4))
                code_lines = []
            else:
                in_code_block = True
                code_lines = []
            continue

        if in_code_block:
            code_lines.append(raw if raw else " ")
            continue

        # Tables
        if "|" in raw and ("---" in raw or in_table or raw.strip().startswith("|")):
            if "---" in raw:
                # table separator line
                continue
            cells = [clean_inline_markdown(c.strip()) for c in raw.split("|")[1:-1]]
            if cells:
                in_table = True
                table_rows.append(cells)
            continue
        elif in_table:
            # End of table
            in_table = False
            if table_rows:
                # Format table
                data_cells = []
                col_count = max(len(r) for r in table_rows)
                for r_idx, row in enumerate(table_rows):
                    row_cells = []
                    for c in row:
                        style = ParagraphStyle(
                            'TCell',
                            fontName=FONT_BOLD if r_idx == 0 else FONT_NAME,
                            fontSize=8 if r_idx > 0 else 8.5,
                            leading=11,
                            textColor=colors.white if r_idx == 0 else colors.HexColor("#222222")
                        )
                        row_cells.append(Paragraph(c, style))
                    # pad if shorter
                    while len(row_cells) < col_count:
                        row_cells.append(Paragraph("", body_style))
                    data_cells.append(row_cells)

                # calculate widths
                available_w = 504
                col_w = available_w / col_count
                t = Table(data_cells, colWidths=[col_w] * col_count)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B5E20")),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D0D7CC")),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FBF8")]),
                    ('PADDING', (0, 0), (-1, -1), 5),
                ]))
                flowables.append(Spacer(1, 4))
                flowables.append(t)
                flowables.append(Spacer(1, 6))
                table_rows = []

        # Blank line
        if not raw.strip():
            continue

        # Horizontal Rule
        if raw.strip() in ["---", "***", "___"]:
            flowables.append(Spacer(1, 4))
            flowables.append(HRFlowable(width="100%", thickness=0.7, color=colors.HexColor("#C8D4C5"), spaceBefore=4, spaceAfter=8))
            continue

        # Callouts (> [!IMPORTANT], > [!NOTE], > text)
        if raw.startswith(">"):
            callout_text = clean_inline_markdown(raw.lstrip("> ").replace("[!IMPORTANT]", "<b>IMPORTANT:</b>").replace("[!NOTE]", "<b>NOTE:</b>").replace("[!WARNING]", "<b>WARNING:</b>"))
            p = Paragraph(callout_text, callout_style)
            t = Table([[p]], colWidths=[504])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EBF5EB")),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#A5D6A7")),
                ('LINEBEFORE', (0, 0), (0, -1), 3.0, colors.HexColor("#1B5E20")),
                ('PADDING', (0, 0), (-1, -1), 6)
            ]))
            flowables.append(Spacer(1, 3))
            flowables.append(t)
            flowables.append(Spacer(1, 5))
            continue

        # Headings
        if raw.startswith("# "):
            flowables.append(Paragraph(clean_inline_markdown(raw[2:]), title_style))
            flowables.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1B5E20"), spaceBefore=2, spaceAfter=8))
            continue
        elif raw.startswith("## "):
            flowables.append(Paragraph(clean_inline_markdown(raw[3:]), h1_style))
            continue
        elif raw.startswith("### "):
            flowables.append(Paragraph(clean_inline_markdown(raw[4:]), h2_style))
            continue
        elif raw.startswith("#### "):
            flowables.append(Paragraph(clean_inline_markdown(raw[5:]), h3_style))
            continue

        # Bullet lists (* or -)
        if raw.strip().startswith(("* ", "- ")):
            bullet_text = clean_inline_markdown(raw.strip()[2:])
            p = Paragraph(f"• &nbsp; {bullet_text}", bullet_style)
            flowables.append(p)
            continue

        # Numbered list
        if re.match(r'^\d+\.\s+', raw.strip()):
            item_text = clean_inline_markdown(raw.strip())
            p = Paragraph(item_text, bullet_style)
            flowables.append(p)
            continue

        # Standard Body paragraph
        p = Paragraph(clean_inline_markdown(raw), body_style)
        flowables.append(p)

    return flowables

def generate_pdf(input_md, output_pdf, title):
    print(f"Generating PDF: {output_pdf} from {input_md}...")
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    story = parse_markdown_to_flowables(input_md)
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {output_pdf} ({os.path.getsize(output_pdf) / 1024:.1f} KB)")

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    
    proj_md = os.path.join(root, "PROJECT_ANALYSIS.md")
    proj_pdf = os.path.join(root, "PROJECT_ANALYSIS.pdf")
    if os.path.exists(proj_md):
        generate_pdf(proj_md, proj_pdf, "Project Analysis — KrishiMitra")

    plan_md = os.path.join(root, "IMPLEMENTATION_PLAN.md")
    plan_pdf = os.path.join(root, "IMPLEMENTATION_PLAN.pdf")
    if os.path.exists(plan_md):
        generate_pdf(plan_md, plan_pdf, "Implementation Plan — KrishiMitra")

if __name__ == "__main__":
    main()
