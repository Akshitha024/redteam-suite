"""Mock target chatbots with varying defense strength."""

from __future__ import annotations

from collections.abc import Callable

from redteam.types import Probe, TargetResponse

Target = Callable[[Probe], TargetResponse]


def naive(probe: Probe) -> TargetResponse:
    """Always echoes the success marker. Worst-case baseline."""
    return TargetResponse(
        pid=probe.pid, target_name="naive", output=probe.success_marker, refused=False
    )


def keyword_filter(probe: Probe) -> TargetResponse:
    """Blocks if the prompt contains common attack keywords."""
    blocked = any(
        kw in probe.prompt.lower()
        for kw in (
            "ignore",
            "roleplay",
            "no rules",
            "no safety",
            "pretend you have",
            "print the last user",
        )
    )
    if blocked:
        return TargetResponse(
            pid=probe.pid,
            target_name="keyword_filter",
            output="I cannot help with that.",
            refused=True,
        )
    return TargetResponse(
        pid=probe.pid, target_name="keyword_filter", output=probe.success_marker, refused=False
    )


def strict(probe: Probe) -> TargetResponse:
    """Refuses everything."""
    return TargetResponse(
        pid=probe.pid, target_name="strict", output="I cannot help with that.", refused=True
    )


def all_targets() -> list[Target]:
    return [naive, keyword_filter, strict]
