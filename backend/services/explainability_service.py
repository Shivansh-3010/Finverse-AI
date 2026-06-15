from schemas.indicator_explanation import IndicatorExplanation


class ExplainabilityService:

    @staticmethod
    def explain_rsi(rsi: float) -> IndicatorExplanation:

        if rsi < 30:
            return IndicatorExplanation(
                indicator="RSI",
                value=rsi,
                signal="Bullish",
                reason="Oversold condition detected"
            )

        if rsi > 70:
            return IndicatorExplanation(
                indicator="RSI",
                value=rsi,
                signal="Bearish",
                reason="Overbought condition detected"
            )

        return IndicatorExplanation(
            indicator="RSI",
            value=rsi,
            signal="Neutral",
            reason="RSI is within normal range"
        )
        
    @staticmethod
    def get_technical_narrative(
        result: dict
    ):

        combined_score = (
            result["combined_score"]
        )

        if combined_score >= 80:

            return (
                "Technical indicators are strongly bullish. "
                f"The combined technical score is "
                f"{combined_score}."
            )

        if combined_score >= 60:

            return (
                "Technical indicators are moderately bullish. "
                f"The combined technical score is "
                f"{combined_score}."
            )

        if combined_score >= 40:

            return (
                "Technical indicators are mixed and "
                "lack strong directional conviction. "
                f"The combined technical score is "
                f"{combined_score}."
            )

        return (
            "Technical indicators remain weak and "
            "bearish overall. "
            f"The combined technical score is "
            f"{combined_score}."
        )

    @staticmethod
    def get_news_narrative(
        result: dict
    ):

        recent = (
            result[
                "recent_news_average"
            ]
        )

        latest = (
            result[
                "latest_news_score"
            ]
        )

        news_score = (
            result[
                "news_intelligence_score"
            ]
        )

        if recent >= 70 and latest >= 70:

            return (
                "News sentiment remains strongly positive. "
                "Both recent and latest news coverage "
                "support a bullish outlook. "
                f"The news intelligence score is "
                f"{news_score}."
            )

        if recent >= 70 and latest < 50:

            return (
                "Recent news sentiment remains positive, "
                "but the latest developments introduce "
                "potential caution for investors. "
                f"The news intelligence score is "
                f"{news_score}."
            )

        if recent < 50 and latest >= 70:

            return (
                "News sentiment is improving after a "
                "period of weakness. Recent developments "
                "suggest a potential positive turnaround. "
                f"The news intelligence score is "
                f"{news_score}."
            )

        if recent < 50 and latest < 50:

            return (
                "News sentiment remains negative across "
                "both recent and latest coverage. "
                f"The news intelligence score is "
                f"{news_score}."
            )

        return (
            "News sentiment is mixed with no clear "
            "dominant direction. "
            f"The news intelligence score is "
            f"{news_score}."
        )

    @staticmethod
    def get_event_narrative(
        result: dict
    ):

        events = result.get(
            "latest_events",
            []
        )

        adjustment = result.get(
            "event_adjustment",
            0
        )

        if not events:

            return (
                "No major market-moving event "
                "was detected in recent news."
            )

        event_names = ", ".join(
            events
        )

        if adjustment > 0:

            return (
                f"Recent events ({event_names}) "
                "act as positive catalysts for the stock. "
                f"The total event impact score is "
                f"{adjustment}."
            )

        if adjustment < 0:

            return (
                f"Recent events ({event_names}) "
                "introduce additional risk and "
                "uncertainty. "
                f"The total event impact score is "
                f"{adjustment}."
            )

        return (
            f"Recent events ({event_names}) "
            "have a neutral overall impact."
        )

    @staticmethod
    def get_recommendation_narrative(
        result: dict
    ):

        recommendation = result[
            "recommendation"
        ]

        final_score = result[
            "final_score"
        ]

        if recommendation == "BUY":

            return (
                "The combined evidence from technical "
                "analysis, candlestick patterns, and "
                "news intelligence supports a BUY "
                f"recommendation with a final score of "
                f"{final_score}."
            )

        if recommendation == "HOLD":

            return (
                "The stock shows promising signals, "
                "but confirmation remains insufficient "
                "for a strong bullish conviction. "
                f"The system therefore maintains a HOLD "
                f"recommendation with a final score of "
                f"{final_score}."
            )

        return (
            "The overall risk-reward profile remains "
            "unfavorable. Technical and/or news signals "
            "do not currently support a bullish outlook. "
            f"The system issues a SELL recommendation "
            f"with a final score of "
            f"{final_score}."
        )
        
    @staticmethod
    def explain_recommendation(
        result: dict
    ):

        sections = [

            ExplainabilityService
            .get_technical_narrative(
                result
            ),

            ExplainabilityService
            .get_news_narrative(
                result
            ),

            ExplainabilityService
            .get_event_narrative(
                result
            ),

            ExplainabilityService
            .get_recommendation_narrative(
                result
            ),
        ]

        return "\n\n".join(
            sections
        )
            
        