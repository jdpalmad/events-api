import requests, json
# La manera en la que se cargan los datos es la siguiente:
# 1. Se abre el archivo json con los datos
# 2. Se carga el archivo json en una variable
# 3. Se itera sobre la variable y se envia cada elemento como payload
# 4. Se envia el payload a la API usando el metodo POST

url = 'http://localhost:8000/events'
f = open("staticdata.json", 'r')
data = json.load(f)
for item in data:
    payload = item
    header = {}
    res = requests.post(url, json = payload, headers = {})

# El archivo staticdata.json contiene los datos de la tabla de eventos, estos archivos se leen en Python
# como una lista de diccionarios.