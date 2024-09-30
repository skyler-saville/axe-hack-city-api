# database/sqlalchemy_repository.py
from typing import Type, TypeVar, Generic, List
from sqlalchemy.orm import Session
from sqlalchemy import select

# Define a generic type T for your SQLAlchemy models
T = TypeVar('T')

class SQLAlchemyRepository(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def create(self, entity: T) -> T:
        """Creates a new record in the database."""
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def get(self, entity_id: int) -> T:
        """Fetches a record by its ID."""
        return self.session.get(self.model, entity_id)

    def update(self, entity: T) -> T:
        """Updates an existing record."""
        self.session.merge(entity)
        self.session.commit()
        return entity

    def delete(self, entity_id: int) -> None:
        """Deletes a record by its ID."""
        entity = self.get(entity_id)
        if entity:
            self.session.delete(entity)
            self.session.commit()

    def list(self, **filters) -> List[T]:
        """Fetches a list of records with optional filters."""
        query = self.session.execute(select(self.model).filter_by(**filters))
        return query.scalars().all()
