from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import date

# Clase para la tabla de eventos 
# Los objetos de esta clase seran utilizados principalmente como payload de las solicitudes.

# Cabe resaltar que un evento sera Unico si y solo si su nombre y fecha son unicos
# Por lo que si se busca registrar dos eventos con el mismo nombre y fecha, se
# recomienda alterar el nombre de uno de ellos para evitar confusiones con un identificador

class Event(BaseModel):
    
    id: int = Field(default=None, hidden=True)
        # El ID es opcional porque se genera automáticamente, en general es recomendable no incluirlo en 
        # las solicitudes POST y GET salvo que sea claro que se requiere. i.e, @events/{id} 
    
    nombre: str = Field(max_length=50)
        # El nombre es obligatorio y no puede tener más de 50 caracteres
    
    tipo: Literal["conferencia", "reunion", "taller", "capacitacion", "seminario", "concierto", 
        "evento deportivo", "feria", "concurso", "mitin politico", "encuentro religioso"]
        # El tipo es obligatorio y debe ser uno de los valores de la lista indicada
    status: Literal["pendiente", "revisado"]
        # El status es obligatorio y debe ser uno de los valores de la ["pendiente", "revisado"], en adelante 
        # podria ser opcional e indicarse una logica aun mas interesante acerca de 
        # la revision de los eventos
    fecha: date
        # La fecha es obligatoria y debe ser una fecha valida y futura.
    descripcion: Optional[str] = Field(default=None, max_length=255)
        # La descripcion es opcional y no puede tener mas de 255 caracteres

    @validator("tipo")
    def tipo_validator(cls, v):
        # Este es un validador personalizado que se encarga de verificar que el tipo de evento
        if v not in ["conferencia", "reunion", "taller", "capacitacion", "seminario", "concierto", 
        "evento deportivo", "feria", "concurso", "mitin politico", "encuentro religioso"]:
            raise ValueError("Tipo no válido")
        return v

    @validator("fecha")
    def fecha_validator(cls, v):
        # Este es un validador personalizado que se encarga de verificar que la fecha sea futura y valida
        if v < date.today():
            raise ValueError("Fecha no válida")
        return v

    @validator("status")
    def status_validator(cls, v):
        # Este es un validador personalizado que se encarga de verificar que el status sea uno de los
        # valores permitidos
        if v not in ["pendiente", "revisado"]:
            raise ValueError("Status no válido")
        return v 

