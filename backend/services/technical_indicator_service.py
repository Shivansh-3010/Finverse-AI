from database.session import SessionLocal

from repositories.technical_indicator_repository import (
    TechnicalIndicatorRepository,
)


class TechnicalIndicatorService:

    @staticmethod
    def get_latest(symbol: str):

        db = SessionLocal()

        try:
            repository = TechnicalIndicatorRepository(db)

            return repository.get_latest(symbol)

        finally:
            db.close()

    @staticmethod
    def get_history(symbol: str):

        db = SessionLocal()

        try:
            repository = TechnicalIndicatorRepository(db)

            return {
                "indicators": repository.get_history(symbol)
            }

        finally:
            db.close()