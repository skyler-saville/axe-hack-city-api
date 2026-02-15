from enum import Enum as PyEnum

from sqlalchemy import ARRAY, Column, Enum, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from .base import (
    Base,
    crafting_recipe_ingredient_association,
    mission_reward_association,
)


class ItemType(str, PyEnum):
    weapon = "weapon"
    armor = "armor"
    consumable = "consumable"
    material = "material"
    tool = "tool"


class Item(Base):
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
    effects: list[dict] = Column(JSON)

    inventory_id: int = Column(Integer, ForeignKey("inventories.id"))
    floor_id: int = Column(Integer, ForeignKey("floors.id"))
    building_id: int = Column(Integer, ForeignKey("buildings.id"))

    inventory = relationship("Inventory", back_populates="items")
    floor = relationship("Floor", back_populates="loot")
    building = relationship("Building", back_populates="loot")
    crafting_recipes = relationship(
        "CraftingRecipe",
        secondary=crafting_recipe_ingredient_association,
        back_populates="ingredients",
    )
    missions = relationship(
        "Mission",
        secondary=mission_reward_association,
        back_populates="rewards",
    )
    crafted_by_recipes = relationship("CraftingRecipe", back_populates="output")
