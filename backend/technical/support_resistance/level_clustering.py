from typing import List

from technical.support_resistance.models import (
    PivotPoint,
    ClusteredLevel,
)


def cluster_levels(
    pivots: List[PivotPoint],
    tolerance_pct: float = 0.5
) -> List[ClusteredLevel]:
    """
    Group nearby pivot prices into a single support/resistance level.

    tolerance_pct=0.5 means:
    1300 level accepts prices within ±0.5%
    """

    if not pivots:
        return []

    pivots = sorted(pivots, key=lambda p: p.price)

    clusters = []

    for pivot in pivots:

        matched_cluster = None

        for cluster in clusters:

            tolerance = cluster["level"] * (
                tolerance_pct / 100
            )

            if abs(pivot.price - cluster["level"]) <= tolerance:
                matched_cluster = cluster
                break

        if matched_cluster:

            matched_cluster["prices"].append(
                pivot.price
            )

            matched_cluster["level"] = (
                sum(matched_cluster["prices"])
                / len(matched_cluster["prices"])
            )

        else:

            clusters.append(
                {
                    "level": pivot.price,
                    "prices": [pivot.price],
                    "type": (
                        "resistance"
                        if pivot.pivot_type == "high"
                        else "support"
                    )
                }
            )

    results = []

    for cluster in clusters:

        results.append(
            ClusteredLevel(
                level=round(cluster["level"], 2),
                touches=len(cluster["prices"]),
                level_type=cluster["type"]
            )
        )

    return results