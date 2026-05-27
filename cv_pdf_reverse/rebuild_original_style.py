#!/usr/bin/env python3
"""First-pass reverse-engineered rebuild of the original ReportLab CV PDF.

This is an experimental reproduction script, not the canonical CV source yet.
It intentionally mirrors the restored PDF's fixed coordinates and typography.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DEFAULT_SOURCE_PDF = REPO_ROOT / "assets/pdf/wei_jin_huang_cv.pdf"
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "output"

W, H = A4

BODY_X = 42.85
HEADER_X = 46.77
BODY_W = 510.0

INK = colors.HexColor("#111827")
MUTED = colors.HexColor("#475569")
BLUE = colors.HexColor("#2563eb")
ORANGE = colors.HexColor("#d84315")


STYLES = {
    "body": ParagraphStyle(
        "body",
        fontName="Helvetica",
        fontSize=8.4,
        leading=10.4,
        textColor=INK,
        spaceAfter=0,
    ),
    "small": ParagraphStyle(
        "small",
        fontName="Helvetica",
        fontSize=7.3,
        leading=9.1,
        textColor=MUTED,
        spaceAfter=0,
    ),
    "section": ParagraphStyle(
        "section",
        fontName="Helvetica-Bold",
        fontSize=11.1,
        leading=13.2,
        textColor=BLUE,
        spaceAfter=0,
    ),
    "title": ParagraphStyle(
        "title",
        fontName="Helvetica-Bold",
        fontSize=9.0,
        leading=10.5,
        textColor=INK,
        spaceAfter=0,
    ),
}


def ensure_headshot(source_pdf: Path, output_dir: Path) -> Path:
    """Extract the embedded headshot from the restored original PDF."""
    photo = output_dir / "extracted-000.jpg"
    if photo.exists():
        return photo

    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = output_dir / "extracted"
    try:
        subprocess.run(
            ["pdfimages", "-all", str(source_pdf), str(prefix)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("pdfimages is required to extract the embedded headshot.") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"pdfimages failed: {exc.stderr.strip()}") from exc

    if not photo.exists():
        raise RuntimeError(f"Expected extracted headshot at {photo}, but it was not created.")
    return photo


def p(c: canvas.Canvas, text: str, x: float, y_top: float, width: float, style: ParagraphStyle) -> float:
    para = Paragraph(text, style)
    _, h = para.wrap(width, 500)
    adjusted_top = y_top - (style.fontSize * 0.282)
    para.drawOn(c, x, H - adjusted_top - h)
    return y_top + h


def draw_header(c: canvas.Canvas, photo: Path) -> None:
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(HEADER_X, H - 51.5, "Wei-Jin Huang")

    c.setFont("Helvetica-Bold", 9.3)
    c.setFillColor(ORANGE)
    c.drawString(HEADER_X, H - 63.8, "Ph.D. Student")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 9.3)
    c.drawString(106.0, H - 63.8, ", Computer Science and Technology")

    c.setFont("Helvetica", 9.3)
    c.setFillColor(MUTED)
    c.drawString(HEADER_X, H - 75.9, "Sun Yat-sen University, Guangzhou, China")

    c.setFont("Helvetica", 7.5)
    c.setFillColor(MUTED)
    c.drawString(HEADER_X, H - 86.2, "Email: ")
    c.setFillColor(BLUE)
    c.drawString(72.8, H - 86.2, "huangwj235@mail2.sysu.edu.cn")
    c.setFillColor(MUTED)
    c.drawString(179.85, H - 86.2, " | Website: ")
    c.setFillColor(BLUE)
    c.drawString(222.5, H - 86.2, "vkgo.github.io")

    c.setFillColor(MUTED)
    c.drawString(HEADER_X, H - 95.4, "Scholar: ")
    c.setFillColor(BLUE)
    c.drawString(76.0, H - 95.4, "Google Scholar")
    c.setFillColor(MUTED)
    c.drawString(130.0, H - 95.4, " | GitHub: ")
    c.setFillColor(BLUE)
    c.drawString(162.0, H - 95.4, "github.com/vkgo")
    c.setFillColor(MUTED)
    c.drawString(218.0, H - 95.4, " | Kaggle: ")
    c.setFillColor(BLUE)
    c.drawString(250.0, H - 95.4, "carmencita")

    c.drawImage(str(photo), 456, H - 126, width=80, height=106.7, preserveAspectRatio=True, mask="auto")


def section(c: canvas.Canvas, title: str, y: float) -> float:
    p(c, title, BODY_X, y, BODY_W, STYLES["section"])
    return y + 21.0


def build_pdf(target: Path, photo: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(target), pagesize=A4)
    c.setTitle("Wei-Jin Huang CV")
    c.setAuthor("Wei-Jin Huang")
    draw_header(c, photo)

    section(c, "Research Summary", 138.77)
    p(
        c,
        "I am currently a Ph.D. student at Sun Yat-sen University, specializing in Humanoid Learning and Video Action Understanding. "
        "I have a strong interest in deep learning and computer vision, with my current research focus on temporal action understanding. "
        "I have a deep passion for all computer science things, and I aim to make significant contributions to the field through extensive "
        "and meaningful research.",
        BODY_X,
        154.5,
        BODY_W,
        STYLES["body"],
    )

    section(c, "Education", 202.92)
    p(c, "<b>Ph.D., Computer Science and Technology - Sun Yat-sen University (SYSU), Guangzhou, China</b>", BODY_X, 218.83, BODY_W, STYLES["body"])
    p(c, '<font color="#d84315"><b>2024.09 - Present</b></font>', BODY_X, 229.41, BODY_W, STYLES["small"])
    p(c, "- Specialization: Humanoid Learning, Video Action Understanding", BODY_X, 238.86, BODY_W, STYLES["body"])
    p(c, "<b>B.E., Network Engineering - South China University of Technology (SCUT), Guangzhou, China</b>", BODY_X, 251.13, BODY_W, STYLES["body"])
    p(c, '<font color="#d84315"><b>2020.09 - 2024.07</b></font>', BODY_X, 261.71, BODY_W, STYLES["small"])
    p(c, "- Average grade ranking 3/66", BODY_X, 271.16, BODY_W, STYLES["body"])

    section(c, "Selected Publications", 287.52)
    pubs = [
        (
            "Beyond Mimicry: Learning Whole-Body Human-Humanoid Interaction from Human-Human Demonstrations",
            '<font color="#2563eb"><b>Wei-Jin Huang</b></font>, Yue-Yi Zhang, Yi-Lin Wei, Zhi-Wei Xia, Juantao Tan, Yuan-Ming Li, Zhilin Zhao, Wei-Shi Zheng',
            '<font color="#d84315"><b>CVPR 2026</b></font> - Proceedings of the Computer Vision and Pattern Recognition Conference',
            "Enabling humanoid robots to physically interact with humans is a critical frontier, but progress is hindered by the scarcity of high-quality human-humanoid interaction data. "
            "While leveraging abundant human-human interaction data presents a scalable alternative, we show that standard retargeting breaks essential contacts. We address this with PAIR and D-STAR for synchronized whole-body interaction behaviors.",
            (303.43, 313.95, 323.02, 332.66),
        ),
        (
            "Modeling Multiple Normal Action Representations for Error Detection in Procedural Tasks",
            '<font color="#2563eb"><b>Wei-Jin Huang</b></font>, Yuan-Ming Li, Zhi-Wei Xia, Yu-Ming Tang, Kun-Yu Lin, Jian-Fang Hu, Wei-Shi Zheng',
            '<font color="#d84315"><b>CVPR 2025</b></font> - Proceedings of the Computer Vision and Pattern Recognition Conference',
            "Error detection in procedural activities is essential for consistent and correct outcomes in AR-assisted and robotic systems. Existing methods often focus on temporal ordering errors or rely on static prototypes to represent normal actions. "
            "We propose an Adaptive Multiple Normal Action Representation framework that predicts all valid next actions and reconstructs their corresponding normal action representations for comparison with the ongoing action.",
            (376.27, 386.80, 395.86, 405.51),
        ),
        (
            "Less Static, More Private: Towards Transferable Privacy-Preserving Action Recognition by Generative Decoupled Learning",
            'Zhi-Wei Xia, Kun-Yu Lin, Yuan-Ming Li, <font color="#2563eb"><b>Wei-Jin Huang</b></font>, Xian-Tuo Tan, Wei-Shi Zheng',
            '<font color="#d84315"><b>ICCV 2025</b></font> - Proceedings of the IEEE/CVF International Conference on Computer Vision',
            "This work focuses on privacy-preserving action recognition, which aims to protect individual privacy in action videos without compromising recognition performance. Existing methods still struggle with video domain shifts. "
            "We propose GenPriv, a transferable framework that decouples static and dynamic video features and removes privacy-sensitive content from static action features.",
            (449.12, 470.64, 479.71, 489.35),
        ),
        (
            "Egoexo-fitness: Towards egocentric and exocentric full-body action understanding",
            'Yuan-Ming Li, <font color="#2563eb"><b>Wei-Jin Huang (Co-First)</b></font>, An-Lan Wang, Ling-An Zeng, Jing-Ke Meng, Wei-Shi Zheng',
            '<font color="#d84315"><b>ECCV 2024</b></font> - European Conference on Computer Vision',
            "We present EgoExo-Fitness, a new full-body action understanding dataset featuring fitness videos recorded from synchronized egocentric and fixed exocentric cameras. Compared with existing datasets, EgoExo-Fitness not only contains first-person videos, but also provides rich annotations, including two-level temporal boundaries, natural language comments, and action quality scores.",
            (522.56, 533.08, 542.15, 551.79),
        ),
    ]
    for title, authors, venue, abstract, ys in pubs:
        title_y, author_y, venue_y, abstract_y = ys
        p(c, f"<b>{title}</b>", BODY_X, title_y, BODY_W, STYLES["title"])
        p(c, authors, BODY_X, author_y, BODY_W, STYLES["small"])
        p(c, venue, BODY_X, venue_y, BODY_W, STYLES["body"])
        p(c, f'<font color="#2563eb">Abstract:</font> {abstract}', BODY_X, abstract_y, BODY_W, STYLES["body"])

    section(c, "Research Interests", 589.09)
    p(c, "Humanoid Learning: embodied intelligence, whole-body control, imitation learning, human-humanoid interaction; Video Understanding: action recognition, temporal action understanding, video representation learning", BODY_X, 604.83, BODY_W, STYLES["body"])
    section(c, "Experience", 631.60)
    p(c, "<b>Algorithm Engineer Intern - China Telecom</b>", BODY_X, 647.50, BODY_W, STYLES["body"])
    p(c, '<font color="#d84315"><b>2023.03 - 2023.05</b></font>', BODY_X, 658.08, BODY_W, STYLES["small"])
    section(c, "Honors and Awards", 673.50)
    p(c, '<font color="#d84315"><b>2024</b></font>', BODY_X, 689.40, BODY_W, STYLES["body"])
    p(c, "- President Scholarship, Sun Yat-sen University (top 5%)", BODY_X, 700.24, BODY_W, STYLES["body"])
    p(c, '<font color="#d84315"><b>2022</b></font>', BODY_X, 712.50, BODY_W, STYLES["body"])
    p(c, "- Kaggle - H&amp;M; Personalized Fashion Recommendations, Silver (85/2952)<br/>- National Scholarship (1/66)<br/>- Tencent Scholarship - First Class (1/66)", BODY_X, 723.34, BODY_W, STYLES["body"])
    p(c, '<font color="#d84315"><b>2021</b></font>', BODY_X, 756.41, BODY_W, STYLES["body"])
    p(c, "- Kaggle - G2Net Gravitational Wave Detection, Silver (57/1219)", BODY_X, 767.24, BODY_W, STYLES["body"])

    c.setFont("Helvetica", 8.5)
    c.setFillColor(MUTED)
    c.drawRightString(557.0, H - 818.0, "Page 1")
    c.showPage()
    c.save()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-pdf", type=Path, default=DEFAULT_SOURCE_PDF)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--target", type=Path, default=None)
    args = parser.parse_args()

    output_dir = args.output_dir
    target = args.target or output_dir / "candidate.pdf"
    photo = ensure_headshot(args.source_pdf, output_dir)
    build_pdf(target, photo)
    print(target)


if __name__ == "__main__":
    main()
