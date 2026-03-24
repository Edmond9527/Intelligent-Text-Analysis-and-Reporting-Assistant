# Project Title <!-- required -->

Intelligent Text Analysis and Reporting Assistant Based on LLM

[中文版本](./README_ZH.md)

## Project Overview <!-- required -->

This project is an intelligent assistant system designed for data processing and text mining. Relying on a locally deployed LLM cluster, it aims to perform deep structural extraction and multi-dimensional analysis on massive unstructured Chinese and English texts (e.g. course materials, academic papers, and assignments). Core features include intelligent summarization, sentiment analysis, and key feature extraction. Advanced features support batch processing pipelines and multi-document comparative analysis.

## Activity Information <!-- required -->

- **Competition / Workshop:** 2026 NJUPT Winter Battle <!-- required: replace with your activity name -->
- **Team Members:** Fengyi Li, Hongqing Du <!-- required: list all team members -->
- **Awarded:** Bronze 

## Environment <!-- required -->

- **Base Image:** Basic GPU Environment (aup-learning-cloud)
- **Extra Dependencies:** Listed in `requirements.txt` <!-- required: briefly describe key packages if any, or write "None" -->

## Quick Start <!-- required -->

<!-- Step-by-step instructions to run your notebook. Be specific. -->

1. In aup-learning-cloud, select **Basic GPU Environment** and set the Git URL to this repository
2. Navigate to `cases/<activity-folder>/<your-folder>/`
3. Open `main.ipynb`
4. Run all cells from top to bottom

## Technical Highlights

* [cite_start]**Prompt Engineering:** Utilized System Roles, Few-shot prompting, and Chain-of-Thought (CoT) to ensure stable formatting and complex logical deduction[cite: 52, 58, 93].
* [cite_start]**Context Window Management:** Implemented cascaded summary generation and an adaptive allocation algorithm to prevent Out-Of-Memory (OOM) errors with long texts[cite: 121, 123, 147].
* [cite_start]**API Lifecycle Management:** Designed robust error handling with a linear backoff retry strategy to mitigate server rate limits and avoid "retry storms"[cite: 249, 251, 253].
* [cite_start]**Robust Data Parsing:** Normalized polymorphic data streams and added a pre-execution circuit breaker to isolate corrupted files without crashing the pipeline[cite: 262, 265].
* [cite_start]**Asynchronous Concurrency:** Used `ThreadPoolExecutor` to parallelize subtasks, masking network I/O latency and significantly boosting throughput[cite: 272, 273].
* [cite_start]**I/O Optimization & Frontend:** Bypassed Jupyter WebSocket limits with a dual-modal I/O (including server-side direct read) and built an embedded GUI using native `ipywidgets`[cite: 281, 283, 288].
## Results / Demo

* **Real-time File Dashboard:** Provides a real-time monitor for file parsing status, extracted character count, and estimated Token consumption, including smart alerts for exceeding text limits.
* **Batch Analysis Pipeline:** Breaks single-request limits, automatically outputting standardized Markdown reports containing summaries, sentiment scores, and keywords to achieve machine-level efficient review.
* **Multi-Document Comparative Report:** Overcomes single-text limitations; the system automatically summarizes and generates a structured deep analysis report encompassing "core themes, commonalities, and key differences" across multiple documents.
## References
* **Ollama API Docs:** https://ollama.readthedocs.io/api/
