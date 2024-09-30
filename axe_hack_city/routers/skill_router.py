from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()

@router.post("/", response_model=Dict[str, Any])
def create_skill(skill: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new skill.

    Args:
        skill: A dictionary containing skill details.

    Returns:
        A dictionary with the created skill's ID and name.
    """
    return {"id": 1, "name": skill.get("name")}

@router.get("/{skill_id}", response_model=Dict[str, Any])
def get_skill(skill_id: int) -> Dict[str, Any]:
    """Retrieve a skill by its ID.

    Args:
        skill_id: The ID of the skill to retrieve.

    Returns:
        A dictionary with the skill's ID and name.
    """
    return {"id": skill_id, "name": "Sample Skill"}

@router.put("/{skill_id}", response_model=Dict[str, Any])
def update_skill(skill_id: int, skill: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing skill.

    Args:
        skill_id: The ID of the skill to update.
        skill: A dictionary containing the updated skill details.

    Returns:
        A dictionary with the updated skill's ID and name.
    """
    return {"id": skill_id, "name": skill.get("name")}

@router.delete("/{skill_id}", response_model=Dict[str, str])
def delete_skill(skill_id: int) -> Dict[str, str]:
    """Delete a skill by its ID.

    Args:
        skill_id: The ID of the skill to delete.

    Returns:
        A confirmation message.
    """
    return {"detail": "Skill deleted successfully"}

@router.get("/", response_model=List[Dict[str, Any]])
def list_skills() -> List[Dict[str, Any]]:
    """List all skills.

    Returns:
        A list of dictionaries, each containing a skill's ID and name.
    """
    return [
        {"id": 1, "name": "Sample Skill 1"},
        {"id": 2, "name": "Sample Skill 2"}
    ]
