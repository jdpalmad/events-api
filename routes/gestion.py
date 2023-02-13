from fastapi import APIRouter, HTTPException
from config.db import conn
from models.event import events
from models.gestion import gestion
from schemas.gestion import gestionEvent
from schemas.event import Event
from utilities.gestion import *

gestion = APIRouter()

@gestion.get("/events/gestion", response_model=list[gestionEvent], description="""Obtenga el estado de gestion
    de todos los eventos""", tags=["gestion"])
def get_gestion_events():
    # Obtenga una lista de todos los 
    # eventos activos y su estado de gestion
    return conn.execute(MostrarGestionActivos).mappings().all()


@gestion.get("/events/gestion/{id}", response_model=gestionEvent, description="""Obtenga el estado de 
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

@gestion.get("/gestion/{clause}", response_model=list[Event], description="""Obtenga el estado de
    gestion de todos los eventos""", tags=["gestion"])
def check_gestion(clause:bool):
    # Hace las correspondientes verificaciones para recuperar los eventos
    # activos en la tabla config que requieren gestion o no
    if clause == True:
        return conn.execute(MostrarEventosRequiereGestion).mappings().all()
    elif clause == False:
        return conn.execute(MostrarEventosNoRequiereGestion).mappings().all()