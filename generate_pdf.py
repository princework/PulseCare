from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageTemplate, Frame
)

def header_footer(canvas, doc, logo_path="static/logo.png"):
    """Function to create a header and footer with a logo."""
    canvas.saveState()
    
    # **Header with Logo and Title**
    if logo_path:
        try:
            # Logo at the left
            canvas.drawImage(logo_path, 0.5 * inch, 9.5 * inch, width=1.2 * inch, height=1.2 * inch, 
                             preserveAspectRatio=True, mask="auto")
        except:
            pass  # If logo path is incorrect, continue

    # **Title Positioned Next to Logo**
    canvas.setFont("Times-Bold", 18)
    canvas.setFillColor(colors.black)
    canvas.drawString(2 * inch, 10 * inch, "IOT Health Care Monitoring - Medical Report")

    # **Footer**
    canvas.setFont("Times-Roman", 11)
    canvas.setFillColor(colors.black)

    footer_text1 = "Designed and Developed by Prince 22BCS50125, Shagun Rana 22BCS17289 , Mohit Dogra 22BCS11438 "
    footer_text2 = "Under the supervision of ER.Monika Kumari (E-17771) Department. of CSE 3rd Year, Chandigarh University"

    canvas.drawString(inch, 0.9 * inch, footer_text1)
    canvas.drawString(inch, 0.7 * inch, footer_text2)
    
    canvas.restoreState()


def create_pdf(name, age, blood_group, image_path=None, pulse_data_path=None, logo_path="static/logo.png"):
    """Function to generate a patient medical report with a logo."""
    pdf_path = f"static/{name}_report.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)

    elements = []
    styles = getSampleStyleSheet()

    # **Patient Information Table**
    user_data = [
        ["Patient Name:", name],
        ["Age:", str(age)],
        ["Blood Group:", blood_group]
    ]
    user_table = Table(user_data, colWidths=[200, 300], hAlign="CENTER")
    user_table.setStyle(TableStyle([
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey)
    ]))
    elements.append(user_table)
    elements.append(Spacer(1, 0.5 * inch))

    # **Patient Image Section**
    elements.append(Paragraph("<b>Patient Image:</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))
    if image_path:
        img = Image(image_path, width=1.5 * inch, height=1.5 * inch)
        img.hAlign = "LEFT"
        elements.append(img)
    else:
        elements.append(Paragraph("<i>No Image Captured</i>", styles["Normal"]))

    elements.append(Spacer(1, 0.5 * inch))

    # **Pulse Data Section**
    elements.append(Paragraph("<b>Pulse Sensor Data:</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.1 * inch))
    if pulse_data_path:
        pulse_img = Image(pulse_data_path, width=4.5 * inch, height=2.5 * inch)
        pulse_img.hAlign = "CENTER"
        elements.append(pulse_img)
    else:
        elements.append(Paragraph("<i>No IOT sensor data available. Connect the devices to get results.</i>", styles["Normal"]))

    elements.append(Spacer(1, 0.5 * inch))

    # **Placeholder for Future Health Graphs**
    elements.append(Paragraph("<b>Health Data Graphs:</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(Paragraph("<i>Graph not available. Thinkspeak data not found Connect device to check results.</i>", styles["Normal"]))
    elements.append(Spacer(1, 1 * inch))

    # **Building the PDF with Header, Footer, and Logo**
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 1 * inch, id="normal")
    template = PageTemplate(id="main", frames=frame, onPage=lambda canvas, doc: header_footer(canvas, doc, logo_path))
    doc.addPageTemplates([template])

    doc.build(elements)

    return pdf_path
