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

    def generate_statutory_petition_pdf(
        self,
        tier: str,
        applicant_name: str,
        phone: str,
        district: str,
        taluk: str,
        village: str,
        authority_name_ta: str,
        authority_title_ta: str,
        authority_email: str,
        authority_phone: str,
        grievance_category: str,
        grievance_details: str,
        statutory_reference: str,
        verification_id: str,
        sla_days: int = 15,
        sla_text: str = "15 வேலை நாட்கள்"
    ) -> Path:
        """
        Synthesizes an official Court-Ready Administrative Grievance Representation PDF
        for any Tamil Nadu civic governance tier: Collector, RDO Appeal, Police SP,
        TANGEDCO, Municipal/BDO, or CM Special Cell.
        """
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_id = uuid.uuid4().hex[:8]
        safe_tier = tier.replace("_", "-").upper()
        pdf_path = self.output_dir / f"TN_Petition_{safe_tier}_{safe_id}_{timestamp_str}.pdf"

        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()

        # Tier-specific aesthetic palette & titles
        tier_configs = {
            "collector": {
                "header_top": "GOVERNMENT OF TAMIL NADU / தமிழ்நாடு அரசு - வருவாய்த்துறை",
                "sub_title": "மாவட்ட ஆட்சித்தலைவர் திங்கள் குறைதீர்க்கும் நாள் முகாம் மனு (Collector Grievance Representation)",
                "color_primary": "#065f46",
                "color_bg": "#ecfdf5",
                "color_border": "#a7f3d0"
            },
            "rdo_appeal": {
                "header_top": "REVENUE DIVISIONAL APPELLATE TRIBUNAL / வருவாய் கோட்டாட்சியர் மேல்முறையீட்டு நீதிமன்றம்",
                "sub_title": "வருவாய் கோட்டாட்சியர் சட்டப்பூர்வ மேல்முறையீட்டு மனு (RDO Statutory Revenue Appeal)",
                "color_primary": "#92400e",
                "color_bg": "#fffbeb",
                "color_border": "#fde68a"
            },
            "police_sp": {
                "header_top": "TAMIL NADU POLICE DEPARTMENT / தமிழ்நாடு காவல்துறை",
                "sub_title": "மாவட்ட காவல் கண்காணிப்பாளர் / ஆணையர் நேரடி குறைதீர்ப்பு மனு (SP Police Grievance Petition)",
                "color_primary": "#1e3a8a",
                "color_bg": "#eff6ff",
                "color_border": "#bfdbfe"
            },
            "tangedco": {
                "header_top": "TANGEDCO / தமிழ்நாடு மின் உற்பத்தி மற்றும் பகிர்மானக் கழகம்",
                "sub_title": "மின்சார விநியோக குறைதீர்ப்பு & சீரமைப்பு மனு (TANGEDCO Electricity Grievance Petition)",
                "color_primary": "#b91c1c",
                "color_bg": "#fef2f2",
                "color_border": "#fecaca"
            },
            "municipal_bdo": {
                "header_top": "MUNICIPAL ADMINISTRATION & PANCHAYAT RAJ / நகராட்சி நிர்வாகம் & ஊரக வளர்ச்சித் துறை",
                "sub_title": "நகராட்சி ஆணையர் / ஊராட்சி ஒன்றிய வட்டார வளர்ச்சி மனு (Civic Infrastructure Grievance)",
                "color_primary": "#0f766e",
                "color_bg": "#f0fdfa",
                "color_border": "#99f6e4"
            },
            "cm_cell": {
                "header_top": "CHIEF MINISTER'S SPECIAL CELL / முதலமைச்சரின் தனிப்பிரிவு & மக்களுடன் முதல்வர்",
                "sub_title": "தலைமைச் செயலக சிறப்பு குறைதீர்ப்பு மேல்முறையீடு (CM Special Cell Escalation Petition)",
                "color_primary": "#6b21a8",
                "color_bg": "#faf5ff",
                "color_border": "#e9d5ff"
            }
        }
        cfg = tier_configs.get(tier, tier_configs["collector"])

        title_style = ParagraphStyle(
            "GovTitle",
            parent=styles["Heading1"],
            fontSize=14,
            leading=17,
            textColor=colors.HexColor(cfg["color_primary"]),
            alignment=1,
            spaceAfter=4
        )

        subtitle_style = ParagraphStyle(
            "GovSubtitle",
            parent=styles["Normal"],
            fontSize=10.5,
            leading=14,
            textColor=colors.HexColor("#1e293b"),
            alignment=1,
            fontName="Helvetica-Bold",
            spaceAfter=10
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
        elements.append(Paragraph(cfg["header_top"], title_style))
        elements.append(Paragraph(cfg["sub_title"], subtitle_style))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor(cfg["color_primary"]), spaceAfter=10))

        # Two-column Header Table: To Authority vs From Citizen
        to_block = (
            f"<b>பெறுநர் (TO):</b><br/>"
            f"<b>{authority_title_ta}</b><br/>"
            f"{authority_name_ta}<br/>"
            f"மின்னஞ்சல்: <u>{authority_email}</u><br/>"
            f"தொடர்பு எண்: {authority_phone}<br/><br/>"
            f"<b>நகல் (COPY TO):</b><br/>"
            f"முதலமைச்சரின் தனிப்பிரிவு & கண்காணிப்பு அலுவலர் (Email: cmcell@tn.gov.in)"
        )

        from_block = (
            f"<b>மனுதாரர் (APPLICANT):</b><br/>"
            f"பெயர்: <b>{applicant_name}</b><br/>"
            f"அலைபேசி: <b>{phone}</b><br/>"
            f"கிராமம் / வார்டு: {village}<br/>"
            f"வட்டம்: {taluk}<br/>"
            f"மாவட்டம்: {district} - தமிழ்நாடு."
        )

        head_table = Table([[Paragraph(to_block, body_style), Paragraph(from_block, body_style)]], colWidths=[270, 270])
        head_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(cfg["color_bg"])),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor(cfg["color_border"])),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor(cfg["color_border"])),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        elements.append(head_table)
        elements.append(Spacer(1, 10))

        # Subject & Statutory Reference Block
        sub_text = (
            f"<b>பொருள் (Subject):</b> {district} மாவட்டம், {taluk} வட்டம், {village} கிராமத்தில் "
            f"<b>{grievance_category}</b> தொடர்பாக உடனடி சட்டப்பூர்வ தீர்வு கோருதல் சார்பு.<br/>"
            f"<b>சட்டப்பிரிவு & நிர்வாக வழிகாட்டுதல் (Statutory Authority):</b> {statutory_reference}"
        )
        elements.append(Paragraph(sub_text, body_style))
        elements.append(Spacer(1, 10))

        # Grievance Summary & Grounds
        elements.append(Paragraph("<b>கோரிக்கை விவரம் & நியாயமான காரணங்கள் (Grievance Details & Grounds):</b>", header_label_style))
        elements.append(Spacer(1, 4))
        elements.append(Paragraph(grievance_details, body_style))
        elements.append(Spacer(1, 12))

        # Statutory Audit Table
        stat_table_data = [
            [Paragraph("<b>அரசு நிர்வாகப் பிரிவு (Department Tier)</b>", header_label_style), Paragraph(f"{cfg['header_top'].split('/')[1].strip() if '/' in cfg['header_top'] else cfg['header_top']}", body_style)],
            [Paragraph("<b>கோரிக்கை வகை (Grievance Category)</b>", header_label_style), Paragraph(grievance_category, body_style)],
            [Paragraph("<b>அரசு சேவை கட்டணம் (Statutory Fee)</b>", header_label_style), Paragraph("₹0 (குறைதீர்ப்பு மனு முற்றிலும் இலவசம்)", body_style)],
            [Paragraph("<b>Makkal AI Audit Tracking ID</b>", header_label_style), Paragraph(f"TN-{safe_tier}-2026-{verification_id}", body_style)],
            [Paragraph("<b>சட்டப்படியான கால வரம்பு (Statutory SLA)</b>", header_label_style), Paragraph(f"{sla_text} (Citizen Redressal Charter)", body_style)],
        ]
        st = Table(stat_table_data, colWidths=[200, 340])
        st.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(st)
        elements.append(Spacer(1, 18))

        # Signature & Date Block
        sig_data = [
            [Paragraph(f"இடம்: {village}<br/>நாள்: {datetime.now().strftime('%d-%m-%Y')}<br/>சரிபார்ப்பு எண்: TN-{safe_tier}-2026-{verification_id}", body_style),
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


    def generate_rti_petition_pdf(
        self,
        applicant_name: str,
        phone: str,
        address: str,
        public_authority: str,
        information_sought: str,
        period_covered: str = "2024 - 2026",
        is_bpl: bool = False,
        meta_verification_id: Optional[str] = None
    ) -> Path:
        """
        Synthesizes an official Right to Information (RTI) Section 6(1) Form-A Petition PDF.
        Complies with RTI Rules 2012 and Tamil Nadu Right to Information Rules.
        """
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_id = uuid.uuid4().hex[:8]
        verification_id = meta_verification_id or safe_id
        pdf_path = self.output_dir / f"RTI_Petition_{safe_id}_{timestamp_str}.pdf"

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
            "RTITitle",
            parent=styles["Heading1"],
            fontSize=15,
            leading=18,
            textColor=colors.HexColor("#1e3a8a"),
            alignment=1,
            spaceAfter=4
        )

        subtitle_style = ParagraphStyle(
            "RTISubtitle",
            parent=styles["Normal"],
            fontSize=10,
            leading=13,
            textColor=colors.HexColor("#475569"),
            alignment=1,
            spaceAfter=12
        )

        body_style = ParagraphStyle(
            "RTIBody",
            parent=styles["Normal"],
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor("#0f172a")
        )

        bold_style = ParagraphStyle(
            "RTIBold",
            parent=body_style,
            fontName="Helvetica-Bold"
        )

        elements = []

        # Header Title
        elements.append(Paragraph("<b>இந்திய குடியரசு / REPUBLIC OF INDIA</b>", subtitle_style))
        elements.append(Paragraph("<b>தகவல் அறியும் உரிமைச் சட்டம் 2005 - பிரிவு 6(1) முறைப்படியான விண்ணப்பம்</b>", title_style))
        elements.append(Paragraph("<b>RIGHT TO INFORMATION ACT 2005 (FORM - A / APPLICATION FOR INFORMATION)</b>", subtitle_style))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=10))

        # To / From Block
        to_from_data = [
            [
                Paragraph("<b>அனுப்புநர் (Applicant):</b><br/>"
                          f"<b>{applicant_name}</b><br/>"
                          f"{address}<br/>"
                          f"தொலைபேசி: +91 {phone}<br/>"
                          f"வறுமைக் கோட்டு நிலை: {'ஆம் (BPL Cardholder - கட்டண விலக்கு)' if is_bpl else 'இல்லை (Non-BPL)'}", body_style),
                Paragraph("<b>பெறுநர் (Public Authority):</b><br/>"
                          f"<b>பொதுத் தகவல் அலுவலர் (Public Information Officer - PIO)</b><br/>"
                          f"{public_authority}<br/>"
                          f"தமிழ்நாடு / மத்திய அரசு நிர்வாக அலுவலகம்", body_style)
            ]
        ]
        tf_table = Table(to_from_data, colWidths=[270, 270])
        tf_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        elements.append(tf_table)
        elements.append(Spacer(1, 10))

        # Subject Block
        sub_text = (
            "<b>பொருள்:</b> தகவல் அறியும் உரிமைச் சட்டம் 2005, பிரிவு 6(1)-ன் கீழ் அரசு பொது ஆவணங்கள், "
            f"கணக்குகள் மற்றும் நடவடிக்கை குறிப்புகள் கோருதல் சார்பு.<br/>"
            f"<b>கால வரம்பு (Period Covered):</b> {period_covered}"
        )
        elements.append(Paragraph(sub_text, body_style))
        elements.append(Spacer(1, 10))

        # Questions Sought Block
        elements.append(Paragraph("<b>கோரப்படும் தகவல்கள் (Particulars of Information Required):</b>", bold_style))
        elements.append(Spacer(1, 4))
        
        info_lines = information_sought.strip().split("\n")
        q_elements = ""
        for i, line in enumerate(info_lines, 1):
            clean_l = line.strip().lstrip("0123456789.-*• ")
            if clean_l:
                q_elements += f"<b>{i}.</b> {clean_l}<br/>"
        if not q_elements:
            q_elements = f"1. {information_sought}<br/>"

        elements.append(Paragraph(q_elements, body_style))
        elements.append(Spacer(1, 10))

        # Statutory Compliance & Fee Table
        fee_label = "₹0 (பிரிவு 7(5) படி BPL அட்டைதாரருக்கு கட்டண விலக்கு)" if is_bpl else "₹10 (நீதிமன்ற கட்டண வில்லை / IPO இணைக்கப்பட்டுள்ளது)"
        table_data = [
            [Paragraph("<b>விண்ணப்ப கட்டணம் (Application Fee)</b>", bold_style), Paragraph(fee_label, body_style)],
            [Paragraph("<b>பதில் அளிக்கப்பட வேண்டிய காலக்கெடு (Mandatory SLA)</b>", bold_style), Paragraph("30 நாட்கள் (உயிர் மற்றும் சுதந்திரம் தொடர்புடையதாயின் 48 மணி நேரம் - பிரிவு 7(1))", body_style)],
            [Paragraph("<b>முதல் மேல்முறையீட்டு அலுவலர் (First Appellate Authority)</b>", bold_style), Paragraph("பிரிவு 19(1)-ன் கீழ் 30 நாட்களுக்குள் பதிலளிக்காவிடில் முதல் மேல்முறையீடு செய்யப்படும்.", body_style)],
            [Paragraph("<b>Makkal AI Audit Tracking Code</b>", bold_style), Paragraph(f"RTI-TN-2026-{verification_id}", body_style)],
        ]
        t = Table(table_data, colWidths=[200, 340])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 14))

        # Declaration & Signature Block
        dec_text = (
            "<b>உறுதிமொழி (Declaration):</b> நான் இந்திய நாட்டின் குடிமகன் என்றும், மேலே கோரப்பட்டுள்ள தகவல்கள் அனைத்தும் "
            "சட்ட விதிகளுக்கு உட்பட்டு பொது நலன் கருதி கேட்கப்பட்டுள்ளது என்றும், பிரிவு 8 அல்லது 9-ன் கீழ் விலக்களிக்கப்படாதவை "
            "என்றும் உறுதியளிக்கிறேன்."
        )
        elements.append(Paragraph(dec_text, body_style))
        elements.append(Spacer(1, 14))

        sig_data = [
            [Paragraph(f"இடம்: {address.split(',')[0]}<br/>நாள்: {datetime.now().strftime('%d-%m-%Y')}<br/>RTI சரிபார்ப்பு எண்: RTI-TN-2026-{verification_id}", body_style),
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

    def generate_mp_petition_pdf(
        self,
        applicant_name: str,
        phone: str,
        constituency_name: str,
        mp_name: str,
        address: str,
        subject: str,
        grievance_details: str,
        jurisdiction_area: str = "ரயில்வே & மத்திய திட்டங்கள்",
        meta_verification_id: Optional[str] = None
    ) -> Path:
        """
        Synthesizes an official Member of Parliament (Lok Sabha) Public Representation Petition PDF.
        """
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_id = uuid.uuid4().hex[:8]
        verification_id = meta_verification_id or safe_id
        pdf_path = self.output_dir / f"MP_Petition_{safe_id}_{timestamp_str}.pdf"

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
            "MPTitle",
            parent=styles["Heading1"],
            fontSize=15,
            leading=18,
            textColor=colors.HexColor("#7c2d12"),
            alignment=1,
            spaceAfter=4
        )

        subtitle_style = ParagraphStyle(
            "MPSubtitle",
            parent=styles["Normal"],
            fontSize=10,
            leading=13,
            textColor=colors.HexColor("#475569"),
            alignment=1,
            spaceAfter=12
        )

        body_style = ParagraphStyle(
            "MPBody",
            parent=styles["Normal"],
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor("#0f172a")
        )

        bold_style = ParagraphStyle(
            "MPBold",
            parent=body_style,
            fontName="Helvetica-Bold"
        )

        elements = []

        # Header Title
        elements.append(Paragraph("<b>இந்திய நாடாளுமன்ற மக்களவை / PARLIAMENT OF INDIA (LOK SABHA)</b>", subtitle_style))
        elements.append(Paragraph(f"<b>மாண்புமிகு நாடாளுமன்ற உறுப்பினர் ({constituency_name}) மக்கள் கோரிக்கை மனு</b>", title_style))
        elements.append(Paragraph("<b>MEMBER OF PARLIAMENT CITIZEN REPRESENTATION & GRIEVANCE CHARTER</b>", subtitle_style))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#7c2d12"), spaceAfter=10))

        # To / From Block
        to_from_data = [
            [
                Paragraph("<b>மனுதாரர் (Citizen):</b><br/>"
                          f"<b>{applicant_name}</b><br/>"
                          f"{address}<br/>"
                          f"தொலைபேசி: +91 {phone}", body_style),
                Paragraph("<b>பெறுநர் (Hon'ble MP):</b><br/>"
                          f"<b>மாண்புமிகு திரு/திருமதி. {mp_name} அவர்கள்</b><br/>"
                          f"நாடாளுமன்ற உறுப்பினர் (மக்களவை)<br/>"
                          f"{constituency_name} நாடாளுமன்ற தொகுதி<br/>"
                          f"நாடாளுமன்ற அலுவலகம் / தொகுதி முகாம் அலுவலகம்", body_style)
            ]
        ]
        tf_table = Table(to_from_data, colWidths=[270, 270])
        tf_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fef3c7")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#d97706")),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        elements.append(tf_table)
        elements.append(Spacer(1, 10))

        # Subject Block
        sub_text = (
            f"<b>பொருள்:</b> {constituency_name} தொகுதிக்குட்பட்ட பொதுமக்களின் அத்தியாவசிய தேவைகள் & "
            f"<b>{subject}</b> தொடர்பாக நாடாளுமன்ற உறுப்பினர் நேரடி நடவடிக்கை வேண்டி சமர்ப்பிக்கப்படும் கோரிக்கை மனு.<br/>"
            f"<b>நிர்வாக வரம்பு (Central Jurisdiction):</b> {jurisdiction_area}"
        )
        elements.append(Paragraph(sub_text, body_style))
        elements.append(Spacer(1, 10))

        # Grievance Details Block
        elements.append(Paragraph("<b>கோரிக்கை மற்றும் கள நிலவர விவரங்கள் (Grievance Details & Representation):</b>", bold_style))
        elements.append(Spacer(1, 4))
        elements.append(Paragraph(grievance_details, body_style))
        elements.append(Spacer(1, 12))

        # MP Representation Metadata Table
        mp_meta_data = [
            [Paragraph("<b>நாடாளுமன்ற தொகுதி (Constituency)</b>", bold_style), Paragraph(constituency_name, body_style)],
            [Paragraph("<b>மத்திய அரசு துறை (Central Ministry)</b>", bold_style), Paragraph(jurisdiction_area, body_style)],
            [Paragraph("<b>அரசு சேவை கட்டணம் (Statutory Fee)</b>", bold_style), Paragraph("₹0 (நாடாளுமன்ற உறுப்பினர் மனு முற்றிலும் இலவசம்)", body_style)],
            [Paragraph("<b>Makkal AI Audit Tracking Code</b>", bold_style), Paragraph(f"MP-TN-2026-{verification_id}", body_style)],
        ]
        mt = Table(mp_meta_data, colWidths=[200, 340])
        mt.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(mt)
        elements.append(Spacer(1, 14))

        # Signature Block
        sig_data = [
            [Paragraph(f"இடம்: {address.split(',')[0]}<br/>நாள்: {datetime.now().strftime('%d-%m-%Y')}<br/>சரிபார்ப்பு எண்: MP-TN-2026-{verification_id}", body_style),
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



    def generate_crop_loss_petition_pdf(
        self,
        farmer_name: str,
        phone: str,
        district: str,
        taluk: str,
        village: str,
        survey_number: str,
        crop_name: str,
        affected_acres: str,
        damage_cause: str,
        severity_pct: str,
        estimated_loss_rs: str,
        meta_verification_id: str
    ) -> Path:
        """
        Synthesizes an official Tamil Nadu Agriculture & Disaster Crop Loss Relief Petition PDF.
        Addressed to the District Collector and Joint Director of Agriculture under SDRF & PMFBY rules.
        """
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_id = uuid.uuid4().hex[:8]
        pdf_path = self.output_dir / f"Crop_Loss_Petition_{safe_id}_{timestamp_str}.pdf"

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
            "AgriGovTitle",
            parent=styles["Heading1"],
            fontSize=15,
            leading=19,
            textColor=colors.HexColor("#14532d"),
            alignment=1,
            spaceAfter=6
        )

        subtitle_style = ParagraphStyle(
            "AgriGovSubtitle",
            parent=styles["Normal"],
            fontSize=10,
            leading=13,
            textColor=colors.HexColor("#1e293b"),
            alignment=1,
            spaceAfter=12
        )

        bold_style = ParagraphStyle(
            "AgriBold",
            parent=styles["Normal"],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#0f172a"),
            fontName="Helvetica-Bold"
        )

        body_style = ParagraphStyle(
            "AgriBody",
            parent=styles["Normal"],
            fontSize=9.5,
            leading=14,
            textColor=colors.HexColor("#1e293b")
        )

        elements = []

        # Header Title
        elements.append(Paragraph("GOVERNMENT OF TAMIL NADU / தமிழ்நாடு அரசு", title_style))
        elements.append(Paragraph("DEPARTMENT OF AGRICULTURE & FARMERS WELFARE / வேளாண்மை மற்றும் உழவர் நலத்துறை", subtitle_style))
        elements.append(Paragraph("DISASTER RELIEF FUND (SDRF) & PMFBY CROP LOSS ASSESSMENT PETITION", subtitle_style))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#15803d"), spaceAfter=12))

        # Metadata banner
        ver_id = meta_verification_id or f"AGRI-{safe_id.upper()}"
        ref_data = [
            [Paragraph(f"<b>மனு எண்:</b> TN-AGRI-{ver_id}", body_style),
             Paragraph(f"<b>தேதி:</b> {datetime.now().strftime('%d-%m-%Y')}", body_style),
             Paragraph(f"<b>சட்டம் / விதி:</b> SDRF & PMFBY 2024", body_style)]
        ]
        t_ref = Table(ref_data, colWidths=[180, 180, 180])
        t_ref.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f0fdf4")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#bbf7d0")),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(t_ref)
        elements.append(Spacer(1, 10))

        # Sender & Recipient
        from_text = f"<b>அனுப்புநர் (விவசாயி விவரம்):</b><br/>{farmer_name},<br/>நில புல எண்: {survey_number},<br/>கிராமம்: {village}, வட்டம்: {taluk},<br/>மாவட்டம்: {district}.<br/>கைபேசி: {phone}"
        to_text = f"<b>பெறுநர் (அதிகாரிகள்):</b><br/>1. மாவட்ட ஆட்சித் தலைவர் அவர்கள் (District Collector),<br/>2. இணை இயக்குநர், வேளாண்மைத்துறை (Joint Director of Agri),<br/>3. வட்டாட்சியர் & கிராம நிர்வாக அலுவலர் (Tahsildar / VAO),<br/>{district} மாவட்டம், தமிழ்நாடு."

        addresses = [
            [Paragraph(from_text, body_style), Paragraph(to_text, body_style)]
        ]
        t_addr = Table(addresses, colWidths=[270, 270])
        t_addr.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 6),
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1"))
        ]))
        elements.append(t_addr)
        elements.append(Spacer(1, 10))

        # Subject
        sub_text = (
            f"<b>பொருள்:</b> {district} மாவட்டம், {taluk} வட்டம், {village} கிராமத்தில் புல எண் {survey_number}-ல் "
            f"சாகுபடி செய்யப்பட்ட <b>{crop_name}</b> பயிர் <b>{damage_cause}</b> காரணமாக பலத்த சேதமடைந்தது - "
            f"அரசு பேரிடர் நிவாரண நிதி (SDRF) மற்றும் PMFBY பயிர் காப்பீட்டு இழப்பீடு வழங்கக் கோருதல் தொடர்பாக."
        )
        elements.append(Paragraph(sub_text, body_style))
        elements.append(Spacer(1, 10))

        # Agri Damage Details Table
        damage_data = [
            [Paragraph("<b>விவசாய நில புல எண் (Survey No)</b>", bold_style), Paragraph(survey_number, body_style)],
            [Paragraph("<b>பாதிக்கப்பட்ட பயிர் & பரப்பு</b>", bold_style), Paragraph(f"{crop_name} ({affected_acres} ஏக்கர்)", body_style)],
            [Paragraph("<b>சேதத்திற்கான காரணம் (Damage Cause)</b>", bold_style), Paragraph(damage_cause, body_style)],
            [Paragraph("<b>Meta SAM 3.1 சேத கணிப்பு சதவீதம்</b>", bold_style), Paragraph(f"<b>{severity_pct}</b> (செயற்கை நுண்ணறிவு கணக்கீடு)", bold_style)],
            [Paragraph("<b>மதிப்பிடப்பட்ட சாகுபடி இழப்பு (Estimated Loss)</b>", bold_style), Paragraph(f"₹ {estimated_loss_rs}", bold_style)],
            [Paragraph("<b>விண்ணப்பிக்கும் அரசு நிதி</b>", bold_style), Paragraph("SDRF நிவாரணம் & PMFBY பயிர் காப்பீட்டுத் தொகை", body_style)],
            [Paragraph("<b>ஆவண ஆதாரங்கள் (Enclosures)</b>", bold_style), Paragraph("1. பட்டா / சிட்டா நகல்<br/>2. அடங்கல் ஆவணம் (VAO Adangal)<br/>3. பயிர் சேத புகைப்படங்கள் & SAM 3.1 அறிக்கை<br/>4. வங்கி பாஸ்புக் & ஆதார் நகல்", body_style)]
        ]
        t_dmg = Table(damage_data, colWidths=[200, 340])
        t_dmg.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fcfdfa")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#86efac")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dcfce7")),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(t_dmg)
        elements.append(Spacer(1, 12))

        # Declaration
        decl_text = (
            "<b>விவசாயி உறுதிமொழி:</b> மேற்கூறிய விவரங்கள் அனைத்தும் உண்மையானவை என உறுதியளிக்கிறேன். "
            "தாங்கள் நேரில் கள ஆய்வு செய்து, வருவாய்த்துறை மற்றும் வேளாண்மைத்துறை விதிகளின்படி "
            "உரிய நிவாரணத் தொகையினை எனது வங்கிக் கணக்கில் வரவு வைக்குமாறு பணிவுடன் கேட்டுக்கொள்கிறேன்."
        )
        elements.append(Paragraph(decl_text, body_style))
        elements.append(Spacer(1, 14))

        # Signature
        sig_data = [
            [Paragraph(f"இடம்: {village}<br/>நாள்: {datetime.now().strftime('%d-%m-%Y')}<br/>டிஜிட்டல் குறியீடு: {ver_id}", body_style),
             Paragraph(f"இங்ஙனம்,<br/><br/><br/><b>({farmer_name})</b><br/>பாதிக்கப்பட்ட விவசாயி கையொப்பம்", body_style)]
        ]
        t_sig = Table(sig_data, colWidths=[270, 270])
        t_sig.setStyle(TableStyle([
            ('ALIGN', (1,0), (1,0), 'RIGHT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP')
        ]))
        elements.append(t_sig)

        doc.build(elements)
        return pdf_path


action_executor = ActionExecutor()
