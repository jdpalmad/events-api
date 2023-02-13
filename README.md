## **Esta API busca monitoriar y gestionar eventos**
*El crud es realizado utilizando FastAPI y SQL*
Es recomendable crear un entorno virtual para instalar las dependencias y ejecutar el proyecto, de este modo se evita que las dependencias se instalen en el entorno global de python y asi evitar conflictos con otras versiones de las mismas. <br>

##### *Los comandos etiquetados con ```console``` son validos para bash, zsh, etc...*

### Requerimientos

Para comenzar, clonamos el repositorio:<br>
> ```console git clone https://github.com/jdpalmad/events-api.git ```   <br> <br> 
Una vez clonado, nos dirigimos al folder del proyecto:<br>
> ```console cd events-api ```   <br> <br>


Para crear un entorno virtual con la version de Python 3.10.9, ejecute el siguiente comando:<br>
> ```console conda create -n envname python=3.10.9 ```   <br> <br>
En este caso lo hacemos con conda 22.0.9, pero puede usar virtualenv o venv. <br>
Una vez creado el entorno virtual, active el mismo con el siguiente comando:<br>
> ```console conda activate envname ```   <br> <br>
Ahora instale las dependencias del proyecto, para ello ejecute el siguiente comando:<br>
> ```console pip install -r requirements.txt ```   <br> <br>

### Base de datos
Dado que la API utiliza una base de datos SQL, debe crear una base de datos en su servidor local. <br>
En caso de que no tenga instalado MySQL, puede descargarlo desde el siguiente enlace: <br>
> - [MySQL Installation Guide](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/) <br>
Finalmente es importante que recuerde el usuario y contraseña de la base de datos, ya que se utilizaran para configurar las variables de entorno. <br>
Una manera de verificarlo es ejecutando el siguiente comando en mysql:<br>
> ```SELECT USER();```   <br> 
Posteriormente ejecute el siguiente comando para verificar el puerto:<br>
> ```SHOW VARIABLES WHERE Variable_name = 'port';```   <br> 
Finalmente cree una base de datos, esto se hace con el siguiente comando:<br>
> ```CREATE DATABASE database_name;```   <br>

### Variables de entorno
Para que la API funcione correctamente, debe ingresar en el archivo ```events-api/config/db.py``` y configurar las variables de entorno. <br>
Estas son: <br>
> - user: usuario de la base de datos <br>
> - sql_password: contraseña de la base de datos <br>
> - database: nombre de la base de datos (database_name en este tutorial)<br>
> - host: host en el que quiere alojar el servidor sql<br>
> - port: puerto de la base de datos, por ejemplo '3306' <br>

### Ejecutar el proyecto
De nuevo en el folder ```events-api``` ejecute el siguiente comando para iniciar el servidor:<br>
> ```console uvicorn main:app --reload ```   <br> <br>
De esta manera, el servidor se iniciara en la direccion: ```http://localhost:8000/``` <br>

## **Puede ver la documentacion de la API en la siguiente direccion:** <br> 
```http://localhost:8000/``` o ```http://localhost:8000/redoc``` <br>

### Cargando los datos de prueba
Para cargar los datos de prueba, ejecute el siguiente comando, en el folder ```events-api/utilities```: <br>
> ```console python loadstatic.py ```   <br> 

# Interactuando con la API
Una vez que la API esta corriendo, usamos el endpont ```/``` para ingresar a la documentacion de la API, donde encontrara la informacion correspondiente a los endpoints. <br>

#### **Elaborado por: jdpalmad** 

