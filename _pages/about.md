---
layout: about
title: About
permalink: /
subtitle: <b>Workshop at the International Conference on Machine Learning (ICML) 2026</b>

profile:
  align: right

news: false # includes a list of news items. TODO: set to true when needed
selected_papers: false # includes a list of papers marked as "selected={true}"
social: false # includes social icons at the bottom of the page
---

The second [ICML](https://icml.cc/) workshop on **Foundation Models for Structured Data (FMSD)** will be held on **July 11, 2026**, in **Grand Ballroom 103** at the [COEX Convention & Exhibition Center](https://www.coexcenter.com/) in **Seoul, South Korea**. Also see the [official ICML event page](https://icml.cc/virtual/2026/workshop/54066). We are looking forward to welcoming you in Seoul!

See the [first edition (ICML 2025)](/2025/) for last year's workshop.

### Introduction

Structured data (tabular and time-series) underpins high-impact applications across finance, healthcare, enterprise decision-making, and climate modeling. Over the past two years, predictive foundation models tailored to structured data have emerged, enabling in-context learning and transfer across heterogeneous datasets and schemas, challenging the traditional "train per dataset" paradigm. Tabular and time-series foundation models share methodological similarities: pretraining on heterogeneous datasets, in-context learning, and transfer under schema and distribution shift. These similarities create natural synergies across the respective communities.

Building on the inaugural Foundation Models for Structured Data workshop at ICML 2025 (99 submissions; 500+ participants), **FMSD @ ICML 2026** will unify the tabular and time-series communities around shared challenges in data curation, scaling, evaluation (including contamination), and real-world deployment (latency, memory, monitoring).

**New in 2026:** We will host nine confirmed in-person industry spotlights to accelerate transfer of practical constraints and failure modes into academic research. We will distill these perspectives into a public workshop summary of open problems and best practices, alongside invited talks, contributed spotlights, and poster sessions. We also explicitly encourage submissions that study scaling across datasets, model size, and compute; and multimodality for structured foundation models (e.g., image-tabular modeling in medical diagnosis; text-time-series modeling for ECG interpretation). While these directions have driven transformative progress in text and vision, they remain largely underexplored for tabular and time-series data.

**Workshop Scope:** We focus on foundation-model approaches for inherently structured objectives on tabular and time-series data, such as classification, regression, forecasting, and structured generation. LLM/agent-based submissions are in scope only if they evaluate on predictive tabular/time-series objectives with strong classical baselines, and report cost/latency and numerical reliability checks. Out of scope are contributions about general-purpose foundation model architectures without a clear structured-data focus, and NLP-centric tasks over tables (e.g., table question answering / semantic parsing).

### Topics

The program of our workshop will focus on the following topics:

- **Building Foundation Models for (Multimodal) Structured Data**: Following the trends in language and vision domains, recent developments in foundation models in tabular and time series capable of zero-shot inference and/or in-context learning on unseen data have challenged the conventional in-domain training and prediction paradigm. Furthermore, models pretrained in one modality (such as tabular) can also demonstrate promising predictive performance in related domains by transforming the input data into a compatible format. We aim to assess progress in this area and the challenges of developing such models, including novel architectures and insights into scaling. A particular focus in 2026 is on multimodal structured foundation models, which integrate tabular and time-series data with complementary modalities such as text and images, enabling richer supervision, improved generalization, and new capabilities beyond unimodal structured learning.
- **Datasets and Synthetic Data Generation Methods**: The amount of high-quality structured data available in the public domain is limited for developing pretrained models, especially when compared with the amount of data available for other domains, such as language and vision. Structured foundation models that rely on real-world data for pre-training are often constrained by the number of available public datasets, or are limited to pre-training on relatively small-scale datasets from Wikipedia and GitHub. To address this limitation, recent work on foundation models for structured data has focused on developing high-fidelity synthetic data generation schemes and has included this data in their training corpus. This workshop welcomes contributions of high-quality large-scale (multimodal) datasets and synthetic data generation methods for training structured foundation models.
- **Benchmarks**: While efforts have been made to develop unified benchmarks for tabular and time series tasks, new efforts are required to evaluate structured foundation models comprehensively along different dimensions, such as different data characteristics, inference throughput, memory usage, scalability, and data memorization. Because structured-data corpora are small and reused, contamination and memorization can dominate reported gains; we explicitly encourage protocols and benchmarks that measure and mitigate contamination.
- **Alternative Paradigms (LLMs and Agents)**: Beyond purpose-built foundation models for structured data, large language models (LLMs) and agentic systems have shown emerging promise on inherently structured tasks. We invite LLM/agent-based work when evaluation centers on predictive tabular/time-series objectives and includes careful baselines, cost/latency reporting, and numerical reliability checks. Structured settings introduce alternative scaling dimensions beyond data and parameters such as schema diversity, cross-domain transfer, and inference-time compute through planning and tool use (with agents effectively scaling compute at inference). This raises a central open question: Are purpose-built structured foundation models fundamentally more sample- or compute-efficient than general-purpose LLM-based approaches for structured objectives? We welcome work that examines these scaling trade-offs, alongside challenges in interpretability, efficiency, and numerical reliability.
- **Applications of Foundation Models for Structured Data**: Foundation models for structured data can transform industries from climate modeling and fraud detection to supply chain optimization and health monitoring. Real-world deployment requires addressing challenges such as domain adaptation, model reliability, and data privacy. This workshop seeks contributions (1) showcasing novel applications in real-world structured data domains, (2) overcoming challenges such as scaling and inference throughput, and (3) demonstrating domain-specific innovation such as domain-specialized foundation models. We also welcome discussions on ethical considerations, fairness, and bias mitigation to ensure these technologies benefit a broad range of users and applications.

Please see the [Call for Papers](/call-for-papers/) for details.

### Schedule

**July 11, 2026, 9:00-17:00, Coex Convention & Exhibition Center, Seoul, South Korea**

The workshop will consist of 3 invited talks, 9 industry spotlights, 8 spotlight paper talks, and two poster sessions with contributed papers. You can find the workshop schedule below:

| Time          | Session |
|---------------|---------|
| 09:00 – 09:15 | <span style="color:#DDDDDD">Opening Remarks</span> |
| 09:15 – 09:45 | <span style="color:#4A90E2">Invited Talk: Multimodal Time-Series Foundation Models</span> |
| 09:45 – 09:55 | <span style="color:#E67E22">Industry Spotlight: AWS — Chronos-2: From Univariate to Universal Forecasting</span> |
| 09:55 – 10:05 | <span style="color:#E67E22">Industry Spotlight: SAP — The Idiosyncrasies of Enterprise Data – the SAP Experience</span> |
| 10:05 – 10:15 | <span style="color:#E67E22">Industry Spotlight: Layer6 — TabDPT: Public Research and Enterprise Impact at TD</span> |
| 10:15 – 10:25 | <span style="color:#E67E22">Industry Spotlight: Prior Labs — Moving from Tensors to Systems in Tabular Foundation Models</span> |
| 10:25 – 10:35 | <span style="color:#9B59B6">Spotlight Paper: SurvivalPFN: Amortizing Survival Prediction via In-Context Bayesian Inference</span> |
| 10:35 – 10:45 | <span style="color:#9B59B6">Spotlight Paper: HEPA: A Self-Supervised Horizon-Conditioned Event Predictive Architecture for Time Series</span> |
| 10:45 – 10:55 | <span style="color:#9B59B6">Spotlight Paper: Foundations without Fundamentals: Zero-Shot Blind Spots in Time Series FMs</span> |
| 10:55 – 11:05 | <span style="color:#9B59B6">Spotlight Paper: Dataset Inference for Data Provenance and Privacy Auditing in Tabular Foundation Models</span> |
| 11:05 – 12:00 | <span style="color:#A8CF79">[Poster Session 1]({{ '/accepted-papers/#poster-session-1' | relative_url }})</span> |
| 12:00 – 13:00 | <span style="color:#A01019">Lunch</span> |
| 13:00 – 13:30 | <span style="color:#4A90E2">Invited Talk: Scaling and Understanding Models for (Scientific) Tabular Data</span> |
| 13:30 – 13:40 | <span style="color:#E67E22">Industry Spotlight: Nixtla — What Is a Good Forecast? Reflections on Accuracy, Architectures, and Incentives</span> |
| 13:40 – 13:50 | <span style="color:#E67E22">Industry Spotlight: TimeCopilot — Agentic Forecasting: Scaling Time Series Foundation Models in Practice</span> |
| 13:50 – 14:00 | <span style="color:#E67E22">Industry Spotlight: Fundamental — What LLMs Learn (and Don't) from Tables</span> |
| 14:00 – 14:10 | <span style="color:#E67E22">Industry Spotlight: StableAI — Unleashing Structured-Data Modeling Capability for Generalist Intelligence</span> |
| 14:10 – 14:20 | <span style="color:#E67E22">Industry Spotlight: Yandex — Tabular Deep Learning: an Industry Researcher's Perspective</span> |
| 14:20 – 14:30 | <span style="color:#9B59B6">Spotlight Paper: Latent Instructions as Context Surrogates: Enhancing Frozen Time Series Forecasters with Instance-Adaptive Prompts</span> |
| 14:30 – 14:40 | <span style="color:#9B59B6">Spotlight Paper: Images as Tables: In-Context Learning with TabPFN for Low-Data Detection of AI-Generated Images</span> |
| 14:40 – 14:50 | <span style="color:#9B59B6">Spotlight Paper: Training Fair Tabular Foundation Models</span> |
| 14:50 – 15:00 | <span style="color:#9B59B6">Spotlight Paper: Bounded Context Management for Tabular Foundation Models on Stream Learning</span> |
| 15:00 – 15:30 | <span style="color:#4A90E2">Invited Talk: TabICLv2: Advancing Open Tabular Foundation Models</span> |
| 15:30 – 15:45 | <span style="color:#DDDDDD">Best Paper Award & Closing Remarks</span> |
| 15:45 – 17:00 | <span style="color:#A8CF79">[Poster Session 2]({{ '/accepted-papers/#poster-session-2' | relative_url }})</span> |

The schedule is also available on the [ICML event page](https://icml.cc/virtual/2026/workshop/54066).

<br>

### Sponsors

We thank our sponsors:

<img src="/assets/img/SAP_logo.png" alt="SAP Logo" width="300"/>

![Layer6Logo](/assets/img/Layer6_Logo.png)
* TD Bank offers products and services to over 27.9 million customers worldwide. Through our AI research lab - Layer6, we develop and deploy industry-leading AI and machine learning systems to advance the field of artificial intelligence in the financial services industry.

<img src="/assets/img/PriorLogo.png" alt="PriorLabsLogo" width="300"/>

* At Prior Labs, we're building Multimodal Tabular Foundation Models (TFMs), starting with TabPFN, that understand tables natively - learning statistical reasoning directly from data.  Our vision: truly agentic AI systems capable of understanding high-level goals, fusing tables, language, and images to reason, integrate domain knowledge, infer causality, and adapt dynamically.

### Contact

You can reach the organizers of the workshop at <a href="mailto:icml-structured-foundation-workshop@googlegroups.com">icml-structured-foundation-workshop@googlegroups.com</a>.
