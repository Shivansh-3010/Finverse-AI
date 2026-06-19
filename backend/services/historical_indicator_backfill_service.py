import math

from models.technical_indicator import (
    TechnicalIndicator,
)

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from repositories.technical_indicator_repository import (
    TechnicalIndicatorRepository,
)

from utils.ohlcv_dataframe import (
    ohlcv_to_dataframe,
)

from technical.momentum.rsi import (
    calculate_rsi,
)

from technical.momentum.macd import (
    calculate_macd,
)

from technical.trend.adx import (
    calculate_adx,
)

from technical.trend.sma import (
    calculate_sma,
)

from technical.trend.ema import (
    calculate_ema,
)

from technical.volatility.atr import (
    calculate_atr,
)

from technical.volatility.bollinger_bands import (
    calculate_bollinger_bands,
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

class HistoricalIndicatorBackfillService:

    @staticmethod
    def backfill_symbol(
        db,
        symbol: str,
        timeframe: str = "1d",
    ):

        ohlcv_repository = (
            OHLCVRepository(db)
        )

        indicator_repository = (
            TechnicalIndicatorRepository(db)
        )

        existing_timestamps = (
            indicator_repository
            .get_existing_timestamps(
                symbol,
                timeframe
            )
        )
        
        print(
            f"{symbol}: "
            f"{len(existing_timestamps):,} "
            f"existing indicators"
        )

        candles = (
            ohlcv_repository
            .get_history_by_symbol_and_timeframe(
                symbol,
                timeframe,
            )
        )

        if len(candles) < 50:

            return {
                "symbol": symbol,
                "inserted": 0,
                "reason": "Not enough candles",
            }
            
        df = (
            ohlcv_to_dataframe(
                candles
            )
        )

        rsi_series = (
            calculate_rsi(df)
        )

        mfi_series = (
            calculate_mfi(df)
        )

        sma_series = (
            calculate_sma(
                df,
                20
            )
        )

        ema_series = (
            calculate_ema(
                df,
                20
            )
        )

        atr_series = (
            calculate_atr(df)
        )

        obv_series = (
            calculate_obv(df)
        )

        vwap_series = (
            calculate_vwap(df)
        )

        macd_df = (
            calculate_macd(df)
        )

        adx_df = (
            calculate_adx(df)
        )

        bb_df = (
            calculate_bollinger_bands(df)
        )

        indicators = []

        inserted = 0
        skipped = 0

        for i in range(
            50,
            len(candles),
        ):

            current_candle = candles[i]

            if (
                current_candle.timestamp
                in existing_timestamps
            ):
                skipped += 1
                continue

            try:

                features = {

                    "rsi":
                        rsi_series.iloc[i],

                    "mfi":
                        mfi_series.iloc[i],

                    "sma_20":
                        sma_series.iloc[i],

                    "ema_20":
                        ema_series.iloc[i],

                    "atr":
                        atr_series.iloc[i],

                    "adx":
                        adx_df["adx"].iloc[i],

                    "macd":
                        macd_df["macd"].iloc[i],

                    "macd_signal":
                        macd_df["signal"].iloc[i],

                    "obv":
                        obv_series.iloc[i],

                    "vwap":
                        vwap_series.iloc[i],

                    "bb_upper":
                        bb_df["upper_band"].iloc[i],

                    "bb_middle":
                        bb_df["middle_band"].iloc[i],

                    "bb_lower":
                        bb_df["lower_band"].iloc[i],
                }

                def safe(value):

                    if value is None:
                        return 0.0

                    if (
                        isinstance(
                            value,
                            float
                        )
                        and math.isnan(value)
                    ):
                        return 0.0

                    return float(value)

                indicators.append(

                    TechnicalIndicator(

                        symbol=symbol,

                        timeframe=timeframe,

                        timestamp=
                            current_candle.timestamp,

                        rsi=safe(
                            features["rsi"]
                        ),

                        mfi=safe(
                            features["mfi"]
                        ),

                        sma_20=safe(
                            features["sma_20"]
                        ),

                        ema_20=safe(
                            features["ema_20"]
                        ),

                        macd=safe(
                            features["macd"]
                        ),

                        macd_signal=safe(
                            features["macd_signal"]
                        ),

                        adx=safe(
                            features["adx"]
                        ),

                        atr=safe(
                            features["atr"]
                        ),

                        obv=safe(
                            features["obv"]
                        ),

                        vwap=safe(
                            features["vwap"]
                        ),

                        bb_upper=safe(
                            features["bb_upper"]
                        ),

                        bb_middle=safe(
                            features["bb_middle"]
                        ),

                        bb_lower=safe(
                            features["bb_lower"]
                        ),
                    )
                )

                inserted += 1

                if len(indicators) >= 1000:

                    indicator_repository.bulk_insert(
                        indicators
                    )

                    indicators = []

                    print(
                        f"{symbol}: "
                        f"{inserted:,}"
                    )

            except Exception as e:

                skipped += 1

                print(
                    f"Skipped: {e}"
                )

        if indicators:

            indicator_repository.bulk_insert(
                indicators
            )

        return {

            "symbol": symbol,

            "inserted": inserted,

            "skipped": skipped,

            "candles": len(candles),
        }