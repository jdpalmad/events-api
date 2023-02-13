from fastapi import HTTPException
from schemas.event import Event
from config.db import conn
from models.event import events
from models.cfg import config
from models.gestion import gestion
from sqlalchemy import text


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