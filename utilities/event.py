from schemas.event import Event
from config.db import conn
from models.event import events
from models.cfg import config
from models.gestion import gestion
from sqlalchemy import text

def GestionCheck(tipo:str):
    # Claramente esta funcion podria ser muchisimo mas interesante si complicaramos la logica del CRUD, si 
    # por ejemplo tambien conocieramos la ubicacion del evento, aforo, etc...
    # podriamos pensar una manera de clasificar el requerimiento de gestion de un evento de una manera
    # mas pertinente

    # Funcion que revisa si el evento requiere gestion o no
    # Comprueba si el evento requiere gestion o no, esto basado en principio solamente en el tipo de evento
    if tipo in ["conferencia", "evento deportivo", "seminario", "concierto", "mitin politico", 
    "encuentro religioso"]:
        return 1
    else:
        # Claramente el requerir gestion por ahora corresponde a estar en una lista de unos tipos de 
        # eventos.
        return 0

def create_event(event:Event):
    # Creamos el evento en la tabla events
    # Creamos el evento en las tablas config y gestion y finalmente devolvemos el evento
    new_event = {"nombre":event.nombre, 
                "tipo":event.tipo, 
                "descripcion":event.descripcion, 
                "fecha":event.fecha,
                "status":event.status}
    # Creamos el diccionario new_event con los datos del evento para poder insertarlo en la tabla events
    result = conn.execute(events.insert().values(new_event))
    # Confirmamos la insercion
    conn.commit()
    # Devolvemos el evento en caso de exito y asi mismo creamos el evento en las tablas config y gestion
    event_result = conn.execute(events.select().where(events.c.id == result.lastrowid)).mappings().first()
    create_backup_tables(event, event_result)
    return event_result
    
def create_backup_tables(event: Event, dict: dict):
    # Creamos el evento en la tabla config, y si el evento esta revisado, 
    # Creamos el evento en la tabla gestion
    conn.execute(config.insert().values({"nombre":event.nombre, "event_id":dict["id"]}))
    if event.status == "revisado":
        conn.execute(gestion.insert().values({"nombre":event.nombre, "event_id":dict["id"], 
        "tipo":event.tipo, "requiere_gestion":GestionCheck(event.tipo)}))
        # Los eventos revisados se evaluan en la funcion GestionCheck y de este modo sabemos si 
        # el evento en cuestion requiere o no gestion
    conn.commit()

def update_event(event: Event, id:int):
    # Actualizamos el evento en la tabla events, y actualizamos o creamos el evento en la tabla gestion
    conn.execute(events.update().values(nombre=event.nombre, tipo=event.tipo, 
    descripcion=event.descripcion, fecha=event.fecha, status=event.status).where(events.c.id == id))
    conn.commit()
    # Actualizamos el evento en la tabla config y gestion
    update_backup_tables(event, id)

def update_backup_tables(event: Event, id:int):
    # Vemos si el evento esta pendiente o revisado, si esta pendiente, lo eliminamos de la tabla gestion
    # si esta revisado, lo actualizamos o agregamos en la tabla gestion
    conn.execute(config.update().values(nombre=event.nombre).where(config.c.event_id == id))
    if event.status == "revisado":
        # Si el evento esta revisado, lo agregamos o actualizamos en la tabla gestion
        # y evaluamos si el evento requiere gestion o no con la funcion GestionCheck
        # aplicada al campo event.tipo
        if conn.execute(gestion.select().where(gestion.c.event_id == id)).mappings().first():
            conn.execute(gestion.update().values(nombre=event.nombre, tipo = event.tipo,
            requiere_gestion = GestionCheck(event.tipo)).where(gestion.c.event_id == id))
        else:
            # Vea que se evalua tambien si el evento ya existe o si debemos agregarlo, por lo que este
            # else corresponde a la condicion de que el evento no exista en la tabla gestion.
            conn.execute(gestion.insert().values({"nombre":event.nombre, "event_id":id,  
                "tipo":event.tipo,"requiere_gestion":GestionCheck(event.tipo)}))
    else:
        # Si se cambia el status a pendiente, eliminamos el evento de la tabla gestion
        conn.execute(gestion.delete().where(gestion.c.event_id == id))
    conn.commit()

MostrarEventosActivos = text("""SELECT events.id, events.nombre, events.tipo, events.descripcion, 
    events.fecha, events.status 
    FROM events INNER JOIN config ON events.id = config.event_id 
    WHERE config.active = 1""")
    # Esta consulta nos permite mostrar los eventos activos, es decir, los eventos que estan en la tabla
    # events y que estan activos en la tabla config

MostrarEventosPendientes = text("""SELECT events.id, events.nombre, events.tipo, events.descripcion, 
    events.fecha, events.status 
    FROM events INNER JOIN config ON events.id = config.event_id 
    WHERE events.status = 'pendiente' AND config.active = 1""")
    # Esta consulta nos permite mostrar los eventos pendientes, es decir, los eventos que estan en la tabla
    # events y que estan activos en la tabla config y que tienen el status pendiente

MostrarEventosRevisados = text("""SELECT events.id, events.nombre, events.tipo, events.descripcion, 
    events.fecha, events.status 
    FROM events INNER JOIN config ON events.id = config.event_id 
    WHERE events.status = 'revisado' AND config.active = 1""")
    # Esta consulta nos permite mostrar los eventos revisados, es decir, los eventos que estan en la tabla
    # events y que estan activos en la tabla config y que tienen el status revisado
