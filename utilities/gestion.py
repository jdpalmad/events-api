from fastapi import HTTPException
from config.db import conn
from models.event import events
from models.cfg import config
from sqlalchemy import text

def gestion_status(num:int):
    # Vemos si event.status es revisado, si no, lanzamos una excepcion, si es revisado,
    # no hacemos nada
    if conn.execute(events.select().where(events.c.id == num)).mappings().first()["status"] == "revisado":
        pass
    else:
        raise HTTPException(status_code=400, detail="El evento no ha sido revisado")

MostrarGestionActivos = text("""SELECT gestion.id, gestion.event_id, gestion.nombre, gestion.tipo, 
    gestion.requiere_gestion FROM gestion INNER JOIN config ON gestion.event_id = config.event_id 
    WHERE config.active = 1""")

MostrarEventosRequiereGestion = text("""SELECT events.id, events.nombre, events.tipo, events.descripcion, 
    events.fecha, events.status 
    FROM events INNER JOIN config ON events.id = config.event_id 
    INNER JOIN gestion ON events.id = gestion.event_id 
    WHERE config.active = 1 AND gestion.requiere_gestion = 1""")

MostrarEventosNoRequiereGestion = text("""SELECT events.id, events.nombre, events.tipo, events.descripcion,
    events.fecha, events.status
    FROM events INNER JOIN config ON events.id = config.event_id
    INNER JOIN gestion ON events.id = gestion.event_id
    WHERE config.active = 1 AND gestion.requiere_gestion = 0""")