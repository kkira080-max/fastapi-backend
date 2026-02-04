import ezdxf

def generate_dxf(gml_data_list, output_path):
    """
    Genera un archivo DXF a partir de una lista de recintos GML.
    Cada recinto se dibuja como una LWPOLYLINE cerrada.
    """
    # 1. Crear un nuevo dibujo DXF (Versión R2010 para máxima compatibilidad)
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    # 2. Definir una capa para los recintos (color 1 = Rojo en AutoCAD)
    if 'RECINTOS_GML' not in doc.layers:
        doc.layers.add(name='RECINTOS_GML', color=1)

    for item in gml_data_list:
        # Extraemos la geometría del diccionario
        # Estructura esperada: item["geometry"]["coordinates"] -> [[[x1,y1], [x2,y2], ...]]
        rings = item.get("geometry", {}).get("coordinates", [])
        local_id = item.get("local_id", "Sin_ID")

        for ring in rings:
            if not ring:
                continue

            # 3. Añadir la polilínea al espacio de modelo
            # close=True asegura que el último punto se conecte con el primero
            msp.add_lwpolyline(
                points=ring, 
                close=True, 
                dxfattribs={
                    'layer': 'RECINTOS_GML',
                    'lineweight': 25 # Grosor de línea visible
                }
            )

            # 4. Opcional: Añadir un texto con el localId en la primera coordenada
            msp.add_text(
                local_id, 
                dxfattribs={
                    'layer': 'RECINTOS_GML',
                    'height': 1.5 # Tamaño del texto
                }
            ).set_placement(ring[0])

    # 5. Guardar el archivo
    doc.saveas(output_path)