# models/item_model.py
from enum import Enum as PyEnum
from typing import Dict, List

from sqlalchemy import ARRAY, Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class ItemType(str, PyEnum):
    """Enumeration of possible item types."""

    weapon = "weapon"
    armor = "armor"
    consumable = "consumable"
    material = "material"
    tool = "tool"


class Item(Base):
    """Represents an item in the game.

    Attributes:
        id (int): Unique identifier for the item.
        name (str): Name of the item.
        type (ItemType): Type of the item.
        value (int): Value of the item.
        weight (float): Weight of the item.
        description (str): Description of the item.
        rarity (str): Rarity of the item.
        durability (int): Durability of the item.
        damage (int): Damage value for weapons.
        defense (int): Defense value for armor.
        effects (list[Dict[str, int]]): Effects applied by the item.
    """

    __tablename__ = "items"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    type: ItemType = Column(Enum(ItemType))
    value: int = Column(Integer)
    weight: float = Column(Float)
    description: str = Column(String)
    rarity: str = Column(String)
    durability: int = Column(Integer)
    damage: int = Column(Integer)
    defense: int = Column(Integer)
    effects: List[Dict[str, int]] = Column(ARRAY(Dict[str, int]))

    inventory_id: int = Column(Integer, ForeignKey("inventories.id"))
    crafting_recipes = relationship("CraftingRecipe", back_populates="ingredients")
    floor_id: int = Column(Integer, ForeignKey("floors.id"))
