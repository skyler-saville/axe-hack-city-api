from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base, crafting_recipe_ingredient_association


class CraftingRecipe(Base):
    __tablename__ = "crafting_recipes"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    description: str = Column(String)

    output_id: int = Column(Integer, ForeignKey("items.id"))
    skill_required_id: int = Column(Integer, ForeignKey("skills.id"))

    ingredients = relationship(
        "Item",
        secondary=crafting_recipe_ingredient_association,
        back_populates="crafting_recipes",
    )
    output = relationship("Item", foreign_keys=[output_id], back_populates="crafted_by_recipes")
    skill_required = relationship("Skill", foreign_keys=[skill_required_id])
