import xml.etree.ElementTree as ET
import re

# Definición de Namespaces para GML 3.2 e INSPIRE
import xml.etree.ElementTree as ET
import re

# Namespaces para ambas versiones
NS = {
    "gml": "http://www.opengis.net/gml/3.2",
    "cp3": "urn:x-inspire:specification:gmlas:CadastralParcels:3.0",
    "cp4": "http://inspire.ec.europa.eu/schemas/cp/4.0", # Namespace V4
    "base": "urn:x-inspire:specification:gmlas:BaseTypes:3.2",
    "base4": "http://inspire.ec.europa.eu/schemas/base/3.3"
}



import xml.etree.ElementTree as ET
import re

def read_gml_polygon(file_path: str):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except Exception as e:
        raise ValueError(f"Error al parsear el XML: {e}")

    # Buscamos todas las parcelas sin importar el prefijo (v3 o v4)
    parcels = root.findall(".//{*}CadastralParcel")
    
    if not parcels:
        raise ValueError("No se encontraron parcelas catastrales (CadastralParcel) en el archivo.")

    results = []
    for parcel in parcels:
        try:
            # 1. Extraer LocalId (Buscamos en cualquier namespace)
            local_id_el = parcel.find(".//{*}localId")
            local_id = local_id_el.text if local_id_el is not None else "SIN_REF"

            # 2. Extraer Área (Buscamos areaValue en cualquier namespace)
            area_el = parcel.find(".//{*}areaValue")
            area = float(area_el.text) if area_el is not None else 0.0

            # 3. Extraer EPSG
            ms = parcel.find(".//{*}MultiSurface")
            srs_name = ms.attrib.get("srsName", "") if ms is not None else ""
            # Si no está en el MultiSurface, buscamos en el primer nodo que tenga srsName
            if not srs_name:
                for el in parcel.iter():
                    if "srsName" in el.attrib:
                        srs_name = el.attrib["srsName"]
                        break
            
            epsg_match = re.search(r"(\d+)$", srs_name)
            epsg = epsg_match.group(1) if epsg_match else "25830"

            # 4. Extraer Geometría (posList)
            pos_list_el = parcel.find(".//{*}posList")
            if pos_list_el is not None and pos_list_el.text:
                raw_coords = pos_list_el.text.split()
                # Crear pares [X, Y]
                ring = [[float(raw_coords[i]), float(raw_coords[i+1])] 
                        for i in range(0, len(raw_coords), 2)]
                
                results.append({
                    "geometry": {"type": "Polygon", "coordinates": [ring]},
                    "epsg": f"EPSG:{epsg}",
                    "local_id": local_id,
                    "area": area
                })
        except Exception as e:
            print(f"Error omitiendo una parcela: {e}")
            continue

    return results