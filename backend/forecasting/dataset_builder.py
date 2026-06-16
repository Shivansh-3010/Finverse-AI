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


class DatasetBuilder:

    @staticmethod
    def build(df: pd.DataFrame):

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

        dataset["target"] = (
            dataset["close"]
            .pct_change()
            .shift(-1)
            * 100
        )

        dataset = dataset.dropna()

        return dataset