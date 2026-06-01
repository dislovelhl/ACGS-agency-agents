---
id: fff
name: fff
description: Fast file and content search toolkit for AI agents and editors, with MCP tools, frecency-ranked path search, typo-resistant content search, git-aware annotations, and Neovim/Lua APIs.
source_url: https://github.com/dmtrKovalenko/fff
install: curl -L https://dmtrkovalenko.dev/install-fff-mcp.sh | bash
commands:
  - ffgrep "TODO"
  - fffind "button"
  - fff-multi-grep "auth" "token" "session"
  - curl -L https://dmtrkovalenko.dev/install-fff-mcp.sh | bash
python_api: []
capabilities:
  - file-search
  - content-search
  - repo-search
  - grep
  - fuzzy-search
  - mcp-server
  - code-navigation
formats:
  - file-path
  - text
  - source-code
  - repository
keywords:
  - fff
  - ffgrep
  - fffind
  - grep
  - search
  - file
  - files
  - repo
  - repository
  - code
  - content
  - fuzzy
  - frecency
  - mcp
  - modified
  - git
  - fast
security_notes:
  - Inspect install scripts before piping them to a shell in sensitive environments.
  - Limit searches to the intended git-indexed directory to avoid leaking private files into agent context.
  - Treat search output as potentially sensitive; avoid copying secrets, credentials, or private data into prompts unless explicitly needed and authorized.
use_when:
  - An MCP-capable agent needs fast repeated repository file search or grep.
  - An agent needs `ffgrep`, `fffind`, or `fff-multi-grep` instead of repeated shell grep/find calls.
  - An editor or agent workflow benefits from frecency, git-aware annotations, typo resistance, or warmed search indexes.
avoid_when:
  - A single local `rg` command is enough and no MCP/tool installation is available.
  - The search root cannot be constrained to the intended repository or project.
---

# fff

Use fff when agents need fast repeated repository path and content search through MCP tools or editor integration.
