---
layout: page
permalink: /call-for-papers/
title: Call for Papers
description:
nav: true
nav_order: 1
---

We welcome researchers working on foundation models for structured data to submit their latest original research work to the [ICML 2026](https://icml.cc/) workshop on **Foundation Models for Structured Data**.

## Key Information

- Submission link: **[OpenReview](https://openreview.net/group?id=ICML.cc/2026/Workshop/FMSD)**
- Submission deadline: ~~May 01, 2026~~ May 08, 2026 (11:59 pm AoE)
- Acceptance notification: ~~May 22, 2026~~ May 24, 2026 (anytime before 11:59 pm AoE)
- Camera ready deadline: June 29, 2026 (11:59 pm AoE)
- Page Limit: short papers with up to 4 pages; unlimited references and appendices
- Misc: double-blind, non-archival, poster presentations for accepted papers, orals for top rated papers

## Submission Instructions

Submissions should take the form of a short paper of up to **4 pages**. Additional pages containing references and appendices are allowed but the reviewers are _not obliged_ to refer to the appendices when reviewing the paper. Submissions should be made on **[OpenReview](https://openreview.net/group?id=ICML.cc/2026/Workshop/FMSD)** in a single `.pdf` file using the [ICML 2026 LaTeX style template](https://media.icml.cc/Conferences/ICML2026/Styles/icml2026.zip). The impact statement is not required for the submission to the workshop.

The review process is _double-blind_, so please ensure that your submission is properly anonymized. Papers that exceed the page limit or have not been properly anonymized will be desk-rejected without review. Please note that there is no rebuttal phase and the final decisions will be made based solely on the submission and the reviews. Rejected and withdrawn submissions will not be made public.

All accepted submissions will be accompanied by a poster presentation. A number of selected submissions will be invited for lightning and oral talks.

**Dual submission policy**: This workshop is **non-archival**; even though all accepted papers will be available on OpenReview and this website, there are no formally-published proceedings. Submission of papers accepted at ICML 2026's main conference are not allowed. If a paper is currently under review at another venue, it can still be submitted to this workshop. If a paper has previously appeared in a journal, workshop, or conference, it should be reasonably extended in order to be accepted at this workshop.

## Scope and Topics

We focus on foundation-model approaches for inherently structured objectives on tabular and time-series data, such as classification, regression, forecasting, and structured generation. LLM/agent-based submissions are in scope only if they evaluate on predictive tabular/time-series objectives with strong classical baselines, and report cost/latency and numerical reliability checks. Out of scope are contributions about general-purpose foundation model architectures without a clear structured-data focus, and NLP-centric tasks over tables (e.g., table question answering / semantic parsing).

To help guide submissions, here are a few clearly relevant prior works that align with the goals of this workshop:

- Time series: Chronos, TimesFM, Moirai, Moment, TiRex, TabPFN-TS, GIFT-Eval
- Tabular: TabPFN, TabICL, TabDPT, Mitra, CARTE, TabSTAR, ConTextTab, TabArena

We invite submissions related to the following topics:

- **Building Foundation Models for (Multimodal) Structured Data**: Following the trends in language and vision domains, recent developments in foundation models in tabular and time series capable of zero-shot inference and/or in-context learning on unseen data have challenged the conventional in-domain training and prediction paradigm. Furthermore, models pretrained in one modality (such as tabular) can also demonstrate promising predictive performance in related domains by transforming the input data into a compatible format. We aim to assess progress in this area and the challenges of developing such models, including novel architectures and insights into scaling. A particular focus in 2026 is on multimodal structured foundation models, which integrate tabular and time-series data with complementary modalities such as text and images, enabling richer supervision, improved generalization, and new capabilities beyond unimodal structured learning.
- **Datasets and Synthetic Data Generation Methods**: The amount of high-quality structured data available in the public domain is limited for developing pretrained models, especially when compared with the amount of data available for other domains, such as language and vision. Structured foundation models that rely on real-world data for pre-training are often constrained by the number of available public datasets, or are limited to pre-training on relatively small-scale datasets from Wikipedia and GitHub. To address this limitation, recent work on foundation models for structured data has focused on developing high-fidelity synthetic data generation schemes and has included this data in their training corpus. This workshop welcomes contributions of high-quality large-scale (multimodal) datasets and synthetic data generation methods for training structured foundation models.
- **Benchmarks**: While efforts have been made to develop unified benchmarks for tabular and time series tasks, new efforts are required to evaluate structured foundation models comprehensively along different dimensions, such as different data characteristics, inference throughput, memory usage, scalability, and data memorization. Because structured-data corpora are small and reused, contamination and memorization can dominate reported gains; we explicitly encourage protocols and benchmarks that measure and mitigate contamination.
- **Alternative Paradigms (LLMs and Agents)**: Beyond purpose-built foundation models for structured data, large language models (LLMs) and agentic systems have shown emerging promise on inherently structured tasks. We invite LLM/agent-based work when evaluation centers on predictive tabular/time-series objectives and includes careful baselines, cost/latency reporting, and numerical reliability checks. Structured settings introduce alternative scaling dimensions beyond data and parameters such as schema diversity, cross-domain transfer, and inference-time compute through planning and tool use (with agents effectively scaling compute at inference). This raises a central open question: Are purpose-built structured foundation models fundamentally more sample- or compute-efficient than general-purpose LLM-based approaches for structured objectives? We welcome work that examines these scaling trade-offs, alongside challenges in interpretability, efficiency, and numerical reliability.
- **Applications of Foundation Models for Structured Data**: Foundation models for structured data can transform industries from climate modeling and fraud detection to supply chain optimization and health monitoring. Real-world deployment requires addressing challenges such as domain adaptation, model reliability, and data privacy. This workshop seeks contributions (1) showcasing novel applications in real-world structured data domains, (2) overcoming challenges such as scaling and inference throughput, and (3) demonstrating domain-specific innovation such as domain-specialized foundation models. We also welcome discussions on ethical considerations, fairness, and bias mitigation to ensure these technologies benefit a broad range of users and applications.

We also explicitly encourage submissions that study scaling across datasets, model size, and compute; and multimodality for structured foundation models (e.g., image-tabular modeling in medical diagnosis; text-time-series modeling for ECG interpretation).

## Camera Ready FAQ

**Q: What is the camera ready page limit?**
**A:** 4 pages with unlimited references and appendices.

---

**Q: What is the required poster format?**
**A:**
Must not exceed 36in (H) x 24in (W) or 91cm (H) x 61cm (W)   
Notice: Workshop posters must be in **portrait format**

Refer to the ICML Conference guidelines: [ICML 2026 Poster Instructions](https://icml.cc/Conferences/2026/PosterInstructions)

---

**Q: How do I update the style file?**
**A:**
Modify the `icml2026.sty` file. For example, replace:
```latex
% \newcommand{\ICML@appearing}{\textit{Proceedings of the
% $\mathit{43}^{rd}$ International Conference on Machine Learning},
% Seoul, South Korea. PMLR 306, 2026.
% Copyright 2026 by the author(s).}
```
with:
```latex
\newcommand{\ICML@appearing}{\textit{Proceedings of the
$\mathit{2}^{nd}$ ICML Workshop on Foundation Models for Structured Data},
Seoul, South Korea. 2026.
Copyright 2026 by the author(s).}
```

---

**Q: How do I submit the camera-ready version? Do I uncomment the camera-ready line in the LaTeX file, download it, and re-upload?**
**A:** Yes. Follow the template instructions to generate the final version and then re-upload it to the system. Ensure you also follow the above style file edit.

---

**Q: I can't find an upload option or clear instructions on the workshop website. What should I do?**
**A:** Please follow the general ICML instructions and the LaTeX template comments to prepare your camera-ready version.

---

**Q: Will there be an option for online attendance?**
**A:** Talks will be livestreamed by ICML. Poster sessions and other in-person events will not be shared online.

---

**Q: None of the authors can attend in-person, can the organizers print our paper's poster and bring it to the workshop for us?**
**A:** The organizers will not be able to assist in poster printing. We recommend seeing if anyone you know (even outside the author list) is attending in-person and would be able to print/bring the poster to the workshop. If you are unable to find someone to deliver the poster, please email the organizers with your situation.

---

**Q: Can the organizers assist with travel issues / fee waivers?**
**A:** Unfortunately we are unable to assist with travel issues or waive registration fees.

---

**Q: What is the camera ready deadline?**
**A:**
The camera ready deadline is June 29, 2026  (11:59 pm AoE).
The camera ready deadline is not strict, as the workshop is non-archival. This means there is no enforcement of the deadline, nor any action required by you for the camera-ready, it is merely a best-effort suggestion.
Workshop papers live in OpenReview, and organizers can re-import any changes up until the conference. The ICML site just links back to OpenReview rather than publishing a final proceedings PDF like it does for main conference papers.

## Reviewer Guidelines

Reviewers should follow these guidelines when evaluating a paper. These guidelines are based on the [reviewer guidelines for TMLR](https://jmlr.org/tmlr/acceptance-criteria.html).

The acceptance decision for a submission is based on the answers to the following questions:

**Are the claims made in the submission supported by accurate, convincing and clear evidence?**

This is the most important criterion. This implies assessing the technical soundness as well as the clarity of the narrative and arguments presented. Papers with large gaps between claims and evidence must be rejected.

- Papers presenting a new method/model with a reasonable proof of concept should be seen as satisfying this criterion.
- Papers solely presenting empirical analysis should present rigorous comparisons before making general claims.

**Would at least some individuals in this workshop's audience be interested in knowing the findings of this paper?**

This is arguably the most subjective criterion, and therefore needs to be treated carefully. Generally, a reviewer that is unsure as to whether a submission satisfies this criterion should assume that it does. Crucially, it should not be used as a reason to reject work that isn't considered "significant" or "impactful" because it isn't achieving a new state-of-the-art on some benchmark. Nor should it form the basis for rejecting work on a method considered not "novel enough", as novelty of the studied method is not a necessary criteria for acceptance. We explicitly avoid these terms ("significant", "impactful", "novel"), and focus instead on the notion of "interest". If the authors make it clear that there is something to be learned by some researchers in their area from their work, then the criterion of interest is considered satisfied.

Papers should be accepted if they meet these criteria, even if the contribution or significance of the work is modest.

Papers that should not be accepted include

- papers that make bold statements unsupported by empirical or rigorous evidence,
- papers that aren't clearly written,
- papers that incorrectly claim novelty over existing published work, and
- papers that merely re-implement an idea that has already been reproduced before.

### Review Format

A review should have the following content.

**Summary of contributions**: Brief description, in the reviewer's words, of the contributions and new knowledge presented by the submission.
**Strengths and weaknesses**: List of the strong aspects of the submission as well as weaker elements (if any) that you think require attention from the authors.
**Suggestions**: Any suggestions to improve the paper for future versions.

## Contact

If you have questions about this workshop or are not sure if your paper's topic is suitable for submission, please feel free to contact the organizers at [icml-structured-foundation-workshop@googlegroups.com](mailto:icml-structured-foundation-workshop@googlegroups.com).
