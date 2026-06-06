"""Probe library tests."""

from __future__ import annotations

from redteam.probes.library import all_probes
from redteam.types import AttackKind


def test_all_kinds_present() -> None:
    kinds = {p.kind for p in all_probes()}
    assert kinds == set(AttackKind)


def test_each_probe_has_success_marker() -> None:
    for p in all_probes():
        assert p.success_marker
