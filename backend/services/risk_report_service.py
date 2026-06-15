from services.risk_analysis_service import (
    RiskAnalysisService,
)

from services.position_sizing_service import (
    PositionSizingService,
)

from services.stop_loss_service import (
    StopLossService,
)


class RiskReportService:

    @staticmethod
    def generate(
        symbol: str,
        timeframe: str,
        capital: float,
        risk_percent: float,
        entry_price: float,
        stop_loss_price: float,
        atr: float,
    ):

        risk_analysis = (
            RiskAnalysisService.analyze(
                symbol=symbol,
                timeframe=timeframe,
            )
        )

        position_size = (
            PositionSizingService.calculate(
                capital=capital,
                risk_percent=risk_percent,
                entry_price=entry_price,
                stop_loss_price=stop_loss_price,
            )
        )

        stop_loss = (
            StopLossService.calculate(
                entry_price=entry_price,
                atr=atr,
            )
        )

        return {
            "risk_analysis": risk_analysis,
            "position_size": position_size,
            "stop_loss": stop_loss,
        }