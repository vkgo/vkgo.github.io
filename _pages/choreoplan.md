---
layout: page
permalink: /ChoreoPlan/
title: "ChoreoPlan: Hybrid Phrase Planning and Execution-Grounded Selection for Music-to-Humanoid Dance"
nav: false
_styles: >
  .post-header {
    display: none;
  }
  .paper-title {
    text-align: center;
    font-weight: 700;
    line-height: 1.3;
    margin-top: 0.5rem;
    margin-bottom: 1.4rem;
  }
  .venue {
    text-align: center;
    font-weight: 600;
    margin-bottom: 1.2rem;
  }
  .authors {
    text-align: center;
    line-height: 1.9;
    margin-bottom: 0.6rem;
  }
  .authors a {
    white-space: nowrap;
  }
  .affiliations {
    text-align: center;
    font-size: 0.95rem;
    line-height: 1.7;
    color: var(--global-text-color-light);
  }
  .authornotes {
    text-align: center;
    font-size: 0.85rem;
    color: var(--global-text-color-light);
    margin-top: 0.5rem;
    margin-bottom: 2rem;
  }
---

<h1 class="paper-title">
  ChoreoPlan: Hybrid Phrase Planning and Execution-Grounded<br class="d-none d-md-inline" />
  Selection for Music-to-Humanoid Dance
</h1>

<div class="venue">
  ACM International Conference on Multimedia (ACM MM), 2026
</div>

<div class="authors">
  Wei-Jin Huang<sup>1,*</sup>,
  Jianhong Fan<sup>1,*</sup>,
  Hao Huang<sup>2</sup>,
  Zhi-Wei Xia<sup>1</sup>,
  Jun-Yi Deng<sup>1</sup>,
  Yuan-Ming Li<sup>1</sup>,
  Kun-Yu Lin<sup>3</sup>,
  Wei-Shi Zheng<sup>1,&dagger;</sup>
</div>

<div class="affiliations">
  <sup>1</sup>Sun Yat-sen University &nbsp;&middot;&nbsp;
  <sup>2</sup>South China University of Technology &nbsp;&middot;&nbsp;
  <sup>3</sup>The University of Hong Kong
</div>

<div class="authornotes">
  <sup>*</sup>Equal contribution &nbsp;&nbsp; <sup>&dagger;</sup>Corresponding author
</div>

## Abstract

Music-to-humanoid dance is commonly implemented as a two-stage pipeline in
which a music-conditioned generator produces a reference motion and a fixed
whole-body controller (WBC) executes it. In this setting, reference-space
quality is only a proxy for the quality of the executed motion. We focus on two
upstream decisions that strongly affect this proxy gap: how temporal planning
units are defined and how generated candidates are selected before execution.
ChoreoPlan introduces beat-snapped, variable-length planning segments with
hybrid discrete and continuous motion attributes, together with an
_Embodied Selector_ trained on offline rollouts of the fixed controller. The
planner provides beat-aligned choreography guidance in humanoid token space,
while the selector reranks candidates using predicted execution quality and
semantic compatibility. Across AIST++- and FineDance-derived humanoid tracks in
IsaacGym and MuJoCo, ChoreoPlan improves rollout success, tracking accuracy,
executed beat alignment, and semantic retention over retrained baselines.
Qualitative Unitree G1 demonstrations further illustrate coherent and
executable dance motions.
