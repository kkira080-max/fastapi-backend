<?xml version="1.0" encoding="utf-8"?>
<!--Parcela Catastral para entregar a la D.G. del Catastro.-->
<!--Generado por chapulincatastral https://github.com/chapulincatastral/generador-gml/ -->
<gml:FeatureCollection gml:id="ES.SDGC.CP" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:cp="http://inspire.ec.europa.eu/schemas/cp/4.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://inspire.ec.europa.eu/schemas/cp/4.0 http://inspire.ec.europa.eu/schemas/cp/4.0/CadastralParcels.xsd">
<gml:featureMember>
      <cp:CadastralParcel gml:id="ES.LOCAL.CP.FR-34400">
<!-- Superficie de la parcela en metros cuadrados. Tiene que coincidir con la calculada con las coordenadas.-->
         <cp:areaValue uom="m2">16189</cp:areaValue>
         <cp:beginLifespanVersion xsi:nil="true" nilReason="other:unpopulated"></cp:beginLifespanVersion>
<!-- Geometria en formato GML       -->
         <cp:geometry>
<!-- srs Name código del sistema de referencia en el que se dan las coordenadas, que debe coincidir con el de la cartografía catastral -->
<!-- El sistema de referencia de la cartografía catastral varia según provincia, siendo accesible desde la consulta de cartografía en Sede -->  
           <gml:MultiSurface gml:id="MultiSurface_ES.LOCAL.CP.FR-34400" srsName="urn:ogc:def:crs:EPSG::25830"> 
             <gml:surfaceMember>
               <gml:Surface gml:id="Surface_ES.LOCAL.CP.FR-34400" srsName="urn:ogc:def:crs:EPSG::25830">
                  <gml:patches>
                    <gml:PolygonPatch>
                      <gml:exterior>
                        <gml:LinearRing>
<!-- Lista de coordenadas separadas por espacios o en líneas diferentes. El recinto debe cerrarse, el pimer par de coordenadas debe ser igual al último    -->
                          <gml:posList srsDimension="2">662585.11 4212531.34 662584.72 4212531.68 662584.31 4212531.99 662583.88 4212532.26 662583.42 4212532.50 662582.95 4212532.70 662582.47 4212532.87 662581.98 4212533.02 662581.48 4212533.16 662580.98 4212533.28 662580.48 4212533.39 662579.98 4212533.48 662579.47 4212533.56 662578.96 4212533.63 662578.45 4212533.68 662577.94 4212533.69 662577.43 4212533.66 662576.92 4212533.59 662576.41 4212533.48 662575.92 4212533.34 662575.44 4212533.16 662573.85 4212532.49 662531.97 4212580.33 662532.40 4212587.50 662602.03 4212651.49 662616.39 4212635.76 662621.93 4212629.75 662708.86 4212535.55 662707.19 4212533.88 662707.23 4212533.83 662702.03 4212529.08 662700.76 4212522.05 662700.14 4212518.55 662698.30 4212512.03 662697.63 4212508.71 662696.93 4212487.53 662696.13 4212484.65 662695.10 4212480.69 662695.67 4212480.55 662694.95 4212477.23 662671.56 4212482.86 662663.84 4212483.70 662653.67 4212482.55 662643.05 4212482.30 662635.08 4212482.11 662635.12 4212485.98 662635.12 4212492.83 662632.55 4212492.85 662624.78 4212492.90 662624.68 4212495.71 662624.62 4212496.39 662624.49 4212497.07 662624.29 4212497.73 662624.03 4212498.36 662623.70 4212498.97 662623.32 4212499.54 662622.90 4212500.09 662622.46 4212500.62 662621.99 4212501.12 662621.50 4212501.60 662620.99 4212502.06 662620.46 4212502.49 662619.90 4212502.89 662619.30 4212503.24 662618.67 4212503.52 662618.02 4212503.75 662617.36 4212503.91 662616.68 4212504.01 662615.99 4212504.05 662615.30 4212504.03 662597.53 4212504.04 662597.51 4212503.94 662596.96 4212504.02 662596.45 4212504.24 662596.01 4212504.57 662595.64 4212505.00 662595.37 4212505.48 662595.19 4212506.01 662594.55 4212508.77 662593.30 4212514.23 662592.01 4212518.05 662591.97 4212518.04 662590.98 4212520.93 662588.54 4212526.37 662587.19 4212529.02 662585.11 4212531.34 </gml:posList>
                        </gml:LinearRing>
                      </gml:exterior>             
                    </gml:PolygonPatch>
                  </gml:patches>
                </gml:Surface>
              </gml:surfaceMember>
            </gml:MultiSurface>
         </cp:geometry>
         <cp:inspireId xmlns:base="http://inspire.ec.europa.eu/schemas/base/3.3">
           <base:Identifier >
<!-- Identificativo local de la parcela. Solo puede tener letras y numeros. Se recomienda (pero no es necesario) poner siempre un digito de control, por ejemplo utilizando el algoritmo del NIF.-->
             <base:localId>FR-34400</base:localId>
             <base:namespace>ES.LOCAL.CP</base:namespace>
           </base:Identifier>
         </cp:inspireId>
         <cp:label/>
<!--Siempre en blanco, ya que todavia no ha sido dada de alta en las bases de datos catastrales.-->
         <cp:nationalCadastralReference/>
      </cp:CadastralParcel>
 </gml:featureMember>
</gml:FeatureCollection>
