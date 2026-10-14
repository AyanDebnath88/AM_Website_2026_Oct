"""
AM Electricals company brochure — built from real site content only.
Run: python build_brochure.py
Output: AM-Electricals-Company-Profile.pdf (same folder)
"""

import json
import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, KeepTogether,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "..", "web", "src", "data")
IMAGES = os.path.join(BASE, "..", "web", "public", "images")
LOGO = os.path.join(BASE, "..", "web", "public", "logo.png")
OUT = os.path.join(BASE, "AM-Electricals-Company-Profile.pdf")

with open(os.path.join(SITE, "panels.json"), encoding="utf-8") as f:
    PANELS = json.load(f)

RED = colors.HexColor("#EC131A")
INK = colors.HexColor("#0A0A0A")
GREY = colors.HexColor("#595959")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle("Hero", parent=styles["Title"], fontSize=26, leading=30,
                           textColor=INK, spaceAfter=4))
styles.add(ParagraphStyle("SubHero", parent=styles["Normal"], fontSize=12, leading=16,
                           textColor=GREY, spaceAfter=18))
styles.add(ParagraphStyle("H2", parent=styles["Heading2"], fontSize=15, leading=18,
                           textColor=INK, spaceBefore=18, spaceAfter=8))
styles.add(ParagraphStyle("Body", parent=styles["Normal"], fontSize=10, leading=14,
                           textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle("Meta", parent=styles["Normal"], fontSize=8, leading=11,
                           textColor=GREY))
styles.add(ParagraphStyle("PanelName", parent=styles["Normal"], fontSize=10, leading=13,
                           textColor=INK, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle("PanelHeader", parent=styles["Normal"], fontSize=10, leading=13,
                           textColor=colors.white, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle("PanelTagline", parent=styles["Normal"], fontSize=8.5, leading=11,
                           textColor=GREY))
styles.add(ParagraphStyle("StatNum", parent=styles["Normal"], fontSize=20, leading=22,
                           textColor=RED, fontName="Helvetica-Bold", alignment=TA_CENTER))
styles.add(ParagraphStyle("StatLabel", parent=styles["Normal"], fontSize=8, leading=10,
                           textColor=GREY, alignment=TA_CENTER))

story = []

# --- Header -----------------------------------------------------------------
if os.path.exists(LOGO):
    story.append(Image(LOGO, width=14 * mm, height=14 * mm))
    story.append(Spacer(1, 6))

story.append(Paragraph("AM Electricals", styles["Hero"]))
story.append(Paragraph(
    "Control panel manufacturer, Kolkata &mdash; CPRI type-tested, "
    "ISO 9001:2008 certified, founder-led since 1991.",
    styles["SubHero"]))

# --- Stats row ---------------------------------------------------------------
stats = [
    ("34", "Years in business"),
    ("5,000", "Sqft Kolkata factory"),
    ("13", "Panel families"),
    ("70 kA / 1s", "MCC / PCC withstand"),
]
stat_cells = [[Paragraph(n, styles["StatNum"]), Paragraph(l, styles["StatLabel"])]
              for n, l in stats]
stat_table = Table(
    [[Paragraph(n, styles["StatNum"]) for n, _ in stats]],
    colWidths=[42 * mm] * 4,
)
stat_labels = Table(
    [[Paragraph(l, styles["StatLabel"]) for _, l in stats]],
    colWidths=[42 * mm] * 4,
)
story.append(stat_table)
story.append(stat_labels)
story.append(Spacer(1, 10))

# --- About --------------------------------------------------------------------
story.append(Paragraph("About", styles["H2"]))
story.append(Paragraph(
    "AM Electricals was founded in Kolkata by Ajit Debnath in 1991 to build "
    "control panels for Bengal's growing industrial base. 34 years later we "
    "still make what we sell, from our own 5,000 sqft factory on Kamardanga "
    "Road. Panels are built to IS 8623 (aligned with IEC 61439-2), with "
    "CPRI type-tested designs and an ISO 9001:2008 quality process "
    "throughout.",
    styles["Body"]))

# --- Certifications -------------------------------------------------------
story.append(Paragraph("Certifications", styles["H2"]))
story.append(Paragraph(
    "<b>CPRI</b> &mdash; Central Power Research Institute short-circuit "
    "withstand strength test, 70 kArms for 1.0 second (verification report, "
    "LT switch board, 6000 A). <b>ISO 9001:2008</b> &mdash; Quality "
    "Management System certified.",
    styles["Body"]))

cert_img = os.path.join(IMAGES, "certificates", "cpri-test-report.jpg")
if os.path.exists(cert_img):
    story.append(Spacer(1, 6))
    story.append(Image(cert_img, width=55 * mm, height=78 * mm))

story.append(PageBreak())

# --- Factory photos --------------------------------------------------------
story.append(Paragraph("On the shopfloor", styles["H2"]))
factory_photos = [
    ("panel-testing.jpg", "Panel testing before dispatch"),
    ("busbar-wiring.jpg", "Colour-coded busbar wiring"),
    ("amf-panel-build.jpg", "AMF control panel build"),
    ("panel-door-open.jpg", "Finished panel, door open"),
]
photo_cells = []
row = []
for fname, caption in factory_photos:
    path = os.path.join(IMAGES, "factory", fname)
    if not os.path.exists(path):
        continue
    cell = [Image(path, width=78 * mm, height=58 * mm),
            Paragraph(caption, styles["Meta"])]
    row.append(cell)
    if len(row) == 2:
        photo_cells.append(row)
        row = []
if row:
    photo_cells.append(row)

for pair in photo_cells:
    t = Table([pair], colWidths=[82 * mm, 82 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

story.append(PageBreak())

# --- Panel families table --------------------------------------------------
story.append(Paragraph("13 panel families", styles["H2"]))
story.append(Paragraph(
    "Every panel ships with a BOQ, SLD, GA drawing and FAT report. Built "
    "to spec for the site, not pulled off a shelf.",
    styles["Body"]))
story.append(Spacer(1, 6))

rows = [[Paragraph("Panel family", styles["PanelHeader"]),
         Paragraph("Spec", styles["PanelHeader"])]]
for p in PANELS:
    rows.append([
        Paragraph(p["name"], styles["PanelName"]),
        Paragraph(p["tagline"], styles["PanelTagline"]),
    ])

panel_table = Table(rows, colWidths=[55 * mm, 108 * mm], repeatRows=1)
panel_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), INK),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("LINEBELOW", (0, 0), (-1, 0), 0.5, INK),
    ("LINEBELOW", (0, 1), (-1, -1), 0.5, colors.HexColor("#E5E5E5")),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
]))
story.append(panel_table)

story.append(Spacer(1, 16))

# --- Contact ----------------------------------------------------------------
story.append(Paragraph("Get in touch", styles["H2"]))
contact_rows = [
    ["Phone", "+91-7003707013"],
    ["WhatsApp", "Click to chat &mdash; wa.me/917003707013"],
    ["Email", "amelectricals@yahoo.co.in"],
    ["Factory", "7S Kamardanga Road, Near Anandapalit, Kolkata 700046, West Bengal"],
    ["Website", "amelectricals.co.in"],
]
contact_table = Table(
    [[Paragraph(f"<b>{k}</b>", styles["Body"]), Paragraph(v, styles["Body"])]
     for k, v in contact_rows],
    colWidths=[30 * mm, 133 * mm],
)
contact_table.setStyle(TableStyle([
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))
story.append(contact_table)

doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    topMargin=18 * mm, bottomMargin=18 * mm,
    leftMargin=18 * mm, rightMargin=18 * mm,
    title="AM Electricals — Company Profile",
)
doc.build(story)
print(f"Built: {OUT}")
