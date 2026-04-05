---
title: "GeoLLM: Extracting Geospatial Knowledge from Large Language Models"
source: https://arxiv.org/abs/2310.06213
author:
  - "[[Rohin Manvi]]"
  - "[[Samar Khanna]]"
  - "[[Gengchen Mai]]"
  - "[[Marshall Burke]]"
  - "[[David Lobell]]"
  - "[[Stefano Ermon]]"
published:
created: 2026-04-04
description: "Abstract page for arXiv paper 2310.06213: GeoLLM: Extracting Geospatial Knowledge from Large Language Models"
tags:
  - clippings
  - mapping
  - ai
topic:
type: note
---
## Title:GeoLLM: Extracting Geospatial Knowledge from Large Language Models

[View PDF](https://arxiv.org/pdf/2310.06213)

> Abstract:The application of machine learning (ML) in a range of geospatial tasks is increasingly common but often relies on globally available covariates such as satellite imagery that can either be expensive or lack predictive power. Here we explore the question of whether the vast amounts of knowledge found in Internet language corpora, now compressed within large language models (LLMs), can be leveraged for geospatial prediction tasks. We first demonstrate that LLMs embed remarkable spatial information about locations, but naively querying LLMs using geographic coordinates alone is ineffective in predicting key indicators like population density. We then present GeoLLM, a novel method that can effectively extract geospatial knowledge from LLMs with auxiliary map data from OpenStreetMap. We demonstrate the utility of our approach across multiple tasks of central interest to the international community, including the measurement of population density and economic livelihoods. Across these tasks, our method demonstrates a 70% improvement in performance (measured using Pearson's $r^2$) relative to baselines that use nearest neighbors or use information directly from the prompt, and performance equal to or exceeding satellite-based benchmarks in the literature. With GeoLLM, we observe that GPT-3.5 outperforms Llama 2 and RoBERTa by 19% and 51% respectively, suggesting that the performance of our method scales well with the size of the model and its pretraining dataset. Our experiments reveal that LLMs are remarkably sample-efficient, rich in geospatial information, and robust across the globe. Crucially, GeoLLM shows promise in mitigating the limitations of existing geospatial covariates and complementing them well. Code is available on the project website: [this https URL](https://rohinmanvi.github.io/GeoLLM)

| Comments: |
| --- |
| Subjects: | Computation and Language (cs.CL); Machine Learning (cs.LG) |
| Cite as: | [arXiv:2310.06213](https://arxiv.org/abs/2310.06213) \[cs.CL\] |
|  | (or [arXiv:2310.06213v2](https://arxiv.org/abs/2310.06213v2) \[cs.CL\] for this version) |
|  | [https://doi.org/10.48550/arXiv.2310.06213](https://doi.org/10.48550/arXiv.2310.06213) |

## Submission history

From: Rohin Manvi \[[view email](https://arxiv.org/show-email/2e94f025/2310.06213)\]  
**[\[v1\]](https://arxiv.org/abs/2310.06213v1)** Tue, 10 Oct 2023 00:03:23 UTC (1,927 KB)  
**\[v2\]** Sat, 24 Feb 2024 16:11:57 UTC (1,931 KB)  

[Which authors of this paper are endorsers?](https://arxiv.org/auth/show-endorsers/2310.06213) | Disable MathJax ([What is MathJax?](https://info.arxiv.org/help/mathjax.html))