from fastapi import FastAPI
from routes.event import event
from routes.cfg import cfg
from routes.gestion import gestionr

# Descripción de la API
descripcion = "API para la gestión de eventos 🚀 <br> \n\n ## EVENTS API \n Recuerde que se busca registrar eventos en una tabla con los siguientes requerimientos: <br> \n\n> - **ID** <br> \n > - **Nombre del evento** <br>\n > - **Tipo del evento** <br>\n > - **Descripcion del Evento** <br> \n> - **Fecha** <br>\n > - **Estado** *(Pendiente por revisar / revisado)*  \n\n La funcionalidad de esta API se divide en tres secciones, las cuales son : <br> \n > - ```events``` <br> \n> - ```gestion``` <br> \n> - ```config``` <br> \n \n\n La seccion ```events``` permite:\n> - Ver todos los eventos <br> \n > - Ver todos los eventos activos <br> \n> - Ver todos los eventos activos a su vez pendientes <br> \n > - Ver todos los eventos activos a su vez revisados <br> \n > - Ver un evento por ID <br> \n > - Actualizar un evento por ID  \n\n La seccion ```gestion``` permite:  <br> \n > - Ver el estado de gestion de todos los eventos activos <br> \n> - Ver el estado de gestion de un evento por ID <br>\n > - Ver todos los eventos activos que requieren gestion o no\n\nLa seccion ```config``` permite:\n > - Soft delete un evento <br> \n> - Activar un evento (deshacer el soft-delete) <br> \n\n Este API busca clasificar los eventos con status *'revisado'* en la tabla **eventos**, y posteriormente segun el tipo de evento, determinar si requiere gestion o no. <br>\n\n Cabe resaltar que la funcion principal del API incluye dos cosas: <br> \n > - *Determinar si un evento revisado requiere gestion* <br> \n > - Soft delete un evento <br> \n Claramente si un elemento ha sido *soft-deleted* entonces em principio no tiene sentido preguntarnos si requiere gestion o no. <br> \n\n Esto lo implementamos de la siguiente manera:<br>\n > - ```Llevamos un registro en la tabla *config* par ver si fue eliminado, por defecto no estara eliminado```<br> \n > - ```Para todos los eventos de la tabla events, revisamos tanto en su creacion, como en su modificacion, si su estado en 'revisado' o 'pendiente' ```<br> \n > - ```Para todos los eventos de la tabla gestion, se aplica en el momento de su insercion o modificacion la funcion necesaria para determinar si el evento requiere gestion o no ``` <br>\n > - ```Creamos los endpoints necesarios para interactuar con el API```<br><br>\n *No olvide que puede interactuar con los HTTPS Metodos en el endpoint:* ```/```<br>\n\n  **Para mas informacion especifica de las funciones involucradas dirijase a:** https://github.com/jdpalmad/events-api fuente de la API. <br> \n *Realizado por jdpalmad.* \n\n "

# Inicialización de la API
app = FastAPI(
    title="API Eventos",
    description="# **Bienvenido a la API de eventos** 🚀 \n Lo invitamos a que se dirija al enlace habilitado ```localhost:8000/docs``` para informarse mas acerca de la API \n A continuacion encontrara los metodos implementados y podra interactuar con ellos asi como obtener informacion basica y ejemplos pertienentes para su interaccion. <br> \n A continuacion una breve guia para su paso por esta API <br> \n > - ```Dirijase a la parte inferior, encontrara tres labels diferentes, (vea /docs)``` <br> \n> - ```Seleccione un HTTP metodo, de click sobre el``` <br> \n> - ```Encontrara informacion de este y un ejemplo si es necesario, busque el boton blanco ``` *Try it out* ```si el metodo lo requiere, vea el ejemplo y llene un registro con la informacion necesaria del objeto Event y presione Execute ``` <br><br>\n\n Algunas recomendaciones utiles podrian ser: \n > - En la parte final de la pagina encontrara el Schema Event para que vea los campos obligatorios de este. <br>\n> - Una vez de click en EXECUTE para cualquier metodo, se le mostrara como interactuar con este metodo usando **cURL** <br>\n> - No olvide cargar los datos estaticos, estos lo hace ejecutando el escript ```loadstatic.py``` en el folder ```events-api/utilities/``` <br>\n\n",
    version="0.1.0",
    docs_url="/",
    tags_metadata = { 
        "events": {"description": "Gestión de eventos\n ```hola```"},
        "gestion": {"description": "Controlador de la gestión de eventos"},
        "config": {"description": "Configuración de eventos"}
    }
)

docapp = FastAPI(redoc_url='/',
    title="Documentacion API eventos",
    description = descripcion,
    tags_metadata = { 
        "events": {"description": "Gestión de eventos\n ```hola```"},
        "gestion": {"description": "Controlador de la gestión de eventos"},
        "config": {"description": "Configuración de eventos"}
    }
    )
app.mount("/docs", docapp)

# Incluimos las rutas de las secciones
app.include_router(event)
app.include_router(cfg)
app.include_router(gestionr)

docapp.include_router(event)
docapp.include_router(cfg)
docapp.include_router(gestionr)