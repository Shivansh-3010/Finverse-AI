from constants.timeframes import (
    SUPPORTED_TIMEFRAMES,
)


def validate_timeframe(
    timeframe: str
):

    if timeframe not in SUPPORTED_TIMEFRAMES:

        raise ValueError(
            f"Unsupported timeframe: {timeframe}"
        )