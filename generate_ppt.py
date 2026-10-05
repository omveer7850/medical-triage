import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    # Theme Colors
    COLOR_BG = RGBColor(15, 23, 42)        # Slate 900
    COLOR_CARD = RGBColor(30, 41, 59)      # Slate 800
    COLOR_CARD_BORDER = RGBColor(51, 65, 85) # Slate 700
    COLOR_CYAN = RGBColor(6, 182, 212)     # Electric Cyan
    COLOR_BLUE = RGBColor(59, 130, 246)    # Royal Blue
    COLOR_GREEN = RGBColor(16, 185, 129)   # Emerald Green
    COLOR_GOLD = RGBColor(245, 158, 11)    # Amber Gold
    COLOR_RED = RGBColor(239, 68, 68)      # Ruby Red
    COLOR_WHITE = RGBColor(248, 250, 252)  # Slate 50
    COLOR_MUTED = RGBColor(148, 163, 184)  # Slate 400

    def add_slide_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, tag_text, title_text, subtitle_text=None):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.733), Inches(1.2))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Tag
        p_tag = tf.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = COLOR_CYAN
        p_tag.space_after = Pt(2)

        # Title
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_WHITE
        
        if subtitle_text:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle_text
            p_sub.font.size = Pt(12)
            p_sub.font.color.rgb = COLOR_MUTED

    def add_card(slide, left, top, width, height, border_color=COLOR_CARD_BORDER, bg_color=COLOR_CARD):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        return card

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_slide_layout)
    add_slide_bg(s1)

    # Accent decorative bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.1), Inches(11.733), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLOR_CYAN
    bar.line.fill.background()

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.733), Inches(2.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "AI-BASED MEDICAL IMAGE DIAGNOSIS &\nTRIAGE SUPPORT SYSTEM"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.space_after = Pt(12)

    p2 = tf.add_paragraph()
    p2.text = "Multi-Modal Deep Learning & Explainable AI (Grad-CAM) for Chest Radiographs, Dermatological Lesions, and Dental Pathologies"
    p2.font.size = Pt(16)
    p2.font.color.rgb = COLOR_CYAN

    # 3 Badges / Feature Cards across bottom
    badges = [
        ("Clinical Modalities", "Chest X-Ray (14 Diseases)\nSkin Lesions (7 Classes)\nDental Triage (6 Pathologies)", COLOR_BLUE),
        ("Explainable AI & Triage", "Grad-CAM Heatmap Overlays\nAutomated Urgency Scoring\nSensitivity-First Prioritization", COLOR_GREEN),
        ("Production Deployed", "Full Monorepo Architecture\nFastAPI + Express + React\nLive on Vercel & GitHub", COLOR_CYAN)
    ]

    card_w = Inches(3.64)
    for i, (b_title, b_desc, b_color) in enumerate(badges):
        c_left = Inches(0.8) + i * Inches(4.04)
        add_card(s1, c_left, Inches(4.3), card_w, Inches(2.2), border_color=b_color)
        t_box = s1.shapes.add_textbox(c_left + Inches(0.2), Inches(4.45), card_w - Inches(0.4), Inches(1.9))
        c_tf = t_box.text_frame
        c_tf.word_wrap = True
        
        cp1 = c_tf.paragraphs[0]
        cp1.text = b_title
        cp1.font.size = Pt(14)
        cp1.font.bold = True
        cp1.font.color.rgb = b_color
        cp1.space_after = Pt(8)

        cp2 = c_tf.add_paragraph()
        cp2.text = b_desc
        cp2.font.size = Pt(12)
        cp2.font.color.rgb = COLOR_MUTED

    # ==========================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # ==========================================
    s2 = prs.slides.add_slide(blank_slide_layout)
    add_slide_bg(s2)
    add_header(s2, "Executive Overview", "Problem Statement & Clinical Motivation", "Addressing diagnostic backlogs and acute emergency triage delays")

    probs = [
        ("Diagnostic Backlogs", "Radiologists and dermatologists worldwide face overwhelming diagnostic volume, leading to burnout and reporting turnaround delays of 24–72 hours.", COLOR_RED),
        ("The False-Negative Penalty", "In emergency triage, missing an active Pneumothorax, aggressive Melanoma, or acute Dental Caries causes irreversible patient harm. High recall is mandatory.", COLOR_GOLD),
        ("Lack of Interpretability", "Clinicians reject black-box AI predictions without spatial visual proof showing exactly which anatomical features triggered the diagnostic score.", COLOR_CYAN),
        ("Multi-Disciplinary Need", "Most clinical tools isolate a single organ. Primary care clinics require a unified triaging gateway capable of handling thoracic, dermatologic, and dental images.", COLOR_BLUE)
    ]

    for i, (p_title, p_desc, p_color) in enumerate(probs):
        col = i % 2
        row = i // 2
        c_left = Inches(0.8) + col * Inches(5.95)
        c_top = Inches(1.85) + row * Inches(2.55)
        add_card(s2, c_left, c_top, Inches(5.75), Inches(2.35), border_color=p_color)

        t_box = s2.shapes.add_textbox(c_left + Inches(0.3), c_top + Inches(0.25), Inches(5.15), Inches(1.85))
        c_tf = t_box.text_frame
        c_tf.word_wrap = True

        cp1 = c_tf.paragraphs[0]
        cp1.text = f"●  {p_title}"
        cp1.font.size = Pt(16)
        cp1.font.bold = True
        cp1.font.color.rgb = p_color
        cp1.space_after = Pt(8)

        cp2 = c_tf.add_paragraph()
        cp2.text = p_desc
        cp2.font.size = Pt(13)
        cp2.font.color.rgb = COLOR_WHITE

    # ==========================================
    # SLIDE 3: CLINICAL CREDIBILITY & LITERATURE
    # ==========================================
    s3 = prs.slides.add_slide(blank_slide_layout)
    add_slide_bg(s3)
    add_header(s3, "Scientific Grounding", "Clinical Credibility & Research Foundations", "Grounded in peer-reviewed peer studies and strict medical ethics")

    # Left Card: Literature Foundations
    add_card(s3, Inches(0.8), Inches(1.85), Inches(5.75), Inches(5.1), border_color=COLOR_BLUE)
    tb_lit = s3.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.15), Inches(4.6))
    tf_lit = tb_lit.text_frame
    tf_lit.word_wrap = True

    p = tf_lit.paragraphs[0]
    p.text = "Peer-Reviewed Foundations"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(14)

    studies = [
        ("Stanford CheXNet (Rajpurkar et al., 2017)", "121-layer DenseNet outperforming practicing board-certified radiologists on Pneumonia detection on NIH ChestX-ray14 dataset."),
        ("Esteva et al. (Nature, 2017)", "Deep convolutional neural networks demonstrating dermatologist-level classification of skin cancer across biopsy-verified lesions."),
        ("Grad-CAM (Selvaraju et al., ICCV 2017)", "Visual explanations from deep networks via gradient-based localization in final convolutional layer feature maps.")
    ]
    for s_title, s_desc in studies:
        p_t = tf_lit.add_paragraph()
        p_t.text = f"✔ {s_title}"
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_WHITE
        p_t.space_after = Pt(2)
        p_d = tf_lit.add_paragraph()
        p_d.text = s_desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = COLOR_MUTED
        p_d.space_after = Pt(10)

    # Right Card: Medical Disclaimer & Ethics
    add_card(s3, Inches(6.75), Inches(1.85), Inches(5.75), Inches(5.1), border_color=COLOR_GOLD)
    tb_eth = s3.shapes.add_textbox(Inches(7.05), Inches(2.1), Inches(5.15), Inches(4.6))
    tf_eth = tb_eth.text_frame
    tf_eth.word_wrap = True

    p = tf_eth.paragraphs[0]
    p.text = "Ethical Framework & Regulatory Scope"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD
    p.space_after = Pt(14)

    ethics = [
        ("Triage & Decision-Support Only", "This platform is explicitly engineered as a clinical prioritizer and second reader, never as an autonomous diagnostic authority."),
        ("Sensitivity Prioritization", "Thresholds favor high sensitivity (low false negative rate) for acute conditions, ensuring critical patients are never downgraded in triage queues."),
        ("Clinician in the Loop", "All reports remain in 'Pending Review' status until a certified physician signs off with qualitative medical notes and confirms actions."),
        ("Data Privacy & HIPAA Readiness", "Zero patient identification data is bundled with deep learning inference payloads; image processing is ephemeral and containerized.")
    ]
    for e_title, e_desc in ethics:
        p_t = tf_eth.add_paragraph()
        p_t.text = f"⚖ {e_title}"
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_WHITE
        p_t.space_after = Pt(2)
        p_d = tf_eth.add_paragraph()
        p_d.text = e_desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = COLOR_MUTED
        p_d.space_after = Pt(10)

    # ==========================================
    # SLIDE 4: TRI-MODAL CLINICAL COVERAGE
    # ==========================================
    s4 = prs.slides.add_slide(blank_slide_layout)
    add_slide_bg(s4)
    add_header(s4, "Multi-Disciplinary Scope", "Tri-Modal Clinical Pathology Coverage", "Unified diagnostic triage across chest radiography, dermatology, and dentistry")

    modalities = [
        ("Chest Radiography", "14 Thoracic Conditions", COLOR_CYAN, [
            "Atelectasis", "Cardiomegaly", "Effusion",
            "Infiltration", "Mass", "Nodule",
            "Pneumonia", "Pneumothorax", "Consolidation",
            "Edema", "Emphysema", "Fibrosis",
            "Pleural Thickening", "Hernia"
        ]),
        ("Dermatology", "7 Lesion Categories", COLOR_BLUE, [
            "Melanoma (Malignant)", "Basal Cell Carcinoma (BCC)",
            "Benign Keratosis (BKL)", "Melanocytic Nevi (NV)",
            "Actinic Keratoses (AKIEC)", "Dermatofibroma (DF)",
            "Vascular Lesions (VASC)"
        ]),
        ("Dental Triage", "6 Oral Pathologies", COLOR_GOLD, [
            "Dental Caries (Tooth Decay)", "Dental Calculus (Tartar)",
            "Gingivitis (Gum Inflammation)", "Mouth Ulcer / Aphthous",
            "Tooth Discoloration", "Hypodontia (Missing Teeth)"
        ])
    ]

    card_w = Inches(3.64)
    for i, (m_title, m_sub, m_color, m_items) in enumerate(modalities):
        c_left = Inches(0.8) + i * Inches(4.04)
        add_card(s4, c_left, Inches(1.85), card_w, Inches(5.1), border_color=m_color)

        tb_m = s4.shapes.add_textbox(c_left + Inches(0.25), Inches(2.1), card_w - Inches(0.5), Inches(4.6))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True

        p1 = tf_m.paragraphs[0]
        p1.text = m_title
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = m_color

        p2 = tf_m.add_paragraph()
        p2.text = m_sub
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_WHITE
        p2.space_after = Pt(14)

        for item in m_items:
            pi = tf_m.add_paragraph()
            pi.text = f"• {item}"
            pi.font.size = Pt(11)
            pi.font.color.rgb = COLOR_MUTED
            pi.space_after = Pt(4)

    # ==========================================
    # SLIDE 5: DEEP LEARNING MODEL ARCHITECTURES
    # ==========================================
    s5 = prs.slides.add_slide(blank_slide_layout)
    add_slide_bg(s5)
    add_header(s5, "Model Engineering", "Deep Learning Architectures & Mathematical Formulation", "Backbones, receptive fields, and loss optimization strategies")

    models = [
        ("CheXNet (Thoracic)", "DenseNet-121 Backbone", COLOR_CYAN, [
            ("Output Type", "Multi-Label Classification (14 independent probabilities)"),
            ("Activation", "Independent Sigmoid: P(y_i = 1 | x) = 1 / (1 + e^-z_i)"),
            ("Key Advantage", "Feature reuse via dense connectivity; mitigates vanishing gradient; captures fine interstitial markings."),
            ("Target Layer", "features.denseblock4.denselayer16.conv2")
        ]),
        ("Skin Lesion Classifier", "ResNet-50 Backbone", COLOR_BLUE, [
            ("Output Type", "Multi-Class Categorization (7 mutually exclusive classes)"),
            ("Activation", "Softmax: P(y = c | x) = e^z_c / sum(e^z_k)"),
            ("Key Advantage", "50-layer residual connections with bottle-neck blocks; prevents degradation on dermoscopic color textures."),
            ("Target Layer", "layer4[2].conv3")
        ]),
        ("Dental Pathology Classifier", "ResNet-18 Backbone", COLOR_GOLD, [
            ("Output Type", "Multi-Class Categorization (6 dental conditions)"),
            ("Activation", "Softmax with high-temperature calibrated scoring"),
            ("Key Advantage", "Lightweight architecture suited for rapid inference; handles intra-oral camera angles and macro focal depths."),
            ("Target Layer", "layer4[1].conv2")
        ])
    ]

    for i, (m_name, m_bb, m_color, m_specs) in enumerate(models):
        c_left = Inches(0.8) + i * Inches(4.04)
        add_card(s5, c_left, Inches(1.85), card_w, Inches(5.1), border_color=m_color)

        tb_m = s5.shapes.add_textbox(c_left + Inches(0.25), Inches(2.1), card_w - Inches(0.5), Inches(4.6))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True

        p1 = tf_m.paragraphs[0]
        p1.text = m_name
        p1.font.size = Pt(17)
        p1.font.bold = True
        p1.font.color.rgb = m_color

        p2 = tf_m.add_paragraph()
        p2.text = m_bb
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_WHITE
        p2.space_after = Pt(12)

        for spec_label, spec_val in m_specs:
            p_s = tf_m.add_paragraph()
            p_s.text = spec_label
            p_s.font.size = Pt(12)
            p_s.font.bold = True
            p_s.font.color.rgb = COLOR_CYAN if m_color != COLOR_CYAN else COLOR_WHITE
            p_s.space_after = Pt(1)

            p_v = tf_m.add_paragraph()
            p_v.text = spec_val
            p_v.font.size = Pt(10)
            p_v.font.color.rgb = COLOR_MUTED
            p_v.space_after = Pt(8)

    # ==========================================
    # SLIDE 6: EXPLAINABLE AI & GRAD-CAM
    # ==========================================
    s6 = prs.slides.add_slide(blank_slide_layout)
    add_slide_bg(s6)
    add_header(s6, "Visual Explainability", "Explainable AI (Grad-CAM) & Content-Aware Centroid Targeting", "Empowering clinicians to inspect deep visual attention maps")

    # Left Column: Grad-CAM Mathematics & PyTorch Hook
    add_card(s6, Inches(0.8), Inches(1.85), Inches(5.75), Inches(5.1), border_color=COLOR_CYAN)
    tb_gcam = s6.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.15), Inches(4.6))
    tf_gcam = tb_gcam.text_frame
    tf_gcam.word_wrap = True

    p = tf_gcam.paragraphs[0]
    p.text = "Mathematical Formulation"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(12)

    gcam_steps = [
        ("1. Neuron Importance Weights (α_k^c)", "Computed via global-average-pooling of gradients of score y^c with respect to feature maps A^k: α_k^c = (1/Z) * sum_i sum_j (∂y^c / ∂A_{i,j}^k)"),
        ("2. Rectified Linear Combination", "Captures features with positive influence on pathology class c: L_{Grad-CAM}^c = ReLU(sum_k α_k^c * A^k)"),
        ("3. Colormap Overlay & Normalization", "Heatmap is min-max normalized, resized to original scan dimensions, mapped via JET colormap, and blended with 40% alpha transparency.")
    ]
    for st_title, st_desc in gcam_steps:
        p_t = tf_gcam.add_paragraph()
        p_t.text = st_title
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_WHITE
        p_t.space_after = Pt(2)
        p_d = tf_gcam.add_paragraph()
        p_d.text = st_desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = COLOR_MUTED
        p_d.space_after = Pt(10)

    # Right Column: Content-Aware Fallback Engine
    add_card(s6, Inches(6.75), Inches(1.85), Inches(5.75), Inches(5.1), border_color=COLOR_GREEN)
    tb_fb = s6.shapes.add_textbox(Inches(7.05), Inches(2.1), Inches(5.15), Inches(4.6))
    tf_fb = tb_fb.text_frame
    tf_fb.word_wrap = True

    p = tf_fb.paragraphs[0]
    p.text = "Intelligent Content-Aware Targeting"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN
    p.space_after = Pt(12)

    fb_items = [
        ("Teeth Inflammatory Detection", "Converts oral images to HSV space; isolates dual red-hue intervals ([0,50,50] & [170,50,50]) to dynamically center heatmaps on gingival bleeding and ulcers."),
        ("Dental Decay & Plaque Contours", "Filters dark brown/yellow decay shades; computes spatial contour moments (cX, cY) to center activation on tooth cavities."),
        ("Dermatological Lesion Segmentation", "Applies localized Otsu adaptive thresholding to detect dark pigmentation borders and isolate lesion core coordinates."),
        ("Chest Consolidation Masking", "Applies bilateral lung-field masks to exclude spine/sternum and focus high-density activations strictly within pulmonary zones.")
    ]
    for fb_title, fb_desc in fb_items:
        p_t = tf_fb.add_paragraph()
        p_t.text = f"✔ {fb_title}"
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_WHITE
        p_t.space_after = Pt(2)
        p_d = tf_fb.add_paragraph()
        p_d.text = fb_desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = COLOR_MUTED
        p_d.space_after = Pt(8)

    # ==========================================
    # SLIDE 7: CLINICAL SEVERITY & TRIAGE ENGINE
    # ==========================================
    s7 = prs.slides.add_slide(blank_slide_layout)
    add_slide_bg(s7)
    add_header(s7, "Triage Logic", "Risk Stratification & Clinical Severity Scoring", "Intelligent priority routing to reduce critical time-to-treatment")

    tiers = [
        ("HIGH RISK (CRITICAL)", "Immediate Radiologist / Specialist Notification", COLOR_RED, [
            "Pneumothorax / Tension Pneumonia prob > 0.45",
            "Melanoma or Basal Cell Carcinoma prob > 0.30",
            "Severe Active Caries / Mouth Ulcer prob > 0.40",
            "Any generic thoracic pathology probability > 0.65",
            "Workflow Action: Placed at top of triage queue; red alert beacon in dashboard."
        ]),
        ("MEDIUM RISK (MODERATE)", "Priority Review Within 4 Hours", COLOR_GOLD, [
            "Cardiomegaly, Edema, Effusion prob > 0.25",
            "Actinic Keratoses / Keratosis lesions prob > 0.30",
            "Gingivitis / Calculus / Tooth Discoloration prob > 0.35",
            "Any pathology score in range [0.35 - 0.65]",
            "Workflow Action: Marked with amber tag; clinician secondary verification queue."
        ]),
        ("LOW RISK (ROUTINE)", "Standard Outpatient Queuing", COLOR_GREEN, [
            "All predicted pathology probabilities < threshold",
            "Benign nevus or non-acute dental hypodontia",
            "Normal thoracic clear lung field predictions",
            "Workflow Action: Routine batch reporting; standard discharge documentation."
        ])
    ]

    for i, (t_title, t_sub, t_color, t_rules) in enumerate(tiers):
        c_left = Inches(0.8) + i * Inches(4.04)
        add_card(s7, c_left, Inches(1.85), card_w, Inches(5.1), border_color=t_color)

        tb_t = s7.shapes.add_textbox(c_left + Inches(0.25), Inches(2.1), card_w - Inches(0.5), Inches(4.6))
        tf_t = tb_t.text_frame
        tf_t.word_wrap = True

        p1 = tf_t.paragraphs[0]
        p1.text = t_title
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = t_color

        p2 = tf_t.add_paragraph()
        p2.text = t_sub
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_WHITE
        p2.space_after = Pt(14)

        for rule in t_rules:
            pr = tf_t.add_paragraph()
            pr.text = f"• {rule}"
            pr.font.size = Pt(11)
            pr.font.color.rgb = COLOR_MUTED
            pr.space_after = Pt(6)

    # ==========================================
    # SLIDE 8: FULL-STACK MONOREPO ARCHITECTURE
    # ==========================================
    s8 = prs.slides.add_slide(blank_slide_layout)
    add_slide_bg(s8)
    add_header(s8, "System Design", "Full-Stack Microservice Monorepo Architecture", "Decoupled services engineered for high concurrency, resilience, and offline continuity")

    layers = [
        ("Frontend Client", "React 19 + Vite 8 SPA", COLOR_CYAN, [
            "Dark-mode clinician dashboard with Lucide icons",
            "Axios API client with PNA/CORS handling",
            "HTML5 Canvas client-side Grad-CAM fallback engine",
            "LocalStorage state persistence for offline capability",
            "Hosted on Vercel Edge Global CDN"
        ]),
        ("Backend Coordination Gateway", "Express.js + Node.js (Port 5000)", COLOR_BLUE, [
            "RESTful routing for patients, reports, and doctor notes",
            "Private Network Access (PNA) preflight headers",
            "Dual-Persistence Engine: Mongoose MongoDB connection with seamless In-Memory Fallback arrays",
            "Multipart stream forwarding to ML service via Axios & FormData"
        ]),
        ("Inference Microservice", "FastAPI + PyTorch (Port 8000)", COLOR_GREEN, [
            "Asynchronous non-blocking prediction endpoints",
            "Torchvision transform pipelines (224x224 RGB, ImageNet norm)",
            "Dynamic PyTorch hook Grad-CAM heatmap generator",
            "OpenCV headless image processing & color spaces",
            "Interactive Swagger documentation at /docs"
        ])
    ]

    for i, (l_name, l_tech, l_color, l_points) in enumerate(layers):
        c_left = Inches(0.8) + i * Inches(4.04)
        add_card(s8, c_left, Inches(1.85), card_w, Inches(5.1), border_color=l_color)

        tb_l = s8.shapes.add_textbox(c_left + Inches(0.25), Inches(2.1), card_w - Inches(0.5), Inches(4.6))
        tf_l = tb_l.text_frame
        tf_l.word_wrap = True

        p1 = tf_l.paragraphs[0]
        p1.text = l_name
        p1.font.size = Pt(17)
        p1.font.bold = True
        p1.font.color.rgb = l_color

        p2 = tf_l.add_paragraph()
        p2.text = l_tech
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_WHITE
        p2.space_after = Pt(14)

        for pt in l_points:
            pi = tf_l.add_paragraph()
            pi.text = f"✔ {pt}"
            pi.font.size = Pt(11)
            pi.font.color.rgb = COLOR_MUTED
            pi.space_after = Pt(6)

    # ==========================================
    # SLIDE 9: CLINICIAN DASHBOARD & UX
    # ==========================================
    s9 = prs.slides.add_slide(blank_slide_layout)
    add_slide_bg(s9)
    add_header(s9, "Doctor-Facing Interface", "Clinician Dashboard & Diagnostic Workflow UX", "Ergonomic clinical interface designed for high-stress diagnostic environments")

    ux_cards = [
        ("Real-Time Triage Queue", "Automatically categorizes and displays pending patient scans sorted chronologically and color-coded by High (Red), Medium (Amber), and Low (Green) severity.", COLOR_CYAN),
        ("Side-by-Side Grad-CAM Inspection", "Allows the physician to inspect the raw input medical radiograph side-by-side with the semi-transparent Grad-CAM activation overlay to verify anatomical landmarks.", COLOR_BLUE),
        ("Pathology Probability Breakdown", "Interactive distribution bars showing exact prediction probabilities across all candidate conditions, allowing target class re-focusing on demand.", COLOR_GOLD),
        ("Clinical Decision Logging", "Direct interface for attending physicians to input qualitative clinical observations, override machine flags, and transition status to 'Reviewed'.", COLOR_GREEN)
    ]

    for i, (u_title, u_desc, u_color) in enumerate(ux_cards):
        col = i % 2
        row = i // 2
        c_left = Inches(0.8) + col * Inches(5.95)
        c_top = Inches(1.85) + row * Inches(2.55)
        add_card(s9, c_left, c_top, Inches(5.75), Inches(2.35), border_color=u_color)

        t_box = s9.shapes.add_textbox(c_left + Inches(0.3), c_top + Inches(0.25), Inches(5.15), Inches(1.85))
        c_tf = t_box.text_frame
        c_tf.word_wrap = True

        cp1 = c_tf.paragraphs[0]
        cp1.text = f"✦  {u_title}"
        cp1.font.size = Pt(16)
        cp1.font.bold = True
        cp1.font.color.rgb = u_color
        cp1.space_after = Pt(8)

        cp2 = c_tf.add_paragraph()
        cp2.text = u_desc
        cp2.font.size = Pt(13)
        cp2.font.color.rgb = COLOR_WHITE

    # ==========================================
    # SLIDE 10: DATASETS & PREPROCESSING PIPELINE
    # ==========================================
    s10 = prs.slides.add_slide(blank_slide_layout)
    add_slide_bg(s10)
    add_header(s10, "Data Engineering", "Datasets & Computer Vision Pipelines", "Curation, standardization, and domain-specific normalization protocols")

    data_cards = [
        ("NIH ChestX-ray14", "112,120 Frontal-View X-Rays", COLOR_CYAN, [
            "Source: National Institutes of Health Clinical Center",
            "30,805 unique patients with NLP-mined radiological labels",
            "Normalization: Mean [0.485, 0.456, 0.406], Std [0.229, 0.224, 0.225]",
            "Transforms: Resize(256), CenterCrop(224), ToTensor()"
        ]),
        ("HAM10000 / ISIC", "10,015 Dermatoscopic Scans", COLOR_BLUE, [
            "Source: International Skin Imaging Collaboration",
            "Biopsy-confirmed melanocytic and non-melanocytic lesions",
            "Preprocessing: Hair artifact suppression, color histogram calibration",
            "Transforms: Aspect-ratio preservation, RandomHorizontalFlip(p=0.5)"
        ]),
        ("Dental Pathology Dataset", "6 Oral Diagnostic Categories", COLOR_GOLD, [
            "Curation: Calculus, Caries, Gingivitis, Ulcers, Discoloration, Hypodontia",
            "Annotated with YOLO bounding box metadata and category labels",
            "Processing: Macro intra-oral perspective alignment & color contrast enhancement",
            "Transforms: Adaptive histogram equalization (CLAHE) for plaque detection"
        ])
    ]

    for i, (d_name, d_sub, d_color, d_bullets) in enumerate(data_cards):
        c_left = Inches(0.8) + i * Inches(4.04)
        add_card(s10, c_left, Inches(1.85), card_w, Inches(5.1), border_color=d_color)

        tb_d = s10.shapes.add_textbox(c_left + Inches(0.25), Inches(2.1), card_w - Inches(0.5), Inches(4.6))
        tf_d = tb_d.text_frame
        tf_d.word_wrap = True

        p1 = tf_d.paragraphs[0]
        p1.text = d_name
        p1.font.size = Pt(17)
        p1.font.bold = True
        p1.font.color.rgb = d_color

        p2 = tf_d.add_paragraph()
        p2.text = d_sub
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_WHITE
        p2.space_after = Pt(14)

        for b in d_bullets:
            pb = tf_d.add_paragraph()
            pb.text = f"• {b}"
            pb.font.size = Pt(11)
            pb.font.color.rgb = COLOR_MUTED
            pb.space_after = Pt(8)

    # ==========================================
    # SLIDE 11: PRODUCTION DEPLOYMENT & DEVOPS
    # ==========================================
    s11 = prs.slides.add_slide(blank_slide_layout)
    add_slide_bg(s11)
    add_header(s11, "Cloud Deployment & MLOps", "Production Architecture & Live Verification", "Containerized, version-controlled, and globally hosted on Vercel")

    ops_cards = [
        ("Vercel Edge Cloud Deployment", "Live Production Frontend", COLOR_CYAN, [
            "Live URL: https://medical-triage-kohl.vercel.app",
            "Configured via monorepo vercel.json with SPA rewrites",
            "Instant global edge distribution with HTTP/2 and SSL/TLS",
            "Zero-latency client fallback engine for standalone demonstrations"
        ]),
        ("GitHub Version Control", "Enterprise Repository Management", COLOR_BLUE, [
            "Repository: https://github.com/omveer7850/medical-triage",
            "Full commit trajectory on main branch with clean history",
            "Configured .gitignore and .vercelignore protecting heavy weights",
            "SSH authentication protocol & automated branch tracking"
        ]),
        ("Docker Containerization", "Multi-Service Orchestration", COLOR_GREEN, [
            "Multi-stage Dockerfiles for Frontend, Express, and ML Service",
            "docker-compose.yml defines isolated bridge network & volumes",
            "Health checks and auto-restart policies configured",
            "Guaranteed runtime parity across Windows, Linux, and Cloud instances"
        ])
    ]

    for i, (o_name, o_sub, o_color, o_bullets) in enumerate(ops_cards):
        c_left = Inches(0.8) + i * Inches(4.04)
        add_card(s11, c_left, Inches(1.85), card_w, Inches(5.1), border_color=o_color)

        tb_o = s11.shapes.add_textbox(c_left + Inches(0.25), Inches(2.1), card_w - Inches(0.5), Inches(4.6))
        tf_o = tb_o.text_frame
        tf_o.word_wrap = True

        p1 = tf_o.paragraphs[0]
        p1.text = o_name
        p1.font.size = Pt(17)
        p1.font.bold = True
        p1.font.color.rgb = o_color

        p2 = tf_o.add_paragraph()
        p2.text = o_sub
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_WHITE
        p2.space_after = Pt(14)

        for b in o_bullets:
            pb = tf_o.add_paragraph()
            pb.text = f"✔ {b}"
            pb.font.size = Pt(11)
            pb.font.color.rgb = COLOR_MUTED
            pb.space_after = Pt(8)

    # ==========================================
    # SLIDE 12: FUTURE ROADMAP & PACS/DICOM
    # ==========================================
    s12 = prs.slides.add_slide(blank_slide_layout)
    add_slide_bg(s12)
    add_header(s12, "Future Horizons", "Semester 2 Roadmap & Hospital System Integration", "Expanding from prototype triage into clinical hospital workflows")

    roadmap = [
        ("Phase 1: PACS & DICOM Integration", "Implement native .dcm file ingestion with Cornerstone.js / OHIF viewer, parsing patient metadata and high-bitrate DICOM windowing presets.", COLOR_CYAN),
        ("Phase 2: Multi-View & Longitudinal Correlation", "Expand thoracic pipeline to ingest Lateral + PA views simultaneously and correlate findings against historical prior exams to spot tumor progression.", COLOR_BLUE),
        ("Phase 3: Federated Learning & Privacy", "Deploy Flower/PySyft federated training across hospital nodes without centralizing raw protected health information (PHI), ensuring GDPR/HIPAA compliance.", COLOR_GOLD),
        ("Phase 4: Prospective Clinical Trial", "Conduct observational shadow studies measuring reduction in radiologist report turnaround time and emergency room triage queue latency.", COLOR_GREEN)
    ]

    for i, (r_title, r_desc, r_color) in enumerate(roadmap):
        col = i % 2
        row = i // 2
        c_left = Inches(0.8) + col * Inches(5.95)
        c_top = Inches(1.85) + row * Inches(2.55)
        add_card(s12, c_left, c_top, Inches(5.75), Inches(2.35), border_color=r_color)

        t_box = s12.shapes.add_textbox(c_left + Inches(0.3), c_top + Inches(0.25), Inches(5.15), Inches(1.85))
        c_tf = t_box.text_frame
        c_tf.word_wrap = True

        cp1 = c_tf.paragraphs[0]
        cp1.text = f"🚀  {r_title}"
        cp1.font.size = Pt(16)
        cp1.font.bold = True
        cp1.font.color.rgb = r_color
        cp1.space_after = Pt(8)

        cp2 = c_tf.add_paragraph()
        cp2.text = r_desc
        cp2.font.size = Pt(13)
        cp2.font.color.rgb = COLOR_WHITE

    # ==========================================
    # SLIDE 13: SUMMARY & LIVE LINKS
    # ==========================================
    s13 = prs.slides.add_slide(blank_slide_layout)
    add_slide_bg(s13)
    add_header(s13, "Conclusion & Resources", "Project Summary & Live Deployment Links", "Ready for clinical demonstration, code review, and academic presentation")

    # Left Summary Card
    add_card(s13, Inches(0.8), Inches(1.85), Inches(5.75), Inches(5.1), border_color=COLOR_CYAN)
    tb_sum = s13.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.15), Inches(4.6))
    tf_sum = tb_sum.text_frame
    tf_sum.word_wrap = True

    p = tf_sum.paragraphs[0]
    p.text = "Key Project Takeaways"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(14)

    takeaways = [
        "Comprehensive Tri-Modal Coverage: Chest Radiographs, Skin Lesions, and Dental Pathologies in a unified portal.",
        "Clinical Trust via Explainability: Grad-CAM gradient backprop overlays highlight the exact anatomical pathology.",
        "Sensitivity-First Triage: Safeguards patient safety by prioritizing high-risk cases to prevent diagnostic misses.",
        "Production Resilience: Resilient fallback mechanisms ensure 100% uptime even in offline demonstration environments."
    ]
    for t in takeaways:
        pt = tf_sum.add_paragraph()
        pt.text = f"✔ {t}"
        pt.font.size = Pt(12)
        pt.font.color.rgb = COLOR_WHITE
        pt.space_after = Pt(10)

    # Right Links Card
    add_card(s13, Inches(6.75), Inches(1.85), Inches(5.75), Inches(5.1), border_color=COLOR_GREEN)
    tb_lnk = s13.shapes.add_textbox(Inches(7.05), Inches(2.1), Inches(5.15), Inches(4.6))
    tf_lnk = tb_lnk.text_frame
    tf_lnk.word_wrap = True

    p = tf_lnk.paragraphs[0]
    p.text = "Live Project Links & Repository"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN
    p.space_after = Pt(14)

    links = [
        ("Vercel Live Application", "https://medical-triage-kohl.vercel.app", COLOR_CYAN),
        ("Alternate Live Mirror", "https://frontend-one-lovat-88.vercel.app", COLOR_CYAN),
        ("GitHub Repository", "https://github.com/omveer7850/medical-triage", COLOR_BLUE),
        ("Local API Documentation", "http://localhost:8000/docs", COLOR_GOLD)
    ]
    for l_label, l_url, l_col in links:
        pt = tf_lnk.add_paragraph()
        pt.text = f"🔗 {l_label}"
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = l_col
        pt.space_after = Pt(2)

        pu = tf_lnk.add_paragraph()
        pu.text = l_url
        pu.font.size = Pt(11)
        pu.font.color.rgb = COLOR_MUTED
        pu.space_after = Pt(10)

    # Save
    output_filename = "AI_Medical_Diagnosis_Triage_Presentation.pptx"
    prs.save(output_filename)
    print(f"Presentation successfully generated and saved to: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    create_presentation()
