import xml.etree.ElementTree as ET
from datetime import datetime
import re

# Excepción personalizada para detectar archivos ya convertidos
class AlreadyV4Error(Exception):
    pass

NS = {
    "gml": "http://www.opengis.net/gml/3.2",
    "cp3": "urn:x-inspire:specification:gmlas:CadastralParcels:3.0",
    "cp4": "http://inspire.ec.europa.eu/schemas/cp/4.0",
    "base": "urn:x-inspire:specification:gmlas:BaseTypes:3.2"
}

def clean_text(text):
    """Limpia el texto: elimina comillas, tabuladores, espacios y caracteres especiales."""
    if not text: return "N-A"
    
    # 1. Quitar comillas (simples y dobles)
    text = text.replace('"', '').replace("'", "")
    
    # 2. Reemplazar CUALQUIER espacio en blanco (espacio, tabulador, salto de línea) por un guion
    text = re.sub(r'\s+', '-', text)
    
    # 3. Eliminar cualquier cosa que no sea Alfanumérico, Punto o Guion
    text = re.sub(r"[^A-Za-z0-9.-]", "", text)
    
    # 4. Asegurar que no queden múltiples guiones seguidos
    text = re.sub(r"-+", "-", text)
    
    # 5. Quitar guiones al principio o final
    return text.strip("-")

def convert_gml_v3_to_v4(input_path: str, output_path: str):
    """
    Convierte GML v3 (Catastro) a v4 (INSPIRE CP 4.0) limpiando los datos.
    """
    try:
        tree = ET.parse(input_path)
        root = tree.getroot()
    except Exception as e:
        raise ValueError(f"Error al leer el archivo GML: {e}")

    # Verificar si ya es v4 (Namespace cp 4.0)
    if "inspire.ec.europa.eu/schemas/cp/4.0" in root.tag:
        raise AlreadyV4Error("El archivo ya es versión 4.0")

    # Namespaces v3 para extraer datos
    ns_v3 = {
        "gml": "http://www.opengis.net/gml/3.2",
        "cp": "urn:x-inspire:specification:gmlas:CadastralParcels:3.0",
        "base": "urn:x-inspire:specification:gmlas:BaseTypes:3.2"
    }

    parcels = root.findall(".//cp:CadastralParcel", ns_v3)
    if not parcels:
        raise ValueError("No se encontraron parcelas CadastralParcel v3 en el archivo")

    # Preparar datos de cabecera
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    count = len(parcels)

    # Construcción manual del XML
    xml_header = f"""<?xml version="1.0" encoding="utf-8"?>
<FeatureCollection
    xmlns="http://www.opengis.net/wfs/2.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:gml="http://www.opengis.net/gml/3.2"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:cp="http://inspire.ec.europa.eu/schemas/cp/4.0"
    xmlns:gmd="http://www.isotc211.org/2005/gmd"
    xsi:schemaLocation="http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd http://inspire.ec.europa.eu/schemas/cp/4.0 http://inspire.ec.europa.eu/schemas/cp/4.0/CadastralParcels.xsd"
    timeStamp="{timestamp}"
    numberMatched="{count}"
    numberReturned="{count}">"""

    xml_members = []

    for parcel in parcels:
        # Extraer datos de la v3
        local_id_el = parcel.find(".//base:localId", ns_v3)
        raw_local_id = local_id_el.text if local_id_el is not None else "SIN_REFERENCIA"
        
        # --- AQUÍ LIMPIAMOS DE FORMA AGRESIVA ---
        cleaned_local_id = clean_text(raw_local_id)
        
        namespace_el = parcel.find(".//base:namespace", ns_v3)
        namespace = clean_text(namespace_el.text) if namespace_el is not None else "ES.SDGC.CP"
        
        area_el = parcel.find(".//cp:areaValue", ns_v3)
        area = area_el.text.strip() if area_el is not None else "0"
        
        pos_list_el = parcel.find(".//gml:posList", ns_v3)
        pos_list = pos_list_el.text.strip() if pos_list_el is not None else ""

        # SRS (Sistema de Referencia)
        ms = parcel.find(".//gml:MultiSurface", ns_v3)
        srs = ms.attrib.get("srsName") if ms is not None else "http://www.opengis.net/def/crs/EPSG/0/25830"

        # Construir el bloque <member> usando el ID LIMPIO
        member = f"""
  <member>
    <cp:CadastralParcel gml:id="ES.SDGC.CP.{cleaned_local_id}">
      <cp:areaValue uom="m2">{area}</cp:areaValue>
      <cp:beginLifespanVersion xsi:nil="true" nilReason="http://inspire.ec.europa.eu/codelist/VoidReasonValue/Unpopulated"/>
      <cp:endLifespanVersion xsi:nil="true" nilReason="http://inspire.ec.europa.eu/codelist/VoidReasonValue/Unpopulated"/>
      <cp:geometry>
        <gml:MultiSurface gml:id="MultiSurface_{cleaned_local_id}" srsName="{srs}">
          <gml:surfaceMember>
            <gml:Surface gml:id="Surface_{cleaned_local_id}.1" srsName="{srs}">
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
          <localId>{cleaned_local_id}</localId>
          <namespace>{namespace}</namespace>
        </Identifier>
      </cp:inspireId>
      <cp:label>{cleaned_local_id}</cp:label>
      <cp:nationalCadastralReference>{cleaned_local_id}</cp:nationalCadastralReference>
    </cp:CadastralParcel>
  </member>"""
        xml_members.append(member)

    # Unir todo
    full_xml = xml_header + "".join(xml_members) + "\n</FeatureCollection>"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_xml)