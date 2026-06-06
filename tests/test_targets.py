"""Target tests."""

from __future__ import annotations

from redteam.probes.library import all_probes
from redteam.targets.mock import keyword_filter, naive, strict


def test_naive_always_succeeds_attacks() -> None:
    for p in all_probes():
        r = naive(p)
        assert not r.refused
        assert p.success_marker in r.output


def test_strict_always_refuses() -> None:
    for p in all_probes():
        r = strict(p)
        assert r.refused


def test_keyword_filter_blocks_some() -> None:
    blocks = sum(1 for p in all_probes() if keyword_filter(p).refused)
    assert 0 < blocks < len(all_probes())
