# controllers/event_controller.py
# controllers/events_controller.py
from typing import List

from sqlalchemy.orm import Session

from ..database.sqlalchemy_repository import SQLAlchemyRepository
from ..models.event_model import Event


class EventsController:
    """Controller for managing Event entities."""

    def __init__(self, session: Session):
        """Initialize the EventsController.

        Args:
            session (Session): SQLAlchemy session.
        """
        self.repository = SQLAlchemyRepository(session, Event)

    def create_event(self, event: Event) -> Event:
        """Create a new event.

        Args:
            event (Event): The event to create.

        Returns:
            Event: The created event.
        """
        return self.repository.create(event)

    def get_event(self, event_id: int) -> Event:
        """Retrieve an event by its ID.

        Args:
            event_id (int): The ID of the event.

        Returns:
            Event: The requested event.
        """
        return self.repository.get(event_id)

    def update_event(self, event: Event) -> Event:
        """Update an existing event.

        Args:
            event (Event): The event to update.

        Returns:
            Event: The updated event.
        """
        return self.repository.update(event)

    def delete_event(self, event_id: int) -> None:
        """Delete an event by its ID.

        Args:
            event_id (int): The ID of the event to delete.
        """
        self.repository.delete(event_id)

    def list_events(self, **filters) -> List[Event]:
        """List events with optional filters.

        Returns:
            List[Event]: A list of events.
        """
        return self.repository.list(**filters)
