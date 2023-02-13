from sqlalchemy import Table, Column, Integer, String, Boolean, CheckConstraint, ForeignKey
from config.db import meta, engine

gestion = Table("gestion", meta,
    Column ("id", Integer, primary_key = True),
    Column ("event_id", Integer, ForeignKey("events.id"), nullable = False),
    Column ("nombre", String(50)),
    Column ("tipo", String(50), CheckConstraint("""tipo in ('conferencia', 'reunion', 'taller',
    'capacitacion', 'seminario', 'concierto', 'evento deportivo', 'feria', 
    'concurso', 'mitin politico', 'encuentro religioso')""" )), 
    Column ("requiere_gestion", Boolean, default = None)
    )

meta.create_all(engine)