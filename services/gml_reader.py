from lxml import etree
from shapely.geometry import Polygon, mapping
import xml.etree.ElementTree as ET

NS = {
    "gml": "http://www.opengis.net/gml/3.2",
    "cp": "urn:x-inspire:specification:gmlas:CadastralParcels:3.0",
    "base": "urn:x-inspire:specification:gmlas:BaseTypes:3.2"
}

def read_gml_polygon(file_path: str):
    tree = ET.parse(file_path)
    root = tree.getroot()

    parcel = root.find(".//cp:CadastralParcel", NS)
    if parcel is None:
        raise ValueError("No se encontró CadastralParcel")

    # ---------------- IDs
    gml_id = parcel.attrib.get("{http://www.opengis.net/gml/3.2}id")

    local_id_el = parcel.find(".//base:localId", NS)
    local_id = local_id_el.text if local_id_el is not None else None

    # ---------------- Área
    area_el = parcel.find(".//cp:areaValue", NS)
    area = float(area_el.text) if area_el is not None else None

    # ---------------- EPSG
    multi_surface = parcel.find(".//gml:MultiSurface", NS)
    srs_name = multi_surface.attrib.get("srsName")
    epsg = srs_name.split("::")[-1]

    # ---------------- Geometría
    pos_list_el = parcel.find(".//gml:posList", NS)
    coords = list(map(float, pos_list_el.text.split()))

    ring = []
    for i in range(0, len(coords), 2):
        ring.append([coords[i], coords[i + 1]])

    geometry = {
        "type": "Polygon",
        "coordinates": [ring]
    }

    return {
        "geometry": geometry,
        "epsg": epsg,
        "area": area,
        "gml_id": gml_id,
        "local_id": local_id
    }
