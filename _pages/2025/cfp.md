---
layout: archive-page
permalink: /2025/call-for-papers/
title: Call for Papers
description:
---

We welcome researchers working on foundation models for structured data to submit their latest original research work to the ICML 2025 workshop on **Foundation Models for Structured Data**.

## Key Information

- Submission link: **[OpenReview](https://openreview.net/group?id=ICML.cc/2025/Workshop/FMSD)**
- Submission deadline: ~~May 19, 2025 (11:59 pm AoE)~~ May 23, 2025 (11:59 pm AoE)
- Acceptance notification: June 09, 2025 (anytime before 11:59 pm AoE)
- Camera ready deadline: July 02, 2025 (11:59 pm AoE) ([Camera Ready FAQ](#camera-ready-faq))
- Page Limit: short papers with up to 4 pages; unlimited references and appendices
- Misc: double-blind, non-archival, poster presentations for accepted papers

## Submission Instructions

Submissions should take the form of a short paper of up to **4 pages**. Additional pages containing references and appendices are allowed but the reviewers are _not obliged_ to refer to the appendices when reviewing the paper. Submissions should be made on **[OpenReview](https://openreview.net/group?id=ICML.cc/2025/Workshop/FMSD)** in a single `.pdf` file using **[this LaTeX style template](https://www.overleaf.com/latex/templates/icml2025-template/dhxrkcgkvnkt)**. The impact statement is not required for the submission to the workshop.

The review process is _double-blind_, so please ensure that your submission is properly anonymized. Papers that exceed the page limit or have not been properly anonymized will be desk-rejected without review. Please note that there is no rebuttal phase and the final decisions will be made based solely on the submission and the reviews. Rejected and withdrawn submissions will not be made public.

All accepted submissions will be accompanied by a poster presentation. A number of selected submissions will be invited for lightning and oral talks.

**Dual submission policy**: This workshop is **non-archival**; even though all accepted papers will be available on OpenReview and this website, there are no formally-published proceedings. If a paper is currently under review at another venue, it can still be submitted to this workshop. If a paper has previously appeared in a journal, workshop, or conference, it should be reasonably extended in order to be accepted at this workshop. Parallel submission of papers under review at ICML 2025 is allowed.

## Scope and Topics

We invite submissions related to the theme of foundation models for structured data. Key topics include, but are not limited to:

- **Building Foundation Models for Structured Data**: Following the trends in language and vision domains, recent development in foundation models (FM) in tabular and time series capable of zero-shot inference and/or in-context learning on unseen data has challenged the conventional in-domain training and prediction paradigm. In this workshop, we seek to understand the progress in this area and the challenges associated with developing such models, including novel model designs or scaling insights. We also welcome contributions that merge structured data with other modalities, such as text and image, for enhanced performance.
- **Datasets and Synthetic Data Generation Methods**: The amount of high-quality structured data available in the public domain is limited for developing pretrained models, especially when compared with the amount of data available for other domains, such as language and vision. Models that use real data for pre-training often use fewer than 200 datasets due to data availability issues, or are limited to pre-training on very small tables scraped from Github and Wikipedia. To address this limitation, recent work on foundation models for structured data has invested effort in developing high-fidelity synthetic data generation schemes and included this data as part of their training corpus. This workshop welcomes contributions of high quality dataset collections and synthetic data generation methods for structured foundation model training.
- **Benchmarks of Structured Data Foundation Models**: While efforts have been made to develop unified benchmarks for tabular tasks and for time series forecasting, new efforts are required to evaluate structured foundation models comprehensively along different dimensions, such as inference throughput, memory usage, scalability, and data memorization. Another challenge exists in evaluating a foundation model where contamination of the training data exists. Mitigating contamination is particularly hard for data-hungry foundation models in the data-scarce structured data domains. We welcome contributions of novel benchmarks evaluating FMs for structured data.
- **LLMs for Structured Data**: Large language models (LLMs) have shown remarkable reasoning and few-shot learning capabilities, and their potential in structured data tasks is emerging. Researchers have explored leveraging LLMs for predictive, reasoning, and generation tasks for structured data, often achieving competitive results without task-specific fine-tuning. However, challenges remain, including (1) the interpretability of LLM-based approaches, (2) their ability to handle large-scale structured datasets efficiently, and (3) their reliability in processing numerical data. This workshop welcomes contributions that improve the effectiveness of LLMs for structured data and highlights their strengths and limitations compared to non-LLM methods.
- **Critiques on Structured Data Foundation Models**: Contributions highlighting the limitations and failure modes of structured data foundation models through theoretical analysis or systematic empirical evaluations are welcome.
- **Applications of Foundation Models for Structured Data**: The development of foundation models for structured data can transform numerous industries, from climate modeling and fraud detection to supply chain optimization and health monitoring. Deploying these models in real-world settings requires addressing key challenges such as model reliability and data privacy. This workshop seeks contributions (1) showcasing novel applications of foundation models in structured data domains, (2) overcoming challenges, such as scaling and inference throughput for existing applications, and (3) demonstrating domain-specific innovation, such as domain specialized foundation models. We also welcome discussions on ethical considerations, fairness, and bias mitigation in structured data models, ensuring these technologies benefit a broad range of users and applications.

**Scope Clarification**: We use the term **structured data** to specifically refer to **tabular and time series data**, and our focus is on **predictive machine learning tasks** such as tabular classification, regression and time series forecasting. For example, general-purpose graph-based methods are out of scope of this workshop, but foundation models for spatio-temporal forecasting that leverage graph-based architectures are considered in-scope, since the primary goal aligns with predictive structured data modeling. Another example is that tabular question answering system falls outside the scope as it does not focus on predictive tasks. To help guide submissions, here are a few clearly relevant prior works that align with the goals of this workshop:
- **Time series**: Chronos, TimesFM, Moirai, Moment
- **Tabular**: TabPFN, TabICL, TabForestPFN, CARTE

## Camera Ready FAQ

**Q: What is the camera ready page limit?**
**A:** 4 pages.

---

**Q: What is the required poster format?**
**A:** Same as the ICML Conference guidelines: [ICML 2025 Poster Instructions](https://icml.cc/Conferences/2025/PosterInstructions)

---

**Q: How do I update the style file?**
**A:**
Modify the `icml2025.sty` file. For example, replace:
```latex
% \newcommand{\ICML@appearing}{\textit{Proceedings of the
% $\mathit{42}^{nd}$ International Conference on Machine Learning},
% Vancouver, Canada. PMLR 267, 2025.
% Copyright 2025 by the author(s).}
```
with:
```latex
\newcommand{\ICML@appearing}{\textit{Proceedings of the
$\mathit{1}^{st}$ ICML Workshop on Foundation Models for Structured Data},
Vancouver, Canada. 2025.
Copyright 2025 by the author(s).}
```

---

**Q: How do I submit the camera-ready version? Do I uncomment the camera-ready line in the LaTeX file, download it, and re-upload?**
**A:** Yes. Follow the template instructions to generate the final version and then re-upload it to the system.

---

**Q: I can't find an upload option or clear instructions on the workshop website. What should I do?**
**A:** Please follow the general ICML instructions and the LaTeX template comments to prepare your camera-ready version.

---

**Q: Will there be an option for online attendance?**
**A:** Talks will be livestreamed by ICML. Poster sessions and other in-person events will not be shared online.

---

**Q: None of the authors can attend in-person, can the organizers print our paper's poster and bring it to the workshop for us?**
**A:** We are still evaluating our options for these cases. We recommend seeing if anyone you know (even outside the author list) is attending in-person and would be able to print/bring the poster to the workshop. If you are unable to find someone to deliver the poster, please email the organizers with your situation.

---

**Q: Can the organizers assist with travel issues / fee waivers?**
**A:** Unfortunately we are unable to assist with travel issues or waive registration fees.

## Call for Reviewers

We are looking for reviewers for the workshop. If you would like to nominate someone (or yourself), please fill the **[Call for Reviewers Google Form](https://docs.google.com/forms/d/e/1FAIpQLSe1pjelLNsrdS6Q18bg2ZH6zTbMOX5AZSqcn-0a3ITVEu95xA/viewform?usp=sharing)**.

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
