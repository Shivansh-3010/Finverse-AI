from typing import Generic, TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    def get(self, db: Session, entity_id):
        return (
            db.query(self.model)
            .filter(self.model.id == entity_id)
            .first()
        )

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def create(self, db: Session, obj):
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, entity_id):
        obj = self.get(db, entity_id)

        if obj:
            db.delete(obj)
            db.commit()

        return obj