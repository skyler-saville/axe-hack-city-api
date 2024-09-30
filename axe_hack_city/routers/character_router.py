from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()

@router.post("/", response_model=Dict[str, Any])
def create_character(character: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new character.

    Args:
        character: The character data.

    Returns:
        A message confirming the character creation along with the character data.
    """
    return {"message": "Character created", "data": character}

@router.get("/{character_id}", response_model=Dict[str, Any])
def get_character(character_id: int) -> Dict[str, Any]:
    """Retrieve a character by ID.

    Args:
        character_id: The ID of the character.

    Returns:
        A message confirming the character retrieval along with the character ID.
    """
    return {"message": "Character retrieved", "character_id": character_id}

@router.put("/{character_id}", response_model=Dict[str, Any])
def update_character(character_id: int, character: Dict[str, Any]) -> Dict[str, Any]:
    """Update a character by ID.

    Args:
        character_id: The ID of the character to update.
        character: The updated character data.

    Returns:
        A message confirming the character update along with the character data.
    """
    return {"message": "Character updated", "character_id": character_id, "data": character}

@router.delete("/{character_id}", response_model=Dict[str, Any])
def delete_character(character_id: int) -> Dict[str, Any]:
    """Delete a character by ID.

    Args:
        character_id: The ID of the character to delete.

    Returns:
        A message confirming the successful deletion of the character.
    """
    return {"message": "Character deleted successfully", "character_id": character_id}

@router.get("/", response_model=List[Dict[str, Any]])
def list_characters() -> List[Dict[str, Any]]:
    """List all characters.

    Returns:
        A list of characters with their IDs and names.
    """
    return [{"character_id": 1, "name": "Character A"}, {"character_id": 2, "name": "Character B"}]
