from fastapi import APIRouter, HTTPException
from config.db import conn
from models.event import events, config, gestion
from schemas.event import Event, gestionEvent
from utilities.event import *

event = APIRouter()

@event.get("/events", response_model=list[Event], description="""Obtener una lista de todos los eventos
    activos""", 
    tags=["events"])
def get_active_events(): 
    # Obtenemos la lista de todos los objetos activos  
    # realizando una union de las tablas de events y config
    return conn.execute(MostrarEventosActivos).mappings().all()

@event.post("/events", response_model=Event, description="Crear un nuevo evento", tags=["events"] )
def new_event(event:Event):
    # Vea si el evento existe, si existe, lanza una excepción, si no, crea el evento
    if conn.execute(events.select().where(events.c.nombre == event.nombre)).mappings().first():
        raise HTTPException(status_code=400, detail="El evento ya existe")
    else:
        return create_event(event)
    
@event.get("/events/all", response_model=list[Event], description="Obtener una lista de todos los eventos", 
    tags=["events"])
def get_all_events():
    # Obtenga una lista de todos los eventos
    return conn.execute(events.select()).mappings().all()

@event.get("/events/pendientes", response_model=list[Event], description="""Obtener una lista de todos los 
    eventos pendientes""", 
    tags=["events"])
def get_pending_events():
    # Obtenga una lista de todos los eventos activos a su vez pendientes
    return conn.execute(MostrarEventosPendientes).mappings().all()

@event.get("/events/revisados", response_model=list[Event], description="""Obtener una lista de todos los 
    eventos revisados""", 
    tags=["events"])
def get_reviewed_events():
    # Obtenga una lista de todos los eventos activos a su vez revisados
    return conn.execute(MostrarEventosRevisados).mappings().all()

@event.get("/events/gestion", response_model=list[gestionEvent], description="""Obtenga el estado de gestion
    de todos los eventos""", tags=["gestion"])
def get_gestion_events():
    # Obtenga una lista de todos los 
    # eventos activos y su estado de gestion
    return conn.execute(MostrarGestionActivos).mappings().all()
    
@event.get("/events/{id}", response_model=Event, description="Obtener un evento por ID", tags=["events"])
def get_event_by_id(id:int):
    #   Vea si el evento existe, si no, lance una excepción
    #  Si existe, devuelva el evento correspondiente a la ID
    event = conn.execute(events.select().where(events.c.id == id)).mappings().first()
    if event:
        return event
    else:
        raise HTTPException(status_code=404, detail="El evento no existe")

@event.put("/events/{id}", response_model=Event, description="Actualizar evento por ID", tags=["events"])
def update_event_by_id(id:int, event:Event):
    # Vea si el evento existe, si no, lance una excepción, si existe, 
    # evalue la funcion update_event para actualizarlo
    if not conn.execute(events.select().where(events.c.id == id)).mappings().first():
        raise HTTPException(status_code=404, detail="El evento no existe")
    else: 
        update_event(event, id)
        return conn.execute(events.select().where(events.c.id == id)).mappings().first()

@event.delete("/events/{id}", response_model = Event, description="Soft delete un evento", tags=["config"])
def soft_delete_event_by_id(id:int):
    # Vea si el evento existe en la tabla de eventos, si no, lance una excepción, si existe, evalue la funcion 
    # soft_delete_event y devuelva el evento correspondiente a la ID si el evento puede ser borrado
    event = conn.execute(config.select().where(config.c.event_id == id)).mappings().first()
    if event:
        soft_delete_event(id, event['active'])
        result = conn.execute(events.select().where(events.c.id == id)).mappings().first()
        return result
    else:
        raise HTTPException(status_code=404, detail="El evento no existe")
        
@event.get("/events/recover/{id}", response_model=Event, description="""Recupere un elemento previamente 
soft deleted""", tags=["config"])
def recover_event_by_id(id:int):
    # Vea si el evento existe, si no, lance una excepción, si existe, evalue la funcion recover_event
    # y devuelva el evento correspondiente a la ID si el evento puede ser recuperado
    event = conn.execute(config.select().where(config.c.event_id == id)).mappings().first()
    if event:
        recover_event(id, event['active'])
        result = conn.execute(events.select().where(events.c.id == id)).mappings().first()
        return result
    else:
        raise HTTPException(status_code=404, detail="El evento no existe")
    
@event.get("/events/gestion/{id}", response_model=gestionEvent, description="""Obtenga el estado de 
    gestion de un evento""", tags=["gestion"])   
def get_gestion_status_by_id(id:int):
    # Vea si el evento existe, si no, lance una excepción, si existe, evalue la funcion gestion_status
    # y devuelva el la columna 'requiere_gestion' correspondiente a la ID del evento en cuestion.
    event = conn.execute(events.select().where(events.c.id == id)).mappings().first()
    if event:
        gestion_status(id)
        return conn.execute(gestion.select().where(gestion.c.event_id == id)).mappings().first()
    else:
        raise HTTPException(status_code=404, detail="El evento no existe")

@event.get("/gestion/{clause}", response_model=list[Event], description="""Obtenga el estado de
    gestion de todos los eventos""", tags=["gestion"])
# check if the clause is boolean or not
def check_gestion(clause:bool):
    # Hace las correspondientes verificaciones para recuperar los eventos
    # activos en la tabla config que requieren gestion o no
    if clause == True:
        return conn.execute(MostrarEventosRequiereGestion).mappings().all()
    elif clause == False:
        return conn.execute(MostrarEventosNoRequiereGestion).mappings().all()
