from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from config.db import meta, engine

config = Table("config", meta,
    Column ("id", Integer, primary_key = True),
    Column ("event_id", Integer, ForeignKey("events.id"), nullable = False),
    Column ("nombre", String(50)),
    Column ("active", Boolean, default = True)
    )

meta.create_all(engine)