from fastapi import HTTPException
from schemas.event import Event
from config.db import conn
from models.event import config, gestion, events
from sqlalchemy import text


def GestionCheck(tipo:str):
    # Comprueba si el evento requiere gestion o no, esto basado en principio solamente en el tipo de evento
    if tipo in ["conferencia", "evento deportivo", "seminario", "concierto", "mitin politico", 
    "encuentro religioso"]:
        return 1
    else:
        return 0

def create_event(event:Event):
    # Creamos el evento en la tabla events
    # Creamos el evento en las tablas config y gestion y finalmente devolvemos el evento
    new_event = {"nombre":event.nombre, 
                "tipo":event.tipo, 
                "descripcion":event.descripcion, 
                "fecha":event.fecha,
                "status":event.status}
    result = conn.execute(events.insert().values(new_event))
    conn.commit()
    event_result = conn.execute(events.select().where(events.c.id == result.lastrowid)).mappings().first()
    create_backup_tables(event, event_result)
    return event_result
    
def create_backup_tables(event: Event, dict: dict):
    # Creamos el evento en la tabla config, y si el evento esta revisado, 
    # creamos el evento en la tabla gestion
    conn.execute(config.insert().values({"nombre":event.nombre, "event_id":dict["id"]}))
    if event.status == "revisado":
        conn.execute(gestion.insert().values({"nombre":event.nombre, "event_id":dict["id"], 
        "tipo":event.tipo, "requiere_gestion":GestionCheck(event.tipo)}))
    conn.commit()

def update_backup_tables(event: Event, id:int):
    # Vemos si el evento esta pendiente o revisado, si esta pendiente, lo eliminamos de la tabla gestion
    # si esta revisado, lo actualizamos o agregamos en la tabla gestion
    conn.execute(config.update().values(nombre=event.nombre).where(config.c.event_id == id))
    if event.status == "revisado":
        if conn.execute(gestion.select().where(gestion.c.event_id == id)).mappings().first():
            conn.execute(gestion.update().values(nombre=event.nombre, tipo = event.tipo,
            requiere_gestion = GestionCheck(event.tipo)).where(gestion.c.event_id == id))
        else:
            conn.execute(gestion.insert().values({"nombre":event.nombre, "event_id":id,  
                "tipo":event.tipo,"requiere_gestion":GestionCheck(event.tipo)}))
    else:
        conn.execute(gestion.delete().where(gestion.c.event_id == id))
    conn.commit()

def soft_delete_event(num:int, clause:bool):
    # Si el evento esta activo, lo desactivamos, si no, lanzamos un error
    if clause == True:
        conn.execute(config.update().values(active=False).where(config.c.event_id == num))
        conn.commit()
    else:
        raise HTTPException(status_code=400, detail="El evento ya ha sido borrado")

def recover_event(num:int, clause:bool):
    # Si el evento esta desactivado, lo activamos, si no, lanzamos un error
    if clause == False:
        conn.execute(config.update().values(active=True).where(config.c.event_id == num))
        conn.commit()
    else:
        raise HTTPException(status_code=400, detail="El evento no ha sido borrado")

def gestion_status(num:int):
    # Vemos si event.status es revisado, si no, lanzamos una excepcion, si es revisado,
    # no hacemos nada
    if conn.execute(events.select().where(events.c.id == num)).mappings().first()["status"] == "revisado":
        pass
    else:
        raise HTTPException(status_code=400, detail="El evento no ha sido revisado")

def update_event(event: Event, id:int):
    # Actualizamos el evento en la tabla events, y actualizamos o creamos el evento en la tabla gestion
    conn.execute(events.update().values(nombre=event.nombre, tipo=event.tipo, 
    descripcion=event.descripcion, fecha=event.fecha, status=event.status).where(events.c.id == id))
    conn.commit()
    update_backup_tables(event, id)


MostrarEventosActivos = text("""SELECT events.id, events.nombre, events.tipo, events.descripcion, 
    events.fecha, events.status 
    FROM events INNER JOIN config ON events.id = config.event_id 
    WHERE config.active = 1""")

MostrarEventosPendientes = text("""SELECT events.id, events.nombre, events.tipo, events.descripcion, 
    events.fecha, events.status 
    FROM events INNER JOIN config ON events.id = config.event_id 
    WHERE events.status = 'pendiente' AND config.active = 1""")

MostrarEventosRevisados = text("""SELECT events.id, events.nombre, events.tipo, events.descripcion, 
    events.fecha, events.status 
    FROM events INNER JOIN config ON events.id = config.event_id 
    WHERE events.status = 'revisado' AND config.active = 1""")

MostrarGestionActivos = text("""SELECT gestion.id, gestion.event_id, gestion.nombre, gestion.tipo, 
    gestion.requiere_gestion FROM gestion INNER JOIN config ON gestion.event_id = config.event_id 
    WHERE config.active = 1""")

#Create a query that retrieves all the fields from the events table when the event is active in the config table and 
#the event requires gestion in the gestion table is equal to 1
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
