import pandas as pd

from agents.support_resistance_agent.agent import SupportResistanceAgent


def test_analyze_returns_support_resistance_results():
    data = pd.DataFrame(
        {
            "high": [120, 125, 130, 127, 122, 118, 123, 128, 132, 129, 124],
            "low": [115, 120, 125, 122, 118, 110, 116, 121, 126, 123, 119],
            "close": [118, 124, 128, 125, 120, 112, 121, 126, 130, 127, 124],
        }
    )

    result = SupportResistanceAgent().analyze(data)

    assert isinstance(result, dict)
    assert {
        "supports",
        "resistances",
        "nearest_support",
        "nearest_resistance",
        "signal",
        "signal_level",
    }.issubset(result)
    assert isinstance(result["supports"], list)
    assert isinstance(result["resistances"], list)
