# El JSON de la propuesta — contrato de datos

Este es el único contrato entre la interpretación (lo que hacés vos leyendo lo que
subió el asesor) y el diseño (lo que hace `generate_propuesta.py`). Si el JSON es
correcto, el PDF sale bien: no hay nada más que ajustar a mano.

Todo campo es opcional salvo `cliente` y `capitulos`. Lo que falta simplemente no
se dibuja — nunca aparece "None" ni una caja vacía en el PDF.

## Estructura raíz

```json
{
  "cliente":   { "nombre": "Cliente Ejemplo S.A." },
  "asesores":  [ { "nombre": "...", "cargo": "...", "email": "...", "telefono": "..." } ],
  "fecha":     "27/08/2026",
  "anio":      "2026",
  "titulo":    "Propuesta de Inversión",
  "subtitulo": "Una frase que resume la tesis de la propuesta.",
  "objetivo":  "Preservación de capital a mediano plazo",
  "mandato":   "USD 1.500.000",
  "portada":   { "imagen": "/ruta/a/foto.jpg" },
  "fecha_corta": "ago/2026",
  "capitulos": [ ... ]
}
```

| Campo | Dónde se ve |
|---|---|
| `cliente.nombre` | Portada, pie de cada slide, pie del documento |
| `asesores` | Bloque "Presentado por" en portada, slide de cierre, pie del one-pager. Es una **lista**: lo habitual es que sean dos. `asesor` en singular sigue valiendo para uno solo. Preguntá siempre quiénes van — ver criterio 43 y [`equipo.md`](equipo.md) |
| `fecha` | "Datos al …" en la portada del deck |
| `fecha_corta` | Fecha junto al cliente en el encabezado del one-pager. Si falta, se deriva de `fecha` (`27/08/2026` → `ago/2026`) |
| `anio` | Pill de la portada. Si falta, se toman los 4 últimos caracteres de `fecha` |
| `titulo` | Título grande de portada y encabezado del one-pager |
| `subtitulo` | Bajada de portada. Una frase, no un párrafo |
| `objetivo` | Banda "OBJETIVO" del one-pager |
| `mandato` | Metadatos de la portada del documento largo |
| `portada.imagen` | Foto de fondo de la portada del deck. Si no hay, usa el degradado de marca |

`portada.imagen` se incrusta en base64: el PDF queda autocontenido, pero una foto
grande pesa. Usá una imagen ya recortada a 16:9 y por debajo de ~500 KB.

## Capítulos

`capitulos` es una lista **ordenada**. Cada elemento tiene un `tipo` y los campos
que ese tipo necesita. El orden de la lista es el orden del deck.

```json
"capitulos": [
  { "tipo": "kpis", "titulo": "...", "items": [...] },
  { "tipo": "divisor", "titulo": "La cartera propuesta" },
  { "tipo": "cartera_sugerida", "titulo": "...", "items": [...] }
]
```

El catálogo completo de tipos, con los campos de cada uno, está en
[`capitulos.md`](capitulos.md).

## Sinónimos de campos

El lector de JSON acepta varios nombres para la misma cosa, porque las hojas de
cada asesor vienen rotuladas distinto y no tiene sentido que la propuesta falle
por eso. En cada par, ambos son válidos:

- `titulo` / `title`
- `valor` / `value`
- `items` / `posiciones` / `instrumentos`
- `descripcion` / `instrumento` / `nombre`
- `rendimiento` / `rendimiento_esperado` / `tir` / `ytm`
- `monto` / `monto_a_invertir` / `importe`
- `ponderacion` / `peso` / `participacion`
- `riesgo` / `nivel_riesgo` / `nivel_de_riesgo`
- `razon` / `motivo` / `por_que`

## Cómo se escriben los números

**Los números van como texto, ya formateados.** El renderer no formatea: imprime
lo que le des. Eso es deliberado — el formato de un monto es una decisión del
asesor (si va con símbolo, con decimales, en qué moneda) y no algo que convenga
adivinar.

```json
"monto": "USD 20.000",     ✅  sale exactamente así
"monto": 20000,            ⚠️  sale "20000", sin separadores ni moneda
"rendimiento": "6,4%",     ✅
"rendimiento": "+2,1%",    ✅  el "+" lo pinta en verde
"rendimiento": "-0,8%"     ✅  el "-" lo pinta en rojo
```

Convención del equipo: separador de miles con punto, decimales con coma,
moneda adelante (`USD 136.367`, `$ 748.933.521`), porcentajes con una decimal.

La excepción son los **gráficos**: ahí `valor` sí puede (y conviene que sea) un
número, porque el renderer calcula los porcentajes sobre el total.

```json
{ "label": "Renta Fija", "valor": 90 }
```

Da igual si los valores suman 100 o son montos absolutos: se normalizan solos —
salvo que pases `"normalizar": false`, para barras que comparan magnitudes
independientes en vez de partes de un todo.

## Niveles de riesgo

Se dibujan como pastillas de color en escala **verde → azul → amarillo**:

| Valor | Color |
|---|---|
| `Bajo` / `Conservador` | verde |
| `Medio` / `Moderado` | azul |
| `Alto` / `Agresivo` | amarillo |

Nunca rojo: el rojo queda reservado para resultados negativos y para el bloque de
"vender". Un riesgo alto es una característica del instrumento, no una alarma.

Se reconoce el prefijo, así que "Medio-Alto" toma el color de "Medio". Cualquier
otro texto sale como pastilla neutra.

## Validar antes de renderizar

```bash
python scripts/generate_propuesta.py --json propuesta.json --validar
```

Reporta capítulos sin tipo, tablas vacías, gráficos sin datos y filas con distinta
cantidad de celdas que columnas. Corre siempre esto antes de generar el PDF: es
instantáneo y evita descubrir una tabla vacía mirando la hoja final.


## Campos que se agregaron sobre la marcha

Aparecieron resolviendo casos reales. Ninguno es obligatorio.

| Campo | Dónde | Para qué |
|---|---|---|
| `resumen` | ficha de `instrumentos` | Versión corta (una cláusula) que usa el one-pager. Sin él, el one-pager recorta `que_hace` a 150 caracteres |
| `normalizar` | gráfico de `distribuciones` | `false` cuando las barras comparan magnitudes independientes (un antes contra un después) en vez de partes de un todo. Ver criterio 17 |
| `base` | capítulo `proyeccion` | Franja sobre los KPIs con la moneda o base de cálculo. Ver criterio 36 |
| `valor_nominal` | ítem de KPI | Cifra secundaria debajo del valor principal: el equivalente nominal de un número real |
| `puntos` | capítulo `perfil` | Lista con viñetas, además de los párrafos de `notas` |
| `destacado` | capítulo `perfil` | Recuadro gris al costado de la ficha con lo que no se negocia. Uno o dos ítems |
| `tentativo` | tramo de `glidepath` | Dibuja el tramo atenuado y punteado: todavía no está decidido |
| `fecha_corta` | raíz | Período propio para el encabezado, si no alcanza con derivarlo de `fecha` |
| `posicion` | bloque `imagen` de `kpis` | `"abajo"` pone las tarjetas arriba en una fila y la captura a lo ancho debajo. Para capturas de 3:1 o más, que en media lámina quedan ilegibles. Ver criterio 90 |
| `eje_cero` / `eje_en_cero` / `cero` | gráfico de `distribuciones` | Fuerza el eje en cero con barras para los dos lados. Se activa solo si algún valor es negativo. Ver criterio 97 |
| `orientacion` / `orientation` | gráfico de `distribuciones` con eje en cero | `"vertical"` lo dibuja como columnas, para una serie por año. Sin el campo, barras horizontales |
| `unidad` / `unit` / `moneda` | gráfico de `distribuciones` | La unidad del rótulo de las barras: `"%"` (default) o una moneda, que sale abreviada con M/K y con signo. Una serie en moneda no se normaliza ni se controla contra 100 |
| `signo` / `conservar_signo` | capítulo `tabla` | Columnas que escriben el signo en vez de pintarse por él: lista de encabezados, lista de posiciones, o `true`. Para columnas de flujo, donde el rojo diría "perdió" sobre un retiro. Ver criterio 89 |
| `orden` | bloque `acciones` de `cartera_actual` | Secuencia de las columnas, p. ej. `["vender","comprar"]`. Sin él, comprar → vender → mantener. En un rebalanceo se vende primero y recién después se coloca el producido; leerlo al revés obliga al cliente a reconstruir de dónde salió la plata |

### Columnas con encabezado propio

`columnas` acepta objetos además de claves sueltas, para cuando el encabezado por
defecto dice lo contrario de lo que la tabla hace — por ejemplo una tabla de
posiciones **que se venden**, donde "Monto a invertir" no corresponde:

```json
"columnas": [
  { "clave": "descripcion", "titulo": "Instrumento", "align": "l" },
  { "clave": "rendimiento", "titulo": "Resultado realizado", "align": "r" },
  { "clave": "monto", "titulo": "Valuación", "align": "r" }
]
```

`align` es `l`, `c` o `r`.
