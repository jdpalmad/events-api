from pydantic import BaseModel, Field

class configEvent(BaseModel):
    id: int 
    event_id: int
    nombre: str = Field(max_length=50)
    active: bool = Field(default=True, hidden=True)
