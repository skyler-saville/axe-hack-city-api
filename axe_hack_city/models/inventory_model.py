from sqlalchemy import Column, Float, Integer
from sqlalchemy.orm import relationship

from .base import Base


class Inventory(Base):
    __tablename__ = "inventories"

    id: int = Column(Integer, primary_key=True, index=True)
    max_capacity: int = Column(Integer)
    current_weight: float = Column(Float)

    items = relationship("Item", back_populates="inventory")
    characters = relationship("Character", back_populates="inventory")

    def add_item(self, item: "Item") -> None:
        if self.current_weight + item.weight <= self.max_capacity:
            self.items.append(item)
            self.current_weight += item.weight

    def remove_item(self, item: "Item") -> None:
        if item in self.items:
            self.items.remove(item)
            self.current_weight -= item.weight
