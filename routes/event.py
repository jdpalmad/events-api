from fastapi import APIRouter, HTTPException
from config.db import conn
from models.event import events
from schemas.event import Event
from utilities.event import *
from sqlalchemy import tuple_

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
    if conn.execute(events.select().where(tuple_(events.c.nombre, events.c.fecha).in_(
    [(event.nombre, event.fecha)]) )).mappings().first():
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
