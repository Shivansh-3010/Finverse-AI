from schemas.candlestick_explanation import (
    CandlestickExplanation,
)

from technical.candlestick.pattern_explainer import (
    explain_pattern,
)


class CandlestickExplainabilityService:

    BULLISH_PATTERNS = {

        "Hammer",
        "Inverted Hammer",
        "Dragonfly Doji",
        "Takuri Line",
        "Long Lower Shadow",
        "Bullish Belt Hold",
        "Paper Umbrella",
        "Shaven Bottom",
        "Bullish Opening Marubozu",
        "Bullish Closing Marubozu",

        "Bullish Engulfing",
        "Bullish Harami",
        "Piercing Line",
        "Tweezer Bottom",
        "Matching Low",
        "Bullish Kicker",
        "Bullish Meeting Lines",
        "Bullish Separating Lines",
        "Bullish Counterattack",
        "Homing Pigeon",
        "Kicking Bullish",
        "Kicking By Length Bullish",

        "Morning Star",
        "Morning Doji Star",
        "Three White Soldiers",
        "Three Inside Up",
        "Three Outside Up",
        "Tri Star Bullish",
        "Three Stars In The South",
        "Three River Bottom",
        "Bullish Doji Star",

        "Rising Three Methods",
        "Bullish Abandoned Baby",
        "Bullish Tasuki Gap",
        "Bullish Window",
        "Stick Sandwich",
        "Bullish Mat Hold",
        "Bullish Breakaway",
        "Side By Side White Lines",
        "Ladder Bottom",
        "Concealing Baby Swallow",
        "Unique Three River",
        "Gap Three Methods Bullish",
        "Three Line Strike",
        "Three Gap Downs",
        "Gapping Side By Side White Lines",
    }

    BEARISH_PATTERNS = {

        "Shooting Star",
        "Hanging Man",
        "Gravestone Doji",
        "Long Upper Shadow",
        "Bearish Belt Hold",
        "Shaven Head",
        "Bearish Opening Marubozu",
        "Bearish Closing Marubozu",

        "Bearish Engulfing",
        "Bearish Harami",
        "Dark Cloud Cover",
        "Tweezer Top",
        "Matching High",
        "Bearish Kicker",
        "Bearish Meeting Lines",
        "Bearish Separating Lines",
        "Bearish Counterattack",
        "On Neck Pattern",
        "In Neck Pattern",
        "Thrusting Pattern",
        "Kicking Bearish",
        "Kicking By Length Bearish",

        "Evening Star",
        "Evening Doji Star",
        "Three Black Crows",
        "Three Inside Down",
        "Three Outside Down",
        "Tri Star Bearish",
        "Advance Block",
        "Deliberation",
        "Identical Three Crows",
        "Three River Top",
        "Bearish Doji Star",

        "Falling Three Methods",
        "Bearish Abandoned Baby",
        "Bearish Tasuki Gap",
        "Bearish Window",
        "Upside Gap Two Crows",
        "Bearish Mat Hold",
        "Bearish Breakaway",
        "Matching Three Crows",
        "Gap Three Methods Bearish",
        "Three Gap Ups",
    }

    @staticmethod
    def explain(
        pattern: str,
    ) -> CandlestickExplanation:

        if (
            pattern
            in CandlestickExplainabilityService
            .BULLISH_PATTERNS
        ):
            signal = "Bullish"

        elif (
            pattern
            in CandlestickExplainabilityService
            .BEARISH_PATTERNS
        ):
            signal = "Bearish"

        else:
            signal = "Neutral"

        return CandlestickExplanation(
            pattern=pattern,
            signal=signal,
            reason=explain_pattern(
                pattern
            ),
        )