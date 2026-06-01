---
id: heretic
name: Heretic
description: Research CLI for automated directional ablation experiments on local transformer models, including refusal-direction analysis, optimization, evaluation, and interpretability-oriented residual geometry features.
source_url: https://github.com/p-e-w/heretic
install: pip install -U heretic-llm
commands:
  - heretic Qwen/Qwen3-4B-Instruct-2507
  - heretic --model google/gemma-3-12b-it --evaluate-model p-e-w/gemma-3-12b-it-heretic
  - heretic --help
python_api: []
capabilities:
  - model-ablation-research
  - transformer-interpretability
  - refusal-analysis
  - residual-geometry
  - model-evaluation
  - local-llm-research
formats:
  - huggingface-model
  - safetensors
  - pytorch
  - toml
  - png
  - gif
keywords:
  - heretic
  - ablation
  - abliteration
  - refusal
  - refusals
  - direction
  - transformer
  - model
  - models
  - local
  - llm
  - research
  - interpretability
  - residual
  - geometry
  - optuna
  - evaluation
  - kl
security_notes:
  - Treat this as a controlled local model-research tool, not a general agent utility.
  - Do not use it to bypass safety controls for harmful, abusive, illegal, or policy-violating deployments.
  - Expect high compute, VRAM, model-license, and supply-chain risk; pin dependencies and review model licenses before running.
  - Generated or modified models require safety evaluation and deployment governance before any release or user-facing use.
use_when:
  - An authorized research agent needs to study refusal directions, ablation parameters, or transformer residual geometry.
  - An agent needs to evaluate an already-generated Heretic model against an original model in a controlled local environment.
  - A model-governance workflow needs evidence about model modification tradeoffs, KL divergence, or refusal behavior.
avoid_when:
  - The task asks for evading safety policies, producing harmful content, or deploying an uncensored model to users.
  - The environment lacks local model permissions, sufficient compute, dependency isolation, or model-risk review.
---

# Heretic

Use Heretic only for authorized local transformer-model research, evaluation, and governance workflows around ablation and refusal-direction analysis.
