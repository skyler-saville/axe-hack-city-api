from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base

Base = declarative_base()

building_street_association = Table(
    "building_street_association",
    Base.metadata,
    Column("building_id", Integer, ForeignKey("buildings.id"), primary_key=True),
    Column("street_id", Integer, ForeignKey("streets.id"), primary_key=True),
)

building_entrance_association = Table(
    "building_entrance_association",
    Base.metadata,
    Column("building_id", Integer, ForeignKey("buildings.id"), primary_key=True),
    Column("location_id", Integer, ForeignKey("locations.id"), primary_key=True),
)

location_connection_association = Table(
    "location_connection_association",
    Base.metadata,
    Column("from_location_id", Integer, ForeignKey("locations.id"), primary_key=True),
    Column("to_location_id", Integer, ForeignKey("locations.id"), primary_key=True),
)

event_participant_association = Table(
    "event_participant_association",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True),
    Column("character_id", Integer, ForeignKey("characters.id"), primary_key=True),
)

crafting_recipe_ingredient_association = Table(
    "crafting_recipe_ingredient_association",
    Base.metadata,
    Column("recipe_id", Integer, ForeignKey("crafting_recipes.id"), primary_key=True),
    Column("item_id", Integer, ForeignKey("items.id"), primary_key=True),
)

mission_reward_association = Table(
    "mission_reward_association",
    Base.metadata,
    Column("mission_id", Integer, ForeignKey("missions.id"), primary_key=True),
    Column("item_id", Integer, ForeignKey("items.id"), primary_key=True),
)

faction_alliance_association = Table(
    "faction_alliance_association",
    Base.metadata,
    Column("faction_id", Integer, ForeignKey("factions.id"), primary_key=True),
    Column("ally_id", Integer, ForeignKey("factions.id"), primary_key=True),
)
