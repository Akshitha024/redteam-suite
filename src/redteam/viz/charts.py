"""Five chart families for redteam-suite."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from redteam.types import ProbeOutcome


def _save(fig: Figure, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    plt.close(fig)
    return out


def asr_per_target_bar(agg: dict[str, dict[str, float]], out: Path) -> Path:
    targets = sorted(agg)
    asr = [agg[t]["asr"] for t in targets]
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(targets, asr, color="#c25a4f")
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("attack success rate")
    ax.set_title("ASR by target")
    for bar, a in zip(bars, asr, strict=True):
        ax.text(bar.get_x() + bar.get_width() / 2, a + 0.02, f"{a:.0%}", ha="center", fontsize=9)
    return _save(fig, out)


def severity_breakdown(rows: list[ProbeOutcome], out: Path) -> Path:
    targets = sorted({r.target_name for r in rows})
    severities = ["low", "medium", "high"]
    x = np.arange(len(targets))
    w = 0.8 / len(severities)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    palette = plt.get_cmap("tab10")
    for i, s in enumerate(severities):
        ys = [
            sum(1 for r in rows if r.target_name == t and r.severity == s and r.succeeded)
            for t in targets
        ]
        ax.bar(x + i * w - w * (len(severities) - 1) / 2, ys, w, label=s, color=palette(i))
    ax.set_xticks(x)
    ax.set_xticklabels(targets)
    ax.set_ylabel("successful attacks")
    ax.set_title("Successful attacks by target and severity")
    ax.legend()
    return _save(fig, out)


def kind_breakdown_stack(rows: list[ProbeOutcome], out: Path) -> Path:
    targets = sorted({r.target_name for r in rows})
    kinds = ["prompt_injection", "jailbreak", "pii_leak"]
    counts = np.zeros((len(kinds), len(targets)))
    for r in rows:
        if r.succeeded:
            counts[kinds.index(r.kind), targets.index(r.target_name)] += 1
    fig, ax = plt.subplots(figsize=(7, 4))
    bottom = np.zeros(len(targets))
    colors = plt.get_cmap("Pastel1")
    for i, k in enumerate(kinds):
        ax.bar(targets, counts[i], bottom=bottom, label=k, color=colors(i))
        bottom += counts[i]
    ax.set_ylabel("successful attacks")
    ax.set_title("Successful attacks by attack kind")
    ax.legend()
    return _save(fig, out)


def per_probe_strip(rows: list[ProbeOutcome], out: Path) -> Path:
    targets = sorted({r.target_name for r in rows})
    pids = sorted({r.pid for r in rows})
    fig, ax = plt.subplots(figsize=(8, 1 + len(targets)))
    for ti, t in enumerate(targets):
        for pi, p in enumerate(pids):
            row = next((r for r in rows if r.target_name == t and r.pid == p), None)
            c = "#c25a4f" if (row and row.succeeded) else "#5b8d4a"
            ax.scatter(pi, ti, c=c, marker="s", s=80)
    ax.set_yticks(range(len(targets)))
    ax.set_yticklabels(targets)
    ax.set_xticks(range(len(pids)))
    ax.set_xticklabels(pids, rotation=45, ha="right", fontsize=8)
    ax.set_title("Per-(target, probe) success (red) / refusal (green)")
    return _save(fig, out)


def severity_heatmap(rows: list[ProbeOutcome], out: Path) -> Path:
    targets = sorted({r.target_name for r in rows})
    severities = ["low", "medium", "high"]
    mat = np.zeros((len(targets), len(severities)))
    cnt = np.zeros_like(mat)
    for r in rows:
        mat[targets.index(r.target_name), severities.index(r.severity)] += int(r.succeeded)
        cnt[targets.index(r.target_name), severities.index(r.severity)] += 1
    rate = np.where(cnt > 0, mat / np.maximum(cnt, 1), 0)
    fig, ax = plt.subplots(figsize=(6, 4))
    im = ax.imshow(rate, aspect="auto", cmap="magma", vmin=0, vmax=1)
    ax.set_xticks(range(len(severities)))
    ax.set_xticklabels(severities)
    ax.set_yticks(range(len(targets)))
    ax.set_yticklabels(targets)
    for i in range(rate.shape[0]):
        for j in range(rate.shape[1]):
            ax.text(j, i, f"{rate[i, j]:.0%}", ha="center", va="center", color="w", fontsize=9)
    ax.set_title("ASR by target x severity")
    fig.colorbar(im, ax=ax)
    return _save(fig, out)
