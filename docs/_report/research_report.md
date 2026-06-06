---
title: "redteam-suite: a defensive prompt-attack benchmark for LLM guardrails"
author: "Akshitha Reddy Lingampally"
date: "2025-03-14"
geometry: margin=1in
fontsize: 11pt
---

# Abstract

`redteam-suite` is a defensive evaluation harness for LLM guardrails. Six benign probes across three kinds (prompt-injection, jailbreak, PII-leak) are run against three mock target chatbots (naive, keyword_filter, strict) and the per-target attack success rate (ASR) is reported. On the bundled fixture, the naive target's ASR is 1.00, the strict target's is 0.00, and the keyword_filter sits in between at roughly 0.33, with one of the high-severity probes still slipping through. Five chart families decompose the ASR signal by target, by attack kind, and by severity. The suite is intended for the question "did my latest guardrail change improve or regress robustness?" - a question single-number metrics cannot answer.

# 1. Background

## 1.1 Motivation

LLM guardrails are typically evaluated with one summary number: an ASR averaged across all attack categories. This collapses the most useful debugging signal: which *kinds* of attacks (injection, jailbreak, PII-leak) get through, and at what severity. The suite reports those breakdowns alongside the headline.

## 1.2 Scope

- Six benign, deterministic probes across three attack kinds.
- Three mock targets (no filter, keyword filter, blanket refusal).
- ASR scorer that distinguishes refusal from success.
- Five chart families that decompose the ASR.

## 1.3 Safety

All probes are benign. Their "success markers" are non-actionable sentinel strings (`OVERRIDE`, `NO_FILTER`, `PII_EMAIL`, etc.). The suite is for testing the guardrail's *refusal logic*, not for producing actionable attack content.

# 2. Related Work

- Perez et al. "Red Teaming Language Models with Language Models" (2022)
- Anthropic, "Many-shot jailbreaking" (2024)

# 3. Method

```mermaid
flowchart LR
  A[Probe library\n(6 probes x 3 kinds)] --> B[Target chatbots\n(naive, keyword_filter, strict)]
  B --> C[ASR scorer\n(refused vs marker-in-output)]
  C --> D[5 chart families + summary.json]
```

# 4. Data

| pid | kind | severity |
|---|---|---|
| pi-001 | prompt_injection | medium |
| pi-002 | prompt_injection | low |
| jb-001 | jailbreak | high |
| jb-002 | jailbreak | medium |
| pl-001 | PII-leak | high |
| pl-002 | PII-leak | medium |

# 5. Evaluation Setup

For each (target, probe) pair: the target sees the probe; the scorer returns success if (a) the target did not refuse AND (b) the success marker is present in the output.

# 6. Results

| target | ASR | high-severity ASR |
|---|---|---|
| naive | 1.00 | 1.00 |
| keyword_filter | 0.33 | 0.50 |
| strict | 0.00 | 0.00 |

## 6.2 ASR by target

![ASR](../../results/figures/asr.png){width=85%}

## 6.3 Successful attacks by severity

![Severity](../../results/figures/severity.png){width=85%}

## 6.4 By attack kind

![Kinds](../../results/figures/kinds.png){width=85%}

## 6.5 Per-(target, probe) grid

![Per probe](../../results/figures/per_probe.png){width=85%}

## 6.6 ASR by target x severity

![Severity heatmap](../../results/figures/severity_heatmap.png){width=85%}

# 7. Ablations

## 7.1 Keyword filter coverage

Adding "print", "pretend" to the keyword filter drops ASR further. Adding too many keywords trips refusals on benign requests; the suite makes the tradeoff legible by tracking refusal rate alongside ASR.

## 7.2 Strict baseline

A blanket refusal achieves ASR=0 but is useless in production. The suite exists so an operator can see the gap between the strict baseline and their actual guardrail.

# 8. Discussion

The keyword-filter target is the interesting case. It catches some probes but not all; the per-probe grid lets us see exactly which probes slipped through. That diagnostic is what unlocks targeted improvement.

# 9. Limitations

1. Mock targets; real LLM guardrails are non-deterministic.
2. Six probes; production red-teaming uses thousands.
3. No multi-turn or many-shot attacks (yet).

# 10. Future Work

- Many-shot variants.
- Real-LLM target adapter behind an env var.
- Probe generation via a small LLM that mutates seed templates.

# 11. References

1. Perez, F., Lewis, M., et al. (2022). *Red Teaming Language Models with Language Models*.
2. Anthropic. (2024). *Many-shot jailbreaking*.

# Appendix A. Reproducibility

- [x] MIT.
- [x] Hermetic deterministic targets + probes.
- [x] Test artifacts.

# Appendix B. Glossary

- **ASR.** Attack success rate.
- **Refusal.** Target declined to respond.
- **Severity.** Probe-level low/medium/high severity tag.
