import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def generate_college_pdf():
    pdf_filename = "College_Minor_Project_3_Person_Presentation.pdf"
    w, h = landscape(A4) # 841.89 x 595.27
    c = canvas.Canvas(pdf_filename, pagesize=(w, h))

    # Color Palette
    C_BG = colors.HexColor('#0F172A')       # Dark Slate 900
    C_CARD = colors.HexColor('#1E293B')     # Slate 800
    C_BORDER = colors.HexColor('#334155')   # Slate 700
    C_CYAN = colors.HexColor('#06B6D4')     # Electric Cyan (Speaker 1)
    C_BLUE = colors.HexColor('#3B82F6')     # Royal Blue (Speaker 2)
    C_GREEN = colors.HexColor('#10B981')    # Emerald Green (Speaker 3)
    C_GOLD = colors.HexColor('#F59E0B')     # Amber Gold
    C_RED = colors.HexColor('#EF4444')       # Ruby Red
    C_WHITE = colors.HexColor('#F8FAFC')    # Slate 50
    C_MUTED = colors.HexColor('#94A3B8')    # Slate 400
    C_LIGHT = colors.HexColor('#E2E8F0')    # Slate 200

    def draw_bg():
        c.setFillColor(C_BG)
        c.rect(0, 0, w, h, fill=1, stroke=0)

    def draw_footer(slide_num, speaker_tag, time_tag):
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(1)
        c.line(40, 32, w - 40, 32)

        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(40, 20, "AI-Based Medical Image Diagnosis & Triage Support System  |  Minor Project Presentation")
        
        c.setFillColor(C_CYAN if "Speaker 1" in speaker_tag else (C_BLUE if "Speaker 2" in speaker_tag else C_GREEN))
        c.setFont("Helvetica-Bold", 8)
        c.drawRightString(w - 110, 20, f"{speaker_tag} ({time_tag})")

        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 8)
        c.drawRightString(w - 40, 20, f"Slide {slide_num} of 10")

    def draw_header(tag, title, speaker_info, speaker_color):
        # Speaker Banner Pill
        c.setFillColor(speaker_color)
        c.roundRect(40, h - 45, 180, 20, 4, fill=1, stroke=0)
        c.setFillColor(C_BG)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(50, h - 38, speaker_info.upper())

        # Sub-category tag
        c.setFillColor(C_MUTED)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(235, h - 38, f"|   {tag.upper()}")

        # Title
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 19)
        c.drawString(40, h - 70, title)

    def draw_card(x, y, card_w, card_h, border_color=C_BORDER):
        c.setFillColor(C_CARD)
        c.setStrokeColor(border_color)
        c.setLineWidth(1.5)
        c.roundRect(x, y, card_w, card_h, 8, fill=1, stroke=1)

    def draw_speaker_script_box(script_text, speaker_col):
        # Bottom helper card telling the student exactly what to say to examiners
        box_y = 45
        box_h = 60
        box_w = w - 80
        c.setFillColor(colors.HexColor('#131D31'))
        c.setStrokeColor(speaker_col)
        c.setLineWidth(1)
        c.roundRect(40, box_y, box_w, box_h, 6, fill=1, stroke=1)

        c.setFillColor(speaker_col)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(55, box_y + box_h - 16, "🎤 WHAT TO SAY TO EXAMINERS (SPEAKER NOTE):")

        c.setFillColor(C_LIGHT)
        c.setFont("Helvetica-Oblique", 8.5)
        words = script_text.split()
        lines, cur = [], []
        for word in words:
            if len(" ".join(cur + [word])) < 115: cur.append(word)
            else: lines.append(" ".join(cur)); cur = [word]
        if cur: lines.append(" ".join(cur))

        ly = box_y + box_h - 30
        for line in lines[:2]:
            c.drawString(55, ly, line)
            ly -= 13

    # ==============================================================
    # SLIDE 1: TITLE SLIDE & TEAM ALLOCATION (ALL SPEAKERS)
    # ==============================================================
    draw_bg()
    c.setFillColor(C_CYAN)
    c.rect(40, h - 80, w - 80, 4, fill=1, stroke=0)

    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(40, h - 125, "AI-BASED MEDICAL IMAGE DIAGNOSIS &")
    c.drawString(40, h - 158, "TRIAGE SUPPORT SYSTEM")

    c.setFillColor(C_CYAN)
    c.setFont("Helvetica", 13)
    c.drawString(40, h - 188, "Minor Project Presentation  |  Estimated Duration: 8 to 10 Minutes Total")

    # 3 Person Roles Split Cards
    roles = [
        ("PERSON 1: CLINICAL OVERVIEW", "Time: 0:00 - 3:00 (~3 mins)", C_CYAN, [
            "• Problem Statement & Clinical Bottlenecks",
            "• Tri-Modal Clinical Scope (Chest, Skin, Dental)",
            "• Medical Ethics & Decision-Support Scope",
            "• Deliverable: Explain WHY this project exists"
        ]),
        ("PERSON 2: AI & ML ENGINE", "Time: 3:00 - 6:00 (~3 mins)", C_BLUE, [
            "• Deep Learning Backbones (DenseNet & ResNet)",
            "• Explainable AI (Grad-CAM Heatmap Overlays)",
            "• Automated Triage & Urgency Stratification",
            "• Deliverable: Explain HOW the AI diagnoses"
        ]),
        ("PERSON 3: FULL-STACK & DEMO", "Time: 6:00 - 9:00 (~3 mins)", C_GREEN, [
            "• Monorepo Architecture (React + Express + FastAPI)",
            "• Cloud Production Deployment on Vercel",
            "• Clinician Dashboard Workflow & Live Demo",
            "• Deliverable: SHOW the software in action"
        ])
    ]
    card_w = (w - 80 - 30) / 3
    for i, (r_t, r_time, r_col, r_items) in enumerate(roles):
        cx = 40 + i * (card_w + 15)
        draw_card(cx, 60, card_w, 270, border_color=r_col)

        c.setFillColor(r_col)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(cx + 14, 305, r_t)

        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(cx + 14, 288, r_time)

        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 9)
        cur_y = 260
        for item in r_items:
            c.drawString(cx + 14, cur_y, item)
            cur_y -= 22

    draw_footer(1, "All Team Members", "Introduction")
    c.showPage()

    # ==============================================================
    # SLIDE 2: PERSON 1 — PROBLEM STATEMENT & MOTIVATION
    # ==============================================================
    draw_bg()
    draw_header("Clinical Motivation", "The Critical Need for AI-Powered Medical Triage", "Person 1 | Slide 1", C_CYAN)

    probs = [
        ("Massive Diagnostic Backlog", "Hospitals worldwide suffer from acute shortages of certified radiologists and dermatologists. Patients wait 24 to 72 hours for initial routine scan interpretation.", C_RED),
        ("The False-Negative Penalty", "In emergency conditions like Pneumothorax or aggressive Melanoma, delays or missed findings cause severe morbidity. High-sensitivity triage is mandatory.", C_GOLD),
        ("Black-Box AI Skepticism", "Doctors distrust automated AI tools that only provide a percentage without visual explanation. Clinicians demand visual proof of what the model saw.", C_CYAN),
        ("Siloed Healthcare Systems", "Most existing diagnostic tools focus on a single organ. Community primary care clinics need a unified platform that triages chest, skin, and oral health together.", C_BLUE)
    ]
    card_w = (w - 80 - 20) / 2
    card_h = 160
    for i, (p_t, p_d, p_c) in enumerate(probs):
        col, row = i % 2, i // 2
        cx = 40 + col * (card_w + 20)
        cy = (h - 95 - card_h) - row * (card_h + 15)
        draw_card(cx, cy, card_w, card_h, border_color=p_c)

        c.setFillColor(p_c)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(cx + 16, cy + card_h - 26, f"●  {p_t}")

        c.setFillColor(C_LIGHT)
        c.setFont("Helvetica", 9.5)
        words = p_d.split()
        lines, cur = [], []
        for w_item in words:
            if len(" ".join(cur + [w_item])) < 58: cur.append(w_item)
            else: lines.append(" ".join(cur)); cur = [w_item]
        if cur: lines.append(" ".join(cur))
        ly = cy + card_h - 52
        for line in lines:
            c.drawString(cx + 16, ly, line)
            ly -= 16

    draw_speaker_script_box(
        "\"Good morning respected professors. Our project addresses a critical real-world problem: hospital diagnostic bottlenecks. Specialists are overwhelmed, leading to delayed treatment. Our system acts as an AI triage assistant that prioritizes critical scans so doctors review high-risk patients first.\"",
        C_CYAN
    )
    draw_footer(2, "Person 1", "0:00 - 1:00")
    c.showPage()

    # ==============================================================
    # SLIDE 3: PERSON 1 — PROPOSED SOLUTION & 3 MODALITIES
    # ==============================================================
    draw_bg()
    draw_header("Proposed Solution", "Tri-Modal Clinical Scope: Chest, Skin, and Dental", "Person 1 | Slide 2", C_CYAN)

    mods = [
        ("Chest Radiography", "14 Thoracic Conditions", C_CYAN, [
            "Pneumonia & Pneumothorax",
            "Cardiomegaly (Enlarged Heart)",
            "Effusion & Consolidation",
            "Atelectasis & Infiltration",
            "Trained on NIH ChestX-ray14"
        ]),
        ("Dermatological Lesions", "7 Skin Pathologies", C_BLUE, [
            "Melanoma (Malignant)",
            "Basal Cell Carcinoma (BCC)",
            "Benign Keratosis (BKL)",
            "Melanocytic Nevi (Common Moles)",
            "Trained on HAM10000 / ISIC"
        ]),
        ("Dental Oral Triage", "6 Dental Conditions", C_GOLD, [
            "Dental Caries (Tooth Decay)",
            "Dental Calculus (Tartar)",
            "Gingivitis (Gum Inflammation)",
            "Mouth Ulcer / Aphthous",
            "Tooth Discoloration & Hypodontia"
        ])
    ]
    card_w = (w - 80 - 30) / 3
    for i, (m_t, m_s, m_c, m_items) in enumerate(mods):
        cx = 40 + i * (card_w + 15)
        draw_card(cx, 120, card_w, 350, border_color=m_c)

        c.setFillColor(m_c)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(cx + 16, 440, m_t)

        c.setFillColor(C_WHITE)
        c.setFont("Helvetica", 10)
        c.drawString(cx + 16, 422, m_s)

        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 9.5)
        cur_y = 390
        for item in m_items:
            c.drawString(cx + 16, cur_y, f"• {item}")
            cur_y -= 25

    draw_speaker_script_box(
        "\"Unlike existing tools that only look at one disease, we unified 3 crucial modalities into one platform: Chest X-rays for pneumonia and lung collapse, Skin lesions for cancer screening like melanoma, and Dental scans for caries and gum disease. This covers the most common community clinic referrals.\"",
        C_CYAN
    )
    draw_footer(3, "Person 1", "1:00 - 2:00")
    c.showPage()

    # ==============================================================
    # SLIDE 4: PERSON 1 — MEDICAL ETHICS & DECISION SUPPORT
    # ==============================================================
    draw_bg()
    draw_header("Ethical Framework", "Clinical Governance: Decision Support vs. Replacement", "Person 1 | Slide 3", C_CYAN)

    card_w = (w - 80 - 20) / 2
    draw_card(40, 120, card_w, 350, border_color=C_BLUE)
    c.setFillColor(C_CYAN)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(60, 440, "Scientific & Clinical Foundations")

    sci_pts = [
        ("Stanford CheXNet (Rajpurkar et al., 2017)", "Validated 121-layer DenseNet architecture on 112,000+ radiographs demonstrating human radiologist parity on pneumonia."),
        ("Esteva et al. (Nature, 2017)", "Demonstrated that deep convolutional networks achieve clinical dermatologist-level precision across biopsy-verified lesions."),
        ("Grad-CAM (Selvaraju et al., 2017)", "Standardized gradient localization showing the exact pixel regions driving model classification decisions.")
    ]
    sy = 405
    for st, sd in sci_pts:
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, sy, f"✔ {st}")
        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 9)
        words = sd.split()
        lines, cur = [], []
        for w_item in words:
            if len(" ".join(cur + [w_item])) < 58: cur.append(w_item)
            else: lines.append(" ".join(cur)); cur = [w_item]
        if cur: lines.append(" ".join(cur))
        ly = sy - 14
        for l in lines: c.drawString(72, ly, l); ly -= 13
        sy = ly - 10

    draw_card(40 + card_w + 20, 120, card_w, 350, border_color=C_GOLD)
    c.setFillColor(C_GOLD)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(60 + card_w + 20, 440, "Clinical Governance & Patient Safety")

    eth_pts = [
        ("Triage, Not Autonomous Diagnosis", "The AI does not prescribe treatment. It acts as an urgent prioritization engine and second reader to help doctors catch missed cases."),
        ("Sensitivity Over Raw Accuracy", "We intentionally prioritize sensitivity (high recall) for emergency conditions like Pneumothorax, ensuring zero critical cases are overlooked."),
        ("Doctor-in-the-Loop Verification", "Every machine finding remains 'Pending Review' until a licensed doctor reviews the scan, logs qualitative notes, and approves it.")
    ]
    sy = 405
    for et, ed in eth_pts:
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60 + card_w + 20, sy, f"⚖ {et}")
        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 9)
        words = ed.split()
        lines, cur = [], []
        for w_item in words:
            if len(" ".join(cur + [w_item])) < 58: cur.append(w_item)
            else: lines.append(" ".join(cur)); cur = [w_item]
        if cur: lines.append(" ".join(cur))
        ly = sy - 14
        for l in lines: c.drawString(72 + card_w + 20, ly, l); ly -= 13
        sy = ly - 10

    draw_speaker_script_box(
        "\"A critical point to emphasize: our system is strictly a decision-support and triage tool, NOT an autonomous doctor replacement. We follow the 'Doctor-in-the-Loop' principle. The AI assists by organizing the queue and highlighting red flags. Now, my teammate Person 2 will explain our deep learning models.\"",
        C_CYAN
    )
    draw_footer(4, "Person 1", "2:00 - 3:00")
    c.showPage()

    # ==============================================================
    # SLIDE 5: PERSON 2 — DEEP LEARNING MODEL ARCHITECTURES
    # ==============================================================
    draw_bg()
    draw_header("AI Architecture", "Deep Learning Backbones & Loss Formulations", "Person 2 | Slide 4", C_BLUE)

    archs = [
        ("Chest X-Ray Model", "DenseNet-121", C_CYAN, [
            ("Task Type", "Multi-Label Classification (14 outputs)"),
            ("Why DenseNet?", "Dense connections pass features from every layer to all subsequent layers. Excellent for faint lung infiltrates."),
            ("Activation", "Independent Sigmoid per pathology"),
            ("Loss Function", "Binary Cross-Entropy Loss with pos-weight")
        ]),
        ("Skin Lesion Classifier", "ResNet-50", C_BLUE, [
            ("Task Type", "Multi-Class Categorization (7 classes)"),
            ("Why ResNet-50?", "50-layer deep residual bottleneck blocks capture fine dermatoscopic pigmentation textures without gradient degradation."),
            ("Activation", "Softmax probability distribution"),
            ("Loss Function", "Categorical Cross-Entropy Loss")
        ]),
        ("Dental Classifier", "ResNet-18", C_GOLD, [
            ("Task Type", "Multi-Class Categorization (6 classes)"),
            ("Why ResNet-18?", "Lightweight residual architecture with ultra-fast inference (<25ms) suited for intra-oral photography."),
            ("Activation", "Softmax with calibrated temperature scaling"),
            ("Loss Function", "Weighted Cross-Entropy Loss")
        ])
    ]
    card_w = (w - 80 - 30) / 3
    for i, (a_t, a_s, a_c, a_specs) in enumerate(archs):
        cx = 40 + i * (card_w + 15)
        draw_card(cx, 120, card_w, 350, border_color=a_c)

        c.setFillColor(a_c)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(cx + 16, 440, a_t)

        c.setFillColor(C_WHITE)
        c.setFont("Helvetica", 11)
        c.drawString(cx + 16, 422, a_s)

        cur_y = 390
        for sl, sv in a_specs:
            c.setFillColor(C_WHITE)
            c.setFont("Helvetica-Bold", 9.5)
            c.drawString(cx + 16, cur_y, sl)
            c.setFillColor(C_MUTED)
            c.setFont("Helvetica", 8.5)
            words = sv.split()
            lines, cur = [], []
            for w_item in words:
                if len(" ".join(cur + [w_item])) < 35: cur.append(w_item)
                else: lines.append(" ".join(cur)); cur = [w_item]
            if cur: lines.append(" ".join(cur))
            ly = cur_y - 13
            for l in lines: c.drawString(cx + 16, ly, l); ly -= 11
            cur_y = ly - 8

    draw_speaker_script_box(
        "\"Thank you Person 1. For our AI architecture, we selected specific backbones tailored to each medical task: DenseNet-121 for Chest X-rays because dense feature reuse excels at capturing faint lung markings; ResNet-50 for Skin Lesions to classify complex dermoscopic textures; and ResNet-18 for Dental scans for high-speed triage.\"",
        C_BLUE
    )
    draw_footer(5, "Person 2", "3:00 - 4:00")
    c.showPage()

    # ==============================================================
    # SLIDE 6: PERSON 2 — EXPLAINABLE AI & GRAD-CAM
    # ==============================================================
    draw_bg()
    draw_header("Explainable AI", "Grad-CAM Heatmap Overlays: Visualizing AI Attention", "Person 2 | Slide 5", C_BLUE)

    card_w = (w - 80 - 20) / 2
    draw_card(40, 120, card_w, 350, border_color=C_CYAN)
    c.setFillColor(C_CYAN)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(60, 440, "How Grad-CAM Works")

    gcam_steps = [
        ("1. Gradient Backpropagation", "We calculate the gradient of the predicted pathology score y^c with respect to the feature activation maps A^k of the final convolutional layer:  ∂y^c / ∂A^k"),
        ("2. Neuron Importance Weights (α_k^c)", "We perform Global Average Pooling over width and height: α_k^c = (1/Z) * sum(∂y^c / ∂A_{i,j}^k). This measures how much feature map k matters for disease c."),
        ("3. ReLU Positive Activation Mapping", "We compute a weighted sum and pass it through ReLU: L_{Grad-CAM} = ReLU(sum(α_k * A^k)). ReLU ensures we only highlight features positively contributing to the disease."),
        ("4. JET Colormap Heatmap Blend", "The heatmap is normalized (0 to 1), resized to match image resolution, and overlaid at 40% opacity on top of the original medical image.")
    ]
    cur_y = 405
    for gt, gd in gcam_steps:
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(60, cur_y, gt)
        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 8.5)
        words = gd.split()
        lines, cur = [], []
        for w_item in words:
            if len(" ".join(cur + [w_item])) < 62: cur.append(w_item)
            else: lines.append(" ".join(cur)); cur = [w_item]
        if cur: lines.append(" ".join(cur))
        ly = cur_y - 12
        for l in lines: c.drawString(72, ly, l); ly -= 11
        cur_y = ly - 6

    draw_card(40 + card_w + 20, 120, card_w, 350, border_color=C_GREEN)
    c.setFillColor(C_GREEN)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(60 + card_w + 20, 440, "Why This Builds Physician Trust")

    trust_pts = [
        ("No Black Box Uncertainty", "Doctors can instantly verify if the AI flagged a genuine consolidative lesion in the lower right lobe or if it was misled by background text or bone artifacts."),
        ("Pinpoints Dental & Skin Anomaly Cores", "In dental triage, our content-aware algorithm targets red inflamed gumline zones for gingivitis and dark decayed cavity contours for dental caries."),
        ("Interactive Re-Focusing", "Doctors can click any candidate disease on our UI (e.g. Cardiomegaly vs Pneumonia) and see the heatmap dynamically refocus on the corresponding anatomical landmark.")
    ]
    cur_y = 405
    for tt, td in trust_pts:
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60 + card_w + 20, cur_y, f"✔ {tt}")
        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 9)
        words = td.split()
        lines, cur = [], []
        for w_item in words:
            if len(" ".join(cur + [w_item])) < 60: cur.append(w_item)
            else: lines.append(" ".join(cur)); cur = [w_item]
        if cur: lines.append(" ".join(cur))
        ly = cur_y - 14
        for l in lines: c.drawString(72 + card_w + 20, ly, l); ly -= 13
        cur_y = ly - 10

    draw_speaker_script_box(
        "\"To eliminate the 'black-box' problem, we integrated Grad-CAM: Gradient-Weighted Class Activation Mapping. By computing gradients at the final convolutional layer, we generate a visual heatmap overlaid on the scan. If the AI detects pneumonia, it highlights the exact lung consolidation, allowing the doctor to verify the diagnosis in seconds.\"",
        C_BLUE
    )
    draw_footer(6, "Person 2", "4:00 - 5:00")
    c.showPage()

    # ==============================================================
    # SLIDE 7: PERSON 2 — AUTOMATED TRIAGE & SEVERITY RULES
    # ==============================================================
    draw_bg()
    draw_header("Triage Rules", "Automated Severity Stratification & Urgency Routing", "Person 2 | Slide 6", C_BLUE)

    tiers = [
        ("HIGH RISK (CRITICAL)", "Immediate Radiologist Notification", C_RED, [
            "• Pneumothorax or Tension Pneumonia score > 0.45",
            "• Malignant Melanoma or Basal Cell Carcinoma > 0.30",
            "• Severe Active Caries or Painful Mouth Ulcer > 0.40",
            "• Any generic thoracic pathology score > 0.65",
            "• Action: Placed at top of doctor queue with red alert"
        ]),
        ("MEDIUM RISK (MODERATE)", "Priority Verification Within 4 Hours", C_GOLD, [
            "• Cardiomegaly, Edema, or Effusion score > 0.25",
            "• Pre-malignant Actinic Keratoses score > 0.30",
            "• Dental Gingivitis, Calculus, or Staining score > 0.35",
            "• Any pathology probability in range [0.35 - 0.65]",
            "• Action: Tagged with amber badge in review queue"
        ]),
        ("LOW RISK (ROUTINE)", "Standard Outpatient Batch Review", C_GREEN, [
            "• All predicted pathology scores below critical threshold",
            "• Benign Melanocytic Nevi (common moles)",
            "• Non-acute dental hypodontia (missing tooth space)",
            "• Completely clear lung field radiographs",
            "• Action: Routine documentation and standard discharge"
        ])
    ]
    card_w = (w - 80 - 30) / 3
    for i, (tt, ts, tc, titems) in enumerate(tiers):
        cx = 40 + i * (card_w + 15)
        draw_card(cx, 120, card_w, 350, border_color=tc)

        c.setFillColor(tc)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(cx + 16, 440, tt)

        c.setFillColor(C_WHITE)
        c.setFont("Helvetica", 10)
        c.drawString(cx + 16, 422, ts)

        cur_y = 390
        for item in titems:
            c.setFillColor(C_MUTED)
            c.setFont("Helvetica", 9)
            words = item.split()
            lines, cur = [], []
            for w_item in words:
                if len(" ".join(cur + [w_item])) < 35: cur.append(w_item)
                else: lines.append(" ".join(cur)); cur = [w_item]
            if cur: lines.append(" ".join(cur))
            for l in lines:
                c.drawString(cx + 16, cur_y, l)
                cur_y -= 13
            cur_y -= 6

    draw_speaker_script_box(
        "\"The AI predictions automatically feed into our clinical triage engine. It classifies cases into High, Medium, or Low severity. A patient with suspected Pneumothorax or Melanoma is immediately tagged as High Risk with a red beacon, ensuring they are attended to first. Now Person 3 will demonstrate our software implementation.\"",
        C_BLUE
    )
    draw_footer(7, "Person 2", "5:00 - 6:00")
    c.showPage()

    # ==============================================================
    # SLIDE 8: PERSON 3 — FULL-STACK ARCHITECTURE
    # ==============================================================
    draw_bg()
    draw_header("System Engineering", "Full-Stack Microservices Architecture", "Person 3 | Slide 7", C_GREEN)

    stacks = [
        ("Frontend Client", "React 19 + Vite 8 SPA", C_CYAN, [
            "• Single-Page Application deployed on Vercel Global Edge CDN",
            "• Dark clinical theme with Lucide medical icons",
            "• Private Network Access (PNA) client-side resilience",
            "• HTML5 Canvas fallback engine for in-browser heatmaps",
            "• LocalStorage persistence for zero-downtime offline demos"
        ]),
        ("Coordination Gateway", "Express.js + Node.js (Port 5000)", C_BLUE, [
            "• REST orchestration gateway managing patients and scans",
            "• Preflight CORS & PNA headers for cloud-to-loopback access",
            "• Dual-Persistence: Mongoose MongoDB with automated in-memory fallback arrays if MongoDB is offline",
            "• Multipart form stream forwarding via Axios & FormData"
        ]),
        ("Inference Microservice", "FastAPI + PyTorch (Port 8000)", C_GREEN, [
            "• High-performance asynchronous non-blocking ML server",
            "• Torchvision transforms (224x224 RGB, ImageNet normalization)",
            "• PyTorch hook mechanism for dynamic Grad-CAM heatmaps",
            "• Headless OpenCV image processing & HSV segmentation",
            "• Interactive Swagger OpenAPI documentation at /docs"
        ])
    ]
    card_w = (w - 80 - 30) / 3
    for i, (st, ss, sc, sitems) in enumerate(stacks):
        cx = 40 + i * (card_w + 15)
        draw_card(cx, 120, card_w, 350, border_color=sc)

        c.setFillColor(sc)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(cx + 16, 440, st)

        c.setFillColor(C_WHITE)
        c.setFont("Helvetica", 10)
        c.drawString(cx + 16, 422, ss)

        cur_y = 390
        for item in sitems:
            c.setFillColor(C_MUTED)
            c.setFont("Helvetica", 8.5)
            words = item.split()
            lines, cur = [], []
            for w_item in words:
                if len(" ".join(cur + [w_item])) < 35: cur.append(w_item)
                else: lines.append(" ".join(cur)); cur = [w_item]
            if cur: lines.append(" ".join(cur))
            for l in lines:
                c.drawString(cx + 16, cur_y, l)
                cur_y -= 12
            cur_y -= 6

    draw_speaker_script_box(
        "\"Thank you Person 2. I will now explain our software engineering architecture. We implemented a decoupled 3-tier microservice architecture: a React 19 single-page dashboard on the frontend; an Express.js gateway that coordinates patient data and handles offline fallback storage; and a FastAPI Python microservice running PyTorch models for inference.\"",
        C_GREEN
    )
    draw_footer(8, "Person 3", "6:00 - 7:00")
    c.showPage()

    # ==============================================================
    # SLIDE 9: PERSON 3 — CLINICIAN DASHBOARD & LIVE DEPLOYMENT
    # ==============================================================
    draw_bg()
    draw_header("Clinical UI & DevOps", "Doctor Dashboard, Vercel Cloud & Live Deployment", "Person 3 | Slide 8", C_GREEN)

    card_w = (w - 80 - 20) / 2
    draw_card(40, 120, card_w, 350, border_color=C_CYAN)
    c.setFillColor(C_CYAN)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(60, 440, "Clinician Dashboard Features")

    ui_pts = [
        ("Real-Time Prioritized Queue", "Displays admitted patients sorted by severity. High-risk scans are color-coded in red at the top so urgent cases are never buried."),
        ("Side-by-Side Diagnostic Viewer", "Allows the physician to view the original medical radiograph side-by-side with the Grad-CAM heatmap to inspect anatomical features."),
        ("Confidence Percentage Bars", "Displays probability distribution across candidate diseases, enabling the clinician to re-verify secondary potential pathologies."),
        ("Doctor Review & Audit Trail", "Physicians can type clinical observation notes, override machine flags, and mark cases as 'Reviewed' for full audit compliance.")
    ]
    cur_y = 405
    for ut, ud in ui_pts:
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, cur_y, f"✦ {ut}")
        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 8.5)
        words = ud.split()
        lines, cur = [], []
        for w_item in words:
            if len(" ".join(cur + [w_item])) < 60: cur.append(w_item)
            else: lines.append(" ".join(cur)); cur = [w_item]
        if cur: lines.append(" ".join(cur))
        ly = cur_y - 12
        for l in lines: c.drawString(72, ly, l); ly -= 11
        cur_y = ly - 6

    draw_card(40 + card_w + 20, 120, card_w, 350, border_color=C_GREEN)
    c.setFillColor(C_GREEN)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(60 + card_w + 20, 440, "Production Cloud Hosting & Links")

    prod_pts = [
        ("Live Vercel Deployment", "Hosted globally on Vercel Edge at:\nhttps://medical-triage-kohl.vercel.app\nAccessible on laptops, tablets, and phones."),
        ("GitHub Repository", "Fully version-controlled with clean main branch commit history:\nhttps://github.com/omveer7850/medical-triage"),
        ("Browser Resilience (PNA)", "Includes client-side fallback engines. The dashboard operates smoothly even if offline or in network-restricted campus environments."),
        ("Docker Containerization", "Dockerfiles and docker-compose.yml allow 1-command local deployment across Linux, Mac, and Windows.")
    ]
    cur_y = 405
    for pt, pd in prod_pts:
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60 + card_w + 20, cur_y, f"✔ {pt}")
        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 8.5)
        words = pd.split()
        lines, cur = [], []
        for w_item in words:
            if len(" ".join(cur + [w_item])) < 60: cur.append(w_item)
            else: lines.append(" ".join(cur)); cur = [w_item]
        if cur: lines.append(" ".join(cur))
        ly = cur_y - 12
        for l in lines: c.drawString(72 + card_w + 20, ly, l); ly -= 11
        cur_y = ly - 8

    draw_speaker_script_box(
        "\"Here you can see our production environment. We deployed our frontend to Vercel at 'medical-triage-kohl.vercel.app' and our full source code is on GitHub. The UI is built specifically for clinicians with side-by-side heatmap comparison and medical notes logging. Anyone can open our live link right now.\"",
        C_GREEN
    )
    draw_footer(9, "Person 3", "7:00 - 8:00")
    c.showPage()

    # ==============================================================
    # SLIDE 10: PERSON 3 — ROADMAP, CONCLUSION & DEMO HANDOFF
    # ==============================================================
    draw_bg()
    draw_header("Conclusion & Future Work", "Major Project Roadmap & Summary", "Person 3 | Slide 9", C_GREEN)

    card_w = (w - 80 - 20) / 2
    draw_card(40, 120, card_w, 350, border_color=C_GOLD)
    c.setFillColor(C_GOLD)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(60, 440, "Semester 2 (Major Project) Roadmap")

    road_pts = [
        ("PACS & DICOM Medical Standard Integration", "Implement native .dcm file ingestion with Cornerstone.js / OHIF viewer, parsing patient metadata and high-bitrate DICOM windowing presets."),
        ("Multi-View Radiograph Correlation", "Extend thoracic models to process lateral and posteroanterior (PA) views simultaneously for higher 3D anatomical accuracy."),
        ("Federated Learning Across Hospitals", "Train models across hospital nodes with Flower/PySyft without centralizing patient protected health information (HIPAA compliant)."),
        ("Prospective Clinical Trial", "Measure real-world reduction in doctor turnaround time in partner outpatient diagnostic facilities.")
    ]
    cur_y = 405
    for rt, rd in road_pts:
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, cur_y, f"🚀 {rt}")
        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 8.5)
        words = rd.split()
        lines, cur = [], []
        for w_item in words:
            if len(" ".join(cur + [w_item])) < 60: cur.append(w_item)
            else: lines.append(" ".join(cur)); cur = [w_item]
        if cur: lines.append(" ".join(cur))
        ly = cur_y - 12
        for l in lines: c.drawString(72, ly, l); ly -= 11
        cur_y = ly - 6

    draw_card(40 + card_w + 20, 120, card_w, 350, border_color=C_GREEN)
    c.setFillColor(C_GREEN)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(60 + card_w + 20, 440, "Project Summary & Demo Handoff")

    sum_pts = [
        ("Tri-Modal Completeness", "Successfully implemented diagnostic triage across Chest Radiographs, Skin Lesions, and Dental Pathologies in a single platform."),
        ("Clinician Trust Achieved", "Grad-CAM heatmaps bridge the gap between machine intelligence and medical accountability."),
        ("Resilient Production Architecture", "Live on Vercel and fully containerized with dual offline persistence fallbacks."),
        ("Ready for Live Demonstration", "We will now demonstrate live image uploading, Grad-CAM heatmap generation, and severity triage on our web app!")
    ]
    cur_y = 405
    for st, sd in sum_pts:
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60 + card_w + 20, cur_y, f"✔ {st}")
        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 8.5)
        words = sd.split()
        lines, cur = [], []
        for w_item in words:
            if len(" ".join(cur + [w_item])) < 60: cur.append(w_item)
            else: lines.append(" ".join(cur)); cur = [w_item]
        if cur: lines.append(" ".join(cur))
        ly = cur_y - 12
        for l in lines: c.drawString(72 + card_w + 20, ly, l); ly -= 11
        cur_y = ly - 6

    draw_speaker_script_box(
        "\"In conclusion, our Minor Project proves that multi-modal explainable AI can significantly improve emergency triage safety. For our Major Project next semester, we will integrate DICOM hospital PACS protocols. Thank you for your time, professors! We are now ready to show you the live demo and answer your questions.\"",
        C_GREEN
    )
    draw_footer(10, "Person 3", "8:00 - 9:00")
    c.showPage()

    c.save()
    print(f"College presentation PDF successfully created: {os.path.abspath(pdf_filename)}")

if __name__ == "__main__":
    generate_college_pdf()
