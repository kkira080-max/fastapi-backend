import os
import shutil
import uuid
import zipfile
import io
from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware

# Importamos los servicios actualizados
from services.gml_reader import read_gml_polygon
from services.gml_v4_generator import convert_gml_v3_to_v4, AlreadyV4Error
from services.dxf_generator import generate_dxf

app = FastAPI()

# ---------------- Configuración
UPLOAD_DIR = "uploads"
TEMP_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# ---------------- CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ---------------- Endpoint: Subir y Visualizar (Múltiples recintos)
@app.post("/upload-gml/")
async def upload_gml(file: UploadFile = File(...)):
    """
    Recibe un archivo GML, lo guarda temporalmente, extrae todos los recintos
    y devuelve una FeatureCollection para visualizar en el mapa.
    """
    # 1. Definir rutas y guardar el archivo
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        return {"error": f"Error al guardar el archivo: {str(e)}"}

    try:
        # 2. Llamar al reader (que ahora devuelve una LISTA de diccionarios)
        data_list = read_gml_polygon(file_path)
        
        # 3. Construir la estructura GeoJSON (FeatureCollection)
        # Esto permite que el frontend reciba N recintos en un solo objeto
        features = []
        for data in data_list:
            features.append({
                "type": "Feature",
                "geometry": data["geometry"],
                "properties": {
                    "gml_id": data.get("gml_id"),
                    "localId": data.get("local_id"),
                    "area": data.get("area"),
                    "epsg": data.get("epsg"),
                    "filename": file.filename
                }
            })
        
        # 4. Respuesta final exitosa
        return {
            "type": "FeatureCollection",
            "features": features,
            "metadata": {
                "count": len(features),
                "status": "success",
                "message": "Fichero procesado correctamente"
            }
        }

    except ValueError as ve:
        # Errores controlados (ej: no se encontraron parcelas)
        return {"error": str(ve), "type": "parsing_error"}
    except Exception as e:
        # Errores inesperados
        print(f"Error crítico en upload-gml: {e}")
        return {"error": "Error interno al procesar el GML", "details": str(e)}
# ---------------- Endpoint: Convertir a DXF (Requisito 2)
@app.post("/convert-to-dxf/")
async def convert_dxf(files: list[UploadFile] = File(...)):
    all_parcels = []
    
    for file in files:
        uid = uuid.uuid4().hex
        temp_path = f"temp/{uid}_{file.filename}"
        
        # Guardar temporalmente cada archivo
        with open(temp_path, "wb") as f:
            f.write(await file.read())
        
        # Leer los recintos de este archivo (pueden ser uno o varios)
        try:
            data_list = read_gml_polygon(temp_path)
            all_parcels.extend(data_list)
        except Exception as e:
            print(f"Error leyendo {file.filename}: {e}")
        finally:
            if os.path.exists(temp_path): os.remove(temp_path)

    if not all_parcels:
        return {"error": "No se encontraron recintos válidos"}

    # Generar un único DXF con TODO
    output_dxf = f"temp/conjunto_fincas_{uuid.uuid4().hex}.dxf"
    generate_dxf(all_parcels, output_dxf)
    
    with open(output_dxf, "rb") as f:
        content = f.read()
    
    return Response(
        content=content, 
        media_type="application/dxf",
        headers={"Content-Disposition": "attachment; filename=fincas_completas.dxf"}
    )
# ---------------- Endpoint: Convertir a GML v4 (Requisito 1 y 3)
@app.post("/convert-multiple")
async def convert_multiple(files: list[UploadFile] = File(...)):
    zip_buffer = io.BytesIO()
    v4_detected = []

    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for file in files:
            in_p = f"temp/{uuid.uuid4()}.gml"
            out_p = in_p.replace(".gml", "_v4.gml")
            with open(in_p, "wb") as f: f.write(await file.read())
            
            try:
                convert_gml_v3_to_v4(in_p, out_p)
                zipf.write(out_p, arcname=file.filename.replace(".gml", "_v4.gml"))
            except AlreadyV4Error:
                v4_detected.append(file.filename)
                zipf.write(in_p, arcname=file.filename)

    headers = {"Content-Disposition": 'attachment; filename="gml_v4_convertidos.zip"'}
    if v4_detected:
        headers["X-Already-V4"] = ",".join(v4_detected)  

    return Response(content=zip_buffer.getvalue(), media_type="application/zip", headers=headers)

@app.get("/ping")
async def ping():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Backend FastAPI funcionando"}

@app.get("/api")
async def api():
    return {"status": "ok"}
