import os
import shutil
import uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

from services.gml_reader import read_gml_polygon
from services.gml_v4_generator import convert_gml_v3_to_v4 as gml_v3_to_v4_service


from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
import zipfile
import io


app = FastAPI()
# ---------------- Configuración
UPLOAD_DIR = "uploads"
TEMP_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# ---------------- CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar a tu dominio en producción
    allow_methods=["*"],
    allow_headers=["*"]
)

# ---------------- Endpoint: subir 1 GML y devolver GeoJSON
@app.post("/upload-gml/")
async def upload_gml(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    data = read_gml_polygon(file_path)
    return {
        "type": "Feature",
        "geometry": data["geometry"],
        "properties": {
    "epsg": data["epsg"],
    "area": data["area"],
    "filename": file.filename,
    "gml_id": data["gml_id"],
    "local_id": data["local_id"]
    
}

    }

# ---------------- Endpoint: subir varios GML y devolver GeoJSON
@app.post("/upload-gml-multiple/")
async def upload_gml_multiple(files: list[UploadFile] = File(...)):
    features = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        data = read_gml_polygon(file_path)
        features.append({
            "type": "Feature",
            "geometry": data["geometry"],
            "properties": {
    "epsg": data["epsg"],
    "area": data["area"],
    "filename": file.filename,
    "gml_id": data["gml_id"],
    "local_id": data["local_id"]
}

        })

    return {"type": "FeatureCollection", "features": features}



# ---------------- Endpoint: convertir GML v3 → v4 y descargar
@app.post("/convert-to-gml-v4/")
async def convert(file: UploadFile = File(...)):
    uid = uuid.uuid4().hex
    input_path = os.path.join(TEMP_DIR, f"{uid}_v3.gml")
    output_path = os.path.join(TEMP_DIR, f"{uid}_v4.gml")

    with open(input_path, "wb") as f:
        f.write(await file.read())

    gml_v3_to_v4_service(input_path, output_path)

    with open(output_path, "rb") as f:
        content = f.read()

    return Response(
        content=content,
        media_type="application/xml",
        headers={
            "Content-Disposition": f'attachment; filename="{file.filename.replace(".gml","")}_v4.gml"'
        }
    )

@app.post("/convert-multiple")
async def convert_multiple(files: list[UploadFile] = File(...)):
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            uid = uuid.uuid4().hex
            input_path = os.path.join(TEMP_DIR, f"{uid}_v3.gml")
            output_path = os.path.join(TEMP_DIR, f"{uid}_v4.gml")

            # Guardar GML v3
            with open(input_path, "wb") as f:
                f.write(await file.read())

            # Convertir a v4
            gml_v3_to_v4_service(input_path, output_path)

            # Añadir al ZIP
            zipf.write(
                output_path,
                arcname=file.filename.replace(".gml", "_v4.gml")
            )

    zip_buffer.seek(0)

    return Response(
        content=zip_buffer.read(),
        media_type="application/zip",
        headers={
            "Content-Disposition": 'attachment; filename="gml_v4_convertidos.zip"'
        }
    )

# ---------------- Opcional: endpoint salud
@app.get("/ping")
async def ping():
    return {"status": "ok"}
