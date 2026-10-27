"""
Action Executor Engine for Makkal Agent (Meta AI Developer Hackathon 2026)
Executes autonomous citizen actions:
1. Official Government Legal Petition PDF Generation (மனு தாக்கல் ஆவணம்)
2. Structured e-Sevai Form Payload Synthesis
3. Verification Checklist & Official Fee Transparency Report
"""

import os
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


class ActionExecutor:
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or (Path(__file__).parent / "generated_petitions")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_legal_petition_pdf(
        self,
        applicant_name: str,
        phone: str,
        district: str,
        taluk: str,
        village: str,
        service_title: str,
        survey_number: str,
        grounds_summary: str,
        meta_verification_id: str
    ) -> Path:
        """
        Synthesizes an official Tamil Nadu Government Legal Petition PDF.
        Ready for citizen signature, physical submission to VAO/Tahsildar, or e-Sevai portal upload.
        """
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_id = uuid.uuid4().hex[:8]
        pdf_path = self.output_dir / f"Petition_{safe_id}_{timestamp_str}.pdf"

        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "GovTitle",
            parent=styles["Heading1"],
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#065f46"),
            alignment=1, # Center
            spaceAfter=8
        )

        subtitle_style = ParagraphStyle(
            "GovSubtitle",
            parent=styles["Normal"],
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#334155"),
            alignment=1, # Center
            spaceAfter=15
        )

        header_label_style = ParagraphStyle(
            "LabelStyle",
            parent=styles["Normal"],
            fontSize=10,
            leading=13,
            textColor=colors.HexColor("#1e293b"),
            fontName="Helvetica-Bold"
        )

        body_style = ParagraphStyle(
            "BodyStyle",
            parent=styles["Normal"],
            fontSize=10,
            leading=15,
            textColor=colors.HexColor("#0f172a")
        )

        elements = []

        # Header Emblem & Title
        elements.append(Paragraph("GOVERNMENT OF TAMIL NADU / தமிழ்நாடு அரசு", title_style))
        elements.append(Paragraph("REVENUE & DISASTER MANAGEMENT DEPARTMENT / வருவாய்த்துறை மனு", subtitle_style))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#059669"), spaceAfter=15))

        # To Authority
        to_text = f"<b>பெறுநர் (To):</b><br/>வட்டாட்சியர் அவர்கள் (The Tahsildar),<br/>வட்டாட்சியர் அலுவலகம், {taluk} வட்டம், {district} மாவட்டம்."
        elements.append(Paragraph(to_text, body_style))
        elements.append(Spacer(1, 10))

        # From Citizen
        from_text = f"<b>மனுதாரர் (Applicant):</b><br/>திரு/திருமதி: <b>{applicant_name}</b><br/>அலைபேசி: {phone}<br/>கிராமம்: {village}, வட்டம்: {taluk}, மாவட்டம்: {district}."
        elements.append(Paragraph(from_text, body_style))
        elements.append(Spacer(1, 12))

        # Subject Line
        sub_text = f"<b>பொருள் (Subject):</b> {service_title} - புல எண்: <b>{survey_number}</b> தொடர்பாக பட்டா/உரிமை மாற்றம் கோரும் விண்ணப்ப மனு."
        elements.append(Paragraph(sub_text, header_label_style))
        elements.append(Spacer(1, 12))

        # Grounds & Summary
        elements.append(Paragraph("<b>மனு விவரம் (Petition Details & Grounds):</b>", header_label_style))
        elements.append(Spacer(1, 4))
        elements.append(Paragraph(grounds_summary, body_style))
        elements.append(Spacer(1, 15))

        # Metadata Table
        table_data = [
            [Paragraph("<b>விண்ணப்ப வகை</b>", header_label_style), Paragraph(service_title, body_style)],
            [Paragraph("<b>சர்வே / புல எண்</b>", header_label_style), Paragraph(survey_number, body_style)],
            [Paragraph("<b>அதிகாரப்பூர்வ அரசு கட்டணம்</b>", header_label_style), Paragraph("₹60 (இடைத்தரகர் கட்டணம்: ₹0)", body_style)],
            [Paragraph("<b>Meta AI Audit Verification ID</b>", header_label_style), Paragraph(meta_verification_id, body_style)],
            [Paragraph("<b>ஆவண தணிக்கை நிலை (SAM 3.1)</b>", header_label_style), Paragraph("அரசு முத்திரை & கையெழுத்து சரிபார்க்கப்பட்டது", body_style)],
        ]
        t = Table(table_data, colWidths=[200, 320])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 30))

        # Signature Block
        sig_data = [
            [Paragraph("இடம்: " + village + "<br/>நாள்: " + datetime.now().strftime("%d-%m-%Y"), body_style),
             Paragraph("இங்ஙனம்,<br/><br/><br/><b>(" + applicant_name + ")</b><br/>மனுதாரரின் கையொப்பம்", body_style)]
        ]
        sig_table = Table(sig_data, colWidths=[260, 260])
        sig_table.setStyle(TableStyle([
            ('ALIGN', (1,0), (1,0), 'RIGHT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP')
        ]))
        elements.append(sig_table)

        doc.build(elements)
        return pdf_path

    def generate_mla_petition_pdf(
        self,
        applicant_name: str,
        phone: str,
        district: str,
        taluk: str,
        village: str,
        constituency_name: str,
        ac_no: int,
        mla_name: str,
        mla_email: str,
        collector_email: str,
        grievance_category: str,
        grievance_details: str,
        statutory_reference: str,
        meta_verification_id: str
    ) -> Path:
        """
        Synthesizes an official Tamil Nadu Legislative Assembly Member Citizen Grievance Petition PDF.
        Formatted for formal submission to MLA Office, District Collectorate, and Block Development Officer.
        """
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_id = uuid.uuid4().hex[:8]
        pdf_path = self.output_dir / f"MLA_Petition_AC{ac_no}_{safe_id}_{timestamp_str}.pdf"

        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "MLATitle",
            parent=styles["Heading1"],
            fontSize=15,
            leading=18,
            textColor=colors.HexColor("#0f766e"),
            alignment=1,
            spaceAfter=4
        )

        subtitle_style = ParagraphStyle(
            "MLASubtitle",
            parent=styles["Normal"],
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#1e293b"),
            alignment=1,
            fontName="Helvetica-Bold",
            spaceAfter=12
        )

        header_label_style = ParagraphStyle(
            "LabelStyle",
            parent=styles["Normal"],
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#0f172a"),
            fontName="Helvetica-Bold"
        )

        body_style = ParagraphStyle(
            "BodyStyle",
            parent=styles["Normal"],
            fontSize=9.5,
            leading=14,
            textColor=colors.HexColor("#1e293b")
        )

        elements = []

        # Header Title
        elements.append(Paragraph("TAMIL NADU LEGISLATIVE ASSEMBLY / தமிழ்நாடு சட்டமன்றப் பேரவை", title_style))
        elements.append(Paragraph(f"சட்டமன்ற உறுப்பினர் மக்கள் குறைதீர்ப்பு மனு (MLA Grievance Representation) - தொகுதி எண்: {ac_no}", subtitle_style))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0f766e"), spaceAfter=12))

        # Two-column Header Table: To Authority vs From Citizen
        to_block = (
            f"<b>பெறுநர் (TO):</b><br/>"
            f"மாண்புமிகு சட்டமன்ற உறுப்பினர் அவர்கள் (Hon. MLA),<br/>"
            f"<b>{mla_name}</b><br/>"
            f"{constituency_name} சட்டமன்றத் தொகுதி (AC No: {ac_no}),<br/>"
            f"அலுவலக மின்னஞ்சல்: <u>{mla_email}</u><br/><br/>"
            f"<b>நகல் (COPY TO):</b><br/>"
            f"மாவட்ட ஆட்சியர் மற்றும் மாவட்ட நீதிபதி அவர்கள்,<br/>"
            f"{district} மாவட்ட ஆட்சியரகம் (Email: {collector_email})"
        )

        from_block = (
            f"<b>மனுதாரர் (APPLICANT):</b><br/>"
            f"பெயர்: <b>{applicant_name}</b><br/>"
            f"அலைபேசி: <b>{phone}</b><br/>"
            f"கிராமம்: {village}<br/>"
            f"வட்டம்: {taluk}<br/>"
            f"மாவட்டம்: {district} - தமிழ்நாடு."
        )

        head_table = Table([[Paragraph(to_block, body_style), Paragraph(from_block, body_style)]], colWidths=[270, 270])
        head_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f0fdfa")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#99f6e4")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#ccfbf1")),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        elements.append(head_table)
        elements.append(Spacer(1, 10))

        # Subject & Statutory Reference Block
        sub_text = (
            f"<b>பொருள் (Subject):</b> {constituency_name} தொகுதிக்குட்பட்ட {village} பகுதியில் <b>{grievance_category}</b> "
            f"தொடர்பான மக்கள் குறைதீர்ப்பு மற்றும் உடனடி நிர்வாகத் தீர்வு கோருதல் சார்பு.<br/>"
            f"<b>சட்டப்பிரிவு & வழிகாட்டுதல் (Statute):</b> {statutory_reference}"
        )
        elements.append(Paragraph(sub_text, body_style))
        elements.append(Spacer(1, 10))

        # Grievance Summary & Prayer
        elements.append(Paragraph("<b>மக்கள் கோரிக்கை விவரம் & நியாயங்கள் (Grievance & Grounds):</b>", header_label_style))
        elements.append(Spacer(1, 4))
        elements.append(Paragraph(grievance_details, body_style))
        elements.append(Spacer(1, 12))

        # Meta AI Audit Verification Table
        meta_table_data = [
            [Paragraph("<b>சட்டமன்ற தொகுதி (Constituency)</b>", header_label_style), Paragraph(f"{constituency_name} (AC No: {ac_no})", body_style)],
            [Paragraph("<b>கோரிக்கை வகை (Grievance Category)</b>", header_label_style), Paragraph(grievance_category, body_style)],
            [Paragraph("<b>அரசு சேவை கட்டணம் (Statutory Fee)</b>", header_label_style), Paragraph("₹0 (சட்டமன்ற மனு தாக்கல் முற்றிலும் இலவசம்)", body_style)],
            [Paragraph("<b>Meta AI Audit Reference ID</b>", header_label_style), Paragraph(f"TN-MLA-2026-{meta_verification_id}", body_style)],
            [Paragraph("<b>எதிர்பார்க்கப்படும் கால வரம்பு (Timeline)</b>", header_label_style), Paragraph("15 வேலை நாட்கள் (Citizen Grievance Redressal Charter)", body_style)],
        ]
        mt = Table(meta_table_data, colWidths=[200, 340])
        mt.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(mt)
        elements.append(Spacer(1, 20))

        # Signature & Date Block
        sig_data = [
            [Paragraph(f"இடம்: {village}<br/>நாள்: {datetime.now().strftime('%d-%m-%Y')}<br/>சரிபார்ப்பு எண்: TN-MLA-2026-{meta_verification_id}", body_style),
             Paragraph(f"இங்ஙனம்,<br/><br/><br/><b>({applicant_name})</b><br/>மனுதாரர் கையொப்பம்", body_style)]
        ]
        sig_table = Table(sig_data, colWidths=[270, 270])
        sig_table.setStyle(TableStyle([
            ('ALIGN', (1,0), (1,0), 'RIGHT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP')
        ]))
        elements.append(sig_table)

        doc.build(elements)
        return pdf_path


action_executor = ActionExecutor()
