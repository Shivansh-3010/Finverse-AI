from repositories.portfolio_repository import (
    portfolio_repository,
)


class PortfolioService:

    @staticmethod
    def create(
        db,
        user_id,
        name,
        total_value=0,
    ):
        portfolio = portfolio_repository.model(
            user_id=user_id,
            name=name,
            total_value=total_value,
        )

        return portfolio_repository.create(
            db,
            portfolio,
        )

    @staticmethod
    def get_by_user(
        db,
        user_id,
    ):
        return portfolio_repository.get_by_user(
            db,
            user_id,
        )


portfolio_service = PortfolioService()