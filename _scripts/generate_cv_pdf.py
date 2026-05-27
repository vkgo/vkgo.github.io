#!/usr/bin/env python3
"""Generate the downloadable CV PDF from site bibliography data."""

from __future__ import annotations

import argparse
import html
from pathlib import Path

import bibtexparser
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]

PUBLICATION_SUMMARIES = {
    "huang2026learning": (
        "Enabling humanoid robots to physically interact with humans is a critical frontier, "
        "but progress is hindered by the scarcity of high-quality human-humanoid interaction data. "
        "While leveraging abundant human-human interaction data presents a scalable alternative, "
        "we show that standard retargeting breaks essential contacts. We address this with PAIR "
        "and D-STAR for synchronized whole-body interaction behaviors."
    ),
    "huang2025modeling": (
        "Error detection in procedural activities is essential for consistent and correct outcomes "
        "in AR-assisted and robotic systems. Existing methods often focus on temporal ordering "
        "errors or rely on static prototypes to represent normal actions. We propose an Adaptive "
        "Multiple Normal Action Representation framework that predicts all valid next actions and "
        "reconstructs their corresponding normal action representations for comparison with the "
        "ongoing action."
    ),
    "xia2025less": (
        "This work focuses on privacy-preserving action recognition, which aims to protect "
        "individual privacy in action videos without compromising recognition performance. "
        "Existing methods still struggle with video domain shifts. We propose GenPriv, a "
        "transferable framework that decouples static and dynamic video features and removes "
        "privacy-sensitive content from static action features."
    ),
    "li2024egoexo": (
        "We present EgoExo-Fitness, a new full-body action understanding dataset featuring "
        "fitness videos recorded from synchronized egocentric and fixed exocentric cameras. "
        "Compared with existing datasets, EgoExo-Fitness not only contains first-person videos, "
        "but also provides rich annotations, including two-level temporal boundaries, natural "
        "language comments, and action quality scores."
    ),
}


def clean_text(value: str) -> str:
    return " ".join(value.replace("\n", " ").split())


def format_author(name: str) -> str:
    name = clean_text(name)
    if "," not in name:
        return name
    last, first = [part.strip() for part in name.split(",", 1)]
    return f"{first} {last}".strip()


def format_authors(entry: dict[str, str]) -> str:
    authors = [format_author(author) for author in entry["author"].split(" and ")]
    cofirst = {
        format_author(name)
        for name in entry.get("cofirst", "").split(" and ")
        if name.strip()
    }
    formatted = []
    for author in authors:
        if author in cofirst:
            author = f"{author} (Co-First)"
        formatted.append(author)
    return ", ".join(formatted)


def load_selected_publications(bib_path: Path) -> list[dict[str, str]]:
    with bib_path.open(encoding="utf-8") as bib_file:
        database = bibtexparser.load(bib_file)

    selected = [
        entry
        for entry in database.entries
        if clean_text(entry.get("selected", "")).lower() == "true"
    ]
    selected.sort(key=lambda entry: entry.get("sortkey", entry.get("year", "")), reverse=True)
    return selected


def visible_link_text(entry: dict[str, str]) -> str:
    parts = []
    if arxiv := entry.get("arxiv"):
        arxiv = clean_text(arxiv)
        parts.append(f'<link href="https://arxiv.org/abs/{arxiv}">arXiv {arxiv}</link>')
    if official := entry.get("official"):
        parts.append(f'<link href="{html.escape(clean_text(official), quote=True)}">Official</link>')
    return " | ".join(parts)


def shorten_venue(entry: dict[str, str]) -> str:
    abbr = clean_text(entry.get("abbr", ""))
    year = clean_text(entry.get("year", ""))
    booktitle = clean_text(entry.get("booktitle", ""))
    pages = clean_text(entry.get("pages", ""))
    venue = f"{abbr} {year}" if abbr or year else booktitle
    if booktitle:
        venue = f"{venue} - {booktitle}"
    if pages:
        venue = f"{venue}, pp. {pages}"
    return venue


def add_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setTitle("Wei-Jin Huang CV")
    canvas.setAuthor("Wei-Jin Huang")
    canvas.setFont("Helvetica", 6.2)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawRightString(A4[0] - 12 * mm, 8 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf(output_path: Path, bib_path: Path) -> None:
    publications = load_selected_publications(bib_path)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=11 * mm,
        leftMargin=11 * mm,
        topMargin=9 * mm,
        bottomMargin=10 * mm,
        title="Wei-Jin Huang CV",
        author="Wei-Jin Huang",
    )

    base = getSampleStyleSheet()
    styles = {
        "name": ParagraphStyle(
            "Name",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=19,
            alignment=TA_CENTER,
            spaceAfter=1,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.2,
            leading=8.4,
            alignment=TA_CENTER,
            spaceAfter=0,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=10.5,
            textColor=colors.HexColor("#1f4e79"),
            spaceBefore=3,
            spaceAfter=1.2,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=6.8,
            leading=8.0,
            spaceAfter=1.5,
        ),
        "compact": ParagraphStyle(
            "Compact",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=6.45,
            leading=7.35,
            spaceAfter=1.0,
        ),
        "pub_title": ParagraphStyle(
            "PublicationTitle",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=7.25,
            leading=8.4,
            spaceBefore=1.6,
            spaceAfter=0.7,
        ),
        "link": ParagraphStyle(
            "Link",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=6.45,
            leading=7.35,
            textColor=colors.HexColor("#005ea8"),
            spaceAfter=1.0,
        ),
    }

    story = [
        Paragraph("Wei-Jin Huang", styles["name"]),
        Paragraph("Ph.D. Student, Computer Science and Technology", styles["subtitle"]),
        Paragraph("Sun Yat-sen University, Guangzhou, China", styles["subtitle"]),
        Paragraph(
            'Email: <link href="mailto:huangwj235@mail2.sysu.edu.cn">huangwj235@mail2.sysu.edu.cn</link> | '
            '<link href="https://vkgo.github.io/">vkgo.github.io</link> | '
            '<link href="https://scholar.google.com/">Google Scholar</link> | '
            '<link href="https://github.com/vkgo">GitHub</link> | Kaggle: carmencita',
            styles["subtitle"],
        ),
        Spacer(1, 3),
        Paragraph("Research Summary", styles["section"]),
        Paragraph(
            "I am currently a Ph.D. student at Sun Yat-sen University, specializing in Humanoid "
            "Learning and Video Action Understanding. I have a strong interest in deep learning "
            "and computer vision, with my current research focus on temporal action understanding "
            "and human-humanoid interaction.",
            styles["body"],
        ),
        Paragraph("Education", styles["section"]),
        Paragraph(
            "<b>Ph.D., Computer Science and Technology</b> - Sun Yat-sen University (SYSU), Guangzhou, China "
            "<b>2024.09 - Present</b><br/>Specialization: Humanoid Learning, Video Action Understanding",
            styles["compact"],
        ),
        Paragraph(
            "<b>B.E., Network Engineering</b> - South China University of Technology (SCUT), Guangzhou, China "
            "<b>2020.09 - 2024.07</b><br/>Average grade ranking 3/66",
            styles["compact"],
        ),
        Paragraph("Selected Publications", styles["section"]),
    ]

    for entry in publications:
        entry_id = entry["ID"]
        story.extend(
            [
                Paragraph(html.escape(clean_text(entry["title"])), styles["pub_title"]),
                Paragraph(html.escape(format_authors(entry)), styles["compact"]),
                Paragraph(html.escape(shorten_venue(entry)), styles["compact"]),
            ]
        )
        if links := visible_link_text(entry):
            story.append(Paragraph(f"<b>Links:</b> {links}", styles["link"]))
        if summary := PUBLICATION_SUMMARIES.get(entry_id):
            story.append(Paragraph(f"<b>Summary:</b> {html.escape(summary)}", styles["compact"]))

    story.extend(
        [
            Paragraph("Research Interests", styles["section"]),
            Paragraph(
                "<b>Humanoid Learning:</b> embodied intelligence, whole-body control, imitation learning, "
                "human-humanoid interaction; <b>Video Understanding:</b> action recognition, temporal action "
                "understanding, video representation learning",
                styles["compact"],
            ),
            Paragraph("Experience", styles["section"]),
            Paragraph("<b>Algorithm Engineer Intern</b> - China Telecom <b>2023.03 - 2023.05</b>", styles["compact"]),
            Paragraph("Honors and Awards", styles["section"]),
            Paragraph(
                "<b>2024:</b> President Scholarship, Sun Yat-sen University (top 5%)<br/>"
                "<b>2022:</b> Kaggle - H&amp;M Personalized Fashion Recommendations, Silver (85/2952); "
                "National Scholarship (1/66); Tencent Scholarship - First Class (1/66)<br/>"
                "<b>2021:</b> Kaggle - G2Net Gravitational Wave Detection, Silver (57/1219)",
                styles["compact"],
            ),
        ]
    )

    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "assets/pdf/wei_jin_huang_cv.pdf",
        help="Output PDF path.",
    )
    parser.add_argument(
        "--bib",
        type=Path,
        default=ROOT / "_bibliography/papers.bib",
        help="Bibliography path.",
    )
    args = parser.parse_args()

    build_pdf(args.output, args.bib)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
