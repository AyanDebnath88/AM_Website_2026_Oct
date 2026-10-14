"""
AM Electricals company brochure — built entirely from real site content
(panels.json, site.ts, about.astro copy, industries/index.astro, live client
list). No invented stats, no stock imagery — matches the site's own anti-slop
copy rule.

Run: python build_brochure.py
Output: AM-Electricals-Company-Profile.pdf (same folder)

Structure (standard B2B manufacturer profile order):
  Cover -> About & scale -> Workshop & facility -> Certifications & quality
  -> Products (13 panel families, full spec) -> Industries served
  -> Clients & track record -> Contact
"""

import json
import os
import tempfile
from xml.sax.saxutils import escape as _esc

from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, KeepTogether, ListFlowable, ListItem,
)
from reportlab.lib.enums import TA_CENTER

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "..", "web", "src", "data")
IMAGES = os.path.join(BASE, "..", "web", "public", "images")
LOGO = os.path.join(BASE, "..", "web", "public", "logo.png")
OUT = os.path.join(BASE, "AM-Electricals-Company-Profile.pdf")

_TMP_DIR = tempfile.mkdtemp(prefix="am-brochure-")


def safe_image(path, width, height):
    """reportlab's Image flowable renders palette-mode (P) PNGs with alpha as
    blank. Normalise to RGBA via PIL first, same visual result either way."""
    img = PILImage.open(path)
    if img.mode in ("P", "PA", "LA"):
        img = img.convert("RGBA")
        tmp_path = os.path.join(_TMP_DIR, os.path.basename(path) + ".png")
        img.save(tmp_path)
        path = tmp_path
    return Image(path, width=width, height=height)


def P(text, style):
    """Paragraph with any data-derived text XML-escaped first — raw '&'
    (e.g. company names like 'L&T') otherwise breaks reportlab's parser."""
    return Paragraph(_esc(str(text)), styles[style] if isinstance(style, str) else style)

with open(os.path.join(SITE, "panels.json"), encoding="utf-8") as f:
    PANELS = json.load(f)

RED = colors.HexColor("#EC131A")
INK = colors.HexColor("#0A0A0A")
GREY = colors.HexColor("#595959")
LIGHT = colors.HexColor("#F5F5F3")
LINE = colors.HexColor("#E5E5E5")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle("Hero", parent=styles["Title"], fontSize=28, leading=32,
                           textColor=INK, spaceAfter=4))
styles.add(ParagraphStyle("SubHero", parent=styles["Normal"], fontSize=12, leading=16,
                           textColor=GREY, spaceAfter=18))
styles.add(ParagraphStyle("H1", parent=styles["Heading1"], fontSize=20, leading=24,
                           textColor=INK, spaceBefore=0, spaceAfter=10))
styles.add(ParagraphStyle("H2", parent=styles["Heading2"], fontSize=15, leading=18,
                           textColor=INK, spaceBefore=16, spaceAfter=8))
styles.add(ParagraphStyle("Kicker", parent=styles["Normal"], fontSize=8.5, leading=11,
                           textColor=RED, fontName="Helvetica-Bold", spaceAfter=4))
styles.add(ParagraphStyle("Body", parent=styles["Normal"], fontSize=10, leading=14,
                           textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle("Meta", parent=styles["Normal"], fontSize=8, leading=11,
                           textColor=GREY))
styles.add(ParagraphStyle("PanelName", parent=styles["Normal"], fontSize=12, leading=15,
                           textColor=INK, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle("PanelTagline", parent=styles["Normal"], fontSize=9, leading=12,
                           textColor=GREY, spaceAfter=6))
styles.add(ParagraphStyle("PanelOverview", parent=styles["Normal"], fontSize=9, leading=13,
                           textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle("SpecLabel", parent=styles["Normal"], fontSize=8, leading=11,
                           textColor=GREY))
styles.add(ParagraphStyle("SpecValue", parent=styles["Normal"], fontSize=8.5, leading=11,
                           textColor=INK, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle("Feature", parent=styles["Normal"], fontSize=8.5, leading=12,
                           textColor=INK))
styles.add(ParagraphStyle("CompBadge", parent=styles["Normal"], fontSize=7.5, leading=10,
                           textColor=RED, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle("TableHeader", parent=styles["Normal"], fontSize=9.5, leading=12,
                           textColor=colors.white, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle("StatNum", parent=styles["Normal"], fontSize=22, leading=24,
                           textColor=RED, fontName="Helvetica-Bold", alignment=TA_CENTER))
styles.add(ParagraphStyle("StatLabel", parent=styles["Normal"], fontSize=8, leading=10,
                           textColor=GREY, alignment=TA_CENTER))
styles.add(ParagraphStyle("IndustryName", parent=styles["Normal"], fontSize=10.5, leading=13,
                           textColor=INK, fontName="Helvetica-Bold", spaceAfter=3))
styles.add(ParagraphStyle("IndustryBody", parent=styles["Normal"], fontSize=8.5, leading=12,
                           textColor=GREY))

story = []


def hr():
    t = Table([[""]], colWidths=[174 * mm], rowHeights=[0.6])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.75, LINE)]))
    return t


def section_kicker_title(kicker, title):
    return [Paragraph(kicker.upper(), styles["Kicker"]), Paragraph(title, styles["H1"])]


# =============================================================================
# COVER
# =============================================================================
if os.path.exists(LOGO):
    story.append(safe_image(LOGO, 18 * mm, 18 * mm))
    story.append(Spacer(1, 10))

story.append(Paragraph("AM Electricals", styles["Hero"]))
story.append(Paragraph(
    "Control panel manufacturer, Kolkata &mdash; CPRI type-tested, "
    "ISO 9001:2008 certified, founder-led since 1991.",
    styles["SubHero"]))

stats = [
    ("34", "Years in business"),
    ("5,000", "Sqft Kolkata factory"),
    ("13", "Panel families"),
    ("70 kA / 1s", "MCC / PCC withstand"),
]
story.append(Table([[Paragraph(n, styles["StatNum"]) for n, _ in stats]],
                    colWidths=[42 * mm] * 4))
story.append(Table([[Paragraph(l, styles["StatLabel"]) for _, l in stats]],
                    colWidths=[42 * mm] * 4))
story.append(Spacer(1, 14))
story.append(hr())
story.append(Spacer(1, 10))
story.append(Paragraph(
    "Company profile prepared for prospective clients and procurement "
    "review. Covers facility, certifications, full product range, "
    "industries served and track record.",
    styles["Meta"]))

story.append(PageBreak())

# =============================================================================
# ABOUT
# =============================================================================
story += section_kicker_title("Established 1991", "Founder-led since 1991.")
story.append(Paragraph(
    "AM Electricals was founded in Kolkata by Ajit Debnath in 1991 to build "
    "control panels for Bengal's growing industrial base. 34 years later we "
    "still make what we sell, from our own 5,000 sqft factory on Kamardanga "
    "Road.",
    styles["Body"]))

story.append(Paragraph("The founder", styles["H2"]))
story.append(Paragraph(
    "Ajit started AM Electricals as a one-man workshop in 1991. Today he "
    "still reviews every non-standard job, every DG-sync SLD, every PLC "
    "panel wiring drawing. When an escalation lands, it lands on his phone. "
    "Three decades of returning customers who don't need to explain their "
    "site twice.",
    styles["Body"]))

story.append(Paragraph("Registered details", styles["H2"]))
registered = [
    ("Founded", "1991"),
    ("Founder / CEO", "Ajit Debnath"),
    ("Legal status", "Proprietorship Firm"),
    ("Business", "Manufacturer, Supplier, Service Provider"),
    ("Sector", "Control Panels and Boards"),
    ("Factory address", "7S Kamardanga Road, Near Anandapalit, Kolkata 700046"),
    ("Phone", "+91-7003707013"),
    ("Email", "amelectricals@yahoo.co.in"),
]
reg_rows = []
for i in range(0, len(registered), 2):
    pair = registered[i:i + 2]
    row = []
    for k, v in pair:
        row.append(Paragraph(f"<font color='#595959' size=8>{k}</font><br/>"
                              f"<font color='#0A0A0A' size=9.5><b>{v}</b></font>",
                              styles["Body"]))
    if len(row) == 1:
        row.append("")
    reg_rows.append(row)
reg_table = Table(reg_rows, colWidths=[87 * mm, 87 * mm])
reg_table.setStyle(TableStyle([
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE),
]))
story.append(reg_table)

story.append(PageBreak())

# =============================================================================
# WORKSHOP & FACILITY
# =============================================================================
story += section_kicker_title("The workshop", "Made where it's sold.")
story.append(Paragraph(
    "5,000 sqft permanent factory in Kolkata with 10 to 20 electrical "
    "engineers, draughtsmen, panel wiremen and test technicians. Every "
    "panel is built, wired, tested and FAT-signed here before dispatch. "
    "CPRI type-tested designs. ISO 9001:2008 quality process. IS 8623 / "
    "IEC 61439-2 as standard.",
    styles["Body"]))
story.append(Spacer(1, 8))

factory_photos = [
    ("panel-testing.jpg", "Panel testing before dispatch"),
    ("busbar-wiring.jpg", "Colour-coded busbar wiring"),
    ("amf-panel-build.jpg", "AMF control panel build"),
    ("panel-door-open.jpg", "Finished panel, door open"),
    ("contactor-wiring-detail.jpg", "Contactor wiring detail"),
    ("fire-pump-finished.jpg", "Fire pump panel, finished"),
]
row = []
for fname, caption in factory_photos:
    path = os.path.join(IMAGES, "factory", fname)
    if not os.path.exists(path):
        continue
    cell = [safe_image(path, 55 * mm, 42 * mm), Paragraph(caption, styles["Meta"])]
    row.append(cell)
    if len(row) == 3:
        t = Table([row], colWidths=[58 * mm] * 3)
        t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3 * mm),
        ]))
        story.append(t)
        story.append(Spacer(1, 8))
        row = []
if row:
    t = Table([row], colWidths=[58 * mm] * len(row))
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3 * mm),
    ]))
    story.append(t)

story.append(PageBreak())

# =============================================================================
# CERTIFICATIONS & QUALITY
# =============================================================================
story += section_kicker_title("Proof, not claims", "Certifications on file.")
story.append(Paragraph(
    "<b>CPRI</b> &mdash; Central Power Research Institute short-circuit "
    "withstand strength test, 70 kArms for 1.0 second with initial peak of "
    "154 kApk (verification report, LT switch board, 6000 A, non-extendable). "
    "<b>ISO 9001:2008</b> &mdash; Quality Management System certified. "
    "<b>MSME</b> &mdash; Entrepreneurs Memorandum registration, filed 1991.",
    styles["Body"]))
story.append(Spacer(1, 8))

cert_imgs = [
    ("certificates/cpri-test-report.jpg", "CPRI test report"),
    ("certificates/msme-registration.jpg", "MSME registration"),
]
cert_row = []
for rel, caption in cert_imgs:
    path = os.path.join(IMAGES, rel)
    if not os.path.exists(path):
        continue
    cert_row.append([safe_image(path, 60 * mm, 85 * mm), Paragraph(caption, styles["Meta"])])
if cert_row:
    t = Table([cert_row], colWidths=[64 * mm] * len(cert_row))
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
    ]))
    story.append(t)

story.append(Spacer(1, 10))
story.append(Paragraph("ISO 9001:2008 certificate and full CPRI test series available on request.",
                        styles["Meta"]))

story.append(PageBreak())

# =============================================================================
# PRODUCTS — all 13 panel families, full spec
# =============================================================================
story += section_kicker_title("The range", "13 panel families.")
story.append(Paragraph(
    "Every panel ships with a BOQ, SLD, GA drawing and FAT report. Built to "
    "spec for the site, not pulled off a shelf. Full detail for each family "
    "follows.",
    styles["Body"]))
story.append(Spacer(1, 6))

for p in PANELS:
    block = []
    block.append(P(p["name"], "PanelName"))
    block.append(P(p["tagline"], "PanelTagline"))
    block.append(P(p["overview"], "PanelOverview"))

    # Specs as a compact 2-col grid
    spec_items = p.get("specs", [])
    spec_rows = []
    for i in range(0, len(spec_items), 2):
        pair = spec_items[i:i + 2]
        row = []
        for spec in pair:
            row.append(Paragraph(
                f"<font color='#595959' size=7.5>{_esc(spec['label'])}</font><br/>"
                f"<font color='#0A0A0A' size=8.5><b>{_esc(spec['value'])}</b></font>",
                styles["Body"]))
        if len(row) == 1:
            row.append("")
        spec_rows.append(row)
    if spec_rows:
        spec_table = Table(spec_rows, colWidths=[87 * mm, 87 * mm])
        spec_table.setStyle(TableStyle([
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        block.append(spec_table)

    # Features as a tight bullet list
    features = p.get("features", [])
    if features:
        items = [ListItem(P(f, "Feature"), leftIndent=10, bulletColor=RED)
                  for f in features]
        block.append(Spacer(1, 4))
        block.append(ListFlowable(items, bulletType="bullet", start="•",
                                   leftIndent=12, bulletFontSize=7))

    # Compliance badges as inline text
    compliance = p.get("compliance", [])
    if compliance:
        block.append(Spacer(1, 4))
        block.append(Paragraph(" &nbsp;&middot;&nbsp; ".join(_esc(c) for c in compliance),
                                styles["CompBadge"]))

    block.append(Spacer(1, 4))
    block.append(hr())
    block.append(Spacer(1, 10))

    story.append(KeepTogether(block))

story.append(PageBreak())

# =============================================================================
# INDUSTRIES SERVED
# =============================================================================
industries = [
    ("Cement, Steel & Material Handling",
     "Conveyor, crusher and ash-handling duty: high motor counts, dusty "
     "sites, heavy restart current. We build MCC and PCC panels with Form "
     "4b segregation so one feeder fault does not drop the line."),
    ("Water, Effluent & Sewage Treatment",
     "STP, ETP and WTP panels for municipal and industrial plants: pump "
     "and dosing motor control, filter and aerator sequencing, IP54 "
     "enclosures for a wet plant room."),
    ("Chemical, Petrochemical & Pharma",
     "Batch process control and fire/gas safety panels for chemical and "
     "pharma sites, built to the segregation and labelling a safety audit "
     "actually checks for."),
    ("Food & Beverage Processing",
     "PLC-driven batching, washdown-duty enclosures and power factor "
     "correction for plants running compressors and refrigeration most of "
     "the day."),
    ("Commercial Real Estate & Hospitality",
     "Malls, hotels and hospitals: HVAC and AHU control, metering panels "
     "per tenant or floor, and DG/AMF changeover that switches over before "
     "anyone in the lobby notices."),
    ("Data Centres & Telecom",
     "Uptime depends on the changeover panel, not just the generator. "
     "AMF/DG sync panels with no manual reset step, plus APFC to keep the "
     "incoming supply penalty-free."),
    ("Utilities, Residential & Small Industry",
     "Single-DG control panels and distribution boards sized for a "
     "housing complex, a small factory or a utility substation, not "
     "over-specified for either."),
    ("Custom Process Plants",
     "Jute and textile mills, boiler houses, furnace and burner lines, oil "
     "refineries: non-catalogue panels built off your SLD, not ours."),
]

story += section_kicker_title("Where our panels run", "Industries we build for.")
story.append(Paragraph(
    "Thirty-four years of panels built to spec for specific sites, not a "
    "catalogue. Eight sectors below cover most of what we build; if yours "
    "isn't listed, it's probably still a custom panel we can quote.",
    styles["Body"]))
story.append(Spacer(1, 8))

ind_rows = []
for i in range(0, len(industries), 2):
    pair = industries[i:i + 2]
    row = []
    for name, body in pair:
        cell = [P(name, "IndustryName"), P(body, "IndustryBody")]
        row.append(cell)
    if len(row) == 1:
        row.append("")
    ind_rows.append(row)

ind_table = Table(ind_rows, colWidths=[87 * mm, 87 * mm])
ind_table.setStyle(TableStyle([
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story.append(ind_table)

story.append(PageBreak())

# =============================================================================
# CLIENTS & TRACK RECORD
# =============================================================================
story += section_kicker_title("Track record", "Panels running on site for.")
story.append(Paragraph(
    "A selection of the organisations currently running AM Electricals "
    "panels on site. Full reference list and site visits available on "
    "request.",
    styles["Body"]))
story.append(Spacer(1, 10))

clients = [
    ("landt.png", "L&T Construction", True),   # logo is white — needs a dark backdrop
    ("patton.png", "Patton", False),
    ("qualicom.png", "Qualicom Solutions", False),
    ("scs-econ.png", "Steam & Control Systems", False),
    ("ovaron.png", "Ovaron Infrastructure & MEP", False),
    ("herringbone.png", "Herringbone Technical Services", False),
    ("wesman.webp", "Wesman", False),
]
# Ipsen ships as SVG — reportlab/PIL can't rasterise it without an extra
# dependency, so it's listed by name alongside the logo images below.
client_names_only = ["Ipsen"]

client_cells = []
row = []
for fname, name, dark in clients:
    path = os.path.join(IMAGES, "clients", fname)
    if not os.path.exists(path):
        client_names_only.append(name)
        continue
    try:
        logo = safe_image(path, 38 * mm, 16 * mm)
        if dark:
            logo_wrap = Table([[logo]], colWidths=[40 * mm], rowHeights=[18 * mm])
            logo_wrap.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), INK),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]))
            logo = logo_wrap
        cell = [logo, P(name, "Meta")]
    except Exception:
        client_names_only.append(name)
        continue
    row.append(cell)
    if len(row) == 3:
        client_cells.append(row)
        row = []
if row:
    client_cells.append(row)

for r in client_cells:
    t = Table([r], colWidths=[58 * mm] * len(r))
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(t)

if client_names_only:
    story.append(Spacer(1, 6))
    story.append(P("Also: " + ", ".join(client_names_only), "Meta"))

story.append(PageBreak())

# =============================================================================
# CONTACT
# =============================================================================
story += section_kicker_title("Get in touch", "Send the spec. We reply in a day.")
story.append(Paragraph(
    "SLD, load list, or a photo of the existing panel. Fastest is "
    "WhatsApp. Everything is reviewed by our founder before we quote.",
    styles["Body"]))
story.append(Spacer(1, 10))

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
    colWidths=[30 * mm, 144 * mm],
)
contact_table.setStyle(TableStyle([
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
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
