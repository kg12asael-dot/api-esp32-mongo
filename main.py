from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from datetime import datetime

app = FastAPI()

MONGO_URI = "mongodb+srv://asael:2509@cluster0.zr3wpxi.mongodb.net/iot?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(MONGO_URI)
    db = client.iot
    collection = db.sensores
    print("Conexión exitosa a MongoDB Atlas")
except Exception as e:
    print(f"Error de conexión: {e}")

@app.get("/")
def inicio():
    return {"mensaje": "API de Asael funcionando correctamente"}

@app.post("/sensor")
async def recibir_datos(datos: dict):
    try:

        print("DATOS RECIBIDOS:")
        print(datos)

        # Solo agrega fecha actual si no se envió una
        if "fecha" not in datos or not datos["fecha"]:
            datos["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("SE GENERÓ FECHA AUTOMÁTICA")

        resultado = collection.insert_one(datos)

        return {
            "status": "Procesado",
            "id_db": str(resultado.inserted_id),
            "fecha_guardada": datos["fecha"],
            "mensaje": "Dato guardado en Atlas"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
