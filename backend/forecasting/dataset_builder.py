import pandas as pd

from technical.momentum.rsi import (
    calculate_rsi,
)

from technical.momentum.macd import (
    calculate_macd,
)

from technical.volatility.atr import (
    calculate_atr,
)
from technical.trend.adx import (
    calculate_adx,
)

from technical.volume.mfi import (
    calculate_mfi,
)

from technical.volume.obv import (
    calculate_obv,
)

from technical.volume.vwap import (
    calculate_vwap,
)

from technical.volatility.bollinger_bands import (
    calculate_bollinger_bands,
)
from repositories.candlestick_pattern_repository import (
    CandlestickPatternRepository,
)
from forecasting.news_feature_builder import (
    NewsFeatureBuilder,
)


class DatasetBuilder:

    @staticmethod
    def build(
        df: pd.DataFrame,
        candlestick_features=None,
    ):

        dataset = df.copy()

        dataset["rsi"] = (
            calculate_rsi(dataset)
        )

        macd = calculate_macd(dataset)

        dataset["macd"] = (
            macd["macd"]
        )

        dataset["macd_signal"] = (
            macd["signal"]
        )

        dataset["atr"] = (
            calculate_atr(dataset)
        )
        
        adx = calculate_adx(dataset)

        dataset["adx"] = adx["adx"]

        dataset["mfi"] = (
            calculate_mfi(dataset)
        )

        dataset["obv"] = (
            calculate_obv(dataset)
        )

        dataset["vwap"] = (
            calculate_vwap(dataset)
        )

        bb = calculate_bollinger_bands(
            dataset
        )

        dataset["bb_upper"] = (
            bb["upper_band"]
        )

        dataset["bb_middle"] = (
            bb["middle_band"]
        )

        dataset["bb_lower"] = (
            bb["lower_band"]
        )
        
        if candlestick_features is not None:

            dataset = dataset.merge(
                candlestick_features,
                on="timestamp",
                how="left"
            )

            dataset["strength"] = (
                dataset["strength"]
                .fillna(0.0)
            )

            dataset["confidence"] = (
                dataset["confidence"]
                .fillna(0.0)
            )

            dataset["candlestick_score"] = (
                dataset["candlestick_score"]
                .fillna(0.0)
            )

        dataset["target"] = (
            dataset["close"]
            .pct_change()
            .shift(-1)
            * 100
        )

        dataset = dataset.dropna()

        return dataset