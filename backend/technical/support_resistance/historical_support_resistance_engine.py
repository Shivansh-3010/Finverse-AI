import pandas as pd

from technical.support_resistance.support_resistance_analysis import (
    analyze_support_resistance,
)


class HistoricalSupportResistanceEngine:

    LOOKBACK_WINDOW = 252

    @classmethod
    def build_features(
        cls,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        rows = []

        for i in range(
            cls.LOOKBACK_WINDOW,
            len(df)
        ):

            history = (
                df.iloc[
                    i - cls.LOOKBACK_WINDOW : i + 1
                ]
                .copy()
            )

            analysis = (
                analyze_support_resistance(
                    history
                )
            )
            
            if (
                analysis.nearest_support is None
                or analysis.nearest_resistance is None
            ):
                continue

            rows.append(
                {
                    "timestamp":
                        df.iloc[i]["timestamp"],
                        
                    "nearest_support":
                        analysis.nearest_support,

                    "nearest_resistance":
                        analysis.nearest_resistance,

                    "distance_to_support_pct":
                        analysis.distance_to_support_pct,

                    "distance_to_resistance_pct":
                        analysis.distance_to_resistance_pct,

                    "support_strength":
                        analysis.support_strength,

                    "resistance_strength":
                        analysis.resistance_strength,

                    "breakout_zone_lower":
                        analysis.breakout_zone_lower,

                    "breakout_zone_upper":
                        analysis.breakout_zone_upper,

                    "breakdown_zone_lower":
                        analysis.breakdown_zone_lower,

                    "breakdown_zone_upper":
                        analysis.breakdown_zone_upper,

                    "signal":
                        analysis.signal,

                    "signal_level":
                        analysis.signal_level,
                }
            )

        result = pd.DataFrame(rows)

        if result.empty:
            return result

        result = result.dropna(
            subset=[
                "nearest_support",
                "nearest_resistance",
            ]
        )

        return result