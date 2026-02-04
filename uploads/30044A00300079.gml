<?xml version="1.0" encoding="utf-8"?>
<!--Parcela Catastral para entregar a la D.G. del Catastro.-->
<!--Generado por chapulincatastral https://github.com/chapulincatastral/generador-gml/ -->
<gml:FeatureCollection xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:cp="urn:x-inspire:specification:gmlas:CadastralParcels:3.0" xmlns:base="urn:x-inspire:specification:gmlas:BaseTypes:3.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:x-inspire:specification:gmlas:CadastralParcels:3.0 http://inspire.ec.europa.eu/schemas/cp/3.0/CadastralParcels.xsd" gml:id="ES.LOCAL.CP.30044A00300079">
   <gml:featureMember>
      <cp:CadastralParcel gml:id="ES.SDGC.CP.30044A00300079">
<!-- Superficie de la parcela en metros cuadrados. Tiene que coincidir con la calculada con las coordenadas.-->
         <cp:areaValue uom="m2">5140</cp:areaValue>
         <cp:beginLifespanVersion xsi:nil="true" nilReason="other:unpopulated"></cp:beginLifespanVersion>
<!-- Geometria en formato GML       -->
         <cp:geometry>
<!-- srs Name codigo del sistema de referencia en el que se dan las coordenadas, que debe coincidir con el de la cartografia catastral -->
<!-- el sistema de referencia de la cartografía catastral varía según provincia, siendo accesible desde la consulta de cartografía en Sede -->  
           <gml:MultiSurface gml:id="MultiSurface_ES.SDGC.CP.30044A00300079" srsName="urn:ogc:def:crs:EPSG::25830"> 
             <gml:surfaceMember>
               <gml:Surface gml:id="Surface_ES.SDGC.CP.30044A00300079" srsName="urn:ogc:def:crs:EPSG::25830">
                  <gml:patches>
                    <gml:PolygonPatch>
                      <gml:exterior>
                        <gml:LinearRing>
<!-- Lista de coordenadas separadas por espacios o en lineas diferentes    -->
                          <gml:posList srsDimension="2">671042.606 4219033.705 671008.907 4219071.997 671018.057 4219079.226 671017.841 4219079.474 671035.238 4219095.074 671036.157 4219094.056 671050.996 4219077.665 671083.995 4219041.724 671132.184 4218987.483 671124.264 4218983.073 671110.994 4218977.293 671096.464 4218968.634 671071.525 4218999.365 671042.606 4219033.705 671042.606 4219033.705 </gml:posList>
                        </gml:LinearRing>
                      </gml:exterior>             
                    </gml:PolygonPatch>
                  </gml:patches>
                </gml:Surface>
              </gml:surfaceMember>
            </gml:MultiSurface>
         </cp:geometry>
         <cp:inspireId>
           <base:Identifier>
<!-- Identificativo local de la parcela. Solo puede tener letras y numeros. Se recomienda (pero no es necesario) poner siempre un digito de control, por ejemplo utilizando el algoritmo del NIF.-->
             <base:localId>30044A00300079</base:localId>
             <base:namespace>ES.SDGC.CP</base:namespace>
           </base:Identifier>
         </cp:inspireId>
         <cp:label/>
<!--Siempre en blanco, ya que todavia no ha sido dada de alta en las bases de datos catastrales.-->
         <cp:nationalCadastralReference/>
      </cp:CadastralParcel>
   </gml:featureMember>
<!-- Si se desea entregar varias parcelas en un mismo fichero, se pondra un nuevo featureMember para cada parcela -->
</gml:FeatureCollection>
