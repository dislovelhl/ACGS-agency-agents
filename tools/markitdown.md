---
id: markitdown
name: Microsoft MarkItDown
description: Convert PDFs, Office documents, images, audio metadata/transcripts, HTML, CSV, JSON, XML, ZIP contents, YouTube URLs, EPubs, and other files into Markdown for LLM and agent text-analysis pipelines.
source_url: https://github.com/microsoft/markitdown
install: pip install 'markitdown[all]'
commands:
  - markitdown path-to-file.pdf -o document.md
  - cat path-to-file.pdf | markitdown
python_api:
  - from markitdown import MarkItDown
  - result = MarkItDown(enable_plugins=False).convert("document.pdf")
capabilities:
  - document-conversion
  - markdown-extraction
  - llm-preprocessing
  - file-ingestion
formats:
  - pdf
  - pptx
  - docx
  - xlsx
  - xls
  - outlook
  - image
  - audio
  - html
  - csv
  - json
  - xml
  - zip
  - youtube
  - epub
keywords:
  - convert
  - conversion
  - document
  - documents
  - markdown
  - office
  - pdf
  - powerpoint
  - word
  - excel
  - extraction
  - ingestion
  - llm
security_notes:
  - MarkItDown performs I/O with the privileges of the current process.
  - Do not pass untrusted paths, URLs, archives, or user-controlled inputs directly without validation and restriction.
  - Prefer the narrowest conversion function or local-file workflow needed for the task.
  - Restrict URI schemes, network destinations, private ranges, loopback, link-local, and metadata-service access in hosted environments.
use_when:
  - An agent needs to turn a PDF, Word, PowerPoint, Excel, HTML, structured text, archive, or media-adjacent file into Markdown.
  - An agent needs token-efficient document text for summarization, review, extraction, or downstream reasoning.
  - Human-readable fidelity is less important than structured Markdown for LLM consumption.
avoid_when:
  - The task needs pixel-perfect or legally authoritative document rendering.
  - Inputs are untrusted and cannot be constrained to safe local files or safe network destinations.
---

# Microsoft MarkItDown

Use this tool when agents need to convert common document and content formats into Markdown for LLM analysis.
