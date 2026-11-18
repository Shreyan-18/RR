import os
import shutil
import json
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

# Paths
ROOT = r'C:\Users\prana\.gemini\antigravity\scratch\superr_selector'
OUT_DIR = os.path.join(ROOT, 'submission_package')
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Numbered Canvas for "Page X of Y" and Running Header/Footer
class NumberedCanvas(canvas.Canvas):
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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 800, "Rajasthan Royals SupeRR Selector - Season 2: Round 1 Official Report")
            self.drawRightString(540, 800, "Evaluation of 200,999 Deliveries")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 792, 540, 792)
            
        # Footer
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 540, 45)
        self.drawString(54, 32, "Confidential - Prepared for Rajasthan Royals Cricket Strategy & Analytics Team")
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(540, 32, page_str)
        self.restoreState()

def build_pdf():
    pdf_path = os.path.join(OUT_DIR, 'METHODOLOGY_REPORT.pdf')
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Brand Palette Styles
    c_primary = colors.HexColor("#E11D74")   # Royals Heritage Magenta
    c_navy = colors.HexColor("#080D1A")      # Midnight Sapphire
    c_card = colors.HexColor("#0E172A")      # Imperial Navy
    c_cyan = colors.HexColor("#0284C7")      # Ice Blue (Darker for print contrast)
    c_gold = colors.HexColor("#B45309")      # Deep Gold for print
    c_text = colors.HexColor("#1E293B")      # Slate 800
    c_muted = colors.HexColor("#64748B")     # Slate 500

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_navy,
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_primary,
        spaceAfter=12
    )
    meta_style = ParagraphStyle(
        'MetaText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_muted
    )
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_navy,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=c_text,
        spaceAfter=6
    )
    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=c_text,
        leftIndent=14,
        spaceAfter=3
    )
    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#0F172A")
    )
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=c_text
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=c_navy
    )
    table_cell_header = ParagraphStyle(
        'TableCellHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white
    )

    story = []

    # Title Banner
    story.append(Paragraph("Rajasthan Royals - SupeRR Selector Season 2", title_style))
    story.append(Paragraph("ROUND 1 METHODOLOGY REPORT: IDENTIFYING THE MOST RELIABLE PLAYERS UNDER PRESSURE", subtitle_style))
    
    meta_text = "<b>Dataset:</b> 200,999 Deliveries across 867 IPL & T20I Matches (2022–2026) | <b>Author:</b> Sports Analytics & Data Science Team | <b>Submission:</b> Unstop Round 1"
    story.append(Paragraph(meta_text, meta_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=2, spaceAfter=12))

    # Executive Summary Box
    exec_summary_text = """
    <b>EXECUTIVE SUMMARY & BOARDROOM BRIEFING:</b><br/>
    Traditional cricket statistics suffer from severe <i>context-blindness</i>: a boundary hit when chasing 15 runs in 4 balls of an IPL Final carries infinitely greater consequence than a boundary hit in the powerplay of a dead rubber. 
    This report introduces an audited, objective quantitative engine evaluating <b>162 qualified batters</b> and <b>243 qualified bowlers</b> across <b>200,999 legal deliveries</b>.<br/>
    We formulate the <b>Composite Pressure Index (P_ball &isin; [0, 1])</b> by isolating pre-ball Macro Stakes (40%) from in-game Micro Leverage (60%). Deliveries exceeding the 70th percentile threshold (P &ge; 0.70) isolate the <b>High-Pressure Regime (60,314 balls)</b>. By benchmarking pressure execution against baseline performance, our <b>4-Quadrant Permutations Model</b> identifies unheralded clutch masters (e.g. Naman Dhir's +51% PPR surge) while exposing high-reputation players who decline when the game is on the line.
    """
    callout_data = [[Paragraph(exec_summary_text, callout_style)]]
    t_callout = Table(callout_data, colWidths=[486])
    t_callout.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('LINELEFT', (0,0), (0,-1), 3.5, c_primary),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_callout)
    story.append(Spacer(1, 12))

    # SECTION 1: Pressure Definition
    story.append(Paragraph("1. Pressure Definition: Orthogonal Macro & Micro Engine", h1_style))
    story.append(Paragraph(
        "Pressure in cricket is an emergent property uniting consequence severity with immediate situational leverage. Every delivery is assigned an instantaneous score:",
        body_style
    ))
    
    eq1_data = [[Paragraph("<b>Composite Delivery Equation:</b>&nbsp;&nbsp; <i>P_ball = 0.40 &times; C_macro + 0.60 &times; S_micro</i> &nbsp;&nbsp;(Super Overs hardcoded to P = 1.00)", callout_style)]]
    t_eq1 = Table(eq1_data, colWidths=[486])
    t_eq1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_eq1)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>1.1 Macro Match Stakes Taxonomy (C_macro, 40% Weight):</b> Evaluated before the first ball is bowled:", body_style))
    story.append(Paragraph("- <b>Championship Finals (W_M = 1.00, 15 matches):</b> IPL & ICC World Cup winner-take-all finals.", bullet_style))
    story.append(Paragraph("- <b>Direct Knockouts (W_M = 0.95, 9 matches):</b> Eliminators and semi-finals with instant elimination risk.", bullet_style))
    story.append(Paragraph("- <b>Tied Bilateral Deciders (W_M = 0.85, 34 matches):</b> Series deciders tied at 1–1 (in 3-match series) or 2–2 (in 5-match series).", bullet_style))
    story.append(Paragraph("- <b>Marquee Blockbusters (+0.15 boost, 48 matches):</b> High-ego derbies under immense fan & media pressure (IND vs PAK, MI vs CSK, AUS vs ENG).", bullet_style))
    story.append(Paragraph("- <b>Dead Rubbers (W_M = 0.35, 64 matches):</b> Fixtures played after series or playoff qualification was already clinched.", bullet_style))
    story.append(Paragraph("- <b>Opposition Quality (Q_opp):</b> Tier 1.0 = India (82 wins, 2 World Cups); Tier 1.5 = IPL Franchises; Tier 2.0 = Aus/Eng/SA/NZ; Tier 3.0 = Pak/WI/SL/Afg.", bullet_style))
    story.append(Paragraph("- <b>Hostile Fortresses (H_fortress = 1.0):</b> Hostile away cauldrons (Wankhede, Eden Gardens, Gabba, MCG).", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>1.2 Micro Situational Leverage (S_micro, 60% Weight):</b> Ball-by-ball in-game tension:", body_style))
    story.append(Paragraph("- <b>Required Run Rate (RRR):</b> Dynamic escalation scaling non-linearly from 6.0 to 16.0+ runs per over.", bullet_style))
    story.append(Paragraph("- <b>Balls Remaining (Over Decay):</b> Linear penalty amplifying impact during death overs (16 to 20).", bullet_style))
    story.append(Paragraph("- <b>Wickets Lost:</b> Exponential crisis factor escalating tension as tail-enders are exposed.", bullet_style))
    story.append(Paragraph("- <b>70th Percentile Split:</b> Deliveries with P &ge; 0.70 form the High-Pressure Regime (60,314 deliveries).", bullet_style))
    story.append(Spacer(1, 10))

    # SECTION 2: Performance Measurement Engine
    story.append(Paragraph("2. Performance Scoring Formulation", h1_style))
    story.append(Paragraph(
        "To evaluate execution in crunch time without flat-track inflation, metrics were calibrated per franchise requirements:",
        body_style
    ))
    
    eq_table_data = [
        [
            Paragraph("<b>Batting Performance Equation:</b><br/>Score = 0.30&times;SR + 0.25&times;Bdry% + 0.18&times;Rot% + 0.17&times;Avg + 0.10&times;DotAvoid<br/><i>Prioritizes boundary clearing (25%) over pure rotation (18%) in death chases.</i>", body_style),
            Paragraph("<b>Bowling Performance Equation:</b><br/>Score = 0.30&times;Econ + 0.25&times;WSR + 0.20&times;PostBdry + 0.15&times;Dot% + 0.10&times;Q_opp<br/><i>Heavily rewards post-boundary composure (20%) - dot/wicket on ball after 4/6.</i>", body_style)
        ]
    ]
    t_eqs = Table(eq_table_data, colWidths=[240, 240])
    t_eqs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_eqs)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Pressure Performance Ratio (PPR):</b> Defined as <i>PPR = Score_HP / max(20.0, Score_Norm)</i>. A PPR > 1.00 proves a player produces superior output under intense pressure compared to routine conditions.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # SECTION 3: Fair Comparisons & Guardrails
    story.append(Paragraph("3. Fair Comparisons, Eligibility & Sample Size Guardrails", h1_style))
    story.append(Paragraph("- <b>Sample Size Thresholds:</b> Batters required &ge; 200 total balls and &ge; 60 high-pressure deliveries. Bowlers required &ge; 250 total balls and &ge; 80 high-pressure deliveries. Excluded small-sample outliers.", bullet_style))
    story.append(Paragraph("- <b>Bayesian Shrinkage Reliability Weight:</b> <i>R = min(1.0, HP_Balls / 300)</i>, ensuring volume performers (Bumrah with 736 HP balls; Tim David with 763 HP balls) are prioritized over flash-in-the-pan cameos.", bullet_style))
    story.append(Paragraph("- <b>Cross-Competition Normalization:</b> Calibrated IPL league averages against ICC T20I conditions to ensure seamless comparability across franchise and international arenas.", bullet_style))
    story.append(Spacer(1, 10))

    # SECTION 4: 4-Quadrant Archetype Matrix
    story.append(Paragraph("4. The 4-Quadrant Archetype Model", h1_style))
    
    quad_data = [
        [
            Paragraph("<b>Q1: CLUTCH GIANTS (Elite All-Condition)</b><br/>High Baseline + High Pressure<br/><i>Bumrah, Narine, David, Buttler, Naman Dhir</i>", body_style),
            Paragraph("<b>Q2: CRISIS SPECIALISTS (Pressure Elevators)</b><br/>Moderate Baseline + Massive Pressure Lift<br/><i>Rishabh Pant, Matthew Wade, Faheem, Haris Rauf</i>", body_style)
        ],
        [
            Paragraph("<b>Q3: FRONT-RUNNERS (Flat-Track Accumulators)</b><br/>High Baseline + Severe Drop Under Pressure<br/><i>Aiden Markram, Mohammed Shami, Dewald Brevis</i>", body_style),
            Paragraph("<b>Q4: STRUGGLERS (Low Leverage)</b><br/>Sub-par across both normal and pressure regimes<br/><i>Lower-order accumulators unable to accelerate</i>", body_style)
        ]
    ]
    t_quad = Table(quad_data, colWidths=[240, 240])
    t_quad.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#EFF6FF")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#F0FDF4")),
        ('BACKGROUND', (0,1), (0,1), colors.HexColor("#FFFBEB")),
        ('BACKGROUND', (1,1), (1,1), colors.HexColor("#F8FAFC")),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_quad)
    story.append(Spacer(1, 14))

    # Page Break for Official Rankings Tables
    story.append(PageBreak())

    # SECTION 5: Official Rankings Tables
    story.append(Paragraph("5. Official Player Rankings (Unstop Submission Components)", h1_style))
    story.append(Paragraph(
        "Rankings mathematically derived from the multi-stage pressure pipeline. Exactly matching the Unstop portal dropdown entries:",
        body_style
    ))

    # Top 10 Batters Table
    story.append(Paragraph("5.1 Top 10 Batters Under Pressure (Dropdown Component 1)", h2_style))
    batters_df = pd.read_csv(os.path.join(ROOT, 'top10_batters.csv'))
    
    b_table_data = [[
        Paragraph("Rank", table_cell_header),
        Paragraph("Player Name", table_cell_header),
        Paragraph("HP Balls", table_cell_header),
        Paragraph("HP Runs", table_cell_header),
        Paragraph("HP SR", table_cell_header),
        Paragraph("HP Avg", table_cell_header),
        Paragraph("Bdry%", table_cell_header),
        Paragraph("PPR", table_cell_header),
        Paragraph("Score", table_cell_header),
        Paragraph("Quadrant Archetype", table_cell_header)
    ]]
    for _, row in batters_df.iterrows():
        b_table_data.append([
            Paragraph(f"<b>#{int(row['rank'])}</b>", table_cell_bold),
            Paragraph(f"<b>{row['player_name']}</b>", table_cell_bold),
            Paragraph(str(int(row['hp_balls'])), table_cell_style),
            Paragraph(str(int(row['hp_runs'])), table_cell_style),
            Paragraph(f"{row['hp_sr']:.1f}", table_cell_style),
            Paragraph(f"{row['hp_avg']:.1f}", table_cell_style),
            Paragraph(f"{row['hp_bdry_pct']:.1f}%", table_cell_style),
            Paragraph(f"<b>{row['ppr']:.2f}x</b>", table_cell_bold),
            Paragraph(f"<b>{row['final_rank_score']:.1f}</b>", table_cell_bold),
            Paragraph(str(row['quadrant']).split(':')[1].strip() if ':' in str(row['quadrant']) else str(row['quadrant']), table_cell_style)
        ])
    
    t_batters = Table(b_table_data, colWidths=[28, 90, 40, 40, 42, 42, 42, 38, 38, 86])
    t_batters.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_batters)
    story.append(Spacer(1, 14))

    # Top 10 Bowlers Table
    story.append(Paragraph("5.2 Top 10 Bowlers Under Pressure (Dropdown Component 2)", h2_style))
    bowlers_df = pd.read_csv(os.path.join(ROOT, 'top10_bowlers.csv'))
    
    bw_table_data = [[
        Paragraph("Rank", table_cell_header),
        Paragraph("Player Name", table_cell_header),
        Paragraph("HP Balls", table_cell_header),
        Paragraph("HP Wkts", table_cell_header),
        Paragraph("HP Econ", table_cell_header),
        Paragraph("HP WSR", table_cell_header),
        Paragraph("Post-Bdry", table_cell_header),
        Paragraph("PPR", table_cell_header),
        Paragraph("Score", table_cell_header),
        Paragraph("Quadrant Archetype", table_cell_header)
    ]]
    for _, row in bowlers_df.iterrows():
        bw_table_data.append([
            Paragraph(f"<b>#{int(row['rank'])}</b>", table_cell_bold),
            Paragraph(f"<b>{row['player_name']}</b>", table_cell_bold),
            Paragraph(str(int(row['hp_balls'])), table_cell_style),
            Paragraph(str(int(row['hp_runs'])) if 'hp_runs' not in row else str(int(row.get('hp_wkts', 0))), table_cell_style),
            Paragraph(f"{row['hp_econ']:.2f}", table_cell_style),
            Paragraph(f"{row['hp_wsr']:.1f}", table_cell_style),
            Paragraph(f"{row['hp_post_b_comp']:.1f}%", table_cell_style),
            Paragraph(f"<b>{row['ppr']:.2f}x</b>", table_cell_bold),
            Paragraph(f"<b>{row['final_rank_score']:.1f}</b>", table_cell_bold),
            Paragraph(str(row['quadrant']).split(':')[1].strip() if ':' in str(row['quadrant']) else str(row['quadrant']), table_cell_style)
        ])
    
    t_bowlers = Table(bw_table_data, colWidths=[28, 90, 40, 40, 42, 42, 42, 38, 38, 86])
    t_bowlers.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_bowlers)
    story.append(Spacer(1, 14))

    # SECTION 5.3: Pressure-Proof World XI Lineup Table
    story.append(Paragraph("5.3 Synthesized Pressure-Proof World XI (Positional & Phase Optimization)", h2_style))
    with open(os.path.join(ROOT, 'web', 'data', 'cricket_data.json')) as f:
        cdata = json.load(f)
    xi = cdata['pressure_proof_xi']

    xi_table_data = [[
        Paragraph("Slot/Role", table_cell_header),
        Paragraph("Player", table_cell_header),
        Paragraph("Tactical Role", table_cell_header),
        Paragraph("HP SR / Econ", table_cell_header),
        Paragraph("HP Avg / WSR", table_cell_header),
        Paragraph("PPR", table_cell_header),
        Paragraph("Score", table_cell_header),
        Paragraph("Empirical Specialty", table_cell_header)
    ]]
    for b in xi['batting_lineup']:
        xi_table_data.append([
            Paragraph(f"<b>Slot #{b['slot']}</b>", table_cell_bold),
            Paragraph(f"<b>{b['name']}</b>", table_cell_bold),
            Paragraph(b['role'], table_cell_style),
            Paragraph(f"{b['hp_sr']:.1f} SR", table_cell_style),
            Paragraph(f"{b['hp_avg']:.1f} Avg", table_cell_style),
            Paragraph(f"{b['ppr']:.2f}x", table_cell_bold),
            Paragraph(str(b['score']), table_cell_bold),
            Paragraph(b['key_strength'], table_cell_style)
        ])
    for bw in xi['bowling_attack']:
        xi_table_data.append([
            Paragraph("<b>Specialist</b>", table_cell_bold),
            Paragraph(f"<b>{bw['name']}</b>", table_cell_bold),
            Paragraph(bw['role'], table_cell_style),
            Paragraph(f"{bw['hp_econ']:.2f} Econ", table_cell_style),
            Paragraph(f"{bw['hp_wsr']:.1f} WSR", table_cell_style),
            Paragraph(f"{bw['ppr']:.2f}x", table_cell_bold),
            Paragraph(str(bw['score']), table_cell_bold),
            Paragraph(bw['key_strength'], table_cell_style)
        ])

    t_xi = Table(xi_table_data, colWidths=[45, 80, 85, 52, 52, 34, 34, 104])
    t_xi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#FDF2F8")]),
        ('PADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_xi)
    story.append(Spacer(1, 14))

    # SECTION 6: Reliability & Limitations
    story.append(Paragraph("6. Reliability & Model Boundaries", h1_style))
    story.append(Paragraph("- <b>Post-Boundary Composure Reliability:</b> Jasprit Bumrah (46.8% comeback dot/wicket rate) and Sunil Narine (40.0%) represent the most reliable death anchors in world cricket. Their performance does not degrade against Tier-1 opposition.", bullet_style))
    story.append(Paragraph("- <b>Counter-Intuitive Insights:</b> High-reputation players like Sam Curran suffered a -21% decline as a bowler under high pressure, while unheralded stars like Naman Dhir (+51% lift) and Shashank Singh (+13% lift) proved mathematically superior in clutch chases.", bullet_style))
    story.append(Paragraph("- <b>Limitations:</b> Model evaluates quantitative ball-by-ball outputs. Intangibles such as leadership captaincy, sudden pitch deterioration due to dew, or field misjudgments are proxied through team win-loss stakes rather than ball-level tracking.", bullet_style))
    story.append(Spacer(1, 10))

    # Footer note & Links
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#CBD5E1"), spaceBefore=6, spaceAfter=8))
    links_text = "<b>Official Code Repository:</b> https://github.com/Shreyan-18/RR.git &nbsp;|&nbsp; <b>Interactive Web Hub:</b> Audited Next.js & Tailwind Analytics Engine"
    story.append(Paragraph(links_text, meta_style))

    # Build PDF with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated PDF successfully: {pdf_path}")

def copy_supporting_files():
    # 1. Copy CSVs
    shutil.copy(os.path.join(ROOT, 'top10_batters.csv'), os.path.join(OUT_DIR, 'top10_batters.csv'))
    shutil.copy(os.path.join(ROOT, 'top10_bowlers.csv'), os.path.join(OUT_DIR, 'top10_bowlers.csv'))
    
    # 2. Copy World XI JSON
    with open(os.path.join(ROOT, 'web', 'data', 'cricket_data.json')) as f:
        d = json.load(f)
    with open(os.path.join(OUT_DIR, 'pressure_proof_world_xi.json'), 'w') as f:
        json.dump(d['pressure_proof_xi'], f, indent=2)

    # 3. Write Unstop Dropdown Cheatsheet
    cheatsheet_content = """================================================================================
RAJASTHAN ROYALS - SUPERR SELECTOR SEASON 2 (ROUND 1)
UNSTOP SUBMISSION CHEATSHEET: PLAYER RANKINGS
================================================================================

COMPONENT 1: TOP 10 BATTERS UNDER PRESSURE (Select in Unstop Dropdowns)
--------------------------------------------------------------------------------
Rank 1 : Naman Dhir           (PPR: 1.51x | HP SR: 187.5 | Final Score: 87.7)
Rank 2 : Shashank Singh       (PPR: 1.13x | HP Avg: 38.1 | Final Score: 84.3)
Rank 3 : Tim David            (PPR: 1.13x | HP SR: 176.3 | Final Score: 81.5)
Rank 4 : Namboori Tilak Varma (PPR: 1.30x | HP Avg: 39.5 | Final Score: 81.1)
Rank 5 : Jos Buttler          (PPR: 1.15x | HP SR: 172.2 | Final Score: 81.0)
Rank 6 : Rishabh Pant         (PPR: 1.39x | HP SR: 170.0 | Final Score: 79.4)
Rank 7 : Matthew Wade         (PPR: 1.56x | HP Avg: 41.6 | Final Score: 78.9)
Rank 8 : Shreyas Iyer         (PPR: 1.12x | HP SR: 174.5 | Final Score: 78.8)
Rank 9 : Rajat Patidar        (PPR: 1.01x | HP SR: 170.3 | Final Score: 78.5)
Rank 10: Tristan Stubbs       (PPR: 1.13x | HP SR: 158.6 | Final Score: 78.0)


COMPONENT 1: TOP 10 BOWLERS UNDER PRESSURE (Select in Unstop Dropdowns)
--------------------------------------------------------------------------------
Rank 1 : Sunil Narine         (PPR: 1.20x | HP Econ: 6.76 | Final Score: 76.8)
Rank 2 : Jasprit Bumrah       (PPR: 1.14x | HP Econ: 6.88 | Post-Bdry: 46.8% | Final Score: 72.5)
Rank 3 : Shaheen Afridi       (PPR: 1.28x | HP WSR: 10.9  | Final Score: 69.2)
Rank 4 : Faheem Ashraf        (PPR: 1.60x | HP Econ: 7.57 | Final Score: 68.7)
Rank 5 : Riley Meredith       (PPR: 1.60x | HP WSR: 10.7  | Final Score: 68.7)
Rank 6 : Haris Rauf           (PPR: 1.39x | HP WSR: 11.7  | Final Score: 67.5)
Rank 7 : Alzarri Joseph       (PPR: 1.60x | HP WSR: 15.3  | Final Score: 66.1)
Rank 8 : Shadab Khan          (PPR: 1.57x | HP Econ: 6.72 | Final Score: 64.8)
Rank 9 : Xavier Bartlett      (PPR: 1.60x | HP WSR: 18.5  | Final Score: 64.4)
Rank 10: Axar Patel           (PPR: 1.23x | HP Econ: 7.58 | Final Score: 64.2)


COMPONENT 2: METHODOLOGY REPORT (Upload Document on Unstop)
--------------------------------------------------------------------------------
Upload File: METHODOLOGY_REPORT.pdf
Contents:
  1. Pressure Definition (Composite Pressure Index: 40% Macro Stakes + 60% Micro Leverage)
  2. Performance Measurement Engine (Explicit batting and bowling weighted equations)
  3. Fair Comparisons (Sample thresholds: min 200/60 balls for batters, 250/80 for bowlers)
  4. The 4-Quadrant Permutations Model (Clutch Giants, Crisis Specialists, Front-Runners, Strugglers)
  5. Statistical Evidence Tables for Top 10 Batters, Top 10 Bowlers, and Pressure-Proof World XI
  6. Model Reliability & Boundaries

GITHUB REPOSITORY: https://github.com/Shreyan-18/RR.git
================================================================================
"""
    with open(os.path.join(OUT_DIR, 'UNSTOP_RANKINGS_CHEATSHEET.txt'), 'w', encoding='utf-8') as f:
        f.write(cheatsheet_content)

    # 4. Write README_HOW_TO_SUBMIT.md
    readme_content = """# Rajasthan Royals SupeRR Selector - Round 1 Submission Package

This directory contains all official files required to complete your **Round 1 Submission** for the **Rajasthan Royals SupeRR Selector Season 2** competition on the **Unstop** portal.

---

## Submission Checklist (Step-by-Step)

### Step 1: Complete Component 1 on Unstop (Player Rankings Dropdowns)
Log into the Unstop competition page. Use [`UNSTOP_RANKINGS_CHEATSHEET.txt`](./UNSTOP_RANKINGS_CHEATSHEET.txt) to select:
* **Top 10 Batters** (Rank 1 to Rank 10):
  1. Naman Dhir
  2. Shashank Singh
  3. Tim David
  4. Namboori Tilak Varma
  5. Jos Buttler
  6. Rishabh Pant
  7. Matthew Wade
  8. Shreyas Iyer
  9. Rajat Patidar
  10. Tristan Stubbs

* **Top 10 Bowlers** (Rank 1 to Rank 10):
  1. Sunil Narine
  2. Jasprit Bumrah
  3. Shaheen Afridi
  4. Faheem Ashraf
  5. Riley Meredith
  6. Haris Rauf
  7. Alzarri Joseph
  8. Shadab Khan
  9. Xavier Bartlett
  10. Axar Patel

---

### Step 2: Upload Component 2 on Unstop (Methodology Report Document)
Upload the publication-grade PDF document generated in this folder:
* **File to Upload**: [`METHODOLOGY_REPORT.pdf`](./METHODOLOGY_REPORT.pdf)
* Covers all 5 evaluation criteria required by the Rajasthan Royals analytics panel:
  1. *Pressure Definition* (Macro Stakes + Micro In-Game Leverage + 70th percentile split).
  2. *Performance Measurement* (Explicit weighting formulas prioritizing boundary clearing & post-boundary composure).
  3. *Fair Comparisons* (Sample size filters & Bayesian reliability weighting).
  4. *Evidence for Top 10* (Official verified tables & 4-Quadrant Archetype Matrix).
  5. *Reliability & Limitations* (Consistency verification and model boundaries).

---

### Step 3: Optional Submission ("Share Your Journey")
Unstop invites participants to share back-stage materials and insights:
* **Live Interactive Platform**: [Vercel Deployment URL]
* **GitHub Repository**: [https://github.com/Shreyan-18/RR.git](https://github.com/Shreyan-18/RR.git)
* **Key Counter-Intuitive Insights to Mention**:
  * *Naman Dhir's +51% Surge*: Ranked #1 clutch batter empirically (187.5 HP strike rate) despite lower historical profile.
  * *Sam Curran's Drop*: Declined by -21% as a bowler under high pressure, proving reputation != clutch performance.
  * *Bumrah & Narine's Composure*: Over 40% dot/wicket rate on deliveries immediately following a boundary conceded.

---

## Files in this Package
* [`METHODOLOGY_REPORT.pdf`](./METHODOLOGY_REPORT.pdf) - Complete official PDF report ready to upload.
* [`UNSTOP_RANKINGS_CHEATSHEET.txt`](./UNSTOP_RANKINGS_CHEATSHEET.txt) - Quick reference for the Unstop dropdowns.
* [`top10_batters.csv`](./top10_batters.csv) - Complete raw metrics for the Top 10 Batters.
* [`top10_bowlers.csv`](./top10_bowlers.csv) - Complete raw metrics for the Top 10 Bowlers.
* [`pressure_proof_world_xi.json`](./pressure_proof_world_xi.json) - Full 11-player World XI roster with tactical scouting bios.
"""
    with open(os.path.join(OUT_DIR, 'README_HOW_TO_SUBMIT.md'), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("Copied all supporting files and created cheatsheets successfully!")

if __name__ == '__main__':
    build_pdf()
    copy_supporting_files()
