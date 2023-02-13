from fastapi import HTTPException
from config.db import conn
from models.cfg import config

# Metodos para la tabla de configuracion,
# estos metodos son utilizados en el archivo routes/cfg.py
# para realizar las operaciones de la tabla de configuracion

# Con el fin de satisfacer principios SOLID, se quiere en el futuro separar las funcines de modo que 
# los eventos tales event['active] == True son todos los que estan activos, por lo que se puede
# implementar una isActive() que devuelva True si el evento esta activo y False si no lo esta y 
# de este modo implementar una funcion que cambie el estado de un evento, sin importar si esta activo
# o no

def soft_delete_event(num:int, clause:bool):
    # Si el evento esta activo, lo desactivamos, si no, lanzamos un error
    if clause == True:
        # Se actualiza el campo active a False
        conn.execute(config.update().values(active=False).where(config.c.event_id == num))
        # Se confirma la actualizacion
        conn.commit()
    else:
        # Si el evento ya esta desactivado, lanzamos un error
        raise HTTPException(status_code=400, detail="El evento ya ha sido borrado")

def recover_event(num:int, clause:bool):
    # Si el evento esta desactivado, lo activamos, si no, lanzamos un error
    if clause == False:
        # Se actualiza el campo active a True
        conn.execute(config.update().values(active=True).where(config.c.event_id == num))
        # Se confirma la actualizacion
        conn.commit()
    else:
        # Si el evento ya esta activado, lanzamos un error
        raise HTTPException(status_code=400, detail="El evento no ha sido borrado")