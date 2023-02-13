from sqlalchemy import create_engine, MetaData

# Configuracion de la conexion a la base de datos
# Valores de ejemplo, cambiar por los valores de su base de datos
user = "root"
sql_password = "sqlpw123"
database = "eventsdb"
host = "localhost"
port = "3306"

engine = create_engine(f"mysql+pymysql://"+user+":"+sql_password+"@"+host+":"+port+"/"+database)

meta = MetaData()
conn = engine.connect()


