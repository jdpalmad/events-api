from sqlalchemy import Table, Column, Integer, String, Boolean, Date, CheckConstraint, ForeignKey
from config.db import meta, engine

# Tabla de eventos
# Esta tabla lleva registro de los eventos y los atributos activos (vea la tabla config).
# Los campos obedecen a los requerimientos provistos por las necesidades de esta API
# Encontrara mas informacion de esto en en el endpoint /docs.

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
# Si desea entender mejor el funcionamiento de esta tabla, por favor lea el archivo
# schemas/event.py

meta.create_all(engine)