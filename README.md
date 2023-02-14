## **Esta API busca monitoriar y gestionar eventos**
*El crud es realizado utilizando FastAPI y SQL*
Es recomendable crear un entorno virtual para instalar las dependencias y ejecutar el proyecto, de este modo se evita que las dependencias se instalen en el entorno global de python y asi evitar conflictos con otras versiones de las mismas. <br>

## Instalacion

### Requerimientos

Para comenzar, clonamos el repositorio:<br>
```console 
git clone https://github.com/jdpalmad/events-api.git 
```  
Una vez clonado, nos dirigimos al folder del proyecto:<br>
```console 
cd events-api 
```   


Para crear un entorno virtual con la version de Python 3.10.9, ejecute el siguiente comando:<br>
```console 
conda create -n envname python=3.10.9 
```   
En este caso lo hacemos con conda 22.0.9, pero puede usar virtualenv o venv. <br>
Una vez creado el entorno virtual, active el mismo con el siguiente comando:<br>
```console 
conda activate envname 
```  
Ahora instale las dependencias del proyecto, para ello ejecute el siguiente comando:<br>
```console 
pip install -r requirements.txt 
```   

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
Para que la API funcione correctamente, debe ingresar en el folder ```events-api/``` y configurar las variables de entorno. <br>
Para esto creamos un archivo ```.env``` y agregamos las siguientes variables de entorno: <br>
Estas son: <br>
```console
USER = "USER"
SQL_PASSWORD = "SQL_PASSWORD" 
DATABASE = "DATABASE" 
HOST = "HOST" 
PORT = "PORT"  
```

### Ejecutar el proyecto
De nuevo en el folder ```events-api``` ejecute el siguiente comando para iniciar el servidor:<br>
```console 
 uvicorn main:app --reload 
```  
De esta manera, el servidor se iniciara en la direccion: ```http://localhost:8000/``` <br>

## **Puede ver la documentacion de la API en la siguiente direccion:** <br> 
Lo invitamos a que ingrese a: ```http://localhost:8000/``` en donde encontrara parte de la documentacion de la API y podra interactuar con los HTTP Methods. <br>
Ademas, encontrara la documentacion completa en: ```http://localhost:8000/docs``` <br>

### Cargando los datos de prueba
Para cargar los datos de prueba, ejecute el siguiente comando, en el folder ```events-api/utilities```: <br>
 ```console 
 python loadstatic.py 
```   

# Interactuando con la API
Una vez que la API esta corriendo, usamos el endpont ```/``` para ingresar a la documentacion de la API, donde encontrara la informacion correspondiente a los endpoints. <br>


*Finalmente puede revisar el codigo para ver como se implemento la API. y que tipo de pull requests se aceptaran: (Principios SOLID, Conexion algo dependiente de conn y la forma en la que se establece la conexion con la base de datos)* <br>

#### **Elaborado por: jdpalmad** 

