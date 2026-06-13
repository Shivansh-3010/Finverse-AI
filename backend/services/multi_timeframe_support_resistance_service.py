from constants.timeframes import (
    SUPPORTED_TIMEFRAMES,
)

from services.support_resistance_service import (
    SupportResistanceService,
)

from schemas.multi_timeframe_support_resistance import (
    MultiTimeframeSupportResistanceResponse,
    TimeframeSupportResistance,
)


class MultiTimeframeSupportResistanceService:

    @staticmethod
    def analyze(
        symbol: str,
    ):

        levels = []

        for timeframe in SUPPORTED_TIMEFRAMES:

            try:

                result = (
                    SupportResistanceService
                    .analyze(
                        symbol=symbol,
                        timeframe=timeframe,
                    )
                )

                levels.append(
                    TimeframeSupportResistance(
                        timeframe=timeframe,
                        nearest_support=
                            result.get(
                                "nearest_support"
                            ),
                        nearest_resistance=
                            result.get(
                                "nearest_resistance"
                            ),
                        signal=
                            result.get(
                                "signal"
                            ),
                    )
                )

            except Exception:

                levels.append(
                    TimeframeSupportResistance(
                        timeframe=timeframe,
                    )
                )

        return (
            MultiTimeframeSupportResistanceResponse(
                levels=levels
            )
        )