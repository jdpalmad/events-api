from pydantic import BaseModel, Field

# Clase para la tabla de configuración de eventos
# Esta clase es utilizada de manera oculta para trackear la actividad de los eventos,
# esto es trackear si el evento esta activo o no. i, e. Soft delete status.
# Se espera que esta clase requiera privilegios de administrador para ser utilizada.
# Esta clase nunca sera recibida como Payload y por ahora tampoco sera utilizada para
# la respuesta de las solicitudes, sin embargo, se espera que en el futuro se utilice.

class configEvent(BaseModel):
    id: int 
        # El ID se genera automaticamente y es unico
    event_id: int
        # El event_id es unico y es el identificador del evento al que pertenece
    nombre: str = Field(max_length=50)
        # El nombre se extrae de la tabla de eventos y es unico
    active: bool = Field(default=True, hidden=True)
        # Bool. Salvo que el evento sea Soft deleted, este campo siempre sera True.
