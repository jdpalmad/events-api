from fastapi import APIRouter, HTTPException
from config.db import conn
from models.event import events
from models.cfg import config
from schemas.event import Event
from utilities.cfg import *

# Creamos el router para gestion
cfg = APIRouter()

@cfg.delete("/events/{id}", response_model = Event, description="Soft delete un evento", tags=["config"])
def soft_delete_event_by_id(id:int):
    # Vea si el evento existe en la tabla de eventos, si no, lance una excepción, si existe, evalue la funcion 
    # soft_delete_event y devuelva el evento correspondiente a la ID si el evento puede ser borrado
    event = conn.execute(config.select().where(config.c.event_id == id)).mappings().first()
    if event:
        soft_delete_event(id, event['active'])
        # Borra el evento si este no fue previamente borrado 
        # vea mas en utilities/cfg.py
        result = conn.execute(events.select().where(events.c.id == id)).mappings().first()
        return result
    else:
        # Si el evento no existe, lance una excepción
        raise HTTPException(status_code=404, detail="El evento no existe")
        
@cfg.get("/events/recover/{id}", response_model=Event, description="""Recupere un elemento previamente 
soft deleted""", tags=["config"])
def recover_event_by_id(id:int):
    # Vea si el evento existe, si no, lance una excepción, si existe, evalue la funcion recover_event
    # y devuelva el evento correspondiente a la ID si el evento puede ser recuperado
    event = conn.execute(config.select().where(config.c.event_id == id)).mappings().first()
    if event:
        # Recupera el evento si este no fue previamente recuperado
        # vea mas en utilities/cfg.py
        recover_event(id, event['active'])
        result = conn.execute(events.select().where(events.c.id == id)).mappings().first()
        return result
    else:
        # Si el evento no existe, lance una excepción
        raise HTTPException(status_code=404, detail="El evento no existe")




# Vea el archivo utilities/cfg.py para ver como se implementan las funciones asi para ver como se espera 
# mejorar el codigo a futuro

    