```python
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Registered Geometra font from the attached assets
pdfmetrics.registerFont(TTFont('Geometra', 'font.ttf'))

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header (Top)
        self.drawString(54, 11 * 72 - 36, "ARC ACCORD — VISUAL IDENTITY & TYPOGRAPHY SYSTEM")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)
        
        # Footer (Bottom)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * 72 - 54, 36, page_text)
        self.drawString(54, 36, "CONFIDENTIAL & PROPRIETARY — BRAND GUIDELINES")
        self.line(54, 48, 8.5 * 72 - 54, 48)
        
        self.restoreState()

def create_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    story = []
    
    # Colors derived from brand assets
    EBONY_CLAY = colors.HexColor("#1F2937")
    WHITE_ROCK = colors.HexColor("#E8E2D8")
    HURRICANE = colors.HexColor("#847C7C")
    FRIAR_GRAY = colors.HexColor("#84847C")
    ANTIQUE_GOLD = colors.HexColor("#B08D57")
    
    # Typography Styles
    styles = getSampleStyleSheet()
    
    # Primary Display (Geometra)
    style_primary_lg = ParagraphStyle(
        'PrimaryLG',
        fontName='Geometra',
        fontSize=28,
        leading=34,
        textColor=EBONY_CLAY,
        spaceAfter=4
    )
    
    style_primary_md = ParagraphStyle(
        'PrimaryMD',
        fontName='Geometra',
        fontSize=20,
        leading=26,
        textColor=EBONY_CLAY,
        spaceAfter=4
    )
    
    style_primary_sm = ParagraphStyle(
        'PrimarySM',
        fontName='Geometra',
        fontSize=14,
        leading=18,
        textColor=EBONY_CLAY,
        spaceAfter=4
    )

    # Subheading (Montserrat)
    style_sub_lg = ParagraphStyle(
        'SubLG',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=24,
        textColor=EBONY_CLAY,
        spaceAfter=4
    )
    
    style_sub_md = ParagraphStyle(
        'SubMD',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=EBONY_CLAY,
        spaceAfter=4
    )
    
    style_sub_sm = ParagraphStyle(
        'SubSM',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=EBONY_CLAY,
        spaceAfter=4
    )

    # Body Copy (Inter/Helvetica)
    style_body_lg = ParagraphStyle(
        'BodyLG',
        fontName='Helvetica',
        fontSize=12,
        leading=17,
        textColor=TEXT_MUTED,
        spaceAfter=4
    )
    
    style_body_md = ParagraphStyle(
        'BodyMD',
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=TEXT_MUTED,
        spaceAfter=4
    )
    
    style_body_sm = ParagraphStyle(
        'BodySM',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_MUTED,
        spaceAfter=4
    )

    # Descriptive / Meta Styles
    style_meta_label = ParagraphStyle(
        'MetaLabel',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=EBONY_CLAY
    )
    
    style_meta_desc = ParagraphStyle(
        'MetaDesc',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_MUTED
    )

    # Title Block
    story.append(Spacer(1, 10))
    story.append(Paragraph("ARC ACCORD", style_primary_lg))
    story.append(Paragraph("Visual Identity & Typography Hierarchy Guide", ParagraphStyle('SubHeader', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=TEXT_MUTED)))
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=1.5, color=DARK_NAVY, spaceAfter=15))

    # Introduction / Overview
    intro_text = (
        "This brand specification document defines the typographic hierarchy for <b>Arc Accord</b>. "
        "The system pairs the custom geometric primary display typeface, <b>Geometra</b>, with highly functional "
        "complementary sans-serif typefaces to establish structural clarity, professional elegance, and optimal readability."
    )
    story.append(Paragraph(intro_text, style_body_md))
    story.append(Spacer(1, 15))

    # Brand Palette Bar
    color_data = [
        [
            Paragraph("<b>Primary Dark</b><br/>#1F2937", ParagraphStyle('C1', fontName='Helvetica', fontSize=8, leading=10, textColor=colors.white)),
            Paragraph("<b>Warm Light</b><br/>#FFF4E7", ParagraphStyle('C2', fontName='Helvetica', fontSize=8, leading=10, textColor=DARK_NAVY)),
            Paragraph("<b>Neutral Soft</b><br/>#E8E2D8", ParagraphStyle('C3', fontName='Helvetica', fontSize=8, leading=10, textColor=DARK_NAVY))
        ]
    ]
    color_table = Table(color_data, colWidths=[168, 168, 168], height=36)
    color_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), EBONY_CLAY),
        ('BACKGROUND', (1,0), (1,0), WARM_CREAM),
        ('BACKGROUND', (2,0), (2,0), SOFT_BEIGE),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.white),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
    ]))
    story.append(color_table)
    story.append(Spacer(1, 20))

    # SECTION 1: PRIMARY DISPLAY FONT
    story.append(Paragraph("1. Primary Display Font — Geometra", style_sub_md))
    story.append(HRFlowable(width="100%", thickness=0.75, color=BORDER_COLOR, spaceAfter=10))
    
    geo_spec = [
        [Paragraph("Role / Application", style_meta_label), Paragraph("Brand Logotype, Main Titles, High-Impact Headers", style_meta_desc)],
        [Paragraph("Classification", style_meta_label), Paragraph("Geometric Sans-Serif", style_meta_desc)],
        [Paragraph("Key Characteristics", style_meta_label), Paragraph("Clean geometric proportions, sharp apexes, modern corporate aesthetic.", style_meta_desc)]
    ]
    t_geo = Table(geo_spec, colWidths=[130, 374])
    t_geo.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#EDF2F7"))
    ]))
    story.append(t_geo)
    story.append(Spacer(1, 10))

    # Size Scale for Geometra
    geo_scale = [
        [Paragraph("Large (32pt)", style_meta_label), Paragraph("Arc Accord Architectural Design", style_primary_lg)],
        [Paragraph("Medium (20pt)", style_meta_label), Paragraph("Arc Accord Architectural Design", style_primary_md)],
        [Paragraph("Small (14pt)", style_meta_label), Paragraph("Arc Accord Architectural Design", style_primary_sm)]
    ]
    t_geo_scale = Table(geo_scale, colWidths=[100, 404])
    t_geo_scale.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#EDF2F7")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_geo_scale)
    story.append(Spacer(1, 20))

    # SECTION 2: SUBHEADING FONT
    story.append(Paragraph("2. Subheading Font — Montserrat / Helvetica Bold", style_sub_md))
    story.append(HRFlowable(width="100%", thickness=0.75, color=BORDER_COLOR, spaceAfter=10))
    
    sub_spec = [
        [Paragraph("Role / Application", style_meta_label), Paragraph("Section Headers, Subtitles, Category Labels, UI Titles", style_meta_desc)],
        [Paragraph("Recommended Typeface", style_meta_label), Paragraph("Montserrat Bold (Google Fonts) / Helvetica Bold", style_meta_desc)],
        [Paragraph("Design Harmony", style_meta_label), Paragraph("Shares geometric architecture with Geometra while providing structure and structural hierarchy.", style_meta_desc)]
    ]
    t_sub = Table(sub_spec, colWidths=[130, 374])
    t_sub.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#EDF2F7"))
    ]))
    story.append(t_sub)
    story.append(Spacer(1, 10))

    # Size Scale for Subheading
    sub_scale = [
        [Paragraph("Large (18pt)", style_meta_label), Paragraph("Strategic Structural Harmony and Governance", style_sub_lg)],
        [Paragraph("Medium (14pt)", style_meta_label), Paragraph("Strategic Structural Harmony and Governance", style_sub_md)],
        [Paragraph("Small (11pt)", style_meta_label), Paragraph("Strategic Structural Harmony and Governance", style_sub_sm)]
    ]
    t_sub_scale = Table(sub_scale, colWidths=[100, 404])
    t_sub_scale.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#EDF2F7")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_sub_scale)
    story.append(Spacer(1, 20))

    # SECTION 3: BODY COPY FONT
    story.append(Paragraph("3. Body Copy Font — Inter / Helvetica Regular", style_sub_md))
    story.append(HRFlowable(width="100%", thickness=0.75, color=BORDER_COLOR, spaceAfter=10))
    
    body_spec = [
        [Paragraph("Role / Application", style_meta_label), Paragraph("Long-form Text, Paragraphs, Brand Narratives, Documentation", style_meta_desc)],
        [Paragraph("Recommended Typeface", style_meta_label), Paragraph("Inter Regular (Google Fonts) / Helvetica Regular", style_meta_desc)],
        [Paragraph("Design Harmony", style_meta_label), Paragraph("Neutral, highly legible grotesque sans-serif with excellent x-height for comfortable reading.", style_meta_desc)]
    ]
    t_body = Table(body_spec, colWidths=[130, 374])
    t_body.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#EDF2F7"))
    ]))
    story.append(t_body)
    story.append(Spacer(1, 10))

    # Size Scale for Body Copy
    sample_paragraph = "Arc Accord delivers precision-crafted architectural solutions that harmonize modern aesthetics with structural integrity. Our commitment to design excellence ensures every project reflects identity and balance."
    body_scale = [
        [Paragraph("Large (12pt)", style_meta_label), Paragraph(sample_paragraph, style_body_lg)],
        [Paragraph("Medium (10pt)", style_meta_label), Paragraph(sample_paragraph, style_body_md)],
        [Paragraph("Small (8.5pt)", style_meta_label), Paragraph(sample_paragraph, style_body_sm)]
    ]
    t_body_scale = Table(body_scale, colWidths=[100, 404])
    t_body_scale.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#EDF2F7")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_body_scale)
    story.append(Spacer(1, 20))

    # SECTION 4: HIERARCHY DEMONSTRATION / MOCKUP
    story.append(Paragraph("4. Complete Typographic Hierarchy Demonstration", style_sub_md))
    story.append(HRFlowable(width="100%", thickness=0.75, color=BORDER_COLOR, spaceAfter=12))

    demo_content = [
        [Paragraph("GEOMETRA (PRIMARY)", style_meta_label)],
        [Paragraph("Building Tomorrow's Vision Today", style_primary_md)],
        [Spacer(1, 4)],
        [Paragraph("MONTSERRAT BOLD (SUBHEADING)", style_meta_label)],
        [Paragraph("Architectural Accord & Modern Design Principles", style_sub_md)],
        [Spacer(1, 4)],
        [Paragraph("INTER / HELVETICA REGULAR (BODY COPY)", style_meta_label)],
        [Paragraph("At Arc Accord, we bridge the gap between bold geometric forms and functional spatial design. By utilizing clean linework and balanced proportions, our visual language establishes confidence and reliability across all touchpoints.", style_body_md)]
    ]
    
    t_demo = Table(demo_content, colWidths=[504])
    t_demo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WARM_CREAM),
        ('BOX', (0,0), (-1,-1), 1, SOFT_BEIGE),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(t_demo)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)

if __name__ == "__main__":
    create_pdf("Arc_Accord_Visual_Identity.pdf")

```