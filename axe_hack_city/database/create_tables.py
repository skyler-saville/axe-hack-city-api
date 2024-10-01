import json
import sqlite3


def create_building_table(cursor: sqlite3.Cursor):
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Building (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL, -- Enum LocationType
        description TEXT,
        coordinates TEXT, -- JSON string (tuple of floats)
        connected_locations TEXT -- JSON string (list of Location IDs)
    );
    """
    )


def create_floor_table(cursor: sqlite3.Cursor):
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Floor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number INTEGER NOT NULL,
        layout TEXT, -- JSON string (FloorLayout)
        building_id INTEGER NOT NULL, -- Foreign key to Building
        FOREIGN KEY (building_id) REFERENCES Building(id)
    );
    """
    )


def create_item_table(cursor: sqlite3.Cursor):
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Item (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL, -- Enum ItemType
        value INTEGER NOT NULL,
        weight REAL NOT NULL,
        description TEXT,
        rarity TEXT,
        durability INTEGER NOT NULL,
        damage INTEGER NOT NULL,
        defense INTEGER NOT NULL,
        effects TEXT -- JSON string (dict of effects)
    );
    """
    )


def create_npc_table(cursor: sqlite3.Cursor):
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS NPC (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        health INTEGER NOT NULL,
        skill_tree TEXT, -- Enum SkillType
        items TEXT, -- JSON string (list of item IDs)
        dialogue TEXT,
        faction TEXT, -- Foreign key to Faction (by name)
        aggression_level TEXT, -- Enum AggressionLevel
        relationship TEXT -- Enum Relationship
    );
    """
    )


def create_character_table(cursor: sqlite3.Cursor):
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Character (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        health INTEGER NOT NULL,
        xp INTEGER NOT NULL,
        clan_name TEXT NOT NULL,
        clan_members TEXT, -- JSON string (list of character IDs)
        skill_tree TEXT, -- Enum SkillType
        inventory_id INTEGER, -- Foreign key to Inventory
        FOREIGN KEY (inventory_id) REFERENCES Inventory(id)
    );
    """
    )


def create_inventory_table(cursor: sqlite3.Cursor):
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        items TEXT, -- JSON string (list of item IDs)
        max_capacity INTEGER NOT NULL,
        current_weight REAL NOT NULL
    );
    """
    )


def create_crafting_table(cursor: sqlite3.Cursor):
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS CraftingRecipe (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        ingredients TEXT, -- JSON string (list of item IDs)
        output_id INTEGER, -- Foreign key to Item (output)
        skill_required TEXT, -- Foreign key to Skill (name)
        FOREIGN KEY (output_id) REFERENCES Item(id)
    );
    """
    )


def create_event_table(cursor: sqlite3.Cursor):
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Event (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        location_id INTEGER, -- Foreign key to Location
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        participants TEXT, -- JSON string (list of character IDs)
        FOREIGN KEY (location_id) REFERENCES Location(id)
    );
    """
    )


def create_faction_table(cursor: sqlite3.Cursor):
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Faction (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        reputation INTEGER NOT NULL,
        allies TEXT, -- JSON string (list of faction IDs)
        enemies TEXT, -- JSON string (list of faction IDs)
        npcs TEXT -- JSON string (list of NPC IDs)
    );
    """
    )


def create_floor_layout_table(cursor: sqlite3.Cursor):
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS FloorLayout (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        walls TEXT, -- JSON string (list of Wall tuples)
        doors TEXT -- JSON string (list of Door objects)
    );
    """
    )


def create_location_table(cursor: sqlite3.Cursor):
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Location (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL, -- Enum LocationType
        description TEXT,
        coordinates TEXT, -- JSON string (tuple of floats)
        connected_locations TEXT -- JSON string (list of Location IDs)
    );
    """
    )


def create_mission_table(cursor: sqlite3.Cursor):
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Mission (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        objectives TEXT, -- JSON string (list of objectives)
        rewards TEXT, -- JSON string (list of item IDs)
        giver_id INTEGER, -- Foreign key to NPC
        status TEXT NOT NULL, -- Enum MissionStatus
        FOREIGN KEY (giver_id) REFERENCES NPC(id)
    );
    """
    )


def create_progression_table(cursor: sqlite3.Cursor):
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS PlayerProgression (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        character_id INTEGER NOT NULL, -- Foreign key to Character
        missions_completed TEXT, -- JSON string (list of mission IDs)
        faction_reputations TEXT, -- JSON string (dict of faction reputations)
        achievements TEXT, -- JSON string (list of achievements)
        FOREIGN KEY (character_id) REFERENCES Character(id)
    );
    """
    )


def create_skill_table(cursor: sqlite3.Cursor):
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Skill (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL, -- Enum SkillType
        level INTEGER NOT NULL,
        description TEXT,
        prerequisites TEXT, -- JSON string (list of prerequisite skill names)
        effects TEXT -- JSON string (dict of effects)
    );
    """
    )


def create_user_table(cursor: sqlite3.Cursor):
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        timezone TEXT NOT NULL,
        character_ids TEXT -- JSON string (list of character IDs)
    );
    """
    )


def create_street_table(cursor: sqlite3.Cursor):
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Street (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL, -- Enum LocationType
        description TEXT,
        coordinates TEXT, -- JSON string (tuple of floats)
        connected_locations TEXT, -- JSON string (list of Location IDs)
        width REAL NOT NULL,
        length REAL NOT NULL,
        traffic INTEGER NOT NULL
    );
    """
    )


def create_tables(connection: sqlite3.Connection):
    cursor = connection.cursor()
    create_building_table(cursor)
    create_floor_table(cursor)
    create_item_table(cursor)
    create_npc_table(cursor)
    create_character_table(cursor)
    create_inventory_table(cursor)
    create_crafting_table(cursor)
    create_event_table(cursor)
    create_faction_table(cursor)
    create_floor_layout_table(cursor)
    create_location_table(cursor)
    create_mission_table(cursor)
    create_progression_table(cursor)
    create_skill_table(cursor)
    create_user_table(cursor)
    create_street_table(cursor)
    connection.commit()
