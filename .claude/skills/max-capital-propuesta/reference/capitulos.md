# Catálogo de capítulos

Los capítulos son bloques que se combinan libremente: no hay una plantilla fija de
propuesta. Elegís los que el caso pide, en el orden que tenga sentido para ese
cliente, y el renderer garantiza que todos salgan con el mismo diseño.

**Ninguno es obligatorio y ninguno es excluyente.** Una propuesta a un cliente
nuevo probablemente no lleve `cartera_actual`; una revisión de cartera vigente tal
vez no lleve `forma_de_trabajo`.

Índice: [perfil](#perfil) · [hitos](#hitos) · [kpis](#kpis) · [proyeccion](#proyeccion) ·
[glidepath](#glidepath) · [forma_de_trabajo](#forma_de_trabajo) ·
[cartera_sugerida](#cartera_sugerida) · [cartera_actual](#cartera_actual) · [trades](#trades) ·
[distribuciones](#distribuciones) · [instrumentos](#instrumentos) ·
[texto](#texto) · [tabla](#tabla) · [divisor](#divisor) · [cierre](#cierre)

Campos comunes a casi todos: `titulo`, `subtitulo` (bajada de una línea) y `nota`
(nota al pie de la slide, en gris chico).

---

## perfil

Quién es el cliente — **no su perfil de riesgo, sino la persona**. Va primero,
antes de cualquier número, y sirve para devolverle lo que el asesor entendió de
la charla y que lo confirme o corrija.

```json
{
  "tipo": "perfil",
  "titulo": "Punto de partida",
  "subtitulo": "Esto es lo que entendimos de nuestra conversación. Si algo no coincide, corrijámoslo antes de avanzar.",
  "rasgos": [
    { "label": "Edad", "valor": "59 años" },
    { "label": "Horizonte de aportes", "valor": "6 años" },
    { "label": "Dónde invierte hoy", "valor": "Santander, principalmente fondos" }
  ],
  "notas": ["Experiencia como inversor principalmente en fondos. Lo que cambia de esta propuesta:"],
  "puntos": [
    "Portfolio adaptado a las necesidades de inversión.",
    "Nivel de riesgo en función al plazo de inversión.",
    "Gestión activa de rebalanceos."
  ]
}
```

Los `rasgos` se leen como ficha de datos: etiqueta a la izquierda, dato a la
derecha —ambas columnas alineadas a la izquierda, para que todos los datos
arranquen en el mismo eje—. Las `notas` son párrafos y los `puntos`, una lista con viñetas — sirve
cuando lo que cambia la propuesta se enumera en vez de argumentarse en prosa.
Se pueden usar las dos: los párrafos van arriba y la lista debajo.

**Escribilo en segunda persona.** Lo lee el cliente, no es una ficha interna: no
va "Martín es especialista en…" —ya sabe cómo se llama y a qué se dedica—
sino "tu experiencia viene de…". Sigue sirviendo igual como antecedente escrito
de lo acordado; lo que cambia es el registro.

### El recuadro de `destacado`

Al costado de la ficha va un recuadro gris con filete navy. Es para **lo que no
se negocia**: el límite que ordena todo lo que viene después. Uno o dos ítems,
no más — con cuatro deja de destacar nada.

```json
"destacado": {
  "titulo": "Lo que no se negocia",
  "items": [
    { "titulo": "El costo, en renta fija",
      "texto": "Un costo chico se come una parte grande del interés." },
    { "titulo": "Riesgo argentino",
      "texto": "No entra un dólar financiero más." }
  ]
}
```

Cuando hay `destacado`, la ficha y las `notas` comparten la columna izquierda y
el recuadro se queda solo en la derecha: eso es lo que le da el peso. Las dos
columnas miden lo mismo de alto.

Lo que va adentro son **reglas del cliente**, no observaciones de la casa. Si un
ítem es una creencia ("en renta fija el costo importa"), escribilo como la regla
que se desprende de ella.

Una propuesta construida sobre un malentendido se cae en la reunión. Este
capítulo hace barato descubrirlo antes.

---

## proyeccion

Proyección de capital a un horizonte, con **los supuestos siempre a la vista**.

```json
{
  "tipo": "proyeccion",
  "titulo": "Proyección al retiro",
  "subtitulo": "Cifras en USD de hoy: lo que ese dinero compra a precios actuales.",
  "base": "Todas las cifras están en USD de hoy: descuentan la inflación, así que representan poder de compra actual. Debajo de cada número, el equivalente en dólares nominales.",
  "kpis": [
    { "label": "Capital aportado", "valor": "USD 510.000",
      "valor_nominal": "USD 544.217 nominales", "nota": "Inicial + 6 años de aportes" },
    { "label": "Capital al retiro", "valor": "USD 618.446", "accent": true,
      "valor_nominal": "USD 721.416 nominales", "nota": "2032 · 1,2x lo aportado" }
  ],
  "supuestos": [
    { "label": "Acciones", "valor": "10,20%" },
    { "label": "Bonos", "valor": "5,00%" },
    { "label": "Inflación", "valor": "2,60%" }
  ],
  "nota": "Proyección ilustrativa. No contempla impuestos ni costos de transacción."
}
```

Los supuestos van en la misma slide, sin excepción: una proyección sin ellos se
lee como una promesa, y lo que muestra es el resultado de un modelo con
parámetros discutibles.

**Decí en qué moneda están las cifras, arriba y visible.** El campo `base`
dibuja una franja sobre los números. Si la proyección está en moneda constante y
no se aclara, el cliente lee el rendimiento como si fuera nominal y le parece
flojo — sin saber que ya tiene la inflación descontada. `valor_nominal` agrega
el equivalente nominal debajo de cada cifra: los dos números juntos cuentan la
historia completa. Ver criterio 36.

**Cruzá la proyección contra la cartera propuesta antes de emitir.** Si el
modelo asumió rendimientos distintos de los instrumentos que efectivamente se
proponen, decilo — y elegí a conciencia si mantenés el anexo original por
consistencia o recalculás. Ver criterio 14.

---

## glidepath

La trayectoria de la asignación a lo largo del horizonte. Sirve tanto para
mostrar un desarme gradual de riesgo como para mostrar que la asignación **no
cambia** — que también es una decisión y conviene que esté dicha.

```json
{
  "tipo": "glidepath",
  "titulo": "Cómo evoluciona la cartera",
  "tramos": [
    { "label": "59", "acciones": 60, "nota": "2026" },
    { "label": "65", "acciones": 60, "nota": "Retiro · 2032" },
    { "label": "Post-retiro", "acciones": 40, "nota": "A definir", "tentativo": true }
  ],
  "etiqueta_variable": "Renta variable",
  "etiqueta_fija": "Renta fija",
  "nota": "Durante la etapa de aportes la asignación se sostiene en 60/40."
}
```

`acciones` es el porcentaje de renta variable; el resto se dibuja como renta
fija. Los tramos con `"tentativo": true` salen atenuados y punteados: son los
que todavía no están decididos y no deben leerse como compromiso.

Todas las barras miden lo mismo, siempre — es un apilado al 100% y una columna
más corta se leería como "acá hay menos".

---

## kpis

Los números que resumen la propuesta. Se dibujan como tarjetas grandes que ocupan
el canvas, porque en esta slide el número **es** el contenido.

```json
{
  "tipo": "kpis",
  "titulo": "La propuesta en cinco números",
  "subtitulo": "Cartera conservadora en dólares, con liquidez en 48 horas.",
  "items": [
    { "label": "Capital inicial", "valor": "USD 100.000", "accent": true },
    { "label": "Rendimiento esperado", "valor": "6,4%", "nota": "Promedio anual" }
  ],
  "nota": "Los rendimientos son estimaciones y no constituyen garantía."
}
```

`accent: true` pinta la tarjeta en negro: usalo en **una sola** por slide, la que
querés que el cliente mire primero. Hasta 5 items; con más, la tipografía baja
demasiado y conviene partir en dos capítulos.

Siempre que muestres rendimientos esperados, poné la advertencia en `nota`. Es
una estimación, no una promesa, y el PDF tiene que decirlo donde se lo lee.

### Una captura al lado de las tarjetas: `imagen`

Cuando el asesor trae la captura de un gráfico —el rendimiento de SPY desde una
plataforma, el P/E forward de FactSet—, va dentro de la lámina con el campo
`imagen`. Se dibuja un recuadro a la izquierda con título, un valor destacado y la
captura, y las tarjetas en grilla de dos columnas a la derecha, estiradas al alto
de la fila. Pensado para cuatro tarjetas (2×2).

```json
{
  "tipo": "kpis",
  "titulo": "S&P 500: el nivel de entrada llegó",
  "imagen": { "ruta": "grafico-spy.png", "titulo": "SPY desde el 31/05/2026", "valor": "−0,3%" },
  "items": [
    { "label": "P/E forward en mayo", "valor": "~21x" },
    { "label": "P/E forward hoy", "valor": "~19x", "accent": true },
    { "label": "Promedio 5 años", "valor": "~20x" },
    { "label": "Promedio 10 años", "valor": "~19x" }
  ],
  "nota": "Fuente: FactSet. SPY: rendimiento del 31/05 al 16/09/2026."
}
```

- `ruta` se busca desde el directorio actual y desde la carpeta del JSON. La
  imagen se incrusta en el PDF, como la foto de portada.
- El recuadro mide lo que mide la imagen: no queda aire debajo. La imagen nunca
  se deforma; el generador lo controla.
- **La captura va recortada al gráfico**, sin pestañas, menús ni selectores de la
  plataforma, y **la `nota` dice la fuente y el período**. Ver criterio 87.
- Una captura muy alta —cuadrada o vertical— desborda la lámina y el generador
  lo avisa: recortala o usá otra.

**`posicion: "abajo"` para capturas muy apaisadas.** Una serie temporal recortada
suele venir en 3:1 o más, y en media lámina queda ilegible. Con este campo las
tarjetas pasan arriba, en una fila a lo ancho, y la captura ocupa toda la lámina
debajo.

```json
"imagen": { "ruta": "img/simulacion.png", "posicion": "abajo" }
```

Acepta `abajo`, `debajo`, `ancho`, `full` o `completo`. Sin el campo, el layout es
el de siempre: captura a la izquierda y tarjetas 2×2.

- **De 3:1 para arriba, a lo ancho.** Más cuadrada que eso conviene al costado,
  que deja las tarjetas más grandes.
- Si el bloque `imagen` **no trae `titulo` ni `valor`**, la captura va sin recuadro
  interno: el recuadro sólo le roba alto y el marco ya lo da el borde de la
  imagen. Si los trae, usa el recuadro de siempre.
- Las tarjetas tienen **alto fijo**, no se estiran al alto de la captura. Así dos
  láminas seguidas con capturas de distinta proporción no hacen saltar las
  tarjetas al pasar de una a otra. Ver criterio 91.

Ver criterio 90.

---

## forma_de_trabajo

Cómo es la relación con el cliente: rol, custodia, reporting, revisiones. Va
temprano en el deck porque ordena la expectativa antes de hablar de instrumentos.

```json
{
  "tipo": "forma_de_trabajo",
  "titulo": "Cómo trabajamos",
  "intro": "Nuestro rol es el de asesor. La cuenta permanece a nombre del cliente.",
  "pasos": [
    { "titulo": "Definimos el mandato", "texto": "Objetivo, horizonte y límites por escrito." },
    { "titulo": "Construimos la cartera", "texto": "Sin managers intermedios ni capas de fees." }
  ]
}
```

`remate` cierra la slide con una línea sobre filete navy: lo que el asesor quiere
que quede resonando, o preguntado, después de la lista.

Los pasos se numeran solos. Hasta 6 por slide (4 o menos quedan en 2 columnas, 5-6
en 3 columnas); con más, se parte en varias slides.

Adaptá el texto al cliente: lo que un family office necesita oír sobre custodia no
es lo que necesita oír una tesorería corporativa sobre cash management. Este es el
capítulo donde el tono del cliente más importa.

---

## hitos

Línea de tiempo sobre fondo navy: qué pasa, en qué orden y cuándo. Va a fondo
completo porque es la slide que el cliente se lleva de la reunión.

```json
{
  "tipo": "hitos",
  "titulo": "Por dónde empezamos",
  "subtitulo": "Por la parte que hoy operás vos.",
  "hitos": [
    { "cuando": "Hoy", "texto": "Cerramos los cuatro compromisos." },
    { "cuando": "Próxima semana", "texto": "Abrimos la cuenta." },
    { "cuando": "A los 90 días", "texto": "Primer performance review." }
  ]
}
```

Se numeran solos (01, 02, 03). Tres o cuatro hitos: con más, cada columna se
angosta hasta que el texto deja de leerse. Alias: `timeline`, `proximos_pasos`.

**No es `forma_de_trabajo`.** Ese capítulo describe *cómo* se trabaja; este dice
*qué pasa cuándo*. Si el deck lleva los dos, van separados y no se repiten.

---

## cartera_sugerida

El capítulo central. KPIs opcionales de encabezado + tabla de detalle.

```json
{
  "tipo": "cartera_sugerida",
  "titulo": "Cartera sugerida",
  "subtitulo": "Renta fija en dólares como núcleo.",
  "columnas": ["clase", "descripcion", "riesgo", "rendimiento", "plazo", "monto", "ponderacion"],
  "kpis": [ { "label": "Total a invertir", "valor": "USD 100.000", "accent": true } ],
  "items": [
    { "clase": "Renta Fija", "descripcion": "Money Market USD", "riesgo": "Bajo",
      "rendimiento": "3,0%", "plazo": "6 meses", "monto": "USD 20.000", "ponderacion": "20,0%" }
  ],
  "total": { "clase": "Total", "riesgo": "Bajo", "rendimiento": "6,4%", "monto": "USD 100.000" },
  "nota": "Trailer promedio ponderado: 0,96% anual."
}
```

`columnas` elige qué mostrar y en qué orden. Claves con encabezado y alineación ya
**`subtotales: true`** agrega una fila de cierre por grupo. Necesita
`agrupar_por`. Suma **toda columna aditiva** —montos, porcentajes y puntos, cada
una en su formato—: la ponderación, pero también un "antes", un "después" y una
"variación". Así se arma la tabla de la cartera resultante por tipo de riesgo
del criterio 84.

Nunca suma columnas que no se agregan sumando —`rendimiento`, `tir`, `duration`,
`precio`, `plazo`, `riesgo`, `volatilidad` y parecidas—: quedan en blanco. Si una
columna propia tiene que sumarse o no, forzalo con `"sumar": true` o `false` en
su definición. Un grupo de una sola línea no lleva subtotal: repetiría el mismo
número dos veces seguidas. Además de informar, le da aire a una tabla larga.

**Tabla de hoy y objetivo por tipo de riesgo** (criterio 84). Agrupada por clase
de activo, con el gap en USD que hay que cubrir para llegar al objetivo:

```json
{
  "tipo": "cartera_sugerida",
  "titulo": "Hoy y objetivo, por tipo de riesgo",
  "agrupar_por": "clase",
  "subtotales": true,
  "columnas": [
    { "clave": "clase", "titulo": "Clase de activo" },
    { "clave": "descripcion", "titulo": "Tipo de riesgo" },
    { "clave": "hoy", "titulo": "Hoy", "align": "r" },
    { "clave": "objetivo", "titulo": "Objetivo", "align": "r" },
    { "clave": "gap", "titulo": "Gap a cubrir", "align": "r" }
  ],
  "items": [
    { "clase": "Renta Variable", "descripcion": "Equity Int",
      "hoy": "18,1%", "objetivo": "48,0%", "gap": "+USD 367.500" },
    { "clase": "Renta Variable", "descripcion": "Equity Arg",
      "hoy": "1,0%", "objetivo": "1,0%", "gap": "USD 0" },
    { "clase": "Renta Fija", "descripcion": "ON",
      "hoy": "11,6%", "objetivo": "30,0%", "gap": "+USD 227.000" },
    { "clase": "Liquidez", "descripcion": "Cash",
      "hoy": "69,3%", "objetivo": "21,0%", "gap": "−USD 594.500" }
  ],
  "total": { "clase": "Total", "hoy": "100,0%", "objetivo": "100,0%", "gap": "USD 0" }
}
```

El gap se carga con signo: `+` si hay que comprar, `−` si hay que vender, `USD 0`
si no se toca. En el PDF el signo se convierte en color y la celda sale sin él:
verde para comprar, rojo para vender (criterio 89). Los subtotales lo suman con
signo y se pintan igual. La
base es la cartera que administramos, y el total cierra en `USD 0` cuando las
compras salen de su propia liquidez. La variación en puntos (`"−7,7 pp"`) sigue
disponible para cuando no hay que dimensionar una operación.

**`barra`** es una columna que dibuja el peso de cada fila como barra
horizontal. Se escala contra la fila más pesada, no contra 100%: en una cartera
de diez líneas ninguna pasa del 20%, y contra 100% todas quedarían igual de
cortas. **Un solo color** — las barras comparan tamaños entre sí, no señalan
bueno y malo. Y **sin pista de fondo**: ver criterio 60.

**No la pongas al lado de una columna de porcentaje.** Dicen el mismo dato dos
veces, y el que se lee es el número. Ahí no aporta: ocupa ancho, alarga la tabla
a lo horizontal y ensucia una lámina que ya se entendía. Si además hay
subtotales, el ojo ya tiene dónde apoyarse y la barra sobra del todo.

*Dónde sí sirve:* cuando la tabla muestra montos pero **no** porcentajes y aun
así querés que se vea la proporción entre líneas. Ahí la barra es la única que
cuenta el peso relativo, y evita agregar una columna de porcentajes que nadie
pidió.

*Frente a un donut de componentes* tiene la ventaja de no competir por lugar con
la tabla, no repetir las etiquetas en una leyenda y no quedarse sin colores con
más de siete líneas. Pero si la lámina ya mostró la composición por clase de
activo antes, ni el donut ni la barra agregan: eso ya está contado.

**`agrupar_por`** evita repetir el valor de una columna: con `"agrupar_por":
"clase"` la etiqueta se escribe una vez por bloque y las filas siguientes la
dejan vacía, con un filete arriba de cada grupo. Diez filas que dicen "Renta
fija" no informan diez veces. **Los ítems tienen que venir ya ordenados por esa
columna** — la tabla no reordena. Y conviene que la columna agrupada vaya
primera: así el rótulo encabeza el bloque en lugar de quedar colgado en el medio.

**`grafico`** agrega un donut a la derecha de la tabla, con la misma forma que en
`distribuciones`. Sólo se dibuja si la cartera entra en una sola slide: partido
en dos no dice nada. Va por clase de activo, no por componente — con diez gajos
los colores dejan de distinguirse.

definidos: `clase`, `descripcion`, `riesgo`, `rendimiento`, `plazo`, `monto`,
`ponderacion`, `geografia`, `custodia`, `duration`, `vencimiento`, `tir`, `moneda`,
`precio`, `nominal`, `trailer`. Cualquier otra clave también funciona (el
encabezado se genera del nombre).

Elegí las columnas según el tipo de cartera: una de bonos pide `duration` y
`vencimiento`; una de fondos pide `custodia` y `trailer`. Más de 7 columnas
aprieta demasiado la tabla en 16:9.

Si hay más filas de las que entran, se parte sola en varias slides y la fila de
`total` va en la última.

---

## cartera_actual

La posición vigente y qué hacer con ella. Acepta la foto de posiciones, el bloque
de acciones, o las dos cosas: se arma con lo que haya.

```json
{
  "tipo": "cartera_actual",
  "titulo": "Situación actual",
  "columnas": ["descripcion", "clase", "monto", "ponderacion"],
  "items": [ { "descripcion": "Plazo fijo USD", "clase": "Liquidez", "monto": "USD 45.000" } ],

  "titulo_acciones": "Qué comprar y qué vender",
  "intro_acciones": "El movimiento central es sacar 70% de liquidez improductiva.",
  "acciones": {
    "comprar":  [ { "nombre": "Pimco Income", "monto": "USD 15.000", "razon": "Ancla de estabilidad global." } ],
    "vender":   [ { "nombre": "Plazo fijo USD", "monto": "USD 45.000", "razon": "Rinde por debajo de la inflación en dólares." } ],
    "mantener": [ { "nombre": "Global 2035", "monto": "USD 30.000", "razon": "Rendimiento adecuado; se reduce al vencimiento." } ]
  }
}
```

El bloque de acciones sale en su propia slide, en tres columnas con borde superior
verde / rojo / gris. Podés omitir cualquiera de las tres listas.

`razon` es lo que convierte este capítulo en algo accionable: sin el porqué, es
una lista de órdenes. Una frase por posición, concreta — qué gana el cliente con
ese movimiento, no una categoría genérica.

**También sirve por clase de activo en vez de por posición**, y ésa suele ser la
forma correcta: poné la clase en `nombre` ("Liquidez en pesos", "ONs corporativas
argentinas") y el peso en `monto` ("de 45% a 10%", "USD 1,8M"). El cliente ve la
estrategia sin la lista de tickers, que es del asesor — criterio 94. Vale igual
para `trades`.

---

## trades

Movimientos emparejados: qué sale y qué entra en cada uno. Es el hermano de
`cartera_actual` y resuelve el caso contrario — ver criterio 63.

Usá `cartera_actual` cuando cada posición se justifica sola contra el mandato
("esto pesa de más, esto falta"). Usá `trades` cuando el argumento es la
comparación entre dos instrumentos: sale este bono, entra este otro, y ninguno de
los dos se entiende sin el otro.

```json
{
  "tipo": "trades",
  "titulo": "El rebalanceo propuesto",
  "subtitulo": "Cada venta tiene su compra.",
  "titulo_razones": "Por qué cada movimiento",
  "items": [
    { "etiqueta": "Rebalanceo 1",
      "sale": "ON Otamerica 6,69% 2026",
      "entra": "FCI Max Renta Fija Dólares",
      "monto": "USD 10.625",
      "razon": ["El bono vence el 23 de octubre.",
                "El fondo rescata en 24 horas, así que el capital sigue rindiendo."] }
  ],
  "nota": "Los montos no se suman: el fondo es estación de paso."
}
```

Salen **dos slides**: la tabla de movimientos y, debajo, una lámina con una
columna por movimiento con su porqué. `razon` acepta un string o una lista de
párrafos, y los movimientos sin razón simplemente no aparecen en la segunda.

`etiqueta` es opcional; sin ella numera "Movimiento 1", "Movimiento 2". Hasta 4
movimientos por lámina de razones, después se parte.

**`sale` y `entra` también aceptan clases de activo**, no sólo instrumentos: "ONs
corporativas argentinas" → "CEDEARs de ETFs", con el monto agregado del tramo. El
ejemplo de arriba está por posición porque es el caso más claro de leer, pero la
propuesta que va al cliente casi siempre se cuenta por clase — el ticker, el
nominal y el precio los decide el asesor al operar (criterio 94). Si leíste este
capítulo y lo descartaste por eso, era esto lo que faltaba ver.

**La razón nunca va como quinta columna de la tabla.** El texto largo parte las
filas en dos y una fila del doble de alto es lo primero que se ve — criterio 59.

**Ojo con la fila de total.** Si los movimientos están encadenados —el producido
de uno alimenta al siguiente— sumarlos cuenta el mismo dinero dos veces. Ahí no
va total, y la `nota` explica por qué.

---

## distribuciones

Cómo queda repartida la cartera. Hasta 3 gráficos por slide.

```json
{
  "tipo": "distribuciones",
  "titulo": "Cómo queda distribuida",
  "graficos": [
    { "titulo": "Por clase de activo", "tipo": "donut",
      "items": [ { "label": "Renta Fija", "valor": 90 }, { "label": "Estructurados", "valor": 10 } ] },
    { "titulo": "Por nivel de riesgo", "tipo": "barras",
      "items": [ { "label": "Bajo", "valor": 70 } ] }
  ]
}
```

`tipo` puede ser `donut` o `barras`. Si lo omitís, elige solo: donut hasta 7
categorías, barras a partir de ahí (un donut de 12 gajos no se lee).

**Series que cruzan el cero: `eje_cero` y `unidad`.** Aportes netos por año, un
flujo de caja, variaciones contra el período anterior. Alcanza con que haya un
valor negativo —el generador lo detecta y manda la serie a barras, porque un
gajo de donut no tiene ángulo negativo—; `"eje_cero": true` lo fuerza cuando
todos los valores son positivos pero el cero igual es la referencia.

```json
{ "titulo": "Aportes netos", "unidad": "USD", "items": [
    { "label": "2023", "valor": -380000 },
    { "label": "2024", "valor": 500000 },
    { "label": "2025", "valor": 2400000 } ] }
```

El cero queda donde le toca según el rango y las barras salen para los dos lados,
verde y rojo. `unidad` rotula con la magnitud abreviada —`USD 2,4M`, `−USD 380K`,
el negativo con signo y el positivo pelado— en lugar de tratar los valores como
porcentajes; con `"%"` o sin el campo, se comporta como siempre. Una serie con
`unidad` en moneda no se normaliza ni se controla contra 100.

**`"orientacion": "vertical"` las dibuja como columnas**, con los rótulos abajo:
es la forma de leer una serie por año, con el tiempo corriendo de izquierda a
derecha. Sin el campo salen horizontales, como el resto de los gráficos del deck.
Ver criterio 97.

**Cuando la slide compara un antes con un después, agregá `deltas`.** Se dibujan
**arriba de los gráficos** y dicen cuánto se movió cada cosa, que es la
conclusión: dos donuts lado a lado obligan al lector a restar de memoria. La
conclusión primero, el detalle debajo.

```json
"deltas": [
  { "label": "Riesgo argentino", "valor": "−34,1 pp", "nota": "47,0% → 12,9%", "destacado": true },
  { "label": "Renta variable", "valor": "+2,8 pp", "nota": "49,5% → 52,3%" }
]
```

`destacado: true` pinta la tarjeta en negro — una sola, la que importa.

**El capítulo también acepta `kpis`**, con la misma forma que en `cartera_sugerida`.
Sirve para armar una ficha de portfolio: las métricas de rendimiento y riesgo
arriba, y debajo cómo está compuesto. Es la forma de mostrar un vehículo que el
cliente todavía no conoce.

Los porcentajes los calcula el renderer sobre el total, así que no hace falta que
sumen 100 ni que los prepares.

**Dos gráficos de la misma lámina no pueden dar dos números a la misma etiqueta.**
Si un vehículo trae adentro una clase que la cartera no tenía —oro dentro de una
cuenta administrada de CEDEARs de ETFs—, decidí una sola vez si se abre como
categoría propia y propagá a los dos gráficos, a los `deltas` y al texto. El
validador lo avisa. Ver criterio 95.

**Cantidad de gráficos por fila.** Un gráfico solo ocupa media fila (criterio 81).
Con tres, cada tarjeta mide un tercio y el donut se apila sobre su leyenda en vez
de ponerse al lado: apilados no compiten por el ancho, así que el donut crece a
132px y llena el alto de la fila. Si una leyenda toca el borde —muchas categorías
con etiquetas largas— el generador lo avisa: acortá las etiquetas o pasá a dos
gráficos por fila. Ver criterio 86.

---

## flujo_de_fondos

Lo que pagan los bonos de la cartera mes a mes, en los próximos 12 meses: renta y
amortización apiladas, con el total de cada mes encima. Para el deck y el
documento largo; no va en el one-pager.

**Sólo se arma si el asesor lo pide.** Y el insumo lo trae él: el flujo de fondos
de cada bono —la exportación en xlsx de la plataforma, con las columnas "Flujo de
fondos c/100 vn"— y los nominales de cada posición. Si pide la lámina y no los
trajo, pedíselos. **Nunca calcules cupones de memoria.** Ver criterio 88.

```json
{
  "tipo": "flujo_de_fondos",
  "titulo": "Flujo de fondos de la cartera",
  "subtitulo": "Lo que pagan los bonos en los próximos 12 meses.",
  "moneda": "USD",
  "desde": "09/2026",
  "posiciones": [
    { "ticker": "LUC5O", "nominales": 150000, "archivo": "LUC5O.xlsx" },
    { "ticker": "MCC3O", "nominales": 100000, "archivo": "MCC3O.xlsx" },
    { "ticker": "BONO27", "nominales": 50000, "pagos": [
        { "fecha": "15/12/2026", "renta": 3.5, "amortizacion": 0 },
        { "fecha": "15/03/2027", "renta": 3.5, "amortizacion": 100 } ] }
  ]
}
```

- **`archivo`** es el xlsx del bono. Se lee la fecha de pago efectiva y la
  amortización y el interés **cada 100 VN**; las columnas de flujo simulado se
  ignoran, porque dependen del nominal que cargó quien exportó. La ruta se busca
  desde el directorio actual y desde la carpeta del JSON.
- **`pagos`** es la alternativa a mano, también cada 100 VN, para un bono del que
  no hay archivo.
- **`nominales`** son los de la posición del cliente. El generador multiplica y
  suma por mes: la cuenta no se hace al escribir el JSON.
- **`desde`** es el primer mes (`mm/aaaa`). Si falta, arranca en el mes de la
  fecha de la propuesta. Los pagos anteriores se ignoran.

Arriba van cuatro tarjetas que calcula solo —renta, amortización y total de los
12 meses, y lo que se cobra **después** de los 12 meses—. `kpis` las reemplaza si
el asesor quiere otras, por ejemplo TIR y duration promedio.

Lo posterior a los 12 meses va en una tarjeta y **nunca como barra**: al lado de
meses de cuatro cifras, una barra de cientos de miles aplasta el gráfico y los doce
meses parecen iguales. En cambio, si un bono amortiza dentro de la ventana, esa
barra sí domina el gráfico: es el dato real, y se deja.

El validador avisa si a un bono le falta el archivo, los pagos o los nominales, y
si su amortización no suma 100 cada 100 VN, que suele ser un calendario
incompleto.

---

## instrumentos

Qué hace cada componente de la cartera. Es el capítulo que más aprovecha los fact
sheets que aporte el asesor.

```json
{
  "tipo": "instrumentos",
  "titulo": "Qué hace cada componente",
  "fichas": [
    {
      "nombre": "FCI Max Renta Fija USD",
      "tipo": "Fondo propio",
      "monto": "USD 56k",
      "riesgo": "Bajo",
      "que_hace": "Renta fija corporativa argentina en dólares, corto plazo y alta calificación. Es donde nuestra selección de crédito local agrega valor.",
      "datos": [ { "label": "Rendimiento", "valor": "8,0%" }, { "label": "1 año", "valor": "9,5%" } ]
    }
  ]
}
```

`que_hace` es **el rol que cumple la posición dentro de esta cartera**, no un
resumen del fact sheet. "Es el colchón de liquidez: cubre el rescate de 48 horas
sin desarmar ninguna otra posición" le dice algo al cliente; "fondo money market
que invierte en instrumentos de corto plazo" le repite la categoría. Una o dos
frases.

`datos` acepta dos formas. Como par —`{"label": "TIR", "valor": "6,6%"}`— sale
como métrica. Como **texto suelto** —`"Custodia USA"`— sale como etiqueta, sin
cifra: sirve para clasificar la posición por rol, horizonte o jurisdicción.

Cuando la lámina propia del producto ya muestra sus números, las fichas de "a
dónde van los fondos" funcionan mejor con etiquetas: el lector está comparando
para qué sirve cada destino, no todavía cuánto rindió.

`datos` son las 2-4 métricas que importan para ese rol, sacadas del fact sheet.
No copies la ficha entera: si el argumento es la liquidez, el dato es el plazo,
no el desvío estándar.

`monto` y `riesgo` van en la esquina derecha de la ficha, el monto arriba. Los
dos son opcionales y se pueden usar juntos o por separado.

**Cuando la lámina dice a dónde van los fondos, el monto es lo que el cliente
busca y la pill de riesgo compite con él.** En ese caso va sólo el monto, y el
nivel de riesgo se cuenta en la lámina propia de cada producto. **Los montos de
esta esquina se redondean a miles** —`USD 235k`, no `USD 234.710`—: es un
titular, y el número exacto ya está en la tabla de la cartera.

Hasta 6 fichas por slide (4 o menos en 2 columnas, 5-6 en 3); con más se parte.

---

## texto

Prosa en columnas. Es el capítulo para argumentar: síntesis, contexto, visión de
mercado, por qué esta cartera y no otra.

```json
{
  "tipo": "texto",
  "titulo": "Por qué esta cartera y no otra",
  "columnas": [
    { "titulo": "El punto de partida", "parrafos": ["70% está en liquidez improductiva.", "Protege el nominal pero pierde poder adquisitivo."] },
    { "titulo": "Qué cambia", "parrafos": ["Ese 70% pasa a renta fija en dólares."] }
  ]
}
```

`formato: "tarjetas"` dibuja cada columna como una tarjeta gris con filete navy
arriba, todas del mismo alto. Es para columnas que se comparan entre sí, no para
un argumento que corre de izquierda a derecha. Con `label` la tarjeta lleva
volanta encima del título.

Hasta 4 columnas. Párrafos cortos: en una slide, tres frases por columna es el
techo de lo legible. Los alias `sintesis` y `vision_mercado` hacen lo mismo y
existen sólo para que el JSON se lea mejor.

---

## tabla

Escotilla de escape para cualquier cosa que el catálogo no cubra: curvas, escalas
de fees, comparaciones, movimientos, cronogramas.

```json
{
  "tipo": "tabla",
  "titulo": "Escala de management fee",
  "headers": ["Patrimonio administrado", "Fee anual"],
  "filas": [["Hasta USD 1.500.000", "1,00%"], ["USD 1.500.000 – 3.000.000", "0,85%"]],
  "alineacion": "lr",
  "total_ultima_fila": false
}
```

`alineacion` es una letra por columna: `l` izquierda, `c` centro, `r` derecha.
`total_ultima_fila: true` destaca la última fila como total. Se pagina sola.

**Columnas de flujo: `signo`.** Por defecto una celda que trae `+` o `−` se pinta
por su signo y se imprime sin él (criterio 89): el color dice la dirección. Eso
sirve para una columna de **resultado**, donde rojo significa "perdió". En una
columna de **flujo** —aportes netos, suscripciones y rescates, un flujo de caja—
el rojo miente, porque un retiro no es una pérdida, y sin el signo `USD 380.000`
se lee como un aporte cuando fue lo contrario. Esas columnas escriben el signo y
no se pintan:

```json
{ "tipo": "tabla",
  "headers": ["Año", "Aportes", "Retiros", "Neto", "Resultado"],
  "alineacion": "lrrrr",
  "signo": ["Neto"],
  "filas": [["2023", "USD 120.000", "−USD 500.000", "−USD 380.000", "+USD 88.400"]] }
```

`signo` acepta la lista de encabezados, la lista de posiciones (`[3]`), o `true`
para toda la tabla.

**Un nombre de la lista también selecciona una fila.** Un corte anual corre al
revés —los años en las columnas y el concepto en la primera celda de cada fila—
y ahí la excepción cae sobre la fila, no sobre la columna:

```json
{ "tipo": "tabla",
  "headers": ["", "2025", "2026"],
  "alineacion": "lrr",
  "signo": ["Aportes netos"],
  "filas": [["Aportes netos", "USD 1.943.736", "−USD 251.115"],
            ["Resultado",     "−USD 75.100",   "USD 632.706"]] }
```

Ahí "Aportes netos" conserva el signo y "Resultado" se sigue pintando por él, que
es lo correcto: un retiro no es una pérdida, un resultado negativo sí. Las
posiciones (`[3]`) siguen nombrando columnas y sólo columnas.

---

## divisor

Separador de sección: fondo azul de marca, número correlativo y título grande.
No lleva contenido.

```json
{ "tipo": "divisor", "titulo": "La cartera propuesta", "subtitulo": "Seis posiciones, seis funciones." }
```

Se numeran solos en el orden en que aparecen. Útiles en decks de más de 8 slides;
en uno corto sólo agregan páginas.

En el one-pager y en el documento largo se ignoran.

---

## cierre

Slide final: agradecimiento, URL, datos del asesor y el disclaimer legal.

```json
{ "tipo": "cierre", "titulo": "¡Muchas gracias!" }
```

No hace falta declararlo: si el deck no tiene uno, se agrega solo. Declaralo sólo
si querés cambiar el título o pasar un `disclaimer` distinto del institucional.
