from fastapi import FastAPI, Form, File, UploadFile
from typing import Optional
from pydantic import BaseModel
from uuid import uuid4
from os import path, makedirs

# Creación del servidor
app = FastAPI()

# Definición de la base de usuarios
class Usuario(BaseModel):
    nombre: str
    direccion: str
    es_vip: Optional[bool] = False

# Crear las carpetas para guardar las fotos
home_usuario = path.expanduser("~")
carpeta_vip = path.join(home_usuario, "fotos-usuarios-vip")
carpeta_no_vip = path.join(home_usuario, "fotos-usuarios")
makedirs(carpeta_vip, exist_ok=True)
makedirs(carpeta_no_vip, exist_ok=True)

# Rutas
@app.get("/")
def bienvenida():
    return {"mensaje": "Bienvenido al servidor de registro de usuarios"}

@app.post("/registro")
async def registrar_usuario(
    nombre: str = Form(...),
    direccion: str = Form(...),
    es_vip: Optional[bool] = Form(False),
    foto: UploadFile = File(...)
):
    # Generar un nombre único para la foto
    nombre_foto = str(uuid4())
    extension_foto = path.splitext(foto.filename)[1]
    carpeta_destino = carpeta_vip if es_vip else carpeta_no_vip
    ruta_foto = path.join(carpeta_destino, f"{nombre_foto}{extension_foto}")

    # Guardar la foto
    with open(ruta_foto, "wb") as archivo:
        contenido = await foto.read()
        archivo.write(contenido)

    # Imprimir los datos en la terminal
    print(f"Nombre: {nombre}")
    print(f"Dirección: {direccion}")
    print(f"VIP: {es_vip}")
    print(f"Foto guardada en: {ruta_foto}")

    # Respuesta
    return {
        "mensaje": "Usuario registrado exitosamente",
        "datos": {
            "nombre": nombre,
            "direccion": direccion,
            "es_vip": es_vip,
            "foto_guardada": ruta_foto,
        },
    }

# Para iniciar el servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
