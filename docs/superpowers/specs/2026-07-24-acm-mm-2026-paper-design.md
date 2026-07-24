# ACM MM 2026 Paper Addition

## Scope

Add the newly accepted paper to the website publication data, the homepage
selected-publications section, the news feed, and the downloadable CV source.
Do not publish or copy the submission PDF, and do not add any paper, project,
DOI, or external links.

## Publication Entry

Add a new `@inproceedings` entry to `_bibliography/papers.bib` with:

- venue abbreviation `ACM MM`;
- year `2026`;
- the title `ChoreoPlan: Hybrid Phrase Planning and Execution-Grounded
  Selection for Music-to-Humanoid Dance`;
- the complete author list supplied by the user;
- `selected={true}` so the entry appears both on Publications and in the
  homepage selected-publications section;
- a 2026 sort key that places it ahead of the existing CVPR 2026 entry.

The entry must omit preview imagery, PDF, arXiv, DOI, official, project, and
other link fields.

## News Entry

Add a dated news item for 2026-07-24 announcing that the paper was accepted to
ACM MM 2026. Keep it consistent with the existing conference-acceptance news
items and do not add a link.

## CV Entry

Add the paper at the top of the publications section in
`cv_latex/wei_jin_huang_cv.tex`, with Wei-Jin Huang highlighted using the
existing `\me{}` convention and the venue rendered as `ACM MM 2026`. Do not
add a link or download action for the paper.

## Verification

Run the repository's narrow content checks, build the Jekyll site, rebuild the
downloadable CV PDF, and inspect the generated publication, homepage, news,
and CV outputs to confirm the title, authors, venue, ordering, and absence of
paper links.
