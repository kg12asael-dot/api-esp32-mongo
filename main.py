from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

MONGO_URI = "mongodb+srv://asael:2509@cluster0.zr3wpxi.mongodb.net/iot?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(MONGO_URI)
    db = client.iot
    collection = db.sensores
    print("Conexión exitosa a MongoDB Atlas")
except Exception as e:
    print(f"Error de conexión: {e}")

class SensorData(BaseModel):
    temperatura: int
    humedad: int
    dispositivo: str
    fecha: Optional[str] = None

@app.get("/")
def inicio():
    return {"mensaje": "API de Asael funcionando correctamente"}

@app.post("/sensor")
async def recibir_datos(datos: SensorData):
    try:
        payload = datos.dict()
        
        if payload["fecha"] is None or payload["fecha"] == "":
            payload["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        resultado = collection.insert_one(payload)
        
        return {
            "status": "Procesado",
            "id_db": str(resultado.inserted_id),
            "fecha_guardada": payload["fecha"],
            "mensaje": "Dato guardado en Atlas"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
