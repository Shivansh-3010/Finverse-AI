
from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from models.portfolio import Portfolio
from models.portfolio_goal import PortfolioGoal


class PortfolioGoalCRUDService:
    """Persistence and validation for portfolio goals."""

    @staticmethod
    def _require_portfolio(db: Session, portfolio_id: UUID) -> Portfolio:
        portfolio = (
            db.query(Portfolio)
            .filter(Portfolio.id == portfolio_id)
            .first()
        )
        if portfolio is None:
            raise LookupError("Portfolio not found")
        return portfolio

    @staticmethod
    def _validate_target_date(target_date: date) -> None:
        if target_date <= date.today():
            raise ValueError("Target date must be in the future")

    @classmethod
    def create(
        cls, db: Session, portfolio_id: UUID, payload: dict
    ) -> PortfolioGoal:
        cls._require_portfolio(db, portfolio_id)
        cls._validate_target_date(payload["target_date"])

        goal = PortfolioGoal(portfolio_id=portfolio_id, **payload)
        db.add(goal)
        db.commit()
        db.refresh(goal)
        return goal

    @classmethod
    def list_for_portfolio(
        cls, db: Session, portfolio_id: UUID
    ) -> list[PortfolioGoal]:
        cls._require_portfolio(db, portfolio_id)
        return (
            db.query(PortfolioGoal)
            .filter(PortfolioGoal.portfolio_id == portfolio_id)
            .order_by(PortfolioGoal.target_date.asc())
            .all()
        )

    @staticmethod
    def get(
        db: Session, portfolio_id: UUID, goal_id: UUID
    ) -> PortfolioGoal | None:
        return (
            db.query(PortfolioGoal)
            .filter(
                PortfolioGoal.id == goal_id,
                PortfolioGoal.portfolio_id == portfolio_id,
            )
            .first()
        )

    @classmethod
    def update(
        cls,
        db: Session,
        portfolio_id: UUID,
        goal_id: UUID,
        changes: dict,
    ) -> PortfolioGoal | None:
        goal = cls.get(db, portfolio_id, goal_id)
        if goal is None:
            return None

        if "target_date" in changes:
            cls._validate_target_date(changes["target_date"])

        for field, value in changes.items():
            setattr(goal, field, value)

        db.commit()
        db.refresh(goal)
        return goal

    @classmethod
    def delete(
        cls, db: Session, portfolio_id: UUID, goal_id: UUID
    ) -> bool:
        goal = cls.get(db, portfolio_id, goal_id)
        if goal is None:
            return False

        db.delete(goal)
        db.commit()
        return True


portfolio_goal_crud_service = PortfolioGoalCRUDService()
