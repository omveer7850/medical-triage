import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def generate_pdf():
    pdf_filename = "AI_Medical_Diagnosis_Triage_Presentation.pdf"
    w, h = landscape(A4) # 841.89 x 595.27
    c = canvas.Canvas(pdf_filename, pagesize=(w, h))

    # Color Palette
    C_BG = colors.HexColor('#0F172A')       # Dark Slate 900
    C_CARD = colors.HexColor('#1E293B')     # Slate 800
    C_BORDER = colors.HexColor('#334155')   # Slate 700
    C_CYAN = colors.HexColor('#06B6D4')     # Electric Cyan
    C_BLUE = colors.HexColor('#3B82F6')     # Royal Blue
    C_GREEN = colors.HexColor('#10B981')    # Emerald Green
    C_GOLD = colors.HexColor('#F59E0B')     # Amber Gold
    C_RED = colors.HexColor('#EF4444')       # Ruby Red
    C_WHITE = colors.HexColor('#F8FAFC')    # Slate 50
    C_MUTED = colors.HexColor('#94A3B8')    # Slate 400
    C_LIGHT = colors.HexColor('#E2E8F0')    # Slate 200

    def draw_background():
        c.setFillColor(C_BG)
        c.rect(0, 0, w, h, fill=1, stroke=0)

    def draw_footer(slide_num, total_slides=13):
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(1)
        c.line(40, 35, w - 40, 35)

        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(40, 22, "AI-Based Medical Image Diagnosis & Triage Support System  |  Clinical Multi-Modal Decision Support")
        c.drawRightString(w - 40, 22, f"Slide {slide_num} of {total_slides}")

    def draw_header(tag, title, subtitle=None):
        # Category Tag
        c.setFillColor(C_CYAN)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(40, h - 45, tag.upper())

        # Main Title
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(40, h - 70, title)

        # Subtitle
        if subtitle:
            c.setFillColor(C_MUTED)
            c.setFont("Helvetica", 10)
            c.drawString(40, h - 86, subtitle)

    def draw_card(x, y, card_w, card_h, border_color=C_BORDER):
        c.setFillColor(C_CARD)
        c.setStrokeColor(border_color)
        c.setLineWidth(1.5)
        c.roundRect(x, y, card_w, card_h, 8, fill=1, stroke=1)

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    draw_background()
    # Decorative accent bar
    c.setFillColor(C_CYAN)
    c.rect(40, h - 110, w - 80, 4, fill=1, stroke=0)

    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(40, h - 160, "AI-BASED MEDICAL IMAGE DIAGNOSIS &")
    c.drawString(40, h - 195, "TRIAGE SUPPORT SYSTEM")

    c.setFillColor(C_CYAN)
    c.setFont("Helvetica", 14)
    c.drawString(40, h - 230, "Multi-Modal Deep Learning & Explainable AI (Grad-CAM) for Chest Radiographs, Skin Lesions, and Dental Pathologies")

    c.setFillColor(C_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(40, h - 260, "Author / Project: Omveer | Deployed on Vercel Edge & GitHub | Full-Stack Microservices Architecture")

    # 3 Badges
    badges = [
        ("Clinical Modalities", ["• Chest X-Ray: 14 Thoracic Conditions", "• Dermatology: 7 Skin Lesion Classes", "• Dental Triage: 6 Oral Pathologies"], C_BLUE),
        ("Explainable AI & Triage", ["• Dynamic Grad-CAM Heatmap Overlays", "• Risk Stratification (High/Med/Low)", "• Sensitivity-First Emergency Routing"], C_GREEN),
        ("Production Deployed", ["• FastAPI + PyTorch Inference Service", "• Express Coordination Server + Fallbacks", "• React 19 Dashboard Live on Vercel"], C_CYAN)
    ]
    card_w = (w - 80 - 30) / 3
    for i, (b_title, b_items, b_col) in enumerate(badges):
        bx = 40 + i * (card_w + 15)
        draw_card(bx, 70, card_w, 210, border_color=b_col)

        c.setFillColor(b_col)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(bx + 16, 250, b_title)

        c.setFillColor(C_LIGHT)
        c.setFont("Helvetica", 10)
        curr_y = 220
        for item in b_items:
            c.drawString(bx + 16, curr_y, item)
            curr_y -= 24

    draw_footer(1)
    c.showPage()

    # ==========================================
    # SLIDE 2: PROBLEM STATEMENT
    # ==========================================
    draw_background()
    draw_header("Executive Overview", "Problem Statement & Clinical Motivation", "Addressing acute diagnostic backlogs and emergency department triage delays")

    probs = [
        ("Diagnostic Volume & Clinician Burnout", "Worldwide shortages of specialized radiologists, dermatologists, and dentists lead to reporting turnaround delays of 24 to 72 hours in outpatient clinics.", C_RED),
        ("The False-Negative Emergency Penalty", "In acute trauma or infection (e.g. Pneumothorax, aggressive Melanoma, acute Caries), missing a diagnosis causes irreversible patient morbidity. High recall is critical.", C_GOLD),
        ("Lack of Clinical Interpretability", "Attending physicians reject opaque 'black-box' neural network predictions. Diagnostic recommendations require visual proof of the underlying anatomical pathology.", C_CYAN),
        ("Siloed Single-Organ Tools", "Existing AI software addresses only isolated specialties. Community healthcare centers urgently need a unified gateway spanning chest, skin, and oral health.", C_BLUE)
    ]

    card_w = (w - 80 - 20) / 2
    card_h = 185
    for i, (p_t, p_d, p_c) in enumerate(probs):
        col = i % 2
        row = i // 2
        cx = 40 + col * (card_w + 20)
        cy = (h - 110 - card_h) - row * (card_h + 20)
        draw_card(cx, cy, card_w, card_h, border_color=p_c)

        c.setFillColor(p_c)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(cx + 18, cy + card_h - 32, f"●  {p_t}")

        c.setFillColor(C_WHITE)
        c.setFont("Helvetica", 10)
        # Simple text wrapping
        words = p_d.split()
        lines = []
        cur = []
        for word in words:
            if len(" ".join(cur + [word])) < 58:
                cur.append(word)
            else:
                lines.append(" ".join(cur))
                cur = [word]
        if cur:
            lines.append(" ".join(cur))

        ly = cy + card_h - 60
        for line in lines:
            c.drawString(cx + 18, ly, line)
            ly -= 18

    draw_footer(2)
    c.showPage()

    # ==========================================
    # SLIDE 3: CLINICAL CREDIBILITY & RESEARCH
    # ==========================================
    draw_background()
    draw_header("Scientific Foundations", "Clinical Credibility & Ethical Regulatory Scope", "Anchored in peer-reviewed literature and patient-safety medical ethics")

    # Left Box
    card_w = (w - 80 - 20) / 2
    draw_card(40, 60, card_w, 420, border_color=C_BLUE)
    c.setFillColor(C_CYAN)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(60, 450, "Peer-Reviewed Academic Foundations")

    studies = [
        ("Stanford CheXNet (Rajpurkar et al., 2017)", "A 121-layer DenseNet trained on 112,120 chest radiographs that exceeded average radiologist performance on Pneumonia detection on NIH ChestX-ray14."),
        ("Esteva et al. (Nature, 2017)", "Deep convolutional neural networks demonstrating dermatologist-level classification accuracy across biopsy-verified melanoma and non-melanocytic lesions."),
        ("Grad-CAM (Selvaraju et al., ICCV 2017)", "Visual explanations from deep networks via gradient-weighted class activation mapping, localizing salient pathology features in final convolutional layers.")
    ]
    sy = 410
    for s_t, s_d in studies:
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(60, sy, f"✔ {s_t}")
        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 9)
        # wrap
        words = s_d.split()
        lines, cur = [], []
        for w_item in words:
            if len(" ".join(cur + [w_item])) < 64: cur.append(w_item)
            else: lines.append(" ".join(cur)); cur = [w_item]
        if cur: lines.append(" ".join(cur))
        ly = sy - 16
        for line in lines:
            c.drawString(75, ly, line)
            ly -= 14
        sy = ly - 16

    # Right Box
    draw_card(40 + card_w + 20, 60, card_w, 420, border_color=C_GOLD)
    c.setFillColor(C_GOLD)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(60 + card_w + 20, 450, "Medical Ethics & Clinical Governance")

    ethics = [
        ("Decision Support, Never Autonomous", "Explicitly designed as a second-reader and queue triage tool. It empowers attending doctors rather than replacing human diagnosis."),
        ("Prioritizing Sensitivity (Low False Negatives)", "In clinical emergencies, false negatives carry a severe penalty. Decision thresholds are calibrated to prevent missing active high-risk conditions."),
        ("Physician-in-the-Loop Confirmation", "All machine evaluations require formal sign-off. Clinicians enter free-text observations and confirm or modify the triage determination."),
        ("Containerized Privacy & Ephemeral Data", "Patient personally identifiable information (PII) is decoupled from the ML pipeline. Inference occurs over ephemeral memory buffers.")
    ]
    sy = 410
    for e_t, e_d in ethics:
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(60 + card_w + 20, sy, f"⚖ {e_t}")
        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 9)
        words = e_d.split()
        lines, cur = [], []
        for w_item in words:
            if len(" ".join(cur + [w_item])) < 64: cur.append(w_item)
            else: lines.append(" ".join(cur)); cur = [w_item]
        if cur: lines.append(" ".join(cur))
        ly = sy - 16
        for line in lines:
            c.drawString(75 + card_w + 20, ly, line)
            ly -= 14
        sy = ly - 14

    draw_footer(3)
    c.showPage()

    # ==========================================
    # SLIDE 4: TRI-MODAL CLINICAL COVERAGE
    # ==========================================
    draw_background()
    draw_header("Pathology Scope", "Tri-Modal Clinical Coverage Overview", "Comprehensive multi-specialty triage in a unified clinical dashboard")

    mods = [
        ("Chest Radiography", "14 Thoracic Conditions", C_CYAN, [
            "Atelectasis (Lung Collapse)", "Cardiomegaly (Enlarged Heart)", "Effusion (Fluid in Lungs)",
            "Infiltration (Substance Infiltration)", "Mass (Tumor / Neoplasm >3cm)", "Nodule (Focal Opacity <=3cm)",
            "Pneumonia (Infectious Infiltrate)", "Pneumothorax (Free Air in Pleura)", "Consolidation (Alveolar Fluid)",
            "Edema (Pulmonary Fluid)", "Emphysema (Hyperinflation)", "Fibrosis (Scarring)",
            "Pleural Thickening", "Hernia (Diaphragmatic Herniation)"
        ]),
        ("Dermatology", "7 Lesion Categories", C_BLUE, [
            "Melanoma (Malignant Melanocytic)", "Basal Cell Carcinoma (BCC)",
            "Benign Keratosis (BKL / Seborrheic)", "Melanocytic Nevi (Common Moles)",
            "Actinic Keratoses (AKIEC / Pre-malignant)", "Dermatofibroma (Benign Fibroma)",
            "Vascular Lesions (Angiomas / Pyogenic)", "Covers primary ISIC / HAM10000 classes"
        ]),
        ("Dental Triage", "6 Oral Pathologies", C_GOLD, [
            "Dental Caries (Active Enamel Decay)", "Dental Calculus (Supragingival Tartar)",
            "Gingivitis (Marginal Gum Inflammation)", "Mouth Ulcer (Aphthous Stomatitis)",
            "Tooth Discoloration (Intrinsic/Extrinsic)", "Hypodontia (Congenital Missing Teeth)",
            "Automated contour localization"
        ])
    ]
    card_w = (w - 80 - 30) / 3
    for i, (m_t, m_s, m_c, m_list) in enumerate(mods):
        cx = 40 + i * (card_w + 15)
        draw_card(cx, 60, card_w, 420, border_color=m_c)

        c.setFillColor(m_c)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(cx + 16, 450, m_t)

        c.setFillColor(C_WHITE)
        c.setFont("Helvetica", 10)
        c.drawString(cx + 16, 432, m_s)

        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 9)
        cur_y = 405
        for item in m_list:
            c.drawString(cx + 16, cur_y, f"• {item}")
            cur_y -= 22

    draw_footer(4)
    c.showPage()

    # ==========================================
    # SLIDE 5: MODEL ARCHITECTURES
    # ==========================================
    draw_background()
    draw_header("Model Engineering", "Deep Learning Architectures & Mathematical Formulations", "Tailored backbones, receptive fields, and loss optimization strategies")

    archs = [
        ("Thoracic Model", "DenseNet-121", C_CYAN, [
            ("Task Type", "Multi-Label Classification (14 outputs)"),
            ("Activation", "Independent Sigmoid: P(y_i=1|x) = 1/(1+e^-z_i)"),
            ("Loss Function", "Binary Cross-Entropy Loss with Pos-Weights"),
            ("Key Strength", "Dense feature reuse concatenates maps across layers; captures faint interstitial patterns."),
            ("Target Layer", "features.denseblock4.denselayer16.conv2")
        ]),
        ("Skin Classifier", "ResNet-50", C_BLUE, [
            ("Task Type", "Multi-Class Categorization (7 classes)"),
            ("Activation", "Softmax: P(y=c|x) = e^z_c / sum(e^z_k)"),
            ("Loss Function", "Focal Loss / Categorical Cross-Entropy"),
            ("Key Strength", "Bottleneck residual blocks avoid vanishing gradients on dermoscopic textures."),
            ("Target Layer", "layer4[2].conv3")
        ]),
        ("Dental Classifier", "ResNet-18", C_GOLD, [
            ("Task Type", "Multi-Class Categorization (6 classes)"),
            ("Activation", "Softmax with calibrated probability scaling"),
            ("Loss Function", "Weighted Cross-Entropy Loss"),
            ("Key Strength", "Lightweight inference (<25ms); handles macro intra-oral perspective angles."),
            ("Target Layer", "layer4[1].conv2")
        ])
    ]
    for i, (a_t, a_s, a_c, a_specs) in enumerate(archs):
        cx = 40 + i * (card_w + 15)
        draw_card(cx, 60, card_w, 420, border_color=a_c)

        c.setFillColor(a_c)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(cx + 16, 450, a_t)

        c.setFillColor(C_WHITE)
        c.setFont("Helvetica", 11)
        c.drawString(cx + 16, 432, a_s)

        cur_y = 400
        for s_lbl, s_val in a_specs:
            c.setFillColor(C_WHITE)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(cx + 16, cur_y, s_lbl)
            c.setFillColor(C_MUTED)
            c.setFont("Helvetica", 9)
            words = s_val.split()
            lines, cur = [], []
            for w_item in words:
                if len(" ".join(cur + [w_item])) < 35: cur.append(w_item)
                else: lines.append(" ".join(cur)); cur = [w_item]
            if cur: lines.append(" ".join(cur))
            ly = cur_y - 14
            for line in lines:
                c.drawString(cx + 16, ly, line)
                ly -= 12
            cur_y = ly - 10

    draw_footer(5)
    c.showPage()

    # ==========================================
    # SLIDE 6: EXPLAINABLE AI & GRAD-CAM
    # ==========================================
    draw_background()
    draw_header("Explainable AI", "Grad-CAM Mathematical Engine & Content-Aware Targeting", "Visualizing saliency activations to verify anatomical landmarks")

    card_w = (w - 80 - 20) / 2
    # Left Card
    draw_card(40, 60, card_w, 420, border_color=C_CYAN)
    c.setFillColor(C_CYAN)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(60, 450, "Gradient-Weighted Class Activation Mapping")

    gcam_info = [
        ("Step 1: Gradient Computation", "Backpropagates class score y^c to target feature maps A^k:  ∂y^c / ∂A^k"),
        ("Step 2: Neuron Importance Weights (α_k^c)", "Global average pooling over spatial coordinates (i, j):  α_k^c = (1/Z) * sum_i sum_j (∂y^c / ∂A_{i,j}^k)"),
        ("Step 3: Rectified Linear Combination", "Linear combination filtered by ReLU to retain positive influences:  L_{Grad-CAM}^c = ReLU(sum_k α_k^c * A^k)"),
        ("Step 4: Jet Colormap Blending", "Min-max normalized, resized to original resolution, and overlaid at 40% alpha transparency over the grayscale radiograph.")
    ]
    cur_y = 410
    for g_t, g_d in gcam_info:
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, cur_y, g_t)
        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 9)
        words = g_d.split()
        lines, cur = [], []
        for w_item in words:
            if len(" ".join(cur + [w_item])) < 64: cur.append(w_item)
            else: lines.append(" ".join(cur)); cur = [w_item]
        if cur: lines.append(" ".join(cur))
        ly = cur_y - 14
        for line in lines:
            c.drawString(75, ly, line)
            ly -= 13
        cur_y = ly - 12

    # Right Card
    draw_card(40 + card_w + 20, 60, card_w, 420, border_color=C_GREEN)
    c.setFillColor(C_GREEN)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(60 + card_w + 20, 450, "Intelligent Content-Aware Centroid Fallback")

    fb_info = [
        ("Dental Inflammatory Targeting", "HSV space segmentation isolates red intervals ([0,50,50] & [170,50,50]) to pinpoint gingival inflammation and aphthous ulcers."),
        ("Dental Caries & Calculus Contours", "Filters dark/brownish/yellow decay values; computes spatial centroid moments (cX, cY) to center activations over cavities."),
        ("Dermoscopic Lesion Bounding", "Applies Otsu adaptive thresholding to detect dark pigmentation borders and isolate lesion boundaries on skin surfaces."),
        ("Pulmonary Mask Constraining", "Applies bilateral lung-field masks to exclude spine/sternum and focus high-density activations strictly within pulmonary zones.")
    ]
    cur_y = 410
    for f_t, f_d in fb_info:
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60 + card_w + 20, cur_y, f_t)
        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 9)
        words = f_d.split()
        lines, cur = [], []
        for w_item in words:
            if len(" ".join(cur + [w_item])) < 64: cur.append(w_item)
            else: lines.append(" ".join(cur)); cur = [w_item]
        if cur: lines.append(" ".join(cur))
        ly = cur_y - 14
        for line in lines:
            c.drawString(75 + card_w + 20, ly, line)
            ly -= 13
        cur_y = ly - 12

    draw_footer(6)
    c.showPage()

    # ==========================================
    # SLIDE 7: TRIAGE LOGIC & SEVERITY
    # ==========================================
    draw_background()
    draw_header("Triage Rules", "Clinical Severity Scoring & Automated Risk Stratification", "Calibrated thresholds routing critical patients to immediate specialist care")

    tiers = [
        ("HIGH RISK (CRITICAL)", "Immediate Specialist Escalation", C_RED, [
            "Pneumothorax / Tension Pneumonia score > 0.45",
            "Malignant Melanoma / BCC probability > 0.30",
            "Severe Active Caries / Acute Ulcer score > 0.40",
            "Any thoracic disease probability > 0.65",
            "System Action: Placed at top of doctor triage queue with pulsing red beacon."
        ]),
        ("MEDIUM RISK (MODERATE)", "Priority Review Within 4 Hours", C_GOLD, [
            "Cardiomegaly, Edema, or Effusion score > 0.25",
            "Actinic Keratoses (pre-malignant) score > 0.30",
            "Gingivitis / Calculus / Discoloration score > 0.35",
            "Any pathology score in range [0.35 - 0.65]",
            "System Action: Marked with amber tag; clinician verification queue."
        ]),
        ("LOW RISK (ROUTINE)", "Standard Outpatient Batch Queuing", C_GREEN, [
            "All predicted pathology probabilities below threshold",
            "Benign nevus or non-acute dental hypodontia",
            "Normal clear lung field radiographs",
            "System Action: Standard report generation; routine discharge queue."
        ])
    ]
    card_w = (w - 80 - 30) / 3
    for i, (t_t, t_s, t_c, t_items) in enumerate(tiers):
        cx = 40 + i * (card_w + 15)
        draw_card(cx, 60, card_w, 420, border_color=t_c)

        c.setFillColor(t_c)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(cx + 16, 450, t_t)
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica", 10)
        c.drawString(cx + 16, 432, t_s)

        cur_y = 400
        for item in t_items:
            c.setFillColor(C_MUTED)
            c.setFont("Helvetica", 9)
            words = item.split()
            lines, cur = [], []
            for w_item in words:
                if len(" ".join(cur + [w_item])) < 35: cur.append(w_item)
                else: lines.append(" ".join(cur)); cur = [w_item]
            if cur: lines.append(" ".join(cur))
            for line in lines:
                c.drawString(cx + 16, cur_y, line)
                cur_y -= 13
            cur_y -= 8

    draw_footer(7)
    c.showPage()

    # ==========================================
    # SLIDE 8: SYSTEM ARCHITECTURE
    # ==========================================
    draw_background()
    draw_header("System Design", "Microservices Architecture & Monorepo Organization", "Decoupled services engineered for high concurrency and zero-downtime offline continuity")

    services = [
        ("Frontend Client", "React 19 + Vite 8 SPA", C_CYAN, [
            "Single-Page Application hosted on Vercel Global Edge CDN.",
            "Dark clinical theme built with modern Tailwind/CSS & Lucide icons.",
            "Private Network Access (PNA) client-side resilience handling.",
            "HTML5 Canvas fallback engine for in-browser Grad-CAM rendering.",
            "Zero network dependencies during standalone demonstrations."
        ]),
        ("Backend Coordination Gateway", "Express.js + Node.js (Port 5000)", C_BLUE, [
            "Central REST orchestration gateway managing patients and triage records.",
            "PNA preflight headers allowing public Vercel HTTPS -> local loopback.",
            "Dual-Persistence Engine: Mongoose MongoDB with automated in-memory fallback.",
            "Multipart stream forwarding via Axios & FormData to ML microservice."
        ]),
        ("Inference Microservice", "FastAPI + PyTorch (Port 8000)", C_GREEN, [
            "Asynchronous non-blocking Python ML prediction service.",
            "Torchvision preprocessing (224x224 RGB, ImageNet normalization).",
            "PyTorch forward/backward hooks for dynamic Grad-CAM computation.",
            "OpenCV headless image processing & color-space conversions.",
            "Interactive Swagger OpenAPI documentation at /docs."
        ])
    ]
    for i, (s_t, s_s, s_c, s_items) in enumerate(services):
        cx = 40 + i * (card_w + 15)
        draw_card(cx, 60, card_w, 420, border_color=s_c)

        c.setFillColor(s_c)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(cx + 16, 450, s_t)
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica", 10)
        c.drawString(cx + 16, 432, s_s)

        cur_y = 400
        for item in s_items:
            c.setFillColor(C_MUTED)
            c.setFont("Helvetica", 9)
            words = item.split()
            lines, cur = [], []
            for w_item in words:
                if len(" ".join(cur + [w_item])) < 35: cur.append(w_item)
                else: lines.append(" ".join(cur)); cur = [w_item]
            if cur: lines.append(" ".join(cur))
            for line in lines:
                c.drawString(cx + 16, cur_y, f"• {line}" if line == lines[0] else f"  {line}")
                cur_y -= 13
            cur_y -= 6

    draw_footer(8)
    c.showPage()

    # ==========================================
    # SLIDE 9: DASHBOARD UX
    # ==========================================
    draw_background()
    draw_header("User Interface", "Doctor-Facing Dashboard & Clinical Workflow", "Ergonomic interface designed for rapid visual verification and decision logging")

    ux = [
        ("Real-Time Prioritized Triage Queue", "Automatically categorizes incoming patient scans. Displays entries sorted chronologically and tagged with High (Red), Medium (Amber), or Low (Green) severity banners.", C_CYAN),
        ("Side-by-Side Grad-CAM Heatmap Viewer", "Permits attending physicians to inspect the raw input radiograph side-by-side with the semi-transparent Grad-CAM activation overlay to verify anatomical structures.", C_BLUE),
        ("Probability Breakdown & Refocusing", "Displays interactive percentage bars for every candidate pathology. Doctors can click alternative conditions to generate targeted Grad-CAM overlays on demand.", C_GOLD),
        ("Clinical Decision & Audit Logging", "Provides dedicated text inputs for attending doctors to record qualitative clinical notes, validate or modify triage severity, and mark reports as 'Reviewed'.", C_GREEN)
    ]
    card_w = (w - 80 - 20) / 2
    card_h = 185
    for i, (u_t, u_d, u_c) in enumerate(ux):
        col = i % 2
        row = i // 2
        cx = 40 + col * (card_w + 20)
        cy = (h - 110 - card_h) - row * (card_h + 20)
        draw_card(cx, cy, card_w, card_h, border_color=u_c)

        c.setFillColor(u_c)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(cx + 18, cy + card_h - 32, f"✦  {u_t}")

        c.setFillColor(C_WHITE)
        c.setFont("Helvetica", 10)
        words = u_d.split()
        lines, cur = [], []
        for word in words:
            if len(" ".join(cur + [word])) < 58: cur.append(word)
            else: lines.append(" ".join(cur)); cur = [word]
        if cur: lines.append(" ".join(cur))

        ly = cy + card_h - 60
        for line in lines:
            c.drawString(cx + 18, ly, line)
            ly -= 18

    draw_footer(9)
    c.showPage()

    # ==========================================
    # SLIDE 10: DATASETS & PREPROCESSING
    # ==========================================
    draw_background()
    draw_header("Data Engineering", "Datasets & Computer Vision Pipelines", "Curation, standardization, and domain-specific normalization protocols")

    data = [
        ("NIH ChestX-ray14", "112,120 Frontal X-Rays", C_CYAN, [
            "Source: National Institutes of Health Clinical Center",
            "30,805 unique patients with NLP-mined radiological labels",
            "Transforms: Resize(256), CenterCrop(224), ToTensor()",
            "Normalization: ImageNet Mean [0.485, 0.456, 0.406], Std [0.229, 0.224, 0.225]"
        ]),
        ("HAM10000 / ISIC", "10,015 Dermoscopy Images", C_BLUE, [
            "Source: International Skin Imaging Collaboration",
            "Biopsy-confirmed melanocytic and non-melanocytic lesions",
            "Hair artifact suppression and color histogram calibration",
            "Transforms: RandomHorizontalFlip(p=0.5), Aspect-ratio preservation"
        ]),
        ("Dental Pathology Dataset", "6 Oral Diagnostic Categories", C_GOLD, [
            "Curation: Calculus, Caries, Gingivitis, Ulcers, Discoloration, Hypodontia",
            "Annotated with YOLO bounding box metadata and category labels",
            "Adaptive histogram equalization (CLAHE) for plaque detection",
            "Macro perspective alignment and color contrast enhancement"
        ])
    ]
    card_w = (w - 80 - 30) / 3
    for i, (d_t, d_s, d_c, d_items) in enumerate(data):
        cx = 40 + i * (card_w + 15)
        draw_card(cx, 60, card_w, 420, border_color=d_c)

        c.setFillColor(d_c)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(cx + 16, 450, d_t)
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica", 10)
        c.drawString(cx + 16, 432, d_s)

        cur_y = 400
        for item in d_items:
            c.setFillColor(C_MUTED)
            c.setFont("Helvetica", 9)
            words = item.split()
            lines, cur = [], []
            for w_item in words:
                if len(" ".join(cur + [w_item])) < 35: cur.append(w_item)
                else: lines.append(" ".join(cur)); cur = [w_item]
            if cur: lines.append(" ".join(cur))
            for line in lines:
                c.drawString(cx + 16, cur_y, f"• {line}" if line == lines[0] else f"  {line}")
                cur_y -= 13
            cur_y -= 8

    draw_footer(10)
    c.showPage()

    # ==========================================
    # SLIDE 11: PRODUCTION DEPLOYMENT & MLOPS
    # ==========================================
    draw_background()
    draw_header("Cloud Deployment", "Production Architecture & Live Verification", "Containerized, version-controlled, and globally hosted on Vercel")

    ops = [
        ("Vercel Edge Cloud Deployment", "Live Production Frontend", C_CYAN, [
            "Live URL: https://medical-triage-kohl.vercel.app",
            "Configured via monorepo vercel.json with SPA rewrites",
            "Global edge CDN distribution with HTTP/2 and SSL/TLS",
            "Zero-latency client fallback engine for standalone demos"
        ]),
        ("GitHub Version Control", "Enterprise Repository Management", C_BLUE, [
            "Repository: https://github.com/omveer7850/medical-triage",
            "Full commit history on main branch",
            "Strict .gitignore and .vercelignore protecting heavy weights",
            "SSH authentication protocol & automated branch tracking"
        ]),
        ("Docker Containerization", "Multi-Service Orchestration", C_GREEN, [
            "Multi-stage Dockerfiles for Frontend, Express, and ML Service",
            "docker-compose.yml defines isolated bridge network & volumes",
            "Automated health checks and restart policies configured",
            "Runtime parity across Windows, Linux, and Cloud environments"
        ])
    ]
    for i, (o_t, o_s, o_c, o_items) in enumerate(ops):
        cx = 40 + i * (card_w + 15)
        draw_card(cx, 60, card_w, 420, border_color=o_c)

        c.setFillColor(o_c)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(cx + 16, 450, o_t)
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica", 10)
        c.drawString(cx + 16, 432, o_s)

        cur_y = 400
        for item in o_items:
            c.setFillColor(C_MUTED)
            c.setFont("Helvetica", 9)
            words = item.split()
            lines, cur = [], []
            for w_item in words:
                if len(" ".join(cur + [w_item])) < 35: cur.append(w_item)
                else: lines.append(" ".join(cur)); cur = [w_item]
            if cur: lines.append(" ".join(cur))
            for line in lines:
                c.drawString(cx + 16, cur_y, f"✔ {line}" if line == lines[0] else f"  {line}")
                cur_y -= 13
            cur_y -= 8

    draw_footer(11)
    c.showPage()

    # ==========================================
    # SLIDE 12: ROADMAP & FUTURE WORK
    # ==========================================
    draw_background()
    draw_header("Future Horizons", "Semester 2 Roadmap & Hospital System Integration", "Expanding from prototype triage into full clinical hospital workflows")

    road = [
        ("Phase 1: PACS & DICOM Integration", "Implement native .dcm file ingestion with Cornerstone.js / OHIF viewer, parsing patient metadata and high-bitrate DICOM windowing presets.", C_CYAN),
        ("Phase 2: Multi-View & Longitudinal Correlation", "Expand thoracic pipeline to ingest Lateral + PA views simultaneously and correlate findings against historical prior exams to spot tumor progression.", C_BLUE),
        ("Phase 3: Federated Learning & Privacy", "Deploy Flower/PySyft federated training across hospital nodes without centralizing raw protected health information (PHI), ensuring GDPR/HIPAA compliance.", C_GOLD),
        ("Phase 4: Prospective Clinical Trial", "Conduct observational shadow studies measuring reduction in radiologist report turnaround time and emergency room triage queue latency.", C_GREEN)
    ]
    card_w = (w - 80 - 20) / 2
    card_h = 185
    for i, (r_t, r_d, r_c) in enumerate(road):
        col = i % 2
        row = i // 2
        cx = 40 + col * (card_w + 20)
        cy = (h - 110 - card_h) - row * (card_h + 20)
        draw_card(cx, cy, card_w, card_h, border_color=r_c)

        c.setFillColor(r_c)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(cx + 18, cy + card_h - 32, f"🚀  {r_t}")

        c.setFillColor(C_WHITE)
        c.setFont("Helvetica", 10)
        words = r_d.split()
        lines, cur = [], []
        for word in words:
            if len(" ".join(cur + [word])) < 58: cur.append(word)
            else: lines.append(" ".join(cur)); cur = [word]
        if cur: lines.append(" ".join(cur))

        ly = cy + card_h - 60
        for line in lines:
            c.drawString(cx + 18, ly, line)
            ly -= 18

    draw_footer(12)
    c.showPage()

    # ==========================================
    # SLIDE 13: SUMMARY & LIVE LINKS
    # ==========================================
    draw_background()
    draw_header("Conclusion", "Project Summary & Live Deployment Links", "Ready for clinical demonstration, code review, and academic presentation")

    card_w = (w - 80 - 20) / 2
    # Left Box
    draw_card(40, 60, card_w, 420, border_color=C_CYAN)
    c.setFillColor(C_CYAN)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(60, 450, "Key Project Takeaways")

    takeaways = [
        ("Tri-Modal Clinical Scope", "Seamlessly handles Chest Radiographs (14 conditions), Skin Lesions (7 conditions), and Dental Scans (6 conditions) in one unified portal."),
        ("Explainable AI via Grad-CAM", "Builds physician trust by highlighting exact spatial anomalies on scans with dynamic gradient activation heatmaps."),
        ("Patient-Safety Triage Engine", "Prioritizes high-risk emergency cases first (low false negative rate) to reduce time-to-treatment for critical patients."),
        ("High-Availability Engineering", "Resilient fallback architecture guarantees uninterrupted uptime even in offline or browser-restricted demonstration environments.")
    ]
    cur_y = 410
    for t_t, t_d in takeaways:
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(60, cur_y, f"✔ {t_t}")
        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 9)
        words = t_d.split()
        lines, cur = [], []
        for w_item in words:
            if len(" ".join(cur + [w_item])) < 64: cur.append(w_item)
            else: lines.append(" ".join(cur)); cur = [w_item]
        if cur: lines.append(" ".join(cur))
        ly = cur_y - 14
        for line in lines:
            c.drawString(75, ly, line)
            ly -= 13
        cur_y = ly - 12

    # Right Box
    draw_card(40 + card_w + 20, 60, card_w, 420, border_color=C_GREEN)
    c.setFillColor(C_GREEN)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(60 + card_w + 20, 450, "Live Deployment Links & Repositories")

    links = [
        ("Vercel Production Application", "https://medical-triage-kohl.vercel.app", C_CYAN),
        ("Alternate Live Mirror", "https://frontend-one-lovat-88.vercel.app", C_CYAN),
        ("GitHub Source Code Repository", "https://github.com/omveer7850/medical-triage", C_BLUE),
        ("FastAPI Interactive Documentation", "http://localhost:8000/docs", C_GOLD)
    ]
    cur_y = 410
    for l_t, l_u, l_c in links:
        c.setFillColor(l_c)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(60 + card_w + 20, cur_y, f"🔗 {l_t}")
        c.setFillColor(C_LIGHT)
        c.setFont("Helvetica", 9)
        c.drawString(75 + card_w + 20, cur_y - 15, l_u)
        cur_y -= 48

    draw_footer(13)
    c.showPage()

    c.save()
    print(f"Simple PDF Presentation generated successfully: {os.path.abspath(pdf_filename)}")

if __name__ == "__main__":
    generate_pdf()
