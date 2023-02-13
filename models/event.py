from sqlalchemy import Table, Column, Integer, String, Boolean, Date, CheckConstraint, ForeignKey
from config.db import meta, engine

events = Table("events", meta, 
    Column ("id", Integer, primary_key = True ), 
    Column ("nombre", String(50)), 
    Column ("tipo", String(50), CheckConstraint("""tipo in ('conferencia', 'reunion', 'taller',
    'capacitacion', 'seminario', 'concierto', 'evento deportivo', 'feria', 
    'concurso', 'mitin politico', 'encuentro religioso')""" )), 
    Column ("descripcion", String(255)), 
    Column ("fecha", Date), 
    Column ("status", String(50), CheckConstraint("status in ('pendiente', 'revisado')")),
)   


meta.create_all(engine)