from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

router = APIRouter()

# In-memory storage for demonstration purposes
fake_users_db: Dict[int, Dict[str, Any]] = {}
user_id_counter = 1

@router.post("/", response_model=Dict[str, Any])
def create_user(user: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new user.

    Args:
        user: A dictionary containing user details.

    Returns:
        The created user instance with an ID.

    Raises:
        HTTPException: If the username already exists.
    """
    global user_id_counter
    for existing_user in fake_users_db.values():
        if existing_user['username'] == user['username']:
            raise HTTPException(status_code=400, detail="Username already exists")
    
    user_id = user_id_counter
    fake_users_db[user_id] = {**user, "id": user_id}
    user_id_counter += 1
    return fake_users_db[user_id]

@router.get("/{user_id}", response_model=Dict[str, Any])
def read_user(user_id: int) -> Dict[str, Any]:
    """Retrieve a user by their ID.

    Args:
        user_id: The ID of the user to retrieve.

    Returns:
        The user instance.

    Raises:
        HTTPException: If the user is not found.
    """
    user = fake_users_db.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=Dict[str, Any])
def update_user(user_id: int, user: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing user.

    Args:
        user_id: The ID of the user to update.
        user: A dictionary containing updated user details.

    Returns:
        The updated user instance.

    Raises:
        HTTPException: If the user is not found.
    """
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")

    fake_users_db[user_id].update(user)
    return fake_users_db[user_id]

@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int) -> Dict[str, str]:
    """Delete a user by their ID.

    Args:
        user_id: The ID of the user to delete.

    Returns:
        A confirmation message.

    Raises:
        HTTPException: If the user is not found.
    """
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    del fake_users_db[user_id]
    return {"detail": "User deleted successfully"}

@router.get("/", response_model=List[Dict[str, Any]])
def list_users() -> List[Dict[str, Any]]:
    """List all users.

    Returns:
        A list of user instances.
    """
    return list(fake_users_db.values())
