import xml.etree.ElementTree as ET
from datetime import datetime
import re
def is_gml_v4(root) -> bool:
    """
    Detecta si el GML ya es versión v4, buscando cp:CadastralParcel con namespace v4
    """
    parcel_v4 = root.find(".//{http://inspire.ec.europa.eu/schemas/cp/4.0}CadastralParcel")
    return parcel_v4 is not None
# ---------------- Namespaces
NS = {
    "gml": "http://www.opengis.net/gml/3.2",
    "cp3": "urn:x-inspire:specification:gmlas:CadastralParcels:3.0",
    "cp4": "http://inspire.ec.europa.eu/schemas/cp/4.0",
    "base": "urn:x-inspire:specification:gmlas:BaseTypes:3.2"
}

# ---------------- Función para limpiar gml:id
def clean_gml_id(value: str) -> str:
    """
    Convierte una cadena en un identificador seguro para gml:id:
    - reemplaza espacios por guion "-"
    - elimina cualquier otro carácter que no sea letra, número, punto o guion
    """
    value = value.strip()
    value = value.replace(" ", "-")           # espacios -> guion
    value = re.sub(r"[^A-Za-z0-9.-]", "", value)  # eliminar todo lo demás
    return value

# ---------------- Función principal


def convert_gml_v3_to_v4(input_gml: str, output_gml: str):
    tree = ET.parse(input_gml)
    root = tree.getroot()

    # -------------- Detectar si ya es v4
    if is_gml_v4(root):
        print(f"El archivo {input_gml} ya está en versión GML v4. No se realizará conversión.")
        return

    # ... resto de tu código de conversión v3 -> v4 ...


    # ---------------- Extraer parcela
    parcel = root.find(".//cp3:CadastralParcel", NS)
    if parcel is None:
        raise ValueError("No se encontró cp:CadastralParcel en el GML v3")

    # ---------------- EPSG
    multi_surface = parcel.find(".//gml:MultiSurface", NS)
    srs_name = multi_surface.attrib.get("srsName") if multi_surface is not None else None
    epsg = srs_name.split("::")[-1] if srs_name else "25830"  # default EPSG si falta

    # ---------------- Área
    area_el = parcel.find("cp3:areaValue", NS)
    area_value = area_el.text if area_el is not None else "0"

    # ---------------- Inspire ID
    local_id_el = parcel.find(".//base:localId", NS)
    namespace_el = parcel.find(".//base:namespace", NS)

    if local_id_el is None or namespace_el is None:
        raise ValueError("No se encontró localId o namespace en el GML v3")

    local_id = local_id_el.text
    namespace = namespace_el.text

    # Limpiar namespace y local_id para gml:id
    clean_namespace = clean_gml_id(namespace)
    clean_local_id = clean_gml_id(local_id)
    gml_id = f"{clean_namespace}.{clean_local_id}"

    # ---------------- Geometría
    pos_list_el = parcel.find(".//gml:posList", NS)
    if pos_list_el is None:
        raise ValueError("No se encontró gml:posList")
    pos_list = pos_list_el.text.strip()

    # ---------------- Timestamp
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

    # ---------------- Generar GML v4
    gml_v4 = f'''<?xml version="1.0" encoding="utf-8"?>
<FeatureCollection
    xmlns="http://www.opengis.net/wfs/2.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:gml="http://www.opengis.net/gml/3.2"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:cp="http://inspire.ec.europa.eu/schemas/cp/4.0"
    xmlns:gmd="http://www.isotc211.org/2005/gmd"
    xsi:schemaLocation="
        http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd
        http://inspire.ec.europa.eu/schemas/cp/4.0 http://inspire.ec.europa.eu/schemas/cp/4.0/CadastralParcels.xsd"
    timeStamp="{timestamp}"
    numberMatched="1"
    numberReturned="1">

  <member>
    <cp:CadastralParcel gml:id="{gml_id}">
      <cp:areaValue uom="m2">{area_value}</cp:areaValue>

      <cp:beginLifespanVersion xsi:nil="true"
        nilReason="http://inspire.ec.europa.eu/codelist/VoidReasonValue/Unpopulated"/>

      <cp:endLifespanVersion xsi:nil="true"
        nilReason="http://inspire.ec.europa.eu/codelist/VoidReasonValue/Unpopulated"/>

      <cp:geometry>
        <gml:MultiSurface gml:id="MultiSurface_{clean_local_id}"
          srsName="http://www.opengis.net/def/crs/EPSG/0/{epsg}">
          <gml:surfaceMember>
            <gml:Surface gml:id="Surface_{clean_local_id}.1"
              srsName="http://www.opengis.net/def/crs/EPSG/0/{epsg}">
              <gml:patches>
                <gml:PolygonPatch>
                  <gml:exterior>
                    <gml:LinearRing>
                      <gml:posList srsDimension="2">{pos_list}</gml:posList>
                    </gml:LinearRing>
                  </gml:exterior>
                </gml:PolygonPatch>
              </gml:patches>
            </gml:Surface>
          </gml:surfaceMember>
        </gml:MultiSurface>
      </cp:geometry>

      <cp:inspireId>
        <Identifier xmlns="http://inspire.ec.europa.eu/schemas/base/3.3">
          <localId>{clean_local_id}</localId>
          <namespace>{clean_namespace}</namespace>
        </Identifier>
      </cp:inspireId>

      <cp:label>{clean_local_id}</cp:label>
      <cp:nationalCadastralReference>{clean_local_id}</cp:nationalCadastralReference>

    </cp:CadastralParcel>
  </member>
</FeatureCollection>
'''

    # ---------------- Escribir salida
    with open(output_gml, "w", encoding="utf-8") as f:
        f.write(gml_v4)

    print(f"GML v4 generado correctamente: {output_gml}")
