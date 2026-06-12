from technical.support_resistance.support_resistance_analysis import (
    analyze_support_resistance,
)


class SupportResistanceAgent:
    """
    Phase 8.5 Support & Resistance Agent
    """

    def analyze(
        self,
        data,
    ):
        result = analyze_support_resistance(
            df=data
        )

        return {
            "supports": result.supports,
            "resistances": result.resistances,
            "nearest_support": result.nearest_support,
            "nearest_resistance": result.nearest_resistance,
            "signal": result.signal,
            "signal_level": result.signal_level,
        }