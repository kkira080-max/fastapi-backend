<?xml version="1.0" encoding="utf-8"?>
<!--Parcela Catastral para entregar a la D.G. del Catastro.-->
<!--Generado por chapulincatastral https://github.com/chapulincatastral/generador-gml/ -->
<gml:FeatureCollection gml:id="ES.SDGC.CP" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:cp="http://inspire.ec.europa.eu/schemas/cp/4.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://inspire.ec.europa.eu/schemas/cp/4.0 http://inspire.ec.europa.eu/schemas/cp/4.0/CadastralParcels.xsd">
   <gml:featureMember>
      <cp:CadastralParcel gml:id="ES.LOCAL.CP.FR-1306">
<!-- Superficie de la parcela en metros cuadrados. Tiene que coincidir con la calculada con las coordenadas.-->
         <cp:areaValue uom="m2">1781</cp:areaValue>
         <cp:beginLifespanVersion xsi:nil="true" nilReason="other:unpopulated"></cp:beginLifespanVersion>
<!-- Geometria en formato GML       -->
         <cp:geometry>
<!-- srs Name codigo del sistema de referencia en el que se dan las coordenadas, que debe coincidir con el de la cartografia catastral -->
<!-- el sistema de referencia de la cartografía catastral varía según provincia, siendo accesible desde la consulta de cartografía en Sede -->  
           <gml:MultiSurface gml:id="MultiSurface_ES.LOCAL.CP.FR-1306" srsName="urn:ogc:def:crs:EPSG::25830"> 
             <gml:surfaceMember>
               <gml:Surface gml:id="Surface_ES.LOCAL.CP.FR-1306" srsName="urn:ogc:def:crs:EPSG::25830">
                  <gml:patches>
                    <gml:PolygonPatch>
                      <gml:exterior>
                        <gml:LinearRing>
<!-- Lista de coordenadas separadas por espacios o en lineas diferentes    -->
                          <gml:posList srsDimension="2">672891.460 4211109.944 672868.564 4211099.240 672836.329 4211124.440 672837.102 4211128.006 672837.432 4211129.906 672838.282 4211134.696 672840.262 4211141.346 672842.182 4211144.666 672842.042 4211145.036 672843.512 4211145.476 672865.670 4211152.070 672870.200 4211146.460 672879.030 4211135.860 672884.944 4211128.971 672889.212 4211117.645 672889.972 4211115.635 672892.019 4211110.206 672891.460 4211109.944 </gml:posList>
                        </gml:LinearRing>
                      </gml:exterior>             
                    </gml:PolygonPatch>
                  </gml:patches>
                </gml:Surface>
              </gml:surfaceMember>
            </gml:MultiSurface>
         </cp:geometry>
         <cp:inspireId xmlns:base="http://inspire.ec.europa.eu/schemas/base/3.3">
           <base:Identifier>
<!-- Identificativo local de la parcela. Solo puede tener letras y numeros. Se recomienda (pero no es necesario) poner siempre un digito de control, por ejemplo utilizando el algoritmo del NIF.-->
             <base:localId>FR-1306</base:localId>
             <base:namespace>ES.LOCAL.CP</base:namespace>
           </base:Identifier>
         </cp:inspireId>
         <cp:label/>
<!--Siempre en blanco, ya que todavia no ha sido dada de alta en las bases de datos catastrales.-->
         <cp:nationalCadastralReference/>
      </cp:CadastralParcel>
   </gml:featureMember>
<!-- Si se desea entregar varias parcelas en un mismo fichero, se pondra un nuevo featureMember para cada parcela -->
</gml:FeatureCollection>
