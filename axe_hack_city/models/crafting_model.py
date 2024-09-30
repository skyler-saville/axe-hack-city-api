from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CraftingRecipe(Base):
    """Represents a crafting recipe in the game.

    Attributes:
        id (int): Unique identifier for the recipe.
        name (str): Name of the crafting recipe.
        description (str): Description of the crafting recipe.
    """
    __tablename__ = 'crafting_recipes'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    description: str = Column(String)
    
    ingredients = relationship("Item", back_populates="crafting_recipes")
    output_id: int = Column(Integer, ForeignKey('items.id'))
    skill_required_id: int = Column(Integer, ForeignKey('skills.id'))

    output = relationship("Item", foreign_keys=[output_id])
    skill_required = relationship("Skill", foreign_keys=[skill_required_id])
