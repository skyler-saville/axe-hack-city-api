# schemas/mission_schema.py
from typing import List, Optional
from sqlmodel import SQLModel, Field
from pydantic import model_validator

class MissionSchema(SQLModel, table=True):
    """Schema for representing a mission."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    objectives: List[str] = Field(default=[])
    reward_ids: List[int] = Field(default=[])
    giver_id: int
    status: str

class MissionCreateSchema(SQLModel):
    """Schema for creating a new mission."""
    
    name: str
    description: str
    objectives: List[str]
    reward_ids: List[int]
    giver_id: int
    status: str

    @model_validator(mode='after')
    def validate_mission(cls, values: dict) -> dict:
        """Validate mission properties."""
        
        name = values.get('name')
        objectives = values.get('objectives')
        status = values.get('status')

        if name is None or len(name.strip()) == 0:
            raise ValueError('Mission name must not be empty.')
        if objectives is not None and len(objectives) == 0:
            raise ValueError('At least one objective must be specified.')
        if status is not None and status not in ['active', 'completed', 'failed']:
            raise ValueError('Status must be one of: active, completed, failed.')

        return values

class MissionUpdateSchema(SQLModel):
    """Schema for updating an existing mission."""
    
    name: Optional[str] = None
    description: Optional[str] = None
    objectives: Optional[List[str]] = None
    reward_ids: Optional[List[int]] = None
    giver_id: Optional[int] = None
    status: Optional[str] = None

    @model_validator(mode='after')
    def validate_mission(cls, values: dict) -> dict:
        """Validate mission properties using the create schema's validation."""
        
        return MissionCreateSchema.validate_mission(values)

