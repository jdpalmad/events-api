from schemas.event import Event
from config.db import conn
from models.event import events
from models.cfg import config
from models.gestion import gestion
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

def update_event(event: Event, id:int):
    # Actualizamos el evento en la tabla events, y actualizamos o creamos el evento en la tabla gestion
    conn.execute(events.update().values(nombre=event.nombre, tipo=event.tipo, 
    descripcion=event.descripcion, fecha=event.fecha, status=event.status).where(events.c.id == id))
    conn.commit()
    update_backup_tables(event, id)

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
