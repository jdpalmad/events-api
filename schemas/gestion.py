from pydantic import BaseModel, Field, validator
from typing import  Literal

# Clase para la tabla de gestion de eventos
# Esta clase NO sera recibida como payload de las solicitudes, pero si sera utilizada para
# la respuesta de algunas.

# En esta tabla solo estan los elementos que estan activos
# y que ademas requieren gestion.

class gestionEvent(BaseModel):
    id: int 
        # ID de la tabla de gestion de eventos
    event_id: int
        # ID del evento al que pertenece en la tabla de eventos
    nombre: str = Field(max_length=50)
        # Nombre del evento especificado en la tabla de eventos
    tipo: Literal["conferencia", "reunion", "taller", "capacitacion", "seminario", "concierto", 
        "evento deportivo", "feria", "concurso", "mitin politico", "encuentro religioso"]
        # Tipo de evento especificado en la tabla de eventos, claramente en la lista contemplada
    requiere_gestion: bool = Field(default=True, hidden=True)
        # Bool. Si el evento requiere gestion o no. Por defecto es True.