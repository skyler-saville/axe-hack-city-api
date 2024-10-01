import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.append(str(Path(__file__).resolve().parent))

from fastapi import FastAPI

app = FastAPI()

# Importing routers
from .routers.authentication_router import router as authentication_router
from .routers.building_router import router as building_router
from .routers.character_router import router as character_router
from .routers.crafting_router import router as crafting_router
from .routers.event_router import router as event_router
from .routers.faction_router import router as faction_router
from .routers.floor_layout_router import router as floor_layout_router
from .routers.floor_router import router as floor_router
from .routers.game_session_router import router as game_session_router
from .routers.inventory_router import router as inventory_router
from .routers.item_router import router as item_router
from .routers.location_router import router as location_router
from .routers.mission_router import router as mission_router
from .routers.npc_router import router as npc_router
from .routers.progression_router import router as progression_router
from .routers.skill_router import router as skill_router
from .routers.user_router import router as user_router

# Including routers with prefixes and tags
app.include_router(game_session_router, prefix="/api/sessions", tags=["game sessions"])
app.include_router(authentication_router, prefix="/api/auth", tags=["authentication"])
app.include_router(user_router, prefix="/api/users", tags=["users"])
app.include_router(inventory_router, prefix="/api/inventories", tags=["inventories"])
app.include_router(item_router, prefix="/api/items", tags=["items"])
app.include_router(location_router, prefix="/api/locations", tags=["locations"])
app.include_router(mission_router, prefix="/api/missions", tags=["missions"])
app.include_router(npc_router, prefix="/api/npcs", tags=["npcs"])
app.include_router(
    progression_router, prefix="/api/progressions", tags=["progressions"]
)
app.include_router(skill_router, prefix="/api/skills", tags=["skills"])
app.include_router(building_router, prefix="/api/buildings", tags=["buildings"])
app.include_router(character_router, prefix="/api/characters", tags=["characters"])
app.include_router(crafting_router, prefix="/api/crafting", tags=["crafting"])
app.include_router(event_router, prefix="/api/events", tags=["events"])
app.include_router(faction_router, prefix="/api/factions", tags=["factions"])
app.include_router(
    floor_layout_router, prefix="/api/floor-layouts", tags=["floor layouts"]
)
app.include_router(floor_router, prefix="/api/floors", tags=["floors"])

# Run the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
