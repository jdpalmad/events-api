from pydantic import BaseModel, Field, validator
from typing import  Literal

class gestionEvent(BaseModel):
    id: int 
    event_id: int
    nombre: str = Field(max_length=50)
    tipo: Literal["conferencia", "reunion", "taller", "capacitacion", "seminario", "concierto", 
        "evento deportivo", "feria", "concurso", "mitin politico", "encuentro religioso"]
    requiere_gestion: bool = Field(default=True, hidden=True)