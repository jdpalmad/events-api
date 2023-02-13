from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import date

class Event(BaseModel):
    id: int = Field(default=None, hidden=True)
    nombre: str = Field(max_length=50)
    tipo: Literal["conferencia", "reunion", "taller", "capacitacion", "seminario", "concierto", 
        "evento deportivo", "feria", "concurso", "mitin politico", "encuentro religioso"]
    status: Literal["pendiente", "revisado"]
    fecha: date
    descripcion: Optional[str] = Field(default=None, max_length=255)

    @validator("tipo")
    def tipo_validator(cls, v):
        if v not in ["conferencia", "reunion", "taller", "capacitacion", "seminario", "concierto", 
        "evento deportivo", "feria", "concurso", "mitin politico", "encuentro religioso"]:
            raise ValueError("Tipo no válido")
        return v

    @validator("fecha")
    def fecha_validator(cls, v):
        if v < date.today():
            raise ValueError("Fecha no válida")
        return v

    @validator("status")
    def status_validator(cls, v):
        if v not in ["pendiente", "revisado"]:
            raise ValueError("Status no válido")
        return v 

class configEvent(BaseModel):
    id: int 
    event_id: int
    nombre: str = Field(max_length=50)
    active: bool = Field(default=True, hidden=True)

class gestionEvent(BaseModel):
    id: int 
    event_id: int
    nombre: str = Field(max_length=50)
    tipo: Literal["conferencia", "reunion", "taller", "capacitacion", "seminario", "concierto", 
        "evento deportivo", "feria", "concurso", "mitin politico", "encuentro religioso"]
    requiere_gestion: bool = Field(default=True, hidden=True)
