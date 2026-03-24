from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

# Tu enlace de MongoDB Atlas personalizado
# Se agregó "/iot" antes del signo "?" para que guarde ahí directamente
MONGO_URI = "mongodb+srv://asael:2509@cluster0.zr3wpxi.mongodb.net/iot?retryWrites=true&w=majority&appName=Cluster0"

try:
    # Conectamos al cliente de MongoDB
    client = MongoClient(MONGO_URI)
    db = client.iot  # Base de datos: iot
    collection = db.sensores  # Colección: sensores
    print("Conexión exitosa a MongoDB Atlas")
except Exception as e:
    print(f"Error de conexión: {e}")

@app.get("/")
def inicio():
    return {"mensaje": "API de Asael funcionando correctamente"}

@app.post("/sensor")
async def recibir_datos(datos: dict):
    try:
        # Añadimos la fecha y hora actual automáticamente
        datos["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Insertamos el JSON en MongoDB
        resultado = collection.insert_one(datos)
        
        return {
            "status": "Procesado", 
            "id_db": str(resultado.inserted_id),
            "mensaje": "Dato guardado en Atlas"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))