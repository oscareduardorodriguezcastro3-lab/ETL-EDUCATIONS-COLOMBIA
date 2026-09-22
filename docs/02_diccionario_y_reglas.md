# Diccionario y reglas de negocio

## DataFrame unificado Gold

`df_unificado.csv` contiene la unión externa de ICFES, CRC y DANE por código-año.
Incluye los mismos campos del panel y cuatro señales adicionales: `tiene_icfes`,
`tiene_crc`, `tiene_dane` e `integrado` (las tres fuentes presentes). Los valores
ausentes se mantienen nulos. La tasa se puede calcular cuando hay CRC y DANE,
aunque falte ICFES; en ese caso la fila no pertenece a `df_final`.
`tasa_mayor_100` queda nula si no se pudo calcular la tasa. La cobertura temporal
queda falsa cuando no se observan ambos periodos ICFES y los cuatro trimestres.

`df_final` corresponde a `panel_municipio_anio.csv`: la selección integrada del
DataFrame unificado. No debe confundirse con el `df_final.csv` antiguo del origen.

## Panel Gold: una fila por municipio-año

| Campo | Tipo lógico | Definición |
| --- | --- | --- |
| codigo_municipio | Texto de cinco dígitos | Municipio del colegio ICFES, cruzado con CRC y DANE |
| anio | Entero | Año de observación |
| municipio | Texto | Nombre del municipio según DANE |
| departamento | Texto | Departamento según DANE |
| estudiantes | Entero | Registros válidos de examen sumados en los periodos disponibles |
| periodos_icfes | Entero | Periodos con registros válidos para el municipio-año |
| puntaje_global | Decimal | Suma de puntajes / registros válidos |
| accesos_residenciales | Decimal | Media de totales trimestrales residenciales observados |
| trimestres_crc | Entero | Trimestres CRC con datos válidos en el municipio-año |
| hogares | Entero | Proyección DANE del total de hogares |
| accesos_por_100_hogares | Decimal | Accesos medios / hogares × 100 |
| cobertura_temporal_completa | Booleano | Dos periodos ICFES y cuatro trimestres CRC |
| tasa_mayor_100 | Booleano | Indicador mayor a 100, conservado para revisión |

CSV no almacena tipos. Al leerlo, especifica el tipo texto para DIVIPOLA. La
serialización de algunos conteos puede contener `.0` por los nulos transitorios
del cruce externo; conceptualmente siguen siendo enteros.

## Silver

| Tabla | Llave | Medidas y trazabilidad |
| --- | --- | --- |
| icfes_municipio_periodo | codigo_municipio, periodo | suma_puntaje, estudiantes, anio, puntaje_promedio |
| crc_municipio_trimestre | codigo_municipio, anio, trimestre | accesos residenciales totales |
| dane_municipio_anio | codigo_municipio, anio | hogares, municipio, departamento, fila_excel |

## Contratos

- DIVIPOLA: de uno a cinco dígitos en origen, completado con ceros a la izquierda.
  Cadenas decimales, vacías, alfabéticas y de más de cinco dígitos se rechazan.
- ICFES: puntaje numérico entre 0 y 500; periodo coincidente con nombre; ID no vacío.
  Un ID repetido dentro del periodo provoca fallo, para revisar su significado.
- CRC: año integral entre 1900 y 2100, trimestre 1–4, accesos enteros no negativos.
  Luego se filtra por años solicitados y segmento residencial.
- DANE: área Total, hogares enteros positivos, código válido y llave única.
- Gold: llaves únicas por fuente y cruce validado uno a uno. Sin imputaciones.

## Resultados de auditoría

`manifest.json` vincula originales y copias mediante SHA-256. `report.json`
guarda configuración, versión, estado y conteos. `pipeline.log` muestra avance
y errores. `balance_fuentes.csv` informa registros por fuente. `rechazos.csv`
ubica registros inválidos. `cobertura_cruces.csv` muestra por cada llave si existe
ICFES, CRC, DANE y si fue integrada.

Las filas inválidas se excluyen y quedan contadas. El proceso no impone un umbral
de porcentaje de rechazos: el analista debe revisar el reporte antes de usar el
panel. Los fallos estructurales, duplicidad de llaves y fuentes vacías detienen
la publicación. Los años parciales y tasas mayores de 100 no la detienen.
