# Resultados de la ejecución con las fuentes entregadas

Verificación realizada el 22 de septiembre de 2026. Se procesaron los siete TXT
ICFES, el CSV CRC y el Excel DANE presentes en `Trabajo Final/Archivos-Datos`.

## Panel obtenido

| Año | Municipios integrados | Puntaje medio entre municipios | Accesos por 100 hogares, media municipal |
| --- | ---: | ---: | ---: |
| 2022 | 1.087 | 238,33 | 15,98 |
| 2023 | 1.090 | 241,11 | 16,59 |
| 2024 | 1.093 | 242,93 | 17,29 |
| 2025 | 157 | 240,89 | 43,41 |

Total: **3.427 filas**, correspondientes a **1.102 municipios distintos**.
2025 solo contiene el periodo ICFES 20251. Sus 157 municipios constituyen una
muestra diferente: el mayor promedio de conectividad no demuestra un aumento
frente a los años anteriores.

## Calidad y cobertura

- Se rechazaron 357.770 registros ICFES por código municipal inválido o vacío.
  El motivo describe un problema para este cruce, no demuestra que el registro
  original sea incorrecto para todos los usos.
- Se rechazaron seis registros DANE de municipio-año por hogares no positivos,
  no integrales o ausentes. El indicador necesita un denominador positivo.
- No hubo rechazos de validación en CRC. De sus 3.288.251 registros, 2.184.153
  quedaron fuera de los años o del segmento residencial solicitado.
- 1.065 llaves municipio-año presentes en alguna fuente no encontraron las tres
  fuentes. Se conservan en el reporte de cobertura, no en el panel analítico.
- Se conservaron seis tasas superiores a 100 accesos por cada cien hogares.
- 2.950 filas no reúnen simultáneamente dos periodos ICFES y cuatro trimestres
  CRC en el mismo municipio-año.

La última señal es descriptiva y conservadora: un municipio puede aparecer
solamente en un periodo ICFES por su oferta de calendarios escolares. No significa
por sí sola que falten registros que deberían existir. Debe distinguirse de la
ausencia confirmada del archivo nacional 20252. No se recomienda excluir todos
los municipios de un solo periodo sin evaluar antes el sesgo que introduciría.

## Comparación con df_final.csv previo

Se compararon código-año, puntaje, accesos y hogares en las llaves comunes.
En **2022–2024** los tres indicadores reproducen la base anterior, con diferencias
numéricas inferiores a `1e-9` debidas a precisión decimal.

Para **2025**, el archivo previo contiene 1.091 municipios, mientras que las
fuentes ICFES disponibles permiten integrar 157. En las llaves comunes, accesos
y hogares coinciden; los puntajes difieren. No se puede reconstruir ni verificar
el puntaje anual previo de 2025 con el único periodo disponible. El proyecto
publica lo calculado desde los originales, sin copiar el resultado anterior.

## Verificación del código

Siete pruebas automáticas comprueban normalización DIVIPOLA, promedio ponderado,
promedio trimestral, cruces sin coincidencia, tasas superiores a 100, denominador
cero, llaves repetidas, cuarentena, invariancia entre tamaños de bloque,
duplicados entre bloques y filtros de CRC.

Consulta `data/latest.json` para ubicar la ejecución vigente. Este documento
describe las fuentes originales de esta entrega; al incorporar archivos nuevos,
los CSV y reportes de la nueva ejecución serán la evidencia actualizada.
