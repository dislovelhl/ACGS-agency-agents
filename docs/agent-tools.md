# Agent Tools

`agent-tools.json` is the machine-readable index for external utilities that agents can use during task execution.

## Registry Contents

- `tools`: every registered tool with install command, source URL, commands, Python API hints, capabilities, formats, keywords, and security notes.
- `tools/*.md`: the source-of-truth tool specs that agents should inspect before using a tool.

## Selection Workflow

1. Parse `agent-tools.json`.
2. Run `python3 scripts/select-tool.py "<task>" --limit 5` for a ranked shortlist.
3. Read the selected tool spec under `tools/`.
4. Follow the security notes before running a tool on user-controlled paths, URLs, archives, or network inputs.

## MarkItDown

`tools/markitdown.md` registers Microsoft MarkItDown for converting PDFs, Office documents, HTML, structured text, ZIP contents, YouTube URLs, EPubs, and related inputs into Markdown for LLM analysis.

Use it when an agent needs document content in Markdown. Do not treat it as a high-fidelity renderer or pass untrusted inputs directly without path, URL, archive, and network restrictions.

## Registered Tools

| Tool | Use When | Avoid When |
| --- | --- | --- |
| `markitdown` | Convert documents and file formats into Markdown for LLM analysis. | Pixel-perfect rendering or unconstrained untrusted inputs. |
| `scrapling` | Scrape or crawl authorized websites with adaptive selectors, browser fetchers, or AI/MCP extraction. | The target forbids scraping, authorization is missing, or network execution cannot be constrained. |
| `impeccable` | Audit, critique, polish, or harden frontend/UI design with deterministic anti-pattern checks. | Backend-only work or unsafe remote URL scanning. |
| `heretic` | Authorized local transformer-model ablation, refusal-analysis, and interpretability research. | Bypassing safety controls, harmful deployments, or environments without model-risk governance. |
| `fff` | Fast repeated repository path/content search through MCP/editor tools such as `ffgrep` and `fffind`. | One-off local searches where `rg` is enough or search roots cannot be constrained. |

## Refresh Workflow

```bash
python3 scripts/build-tool-registry.py
python3 scripts/select-tool.py "convert pdf docx pptx xlsx files into markdown" --limit 3
python3 scripts/select-tool.py "scrape a dynamic website with adaptive selectors" --limit 3
python3 scripts/select-tool.py "audit frontend design anti patterns" --limit 3
python3 scripts/select-tool.py "fast repo file search grep modified files" --limit 3
python3 -m unittest tests/test_tool_registry.py
```
