from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .item_model import Item

Base = declarative_base()

class Inventory(Base):
    """Represents an inventory for a character.

    Attributes:
        id (int): Unique identifier for the inventory.
        max_capacity (int): Maximum capacity of the inventory.
        current_weight (float): Current weight of items in the inventory.
    """
    __tablename__ = 'inventories'

    id: int = Column(Integer, primary_key=True, index=True)
    max_capacity: int = Column(Integer)
    current_weight: float = Column(Float)

    items = relationship("Item", back_populates="inventory")

    def add_item(self, item: 'Item') -> None:
        """Adds an item to the inventory.

        Args:
            item (Item): The item to add.
        """
        if self.current_weight + item.weight <= self.max_capacity:
            self.items.append(item)
            self.current_weight += item.weight
        else:
            # Handle inventory full scenario
            pass

    def remove_item(self, item: 'Item') -> None:
        """Removes an item from the inventory.

        Args:
            item (Item): The item to remove.
        """
        if item in self.items:
            self.items.remove(item)
            self.current_weight -= item.weight
