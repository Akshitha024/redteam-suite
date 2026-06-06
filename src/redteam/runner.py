"""End-to-end runner."""

from __future__ import annotations

import json
from pathlib import Path

from redteam.probes.library import all_probes
from redteam.scoring.asr import aggregate, score
from redteam.targets.mock import all_targets
from redteam.types import ProbeOutcome
from redteam.viz.charts import (
    asr_per_target_bar,
    kind_breakdown_stack,
    per_probe_strip,
    severity_breakdown,
    severity_heatmap,
)


def run(out_dir: Path) -> dict[str, object]:
    out_dir.mkdir(parents=True, exist_ok=True)
    figs = Path("results/figures")
    probes = all_probes()
    targets = all_targets()
    rows: list[ProbeOutcome] = []
    for target in targets:
        for probe in probes:
            response = target(probe)
            rows.append(score(probe, response))

    agg = aggregate(rows)
    asr_per_target_bar(agg, figs / "asr.png")
    severity_breakdown(rows, figs / "severity.png")
    kind_breakdown_stack(rows, figs / "kinds.png")
    per_probe_strip(rows, figs / "per_probe.png")
    severity_heatmap(rows, figs / "severity_heatmap.png")

    summary: dict[str, object] = {
        "n_probes": len(probes),
        "n_targets": len(targets),
        "aggregate": agg,
        "rows": [r.model_dump() for r in rows],
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, default=str))
    return summary
