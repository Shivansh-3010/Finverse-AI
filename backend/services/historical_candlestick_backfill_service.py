from models.candlestick_pattern import (
    CandlestickPattern,
)

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from repositories.candlestick_pattern_repository import (
    CandlestickPatternRepository,
)

from technical.candlestick.candlestick_analysis import (
    analyze_candlestick,
)


class HistoricalCandlestickBackfillService:

    @staticmethod
    def backfill_symbol(
        db,
        symbol: str,
        timeframe: str = "1d",
    ):

        ohlcv_repository = (
            OHLCVRepository(db)
        )

        pattern_repository = (
            CandlestickPatternRepository(db)
        )

        existing_keys = (
            pattern_repository
            .get_existing_keys(
                symbol,
                timeframe,
            )
        )

        print(
            f"{symbol}: "
            f"{len(existing_keys):,} "
            f"existing patterns"
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

        patterns_to_save = []

        inserted = 0
        skipped = 0
        
        for i in range(
            50,
            len(candles),
        ):

            current_candle = candles[i]

            try:

                history = candles[: i + 1]

                result = (
                    analyze_candlestick(
                        history
                    )
                )

                patterns = result[
                    "patterns"
                ]

                if not patterns:
                    continue

                for pattern in patterns:
                    
                    key = (
                        current_candle.timestamp,
                        pattern["pattern"],
                    )

                    if key in existing_keys:
                        continue
                    
                    existing_keys.add(key)

                    patterns_to_save.append(

                        CandlestickPattern(

                            symbol=symbol,

                            timeframe=timeframe,

                            timestamp=
                                current_candle.timestamp,

                            pattern_name=
                                pattern["pattern"],

                            signal=
                                pattern["signal"].value,

                            strength=float(
                                pattern["strength"]
                            ),

                            confidence=float(
                                pattern["confidence"]
                            ),

                            candlestick_score=float(
                                result[
                                    "candlestick_score"
                                ]
                            ),
                        )
                    )

                    inserted += 1

                if len(patterns_to_save) >= 1000:

                    pattern_repository.bulk_insert(
                        patterns_to_save
                    )

                    patterns_to_save = []

                    print(
                        f"{symbol}: "
                        f"{inserted:,}"
                    )

            except Exception as e:

                skipped += 1

                print(
                    f"Skipped: {e}"
                )

        if patterns_to_save:

            pattern_repository.bulk_insert(
                patterns_to_save
            )

        return {

            "symbol": symbol,

            "inserted": inserted,

            "skipped": skipped,

            "candles": len(candles),
        }