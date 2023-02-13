from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from config.db import meta, engine

# Tabla "config" de configuracion y actividad de los atributos.

config = Table("config", meta,
    Column ("id", Integer, primary_key = True),
    Column ("event_id", Integer, ForeignKey("events.id"), nullable = False),
    Column ("nombre", String(50)),
    Column ("active", Boolean, default = True)
    )
# Si desea entender mejor el funcionamiento de esta tabla, por favor lea el archivo
# schemas/cfg.py

meta.create_all(engine)