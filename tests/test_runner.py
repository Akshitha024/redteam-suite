"""End-to-end runner."""

from __future__ import annotations

from pathlib import Path

from redteam.runner import run


def test_runner_smoke(tmp_path: Path) -> None:
    s = run(tmp_path / "out")
    agg = s["aggregate"]
    assert isinstance(agg, dict)
    # The naive target should have ASR == 1.0.
    assert agg["naive"]["asr"] == 1.0  # type: ignore[index]
    # The strict target should have ASR == 0.0.
    assert agg["strict"]["asr"] == 0.0  # type: ignore[index]
