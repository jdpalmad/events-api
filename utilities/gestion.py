from fastapi import HTTPException
from config.db import conn
from models.event import events
from sqlalchemy import text

# Modulo de uilidades para las funciones indicadas en el archivo routes/gestion.py

def gestion_status(num:int):
    # Esta funcion mira si el evento ha sido revisado
    if conn.execute(events.select().where(events.c.id == num)).mappings().first()["status"] == "revisado":
        # Vemos si event.status es revisado, si no, lanzamos una excepcion, si es revisado,
        # no hacemos nada
        pass
    else:
        raise HTTPException(status_code=400, detail="El evento no ha sido revisado")

MostrarGestionActivos = text("""SELECT gestion.id, gestion.event_id, gestion.nombre, gestion.tipo, 
    gestion.requiere_gestion FROM gestion INNER JOIN config ON gestion.event_id = config.event_id 
    WHERE config.active = 1""")
    # Esta consulta nos muestra la tabla gestion de los elementos activos. Claramente,
    # esta verificacion se hace sobre los elementos de la tabla gestion por lo que 
    # los eventos fueron previamente revisados.

MostrarEventosRequiereGestion = text("""SELECT events.id, events.nombre, events.tipo, events.descripcion, 
    events.fecha, events.status 
    FROM events INNER JOIN config ON events.id = config.event_id 
    INNER JOIN gestion ON events.id = gestion.event_id 
    WHERE config.active = 1 AND gestion.requiere_gestion = 1""")
    # Esta consulta nos muestra los eventos que requieren gestion. Claramente,
    # esta verificacion se hace sobre los elementos de la tabla gestion por lo que
    # los eventos fueron previamente revisados.

MostrarEventosNoRequiereGestion = text("""SELECT events.id, events.nombre, events.tipo, events.descripcion,
    events.fecha, events.status
    FROM events INNER JOIN config ON events.id = config.event_id
    INNER JOIN gestion ON events.id = gestion.event_id
    WHERE config.active = 1 AND gestion.requiere_gestion = 0""")
    # Esta consulta nos muestra los eventos que no requieren gestion. Claramente,
    # esta verificacion se hace sobre los elementos de la tabla gestion por lo que
    # los eventos fueron previamente revisados.