from repositories.holding_repository import (
    holding_repository,
)


class HoldingService:

    @staticmethod
    def create(
        db,
        portfolio_id,
        symbol,
        quantity,
        avg_price,
        current_price,
        market_value,
    ):
        holding = holding_repository.model(
            portfolio_id=portfolio_id,
            symbol=symbol,
            quantity=quantity,
            avg_price=avg_price,
            current_price=current_price,
            market_value=market_value,
        )

        return holding_repository.create(
            db,
            holding,
        )

    @staticmethod
    def get_by_portfolio(
        db,
        portfolio_id,
    ):
        return holding_repository.get_by_portfolio(
            db,
            portfolio_id,
        )


holding_service = HoldingService()