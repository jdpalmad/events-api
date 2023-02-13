from fastapi import FastAPI
from routes.event import event
from routes.cfg import cfg
from routes.gestion import gestion

# Descripción de la API
descripcion = "API para la gestión de eventos 🚀  \n\n La seccion ```events``` permite:\n> - Ver todos los eventos <br> \n > - Ver todos los eventos activos <br> \n> - Ver todos los eventos activos a su vez pendientes <br> \n > - Ver todos los eventos activos a su vez revisados <br> \n > - Ver un evento por ID <br> \n > - Actualizar un evento por ID  \n\n La seccion ```gestion``` permite:  <br> \n > - Ver el estado de gestion de todos los eventos activos <br> \n > - Ver el estado de gestion de un evento por ID <br>\n > - Ver todos los eventos activos que requieren gestion o no\n\nLa seccion ```config``` permite:\n > - Soft delete un evento <br> \n    > - Activar un evento (deshacer el soft-delete) <br>"

# Inicialización de la API
app = FastAPI(
    title="API Eventos",
    description=descripcion,
    version="0.1.0",
    redoc_url="/docs",
    docs_url="/",
    tags_metadata = { 
        "events": {"description": "Gestión de eventos\n ```hola```"},
        "gestion": {"description": "Controlador de la gestión de eventos"},
        "config": {"description": "Configuración de eventos"}
    }
)

# Incluimos las rutas de las secciones
app.include_router(event)
app.include_router(cfg)
app.include_router(gestion)