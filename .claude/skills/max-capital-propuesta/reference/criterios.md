# Criterios de propuestas

Los criterios del equipo de Wealth Management, cada uno con el porqué y el caso
real del que salió. Leelos antes de armar la primera propuesta: casi todos son
cosas que sólo se descubren mirando un PDF terminado, y varios corrigen errores
que ya se cometieron una vez.

Están ordenados por cuándo aparecieron, no por importancia. **El único que no
tiene excepciones es el 42: nada entra al PDF si no lo pidió el asesor.** Si
tenés que elegir tres más: no inventar datos de la casa (20), lo que la casa
hace o cobra se confirma (34) y escribir desde la mirada del cliente (19).

---

## 1. La clase de cuotaparte no se identifica

En material de cliente el fondo se nombra sin la clase: **"Max Renta Fija
Dólares"**, no "Max Renta Fija Dólares (Clase A)".

*Por qué:* la clase es una distinción comercial interna (fee, mínimo de
suscripción). Al cliente no le agrega información y abre una pregunta que no
hace falta contestar en una propuesta.

*Origen:* revisión del primer one-pager, 27/08/2026.

---

## 2. Nada de gráfico de distribución por vehículo

La torta "por vehículo" o "por fondo" no va nunca: repite exactamente lo que ya
dice la columna de ponderación de la tabla, con menos precisión.

*Por qué:* un gráfico tiene que mostrar algo que la tabla no muestra. Si es la
misma información en otro formato, ocupa espacio sin agregar nada.

*Origen:* revisión del primer one-pager, 27/08/2026.

---

## 3. Un gráfico de distribución solo si la distribución varía

La torta por clase de activo **sí** es relevante en general, pero no cuando la
cartera es de una sola clase. Una propuesta 100% renta fija no necesita un
gráfico que diga "renta fija 100%".

El criterio general: antes de poner un gráfico, mirar si la distribución tiene
dispersión real. Si no la tiene, el corte relevante es otro — en el primer
one-pager la clase de activo era uniforme pero la moneda era 50/50, y esa sí
era la torta que valía.

*Por qué:* un gráfico de una sola categoría no informa, y ocupa el lugar del
corte que sí importaba.

*Origen:* revisión del primer one-pager, 27/08/2026.

---

## 4. En formato compacto, los instrumentos van como nota

En el one-pager, el "qué hace cada instrumento" es una **nota al pie chica**, una
línea por vehículo — o directamente no va. Nunca tarjetas.

El espacio de una hoja sola se lo tienen que quedar la tabla de cartera y las
distribuciones, que es lo que el cliente vino a ver. En el deck es distinto: ahí
los instrumentos son un capítulo propio con tarjetas y datos.

*Implementado:* el campo `resumen` de cada ficha (una cláusula corta) se usa en
el one-pager; `que_hace` (el texto largo) se usa en el deck.

*Origen:* revisión del primer one-pager, 27/08/2026.

---

## 5. El texto legal es el del `CONFIG`, y no se toca por propuesta

El disclaimer y las matrículas viven en el `CONFIG` de
`generate_propuesta.py`. **No se redactan, no se resumen y no se ajustan caso
por caso.** Si hace falta un cambio, se cambia ahí y vale para todas las
propuestas del equipo.

Hay una distinción que sí importa:

- **Una propuesta no puede decir que no es una recomendación.** El disclaimer de
  informes arranca con "no constituye oferta, invitación o recomendación". En
  una propuesta esa frase contradice el contenido del propio PDF, que recomienda
  instrumentos concretos para un cliente concreto. Por eso el texto de
  propuestas reconoce la recomendación y la funda en el perfil que aportó el
  cliente, conservando que no es oferta pública.
- **Las matrículas CNV van completas**, con el texto oficial y una sola vez por
  documento, junto al disclaimer.

*Origen:* pregunta de Pablo, 27/08/2026; texto vigente definido el 28/08/2026.

---

## 6. En propuestas 100% dólares, mostrar el interés compuesto

Cuando toda la cartera está en dólares, la propuesta lleva **renta anual
esperada** y **capital proyectado a N años** capitalizando. Es el modelo que ya
usan las propuestas del equipo: una cartera en dólares muestra "Rendimiento
anual esperado USD 25.500" y "Capital Proyectado a 5 años USD 328.867"; la
cartera conservadora de banca privada muestra "USD 6.400" y "USD 136.367" a 5
años.

*Por qué:* proyectar a varios años solo tiene sentido en moneda dura. En pesos,
capitalizar una tasa nominal produce un número grande que no dice nada, porque
la inflación se come la diferencia — por eso una propuesta mixta o en pesos se
queda en el rendimiento del período y no proyecta.

*Cuándo NO:* carteras con un tramo en pesos o con horizonte
menor a un par de años.

*Origen:* indicación de Pablo, 27/08/2026.

---

## 7. La liquidez de los FCI de Max es 24 horas

No 48. El plazo de liquidación de los fondos es 24 hs y así va en el KPI de
disponibilidad. Las 48 hs corresponden a otros vehículos (fondos de terceros en
la plataforma de Uruguay, por ejemplo), así que el dato hay que tomarlo del
fact sheet de cada instrumento y no por defecto.

*Origen:* corrección de Pablo, 27/08/2026.

---

## 8. Escala de color del nivel de riesgo: verde → azul → amarillo

- **Bajo / Conservador** → verde
- **Medio / Moderado** → azul
- **Alto / Agresivo** → amarillo

Nunca rojo. El rojo queda reservado para resultados negativos y para el bloque
de "vender".

*Por qué:* un nivel de riesgo alto es una característica del instrumento, no un
problema. Pintarlo de rojo lo lee como una alarma y desalienta una posición que
puede estar perfectamente justificada dentro de la cartera.

*Origen:* indicación de Pablo, 27/08/2026.

---

## 9. En el one-pager, la distribución va debajo de la tabla

La tabla de cartera toma el ancho completo de la hoja; los gráficos de
distribución van debajo, en fila. Las tarjetas de KPI arrancan pegadas al
encabezado, sin aire arriba.

*Por qué:* la tabla es lo que el cliente viene a leer y sus columnas necesitan
espacio — con la distribución al costado, la descripción de los instrumentos se
partía en varias líneas. Y con un solo gráfico, la columna lateral dejaba media
hoja vacía.

*Origen:* indicación de Pablo, 27/08/2026.

---

## 10. La nota de instrumentos cierra la hoja

En el one-pager va apoyada contra el disclaimer, al pie, a ancho completo — no
al costado de un gráfico ni flotando en el medio. Es contexto de lectura final,
posterior a la propuesta, y ese es su lugar en el orden de lectura.

*Origen:* indicación de Pablo, 27/08/2026.

---

## 11. Todo documento va fechado y la fecha tiene que verse

Formato **mes/año** (`ago/2026`), en el encabezado, junto al nombre del cliente
y con el mismo tratamiento tipográfico que él —mayúsculas y tracking— apenas más
chica. No en letra chica al pie.

Se fecha por mes y no por día: el día exacto en que se armó la propuesta no le
dice nada al cliente y envejece el documento más rápido de lo que corresponde.
El generador deriva `ago/2026` de la fecha completa automáticamente; el campo
`fecha_corta` permite escribir un período propio si hace falta.

*Por qué:* una propuesta sin fecha visible no se puede archivar ni comparar
contra una posterior — y con tres clientes en paralelo, saber cuál versión es
cuál deja de ser un detalle. La fecha estaba al pie en gris de 7,6px y ni el
propio autor la encontró; si no la ve quien la armó, no la ve el cliente.

*Origen:* indicación de Pablo, 27/08/2026.

---

## 12. Capítulo `perfil` — quién es el cliente

No es el perfil de riesgo: es la persona. Edad, horizonte, dónde invierte hoy,
a qué se dedica, condiciones particulares — y un texto que le devuelve al
cliente lo que el asesor entendió de la charla.

Va **primero**, antes de cualquier número, y con una bajada que invite a
corregirlo. Una propuesta construida sobre un malentendido se cae en la reunión;
este capítulo hace barato descubrirlo antes.

*Implementado:* tipo `perfil`, con `rasgos` (etiqueta/valor, se leen como ficha
de datos) y `notas` (párrafos).

*Origen:* pedido de Pablo sobre la propuesta con proyección de retiro, 28/08/2026.

---

## 13. Capítulo `proyeccion` — con los supuestos a la vista

Los números grandes arriba (capital aportado, rendimiento generado, capital al
retiro, retiro sostenible, TIR) y **los supuestos siempre visibles** en la misma
slide: rendimiento de acciones, de bonos, inflación, tasa de retiro.

*Por qué:* una proyección sin sus supuestos a la vista se lee como una promesa.
Mostrarlos convierte el número en el resultado de un modelo discutible, que es
lo que efectivamente es.

*Implementado:* tipo `proyeccion`, con `kpis` y `supuestos`.

*Origen:* pedido de Pablo sobre la propuesta con proyección de retiro, 28/08/2026.

---

## 14. La proyección y la cartera propuesta tienen que cerrar entre sí

Antes de emitir, cruzar los supuestos de la proyección contra los rendimientos
de los instrumentos que realmente se proponen. Si no coinciden, decirlo — y
elegir a conciencia si se mantiene la proyección original (por consistencia con
el anexo que se entrega) o se recalcula.

*El caso:* el anexo asumía bonos genéricos al 5,00%; la cartera propuesta
tiene renta fija al 6,84% ponderado (6,17% del fondo + 7,50% de las ONs). La
propuesta proyecta **más** que el anexo: USD 633.458 contra USD 618.446 en USD
de hoy. Se mantuvieron los números del anexo por consistencia entre los dos
documentos, aclarando en la slide que los supuestos de renta fija son
conservadores.

*El desajuste está en la renta fija, no en la asignación.* Despejando el peso en
acciones que reproduce el número del anexo, da 60,88% constante: el glidepath de
un horizonte de seis años ya arranca cerca del piso 60/40, así que contra una
cartera 60/40 fija la diferencia de asignación es 0,16% — ruido. Todo el desvío
lo explica el supuesto de bonos.

*Cómo verificarlo:* reconstruir el modelo del anexo (aportes a fin de año
ajustados por inflación, capitalizando al rendimiento ponderado del año) y
chequear que los aportes nominales den el mismo total que el reporte. Si cierran
los aportes, cualquier diferencia restante está en el camino de rendimiento y se
puede despejar.

*Origen:* verificación al armar la propuesta con proyección de retiro, 28/08/2026.

---

## 15. El logotipo es el archivo oficial de marketing, sin modificar

Los únicos archivos válidos son los que provee marketing:

- `logo_negativo.png` — blanco, para fondos oscuros (portada del deck, divisores,
  cierre, banda del encabezado del one-pager)
- `logo_positivo.png` — negro, para fondos claros (portada del documento largo)

**No se recolorea, no se le baja la opacidad, no se le recortan los márgenes.**
Los márgenes del archivo son el área de resguardo de la marca; el generador
compensa el ancho (factor 0,648) para que el logotipo visible quede del tamaño
buscado sin tocar el archivo.

*Qué había mal:* la skill venía usando un SVG heredado de la skill de fact sheet
que **no es el logotipo oficial** — trazo más pesado y menos tracking que el de
marketing. Además se lo estaba tintando: 50% de opacidad en la portada del deck
y 92% en el encabezado del one-pager. Ese SVG se eliminó del repositorio para
que nadie lo use por error.

*Si aparece una variante nueva* (isologotipo, monograma, versiones "Tip B"),
agregarla como archivo aparte y elegirla por contexto — nunca derivarla
editando otra.

*Origen:* logos provistos por marketing vía Pablo, 28/08/2026.

---

## 16. El logotipo va siempre arriba a la derecha

Misma posición en todos los formatos y en todas las slides de marca: **esquina
superior derecha**.

- **Portada del deck:** grande (150px de logotipo visible). Es la firma de la
  marca en la primera hoja y tiene que lucirse.
- **Divisores y cierre:** mismo lugar, tamaño menor (84px).
- **Encabezado del one-pager:** en la banda negra, arriba a la derecha.
- **Slides de contenido:** no llevan logotipo. Ahí la esquina superior la ocupan
  el número de slide y el nombre del cliente, y la firma institucional ya va en
  la leyenda regulatoria del pie.

*Qué había mal:* la portada del deck lo tenía abajo a la izquierda mientras el
one-pager lo tenía arriba a la derecha. Dos documentos del mismo cliente abrían
con la marca en lugares distintos.

*Origen:* corrección de Pablo, 28/08/2026.

---

## 17. Barras: normalizar sólo si son partes de un todo

El gráfico de barras reparte los valores sobre el total por defecto, que es lo
correcto para una distribución. Pero cuando las barras comparan **magnitudes
independientes** —un antes contra un después, dos carteras distintas— hay que
pasar `"normalizar": false`, porque sumarlas no significa nada.

*Qué pasaba:* "riesgo argentino hoy 63,9% / después 38,8%" salía impreso como
62,2% / 37,8%, sólo porque los dos valores sumaban 102,7 y se repartían sobre
ese total. Números inventados por el renderer, en una slide de cliente.

*Cómo detectarlo:* si los porcentajes del gráfico no coinciden con los del texto
de la misma propuesta, es esto.

*Origen:* error encontrado al armar el primer deck completo, 28/08/2026.

---

## 18. Los encabezados de la tabla tienen que decir lo que la tabla hace

Las columnas traen títulos por defecto pensados para una cartera que se compra
("Rendimiento esperado", "Monto a invertir"). En una tabla de posiciones **que
se venden** eso dice lo contrario de lo que pasa: van "Resultado realizado" y
"Valuación".

Se resuelve pasando `columnas` como objetos con `clave`, `titulo` y `align` en
vez de sólo la clave.

*Origen:* revisión al armar el primer deck completo, 28/08/2026.

---

## 19. Escribir desde la mirada del cliente, no como ficha interna

El capítulo de perfil describe al cliente, pero **lo lee el cliente**. No se
escribe "Martín es especialista en…" —ya sabe su nombre y a qué se dedica—:
se escribe en segunda persona, como devolución de lo conversado.

Sirve igual como antecedente escrito de lo que se acordó; lo que cambia es el
registro, no el contenido.

*Origen:* indicación de Pablo, 28/08/2026.

---

## 20. No inventar nada de la casa: ni URLs, ni textos, ni datos

La slide de cierre traía "WWW.MAX.CAPITAL" como valor por defecto. **Lo había
puesto yo**, no salía de ningún material de la casa. Se eliminó del `CONFIG` y
ahora, si el capítulo no trae `url`, la slide no la muestra.

Vale para todo: URLs, leyendas, textos legales, nombres de producto, teléfonos.
Si no está en el material que aportó el asesor, no va — y si hace falta, se
pide.

*Origen:* corrección de Pablo, 28/08/2026.

---

## 21. Capítulo `glidepath` — la trayectoria de la asignación

Muestra cómo evoluciona el asset allocation a lo largo del horizonte. Sirve
tanto para un desarme gradual de riesgo como para mostrar que la asignación **no
cambia** — que también es una decisión y conviene que esté dicha.

Los tramos marcados `"tentativo": true` se dibujan atenuados y punteados: son
los que todavía no están decididos y no deben leerse como compromiso.

*El caso:* 60/40 fijo durante los seis años de aportes, y una revisión
hacia 40/60 al llegar al retiro, dibujada como tentativa.

*Origen:* pedido de Pablo, 28/08/2026.

---

## 22. El riesgo se cuenta con el tiempo de recuperación, no sólo con la caída

Para un horizonte definido, lo que importa no es cuánto cae el portfolio sino
**cuánto tarda en volver**. Una caída del 36% que se recupera en seis meses es
menos problema que una del 22% que tarda casi dos años, si el retiro está cerca.

Los dos datos salen del fact sheet: "Caída máxima" y "Recuperación" (la racha
más larga bajo el agua). Conviene dar también la del índice de referencia: la
serie del portfolio suele ser corta y subestima el peor caso.

*Datos CEDEARs de ETFs al 07/2026:* caída máxima -36,2% (feb–mar 2020);
recuperación 1,7 años (nov 2021 – jul 2023). ACWI: -33,5% y 2,3 años
(nov 2021 – mar 2024).

*Origen:* indicación de Pablo, 28/08/2026.

---

## 23. Las barras de un gráfico apilado van todas del mismo largo

En un apilado al 100% cada columna representa el total, así que todas tienen que
medir exactamente lo mismo. Una más corta que otra se lee como "acá hay menos",
que es justo lo contrario de lo que el gráfico dice.

*Qué pasaba:* el pie de cada columna crecía con su contenido, y las que llevaban
una nota debajo de la etiqueta —"2026", "Retiro · 2032", "A definir"— le robaban
alto a su propia barra. Se resolvió dándole alto fijo al pie, lleve una línea o
dos.

*Cómo verificarlo:* medir los altos en el navegador antes de dar por buena la
slide. Deben ser idénticos, no parecidos.

*Origen:* corrección de Pablo, 28/08/2026.

---

## 24. El mismo instrumento dice lo mismo en todas las propuestas

Si dos clientes reciben una propuesta con el mismo vehículo, la descripción y
los datos tienen que ser idénticos. Un cliente con -28,05% de caída máxima y
otro con -36,2% para el mismo portfolio es un problema, no un matiz.

*Qué pasaba:* se actualizó la ficha de CEDEARs de ETFs en una propuesta con la
definición oficial nueva y el dato correcto, y quedó desincronizada con la de
otra, que seguía con el texto viejo del PDF anterior.

*Cómo evitarlo:* al cambiar la descripción de un instrumento, revisar qué otras
propuestas lo usan. Con el tiempo conviene que las fichas vivan en un archivo
compartido y las propuestas las referencien por nombre.

*Origen:* detectado al actualizar el primer deck completo, 28/08/2026.

---

## 25. Toda tarjeta de KPI lleva las cifras abreviadas con M y K

Cualquier tarjeta de KPI —la de la página de resumen y las del medio del deck—
usa **M para millones y K para miles**: `USD 1,3M`, `+USD 450K`. También el
rótulo de una barra que muestra una magnitud en moneda. El detalle completo va
en las tablas, que es donde se audita.

*Por qué:* la tarjeta se lee de un vistazo y desde lejos. "USD 1.300.056" obliga
a contar dígitos para saber de qué orden de magnitud se está hablando; "USD
1,3M" se entiende de una. Eso vale igual en la primera página que en la séptima:
lo que manda es el formato de la pieza, no dónde está.

*Dónde no:* en las tablas de detalle y en el menú de instrumentos, donde el
número exacto es el dato.

*Cómo se rompió:* el criterio decía *"en la página de resumen"* y por eso no se
aplicó a una lámina de KPIs del medio de un deck de rebalanceo, hasta
que Pablo lo pidió a mano. Una regla acotada a un lugar se lee como que afuera de
ese lugar no rige.

*Origen:* indicación de Pablo, 28/08/2026. Extendido a toda tarjeta el
20/09/2026, con un deck de rebalanceo.

---

## 26. Las tarjetas de una fila se alinean pieza por pieza

En una fila de tarjetas, cada parte se ancla por separado: **la etiqueta arriba,
el número siempre a la misma altura, la nota al pie**. No alcanza con alinear el
bloque entero.

*Qué pasaba:* las tarjetas de KPI iban todas alineadas al pie
(`justify-content:flex-end`), así que la que tenía nota empujaba su número una
línea hacia arriba y la que no la tenía lo dejaba abajo. En una fila de cuatro
donde dos tienen nota y dos no, los números quedan a dos alturas distintas.

Lo mismo con las etiquetas: si una envuelve a dos líneas y otra no, el número se
corre. Por eso la etiqueta lleva alto mínimo de dos líneas.

*Cómo verificarlo:* medir en el navegador los `top` de `.k-label` y `.k-value`
de la fila. Tienen que ser todos el mismo número, no parecidos:

```js
[...document.querySelectorAll('.kpi-grid.hero .k-value')]
  .map(e => Math.round(e.getBoundingClientRect().top))
```

*Vale como método general:* cuando un bloque se repite en fila o en grilla,
comparar las posiciones de sus partes antes de dar la slide por buena. Los
desalineados de una o dos líneas no se ven mirando, y se ven todos juntos en la
reunión.

**Ahora lo mide el generador.** Al armar un deck compara, en cada fila de
`.deltas` y `.kpi-grid`, a qué altura arranca el número dentro de cada tarjeta.
Si difieren en más de 2px avisa por consola con el número de slide.

*Cómo se volvió a romper (v1.3):* en el rebalanceo armado por otro asesor la tarjeta
destacada de una fila de deltas tenía el número 18px más abajo que las otras dos,
una raya navy a la izquierda y el contenido repartido a lo alto; la fila entera
salió inflada y las tarjetas vecinas, vacías. No era un error de contenido: el
recuadro de `perfil` que entró en la v1.3 se llamaba `.destacado` a secas y
**chocó de nombre** con `.delta.destacado`, así que la tarjeta heredó su padding,
su centrado vertical y su filete. Se renombró a `.perfil-destacado`.

*La lección de oficio:* un nombre de clase genérico —`destacado`, `nota`,
`caja`— se va a repetir en otro componente tarde o temprano. Los estilos nuevos
llevan el nombre del componente como prefijo.

*Origen:* propuesta armada por un asesor del equipo, 28/08/2026. Ampliado con el
ese caso, 16/09/2026.

---

## 27. No renunciar por escrito a lo que la casa sí hace

Una advertencia del tipo "esto no lo contemplamos, fijate vos" es una renuncia
de servicio escrita en la propuesta. Antes de escribir que algo queda fuera,
verificar si la casa efectivamente lo cubre.

*Caso concreto:* Max Capital **sí provee cierto grado de asesoramiento
impositivo**. Una de las propuestas decía que los impuestos no estaban
contemplados y que "siendo tu especialidad, es el primer ajuste que corresponde
hacer" — le pasaba el tema al cliente en algo sensible que nosotros sí
acompañamos. Quedó reescrito como: el anexo está antes de impuestos, definir el
tratamiento es parte de lo que trabajamos con vos, y conviene hacerlo antes de
la primera operación.

Reconocer la especialidad del cliente está bien. Usarla para delegarle el tema,
no.

*Origen:* corrección de Pablo, 28/08/2026.

---

## 28. Los costos se dicen una vez, en su lugar

Los honorarios y costos van declarados con claridad **donde informan la
decisión** —en la descripción del producto o en la estructura de la relación—,
no repetidos después como advertencia que erosiona los números propios.

*Qué pasaba:* la propuesta ya decía en el punto de partida que los tres
componentes son productos de administración, sin costo de entrada ni salida y
con honorario anual. Estaba bien dicho y en el lugar correcto. Pero una slide
más adelante volvía sobre el tema para agregar que esos honorarios "tampoco
están descontados de la proyección". Redundante y defensivo: llevaba al frente
el costo propio como si fuera una objeción.

Esto **no es ocultar costos** —el dato sigue estando, completo y temprano—: es
no repetirlo en tono de disculpa.

**Este criterio dice dónde van los costos cuando el asesor decidió incluirlos.
No decide si se incluyen.** Si con el cliente no se habló del esquema de
honorarios, antes de escribir una palabra sobre cobros vale el criterio 79.

*Origen:* corrección de Pablo, 28/08/2026. Acotado el 16/09/2026.

---

## 29. La cuenta internacional entra cuando el patrimonio la habilita

Una propuesta instrumentada solo a través de Argentina conviene que diga que lo
es, y que anticipe el salto: **superados los USD 250.000 bajo administración se
sugiere abrir una cuenta internacional a través de Max Capital**, que habilita
notas estructuradas y fondos del exterior.

Poné la fecha estimada del cruce calculándola con los aportes proyectados: dice
mucho más "hacia 2028" que "cuando crezca". Es un capítulo de crecimiento de la
relación, no una limitación de la propuesta.

*Origen:* indicación de Pablo, 28/08/2026.

---

## 30. El título de la slide de riesgos no puede sonar a lista de problemas

"Las cuatro decisiones que hay que discutir" le tira el quilombo al cliente:
suena a que la propuesta viene con pendientes que él tiene que resolver. **"Cuatro
puntos bajo la mira"** dice lo mismo sin trasladarle la carga — son temas que el
asesor ya identificó y sobre los que va a estar encima.

El contenido de la slide no cambia: los riesgos se siguen exponiendo de frente.
Lo que cambia es de quién parece ser el problema.

*Origen:* corrección de Pablo, 28/08/2026.

---

## 31. No decir "la más larga" si sólo se mira una ventana corta

Los indicadores de racha bajo el agua y caída máxima de un fact sheet se miden
sobre **la historia disponible del portfolio**, no sobre la historia del mercado.
Para el portfolio de CEDEARs de ETFs eso son poco más de seis años (desde fines
de 2019).

Escribir "la racha más larga fue de 1,7 años" sugiere un máximo histórico que no
es. Corresponde acotar la ventana —"desde el inicio del portfolio, a fines de
2019"— y decir que con más historia de mercado aparecen episodios más largos.

Si hace falta afirmar un máximo real, hay que ir a buscar la serie del índice
desde los 90 en adelante. No se infiere del fact sheet.

*Origen:* corrección de Pablo, 28/08/2026.

---

## 32. El tratamiento impositivo local es un argumento, no una advertencia

En una cartera instrumentada en Argentina, los impuestos juegan a favor y hay que
contarlo así:

- **Los instrumentos con cotización pública local no están alcanzados por el
  impuesto a las ganancias de capital.** Es un beneficio concreto de operar
  localmente.
- Dentro de una cartera con CEDEARs, el único ítem alcanzado por ganancias son
  **los dividendos**, con incidencia baja (rendimiento por dividendos en torno
  al 2%).
- Eso conecta con la custodia: la cuenta internacional se sugiere cuando el
  patrimonio la justifica, y el tramo local **es donde están los mayores
  beneficios impositivos**.

Los tres puntos se sostienen entre sí: explican por qué la propuesta arranca en
Argentina y por qué el salto al exterior llega después, por diversificación y no
por conveniencia fiscal.

*Origen:* indicación de Pablo, 28/08/2026.

---

## 33. El dato va escrito, la lectura la da el asesor en la reunión

Una propuesta expone los riesgos con datos. **La interpretación dramática de esos
datos no se escribe.**

*Qué pasaba:* la slide de riesgos cerraba con "un episodio así arrancando en 2030
se resuelve dentro del horizonte; arrancando en 2031, no". Es un escenario
inventado, con fecha puesta, sobre algo que no sabemos cuándo va a pasar ni si va
a pasar. Quedó reemplazado por el dato pelado: cuánto cayó, cuánto tardó en
recuperarse, y sobre qué ventana se mide.

*Por qué:* un riesgo dramatizado por escrito no se puede matizar después. El
asesor puede decir esa misma frase en la reunión, leyendo la cara del cliente y
respondiendo la repregunta en el momento. El PDF queda, se reenvía, y se lee
solo dentro de dos años.

No es esconder el riesgo: es dejar el dato completo y no ponerle encima una
conclusión que nadie puede sostener.

*Origen:* corrección de Pablo, 28/08/2026.

---

## 34. Lo que la casa hace, cubre o cobra se confirma — nunca se infiere

Cualquier afirmación sobre **alcance de servicio, cobertura o costos de Max
Capital** se verifica con el asesor antes de escribirla. No se deduce del
material aportado: del fact sheet de un fondo no sale qué servicios presta la
casa, y de una propuesta anterior tampoco.

Es la categoría donde el error sale más caro, porque el PDF lleva la identidad
de la firma y se lee como institucional. Un cliente que lee "esto no lo
contemplamos" asume que es política de la casa.

Errores reales de esta clase, todos en una misma tarde:

| Lo que se escribió | Por qué estaba mal |
|---|---|
| `WWW.MAX.CAPITAL` en el cierre | Inventada; no salía de ningún material |
| El disclaimer legal, redactado condensando otro | El texto legal vive en el `CONFIG` y no se reescribe por propuesta |
| "El anexo no contempla impuestos, es el primer ajuste que te corresponde" | La casa **sí** provee asesoramiento impositivo |
| "Los honorarios tampoco están descontados de la proyección" | Llevaba el costo propio al frente, ya declarado antes |

Ante la duda: preguntar. Cuesta un mensaje y evita un PDF que dice algo que la
casa no dice.

Ver también [20](#20-no-inventar-nada-de-la-casa-ni-urls-ni-textos-ni-datos),
[27](#27-no-renunciar-por-escrito-a-lo-que-la-casa-sí-hace) y
[28](#28-los-costos-se-dicen-una-vez-en-su-lugar).

*Origen:* patrón detectado repasando las correcciones de Pablo, 28/08/2026.


---

## 35. El texto legal nunca se recorta

Ningún disclaimer ni leyenda de matrículas puede quedar cortado por una caja de
alto fijo. Si no entra, se agranda el espacio o se achica la tipografía — nunca
se recorta.

*Qué pasaba:* el disclaimer del one-pager estaba dentro de una caja de
`max-height:64px` con `overflow:hidden`, y el del cierre del deck en una de
118px. Con el texto corto no se notaba. Al cargar el disclaimer oficial completo
—de 1.076 a 2.592 caracteres— el texto legal empezó a cortarse **en silencio**:
la caja medía 64px y el contenido 104px, sin ninguna señal visible.

*Cómo verificarlo:* comparar `scrollHeight` contra el alto real de la caja. Si
difieren, hay texto cortado:

```js
const d = document.querySelector('.disclaimer');
d.scrollHeight > d.getBoundingClientRect().height  // true = recortado
```

Hacerlo cada vez que cambie el texto legal, y también cada vez que cambie el
layout del pie.

**Y tampoco se encima.** En el one-pager el texto legal va anclado al pie de una
hoja de alto fijo. Si el contenido crece —más filas, tres gráficos, la nota de
instrumentos—, pasa por debajo del disclaimer y queda tapado.

*Qué hace el generador, en este orden,* midiendo la hoja ya maquetada:

1. ajusta el lugar reservado al pie al alto real del texto legal;
2. si no entra, comprime un paso más (`.tight`, después `.tighter`);
3. si ni con la compresión máxima entra, **pasa el disclaimer entero a una
   segunda hoja, solo**, y vuelve a la compresión original: con el lugar
   liberado suele sobrar.

Rompe la idea de una página, y está bien: en la segunda hoja no hay nada más que
el texto legal, así que no se lee como una propuesta de dos páginas. Lo que no
puede pasar nunca es un disclaimer encimado. Cuando pasa a la segunda hoja, lo
dice por consola; si aun así el contenido pisa los datos de contacto, avisa
DESBORDE y hay que sacar contenido — ver criterio 62.

*Cómo se rompió:* un one-pager con dos gráficos —"Por clase de activo" y "Por
nivel de riesgo"— quedó con el disclaimer tapando la mitad de los donuts. Al
reproducirlo apareció que **el propio ejemplo de la skill ya tenía el defecto**:
la nota de instrumentos quedaba 43px debajo del texto legal desde que el
disclaimer aprobado por legales en la v1.3 creció. La compresión elegía la clase
contando filas, no midiendo, y no lo veía.

*Origen:* detectado al cargar el disclaimer oficial, 28/08/2026. Ampliado con el
caso del one-pager encimado, corrección de Pablo, 16/09/2026.


---

## 36. Una proyección tiene que decir en qué moneda está

Si las cifras están en moneda constante —"USD de hoy", ya descontada la
inflación— hay que decirlo **sobre los números**, no en la bajada de la slide,
que se saltea. Y conviene dar también el equivalente nominal.

*Por qué:* sin la aclaración, el cliente lee el rendimiento como nominal y le
parece flojo. Seis años de aportes que generan USD 108.446 se leen distinto
cuando al lado dice USD 177.199 nominales y arriba dice que el primero ya tiene
la inflación descontada. **La cifra real es la honesta; la nominal es la que el
cliente reconoce.** Las dos juntas cuentan la historia completa; una sola, a
medias.

*Implementado:* `base` en el capítulo `proyeccion` dibuja la franja sobre los
KPIs; `valor_nominal` en cada ítem agrega la cifra secundaria debajo del número
principal.

*Vale igual para la TIR:* "5,4% real / 8,2% nominal" en vez de "TIR real 5,4%"
con el nominal escondido en la nota al pie.

*Origen:* indicación de Pablo, 28/08/2026.

---

## 37. "Riesgo argentino" hay que definirlo, no suponerlo

No todo lo emitido por una entidad argentina cuenta como riesgo argentino. La
definición del equipo:

**Riesgo argentino = soberano argentino (hard dollar y pesos) + equity argentino.**

Quedan **fuera**, deliberadamente:

- **ONs corporativas bajo ley NY** de empresas de primera línea (Vista, YPF,
  PCR). Es riesgo de crédito corporativo con legislación extranjera: otra cosa.
- **Deuda provincial.**

*Qué pasaba:* mezclé todo en un solo número —"riesgo argentino 63,9%"— sumando
soberano, provincial, ONs corporativas y equity. Con las ONs adentro, el
indicador se movía por razones que no tenían que ver con el riesgo país, y la
propuesta parecía reducir una exposición que en realidad se mantenía a
propósito. Con la definición correcta, el número real de ese
reposicionamiento es **47,0% → 12,9%**.

*Y siempre declarar la definición al pie del gráfico.* Un porcentaje de "riesgo
argentino" sin decir qué incluye es un número que cada lector interpreta
distinto — empezando por el asesor.

*Origen:* corrección de Pablo, 28/08/2026.

---

## 38. Clasificar por tipo de activo, nunca por cuenta

Las posiciones se agrupan por **qué son**, no por dónde están custodiadas. Un
cliente con cuenta en Argentina y en Uruguay tiene los mismos tipos de activo
repartidos entre las dos.

*Qué pasaba:* tomé el bloque "Renta Variable USD — Max Argentina" (USD 533.020)
y lo etiqueté "Renta variable Argentina" en la propuesta. Pero ese bloque son
**todos** los CEDEARs de la cuenta argentina: SPY, MELI, AMD, TSM y compañía.
El equity argentino real era USD 237.588, menos de la mitad. Por el mismo error
las ONs corporativas figuraban como USD 158.056 en vez de 245.869, porque las
dos de Uruguay quedaban en otro bloque.

*Cómo evitarlo:* antes de escribir un solo monto, reconstruir la cartera por
tipo de activo y **pasarle la tabla al asesor para que la confirme**. Cuesta un
mensaje y evita que toda la propuesta se apoye en una clasificación equivocada.

*Origen:* error propio detectado por Pablo, 28/08/2026.

---

## 39. Lo que se mantiene tiene que sumar tanto como lo que se vende

En una propuesta de reposicionamiento, el bloque "mantener" debe cubrir **todo**
lo que no se vende. Si el cliente suma lo que ve y no le da el total de su
cartera, la propuesta pierde credibilidad justo donde más la necesita.

*Qué pasaba:* una propuesta de reposicionamiento listaba en "mantener" las ONs,
el equity argentino, la nota estructurada y dos bonos — USD 552.418. Pero lo que no
se vendía eran USD 774.927. Faltaba un bloque entero: **USD 213.828 de equity
internacional (MELI, SPY, DIA, PBR, AMD, TSM), el 16,4% de la cartera**, el
mayor bloque de renta variable que quedaba en pie y no figuraba en ninguna
slide.

*Cómo verificarlo, siempre:*

```
total de la cartera − suma de lo que se vende = suma de lo que se mantiene
```

Si no cierra al peso, falta un bloque. Y contar también las posiciones nuevas:
"de 32 posiciones a 19" era 20 — quedaban 17 y entraban tres líneas.

*Origen:* verificación pedida por Pablo, 29/08/2026.

---

## 40. En columnas de altura pareja, el sobrante se reparte entre los ítems

Las columnas de comprar / vender / mantener las estira la grilla al mismo alto,
pero casi nunca tienen la misma cantidad de entradas. Sin repartir, la columna
con menos ítems deja un hueco muerto al pie y las tres se ven desbalanceadas.

Cada ítem toma `flex:1 0 auto`: se reparte el espacio sobrante y el aire se
convierte en interlineado. El `0 auto` evita que un ítem se comprima por debajo
de su contenido cuando la columna va llena.

*Cómo verificarlo:* medir el hueco entre el último ítem y el pie de la columna.
Tiene que ser el mismo en las tres, no sólo parecido.

*Origen:* indicación de Pablo, 29/08/2026.


---

## 41. Si la slide compara un antes y un después, escribí el delta

Dos gráficos lado a lado muestran los dos estados pero **no muestran el cambio**:
el lector tiene que restar de memoria, y el cambio es justamente la conclusión de
la slide.

Va una franja de tarjetas **arriba de los gráficos** con cuánto se movió cada
cosa —`riesgo argentino −34,1 pp`, `renta variable +2,8 pp`— con el antes y el
después en letra chica debajo. Una sola tarjeta destacada, la que sostiene el
argumento.

*Arriba y no al pie:* el delta es la conclusión, y la conclusión se lee primero.
Debajo van los gráficos, que son el detalle que la sostiene. Es el mismo orden
que usan las slides de ficha de portfolio — métricas arriba, composición abajo
(criterio 45) — y hace que el deck tenga una sola gramática. Sin línea
divisoria: separar los dos bloques con una raya le mete fricción a la slide.

*Ojo con el color:* una baja no siempre es mala noticia. "Riesgo argentino
−34,1 pp" es el mejor número de la propuesta. Por eso los deltas no usan la
escala verde/rojo: el signo lo dice todo y el color sólo confundiría.

*Implementado:* campo `deltas` del capítulo `distribuciones`.

*Origen:* indicación de Pablo, 29/08/2026.


---

## 42. Nada entra al PDF si no lo pidió el asesor

**El criterio más importante de esta lista, y el único sin excepciones.**

Trabajando sobre una cartera vas a encontrar cosas que nadie te pidió mirar: una
concentración por emisor, un costo alto, una posición que perdió su tesis, un
número que no cierra. **Ese hallazgo se le dice al asesor, en el chat, y ahí
termina.** No entra a la propuesta: ni como columna, ni como nota al pie, ni
como "tema de la próxima conversación".

*Qué pasó:* en una propuesta de reposicionamiento metí una columna titulada **"Lo que
esta propuesta no resuelve"**, contándole al cliente que tenía 12,3% en YPF y
12,2% en Vista, que eran concentraciones que no se veían en su estado de cuenta,
y que era el tema de la próxima conversación. El análisis era correcto. La
decisión de ponerlo en un PDF firmado no era mía, y nadie me la pidió.

*Por qué es tan grave:*

- **Le traslada al cliente un problema que la casa no eligió plantearle.** El
  asesor decide qué conversación se da, cuándo y con qué palabras.
- **Queda por escrito y se reenvía.** Una frase dicha en una reunión se matiza
  con la repregunta; una línea en un PDF no.
- **Erosiona la propuesta desde adentro.** Un documento que dice lo que no
  resuelve se está discutiendo a sí mismo.
- **Suena a que la casa entrega trabajo incompleto**, aunque el hallazgo sea
  exactamente lo contrario: evidencia de que se miró en profundidad.

*No existe la versión suave.* No hay forma de redactar bien una limitación que
el asesor no aprobó: el problema no es el tono, es quién decidió incluirla.

*La regla operativa:* si el hallazgo no está en lo que el asesor te pidió, va al
chat. Si te parece importante, decíselo con todas las letras — pero en el chat,
y esperá su respuesta antes de tocar el PDF.

*Origen:* error propio, señalado por Pablo, 29/08/2026.


---

## 43. Preguntá quiénes van en los datos de contacto

**No lo deduzcas de quién te está hablando.** En Max Capital lo habitual es
trabajar en dupla, y el cliente tiene que poder escribirle a los dos. El asesor
que arma la propuesta no siempre es el único que atiende la relación.

*Qué pasaba:* las tres propuestas salieron con un solo contacto, el de quien me
estaba dictando. Pablo trabaja siempre con Marcos Sanchez Negrete y sus datos no
figuraban en ninguna — algo que el generador no puede adivinar y que yo nunca
pregunté.

*El directorio del equipo está en* [`equipo.md`](equipo.md) *y se completa así:*

```json
"asesores": [
  { "nombre": "Pablo Haro", "cargo": "Wealth Management", "email": "pharo@max.capital" },
  { "nombre": "Marcos Sanchez Negrete", "cargo": "Wealth Management", "email": "msancheznegrete@max.capital" }
]
```

El orden importa: el primero encabeza la relación y es quien aparece en
"Presentado por" de la portada. `asesor` en singular sigue funcionando para una
sola persona.

*Si falta un teléfono o un dato, va sin él.* No se inventa ni se reutiliza el de
otra propuesta — ver criterio 34.

*Origen:* indicación de Pablo, 29/08/2026.


---

## 44. En banca privada la cartera lleva vehículos administrados

Una propuesta para persona física se arma **con vehículos administrados**, no
sobre operaciones sueltas. Si la cartera que trae el asesor no tiene ninguno,
planteáselo antes de escribirla.

*Por qué:* la comodidad empuja al modelo de trading — es más rápido proponer lo
que el cliente ya opera. Para **empresas** ese modelo tiene sentido y se evalúa
caso por caso. Para **banca privada alinea mal los incentivos**: cobra por
operar en vez de por administrar, encarece cada rebalanceo y convierte al asesor
en ejecutor.

*Los tres que van siempre* (salvo que el caso lo desaconseje): FCI Max Renta
Fija Dólares, Cuenta Administrada CEDEARs de ETFs, y notas estructuradas para
inversores desde USD 250.000. El detalle completo está en [`oferta.md`](oferta.md).

*Planteáselo, no lo cambies.* La cartera la decide el asesor — ver criterio 42.
Lo que corresponde es decirle, en el chat, que la propuesta quedó sin componente
administrado y por qué eso importa.

**Esta regla decide qué va en la cartera, no qué dice la propuesta.** Todo el
razonamiento de arriba es para el asesor. Frente al cliente, del esquema de
comisiones no se habla salvo confirmación expresa — ver criterio 79.

*Origen:* política comercial definida por Pablo, 29/08/2026. Acotada el
16/09/2026, cuando la regla se filtró a la portada de una propuesta.

---

## 45. Mostrá el vehículo que el cliente todavía no conoce

Cuando la propuesta incorpora una cartera administrada que el cliente no tenía,
dedicale **una slide propia**: métricas de rendimiento y riesgo arriba,
composición debajo.

*Por qué:* un cliente que viene de posiciones directas necesita entender qué
está comprando antes de aceptar delegar. Una línea en la tabla de cartera no
alcanza para eso, y es justo donde se cae la conversación de cuentas
administradas.

*Qué mostrar,* según lo que tenga el fact sheet:

- **Renta variable:** anualizado a 5 años, desde inicio, volatilidad, caída
  máxima y cuánto tardó en recuperar. Composición por región y por sector.
- **Renta fija:** TIR, duration y calidad crediticia promedio — son los tres
  datos que un cliente con bonos directos va a comparar contra los suyos.
  Composición por calificación, tipo de emisor y región.

*Mostrá la calificación completa*, incluido el tramo de alto rendimiento. Es
mejor que lo vea en la propuesta y no cuando revise el fondo por su cuenta.

*Implementado:* el capítulo `distribuciones` acepta `kpis` de encabezado.

*Origen:* el primer deck completo, 29/08/2026.


---

## 46. Prohibidas las tensiones, los dilemas y las preguntas incómodas

Nunca, en ninguna propuesta, construcciones del tipo:

- "Lo que esta propuesta **no resuelve**"
- "La **tensión** que hay que definir"
- "La **pregunta incómoda** es"
- "El **punto débil** de este esquema"
- "**Hay que reconocer que**…"
- "Lo que **queda pendiente**"

Ni con esas palabras ni con sinónimos. No es cuestión de redacción: es la
construcción misma.

*Por qué aparece:* plantear tensiones y contradicciones es un hábito
conversacional. En un chat genera diálogo y suena a honestidad intelectual —el
interlocutor engancha, repregunta, discute. **En un documento de venta es
autosabotaje.**

*Por qué está mal acá:* el cliente no está conversando, está evaluando una
recomendación de su asesor. Una propuesta que se plantea dilemas a sí misma se
está discutiendo por escrito, y le deja al cliente un problema que la casa no
eligió plantearle. Encima queda en un PDF que se reenvía y se lee dentro de dos
años, sin nadie que lo matice.

*Qué sí se hace:* los riesgos se exponen **con datos**. "La caída más profunda
fue -36,2% y tardó 1,7 años en recuperarse" informa el mismo riesgo sin
convertirlo en un dilema del cliente. La lectura de ese dato la da el asesor en
la reunión — ver criterio 33.

*Origen:* corrección de Pablo, 29/08/2026. Es la extensión del criterio 42.

---

## 47. De los costos se habla en positivo, o no se habla

Cuando el costo entra en una propuesta es **para decir lo que el cliente gana**:

- No hay arancel de entrada ni de salida
- El rebalanceo no tiene costo asociado
- El esquema de administración alinea los incentivos
- El marco impositivo local genera eficiencias concretas — instrumentos con
  cotización pública exentos de ganancias de capital

**Nunca como advertencia ni erosionando los números propios.** Frases como "los
honorarios tampoco están descontados de la proyección" o "a esto hay que
restarle nuestro fee" no van: llevan al frente el costo propio como si fuera una
objeción que el cliente todavía no hizo.

*El foco es el beneficio del cliente, la propuesta y el servicio.* Esa es la
conversación; el costo es un dato dentro de ella, no su eje.

*Esto no habilita ocultar nada.* Los costos se declaran completos y donde
informan la decisión —en la descripción del producto o en la estructura de la
relación, ver criterio 28—. Lo que cambia es el registro: factual y positivo, no
apologético.

*Origen:* corrección de Pablo, 29/08/2026.


---

## 48. Un decimal en los porcentajes, nunca dos

`10,1%` y no `10,11%`. `7,0%` y no `7,00%`.

*Por qué:* es lo mismo que hablar de centavos cuando el monto está en dólares —
no aporta precisión útil y le quita seriedad al número. Un rendimiento de
"10,11% anualizado a 5 años" sugiere una exactitud que la estimación no tiene.

Vale para rendimientos, TNA, TEA, volatilidades, ponderaciones y puntos
porcentuales. **Los fact sheets suelen venir con dos decimales: hay que
redondear al pasarlos a la propuesta.**

*Cómo verificarlo:* buscar en el JSON el patrón `dígito,dígito dígito%` antes de
generar.

*Origen:* indicación de Pablo, 30/08/2026.

---

## 49. Escala de riesgo: Bajo, Medio, Alto — y es relativa al inversor

La escala del equipo tiene tres niveles. La referencia por tipo de activo:

| Instrumento | Nivel |
|---|---|
| Fondos de renta fija (Max Renta Fija Dólares, mutual funds RF) | **Bajo** |
| ONs corporativas | **Medio** |
| CEDEARs de ETFs | **Alto** |

**Pero el nivel es relativo al punto de partida del inversor.** A alguien que
sólo hizo plazo fijo, un fondo de renta fija en dólares se le presenta como
**medio**: no es devengamiento, el valor de la cuotaparte se mueve, y para él eso
es riesgo aunque la volatilidad sea baja.

*La decisión es del asesor.* Preguntale de dónde viene el cliente antes de
asignar niveles, y si el caso lo pide, corré la escala.

*Cuando el fact sheet dice otra cosa:* el fact sheet de Max Renta Fija Dólares
dice "perfil moderado, riesgo 2 de 5" y el equipo lo trata como bajo. Prevalece
el criterio del asesor para la propuesta; el fact sheet queda como anexo con su
propia escala.

**El badge va rotulado.** Una pastilla que dice "Alto" arriba a la derecha no se
entiende sola: lleva "Nivel de riesgo" al lado. Para quien ve la propuesta por
primera vez, no es obvio a qué se refiere.

*Origen:* definido por Pablo, 30/08/2026.

---

## 50. Detrás de cada producto hay gestión activa, y hay que decirlo

En los tres vehículos que más se proponen —CEDEARs de ETFs, mutual funds de
renta fija y FCI Max Renta Fija Dólares— **es importante señalar que hay
management activo detrás**, buscando las mejores oportunidades para optimizar el
patrimonio del cliente.

*Cuidado con el vocabulario.* Escribir que "la cartera **replica** los
principales índices" es un error grave: suena a que no hacemos nada, describe
algo pasivo. La construcción correcta es **"invierte en instrumentos que
replican"** — el que replica es el ETF, no nuestra gestión.

Otras palabras que restan: "sigue", "espeja", "copia". Las que suman: invierte,
selecciona, utiliza, construye, ajusta.

En los fondos de terceros, decir explícitamente que **la selección es nuestra**,
hecha en base a nuestro análisis y a nuestra visión de mercado. Sin eso, una
lista de cinco fondos parece un menú y no una decisión.

**Las descripciones oficiales están en [`oferta.md`](oferta.md) y se usan
literales.** No se resumen ni se reescriben. Comprimirlas pierde matices que sí
importan: que los ETFs cotizan como CEDEARs en el mercado local, que la
diversificación es también por clase de activo, que el oro descorrelaciona
*frente a los mercados accionarios*. Si no entran en el espacio, recortá
oraciones enteras del final antes que parafrasear.

*Cómo se rompió:* al comprimir la descripción oficial quedó "la cartera replica
los principales índices" en lugar de "invierte en instrumentos que replican los
principales índices del mercado". Una palabra, y el sentido pasó de gestión
activa a producto pasivo.

*Origen:* corrección de Pablo, 30/08/2026.

---

## 51. La propuesta termina mostrando cómo queda la cartera

Antes del cierre va una slide con **la composición resultante**: qué queda, en
qué proporción y con qué nivel de riesgo.

*Por qué:* sin eso, una propuesta de reposicionamiento muestra lo que se vende y
lo que se compra, pero nunca la foto final. El cliente tiene que poder ver el
resultado de la operación completa, no reconstruirlo sumando slides.

Se arma con `cartera_sugerida`, reutilizando los KPIs de encabezado y los badges
de riesgo. Incluí **todo** lo que queda, también lo que no se tocó — ver
criterio 39.

*Origen:* indicación de Pablo, 30/08/2026.

---

## 52. Los encabezados no se mueven entre slides

El número, el nombre del cliente y el título tienen que estar **en la misma
posición en todas las slides**. Si una comprime su contenido, se comprime el
cuerpo, nunca la cabecera.

*Qué pasaba:* el modo denso achicaba el padding superior y el tamaño del título,
así que al pasar de una slide normal a una comprimida el número y el título
saltaban de lugar. Pasando páginas se ve como un temblor.

*El criterio general:* al ajustar el espacio de una slide hay que mirar **de
dónde viene el lector**, no sólo si el contenido entra. Una slide puede estar
perfecta sola y estar mal en la secuencia.

*Cómo verificarlo:* medir el `top` del badge en todas las slides del deck. Debe
haber un solo valor.

*Origen:* corrección de Pablo, 30/08/2026.

---

## 53. La proyección de retiro va en toda propuesta de primera vez

En una propuesta a un cliente nuevo, **sugerí incorporar la proyección de
retiro** aunque el asesor no la pida.

*Por qué:* es lo que estimula al inversor a hacer **aportes recurrentes**. Y los
aportes recurrentes permiten hacer DCA sobre la cartera objetivo, lo que vuelve
mucho más robusta la generación de rendimientos a largo plazo y mejora
considerablemente la experiencia del cliente con su portfolio.

No es un capítulo decorativo: es el que convierte una inversión única en un plan
de aportes.

*Cómo:* capítulo `proyeccion`, con la base declarada y los supuestos a la vista
— ver criterio 36. Si el asesor no tiene una proyección armada, pedísela antes de
inventar los números.

**La regla es por los aportes, no por el nombre del caso: si entra dinero nuevo,
proyectá.** No importa que la propuesta sea de primera vez, una revisión o un
reposicionamiento. Lo único que decide es si hay capital entrando: eso es lo que
la proyección tiene para proyectar.

Cuando la propuesta sólo reordena una cartera que ya existe y no entra nada, la
proyección no tiene materia prima y el argumento es cómo queda la cartera. Fue el
caso del primer deck completo, 30/08/2026.

*Por qué está escrito así:* antes decía "no va en un reposicionamiento", y esa
excepción se aplicó mal en el deck de canje (06/09/2026). El caso se clasificó como
reposicionamiento por la palabra —había una cartera vigente que se reordenaba— y
se salteó la proyección, sin mirar que ese año habían entrado aportes y estaban
entrando más. La pidió Pablo varias rondas después.
Una regla con un "salvo que" invita a resolverla mirando la etiqueta del caso en
vez del hecho que importa.

*Origen:* indicación de Pablo, 30/08/2026.

---

## 54. Los gajos del donut son arcos, no guiones

Cada gajo se dibuja como un `<path>` con un arco explícito. **Nunca con
`stroke-dasharray` sobre un `<circle>`.**

*Por qué:* un `<circle>` es un path que abre y cierra en el mismo punto. Si un
gajo cae sobre esa costura —y el último gajo siempre termina ahí—, el navegador
lo traza como un tramo continuo que la cruza y le aplica un *join*. El resultado
es una punta que se escapa del anillo, con forma de flecha. No es antialiasing
ni un gajo demasiado chico: es geometría mal planteada, y aparece más cuanto más
chico es el último gajo.

*Cómo se rompió:* en el primer deck completo, el donut "Perfil de la cartera
hoy" tenía Cash en 0,7%. Ese gajo salió impreso como un zigzag azul claro que
atravesaba el borde del anillo. Pasó la validación, pasó la generación del PDF y
lo encontró el asesor mirando la lámina.

*Cómo verificarlo:* exportar con `--design-html`, abrir el SVG del donut y
comprobar que hay un `<path d="M ... A ...">` por gajo y ningún
`stroke-dasharray`. Visualmente, ampliar el donut que tenga el gajo más chico:
los bordes entre gajos tienen que ser radios rectos.

*Ojo con el 100%:* un arco de 360° empieza y termina en el mismo punto y no
dibuja nada. Un gajo único va como `<circle>` completo — está contemplado en el
código.

*Origen:* lo detectó Pablo en el primer deck completo, 30/08/2026.

---

## 55. "La slide 8" es ambiguo: contestá con el título

**Cuando el asesor identifica una slide por número, respondé nombrándola por su
título antes de tocar nada.** "Dale, en *A dónde van los fondos* saco las pills"
— si le erraste, te corrige ahí, antes de la regeneración.

*Por qué:* un deck tiene **dos numeraciones que no coinciden**. El badge no
cuenta la portada, así que ya arranca corrido; y cualquier capítulo que pagine
—fichas, tablas largas— agrega páginas que el badge tampoco cuenta. Cuanto más
larga la propuesta, más se separan. El asesor mira el visor de PDF y dice "la 8"
pensando en la página; el badge de esa página puede decir 7.

*Antes de preguntar, usá lo que ya tenés.* Casi siempre el propio pedido
desambigua: si dice "los badge" en plural, es una lámina con varias fichas y no
una con un solo badge de esquina; si dice "la columna del medio", es una de
texto; si menciona un dato, buscá en qué slide está. Preguntar es el último
recurso, no el primero — pero es infinitamente mejor que editar la equivocada.

*Si sigue sin estar claro, preguntá con los dos títulos a la vista:* "¿la de *A
dónde van los fondos* o la de *CEDEARs de ETFs*?". Nunca "¿a qué slide te
referís?", que le devuelve el problema sin ayudarlo a resolverlo.

*Cómo se rompió:* Pablo pidió sacar el badge de riesgo de "la slide 8". El badge
8 estaba en *CEDEARs de ETFs*, pero él miraba la página 8 del PDF, que es *A
dónde van los fondos*. Se editó la slide equivocada y hubo que revertirla. El
plural de "los badge" ya decía cuál era —esa lámina tiene tres fichas con tres
pills— y no se leyó.

*Origen:* indicación de Pablo, 30/08/2026.

---

## 56. Un dato en la esquina se alinea por línea de base y no le compite al título

Cuando una tarjeta lleva un dato en la esquina —el monto de una ficha, el nivel
de riesgo— se rige por dos reglas:

**Alineación por línea de base, no por el borde de la caja.** En flex es
`align-items:baseline`, no `flex-start`. Dos textos de distinto tamaño o
interlínea que arrancan sus cajas a la misma altura **no** apoyan sus letras a
la misma altura, y el ojo lee la línea de base: la de abajo, no el borde de
arriba. Con `flex-start` el dato queda flotando entre el título y el subtítulo,
sin coincidir con ninguno.

**Peso tipográfico igual o menor que el del título.** El dato acompaña, no
encabeza: quien manda en la tarjeta es el nombre del instrumento. Mismo cuerpo
que el título y un gris oscuro —`--gray-d`— rinde mejor que un cuerpo más grande
en color de marca, que se come la lámina.

*Cómo se rompió:* el monto salió a 13px, bold, en navy, contra un nombre de
instrumento de 12px. Pesaba más que el título y no coincidía con nada: ni con el
nombre, ni con el subtítulo, ni con el centro del bloque.

*Cómo verificarlo:* medir sobre el PDF, no mirar el HTML aislado —fuera del
documento no carga Inter y las medidas cambian—. Con `pypdf`, `extract_text`
acepta un `visitor_text` que entrega la matriz de texto: `tm[5]` es la línea de
base. La del dato y la del título tienen que dar el mismo número.

*Origen:* lo detectó Pablo en el primer deck completo, 30/08/2026.

---

## 57. La leyenda de un gráfico no puede contradecir un KPI de la misma slide

**Si los valores de un gráfico ya vienen en porcentaje, la leyenda muestra el que
escribió el asesor.** No uno recalculado sobre la suma de los ítems.

*Por qué:* las ponderaciones de una cartera redondeadas a un decimal casi nunca
suman 100 exacto — suman 100,1 o 99,8. Si la leyenda divide cada valor por esa
suma, devuelve un número apenas distinto del original. El resultado es una slide
que dice **52,3%** en la tarjeta de arriba y **52,2%** en la leyenda de abajo,
para la misma cosa. El cliente no piensa "redondeo": piensa que uno de los dos
está mal, y a partir de ahí desconfía del resto de los números.

*La tentación es aclararlo al pie.* No: una nota que explica una diferencia de
redondeo ocupa lugar, mete ruido y no le sirve a nadie. Se arregla el número, no
se justifica.

*Cómo:* el generador detecta que los valores ya son porcentajes cuando suman
entre 99 y 101, y en ese caso imprime el valor tal cual. La geometría del gajo sí
se normaliza — esa diferencia no se ve.

*Origen:* lo detectó Pablo en el primer deck completo, 30/08/2026.

---

## 58. Toda tabla lleva total, y la tabla tiene que cerrar con él

**Si una tabla tiene porcentajes o montos, lleva fila de total.** Y las filas
tienen que sumar exactamente lo que dice esa fila.

*El invariante no es "los porcentajes suman 100".* Es **que la tabla cierre con
su propio total**. Una tabla de posiciones a vender es un subconjunto: sus pesos
son sobre la cartera entera y suman 40,4%, que es correcto. Lo que nunca puede
pasar es que las filas digan una cosa y el total otra. Cuando no hay fila de
total, el único cierre posible es el 100%.

*Por qué:* el cliente suma. No toda la tabla, pero sí las dos o tres líneas que
le interesan, y si el total no da, deja de confiar en el resto de los números.
Una propuesta se sostiene sobre que las cifras cierren.

**Si no cierra, avisale al asesor y ofrecele el ajuste. No lo hagas por tu
cuenta:** cambiar un peso o un total es cambiar un número que él eligió.

*Los dos ajustes, y cuándo sirve cada uno:*

- **Rebasear.** La tabla muestra 5-86-4 sobre una base de 95 y se quiere leer
  sobre 100: cada valor pasa a `v/95`. Sirve cuando la base declarada no es la
  suma real.
- **Reparto por resto mayor.** Diez líneas redondeadas a un decimal suman 100,2%
  aunque la base esté perfecta: el desvío es la acumulación de los redondeos, no
  la base. Se baja 0,1pp a las líneas con el resto fraccionario más chico hasta
  cerrar en 100,0. **Rebasear acá no arregla nada** — recalculado da los mismos
  valores redondeados.

Diagnosticá cuál de los dos es antes de ofrecer: si al recalcular sobre la suma
real los redondeos no se mueven, es resto mayor.

*Cómo se verifica:* `--validar` lo controla solo y avisa. Compara las filas
contra la fila de total, tanto en porcentaje como en monto.

*Cómo se rompió:* en una cartera final la columna sumaba 100,2% con
la fila de total diciendo 100%, y las valuaciones sumaban USD 1.300.052 contra
un total declarado de USD 1.300.056. Había una nota al pie que lo explicaba;
se sacó la nota —bien— pero no se arregló el número, que era lo que había que
hacer.

*Origen:* buena práctica de Pablo, 30/08/2026.

---

## 59. Ninguna fila puede medir el doble que las otras

**En una tabla o en una leyenda, todas las filas tienen la misma altura.** Si un
texto parte en dos líneas, esa fila queda del doble de alto y es lo primero que
se ve — antes que cualquier número.

*Por qué pasa:* el ancho se reparte mal. Las columnas numéricas se quedan un
espacio que no usan —`USD 1.300.056` mide lo que mide y no crece— mientras la
columna de texto, que es la única que puede necesitarlo, queda ahogada. En una
tabla ancha no se nota; cuando la tabla comparte la lámina con un gráfico, sí.

*Cómo se arregla:* **la columna de texto se lleva lo que sobra y las numéricas
ocupan lo que miden.** En la cartera con gráfico al lado el reparto es
19% / 45% / 21% / 15%. Si aun así un nombre no entra, se acorta el nombre o se
agranda la tabla — nunca se acepta la fila doble.

*Lo mismo vale para la leyenda de un donut.* En una columna angosta, "Renta
variable" al costado del gráfico parte en dos. Apilada debajo, cada fila dispone
del ancho completo de la tarjeta.

*Cómo verificarlo:* extraer el texto de la página y mirar las filas. Cada fila de
datos tiene que salir en **una sola línea**, con su etiqueta y sus números
juntos. Si aparece una línea de texto suelta, sin monto ni porcentaje, ése es el
nombre partido. Medir las líneas de base no sirve en estas tablas: las celdas
comparten la matriz de texto y el desplazamiento de fila viaja en la matriz de
transformación.

*Origen:* lo detectó Pablo en el primer deck completo, 30/08/2026.

---

## 60. Una barra sin pista de fondo, salvo que la escala sea 100%

**Si las barras escalan contra el valor más grande y no contra 100%, no llevan
pista gris de fondo.**

*Por qué:* una pista se lee como "lo que falta". Eso sólo es cierto cuando la
pista llena vale 100%. Si escala contra la fila más pesada, la pista completa
equivale a esa fila —18,9% en el caso que lo destapó— y entonces no representa
nada, pero el ojo igual la interpreta como el total.

*Cómo se rompió:* la fila de Cash, con 0,7%, quedó como un punto azul contra una
pista gris entera. Parecía que le faltaba el 99% de algo. La escala relativa era
la decisión correcta —contra 100% ninguna barra de una cartera de diez líneas se
distinguiría de las otras— pero arrastraba una pista que ya no tenía sentido.

*La regla general:* **cada elemento gráfico tiene que significar algo.** Un fondo,
una línea divisoria o un ícono que están "porque quedan bien" le dan al lector
una referencia falsa. Si no se puede decir en una frase qué representa, se saca.

*Y el reverso: nada puede significar algo que el dato no dice.* La paleta de
gráficos es sólo azules, navies y grises. **Nunca verde, rojo ni amarillo**: son
los colores de positivo, negativo y atención, y en una serie de categorías se
reparten por orden de aparición, sin relación con el contenido. En la
distribución por calificación crediticia el verde le tocó a "CCC y menor" — el
peor rating pintado con el color de "bien". Esos tres colores quedan reservados
para donde sí significan: pills de riesgo, comprar/vender, variaciones.

*Origen:* lo detectó Pablo en el primer deck completo, 30/08/2026.

---

## 61. Elegir una ventana es decisión del asesor, nunca tuya por omisión

**Vos no elegís ventanas. Las mostrás todas, o le preguntás al asesor cuáles
van.** Él sí puede elegir: si considera que hay un período que vale la pena
destacar, está bien y es su criterio profesional.

*La diferencia es quién decidió.* Un asesor que dice "acá lo que importa son los
12 meses desde que reposicionamos, lo anterior es otra cartera" está haciendo su
trabajo, y esa selección tiene un argumento detrás que puede defender frente al
cliente. Una selección que aparece porque se tomaron las métricas que "quedaban
bien" no tiene ningún argumento: nadie la pensó, y no hay con qué sostenerla si
el cliente pregunta.

*Por qué importa tanto:* es el error más caro, porque no se descubre en la
reunión. Se descubre después, cuando el cliente mira el fact sheet completo y
encuentra la ventana que faltaba. Ahí no perdés el argumento: perdés la
confianza en todo lo demás que dijiste, incluido lo que estaba bien.

**Tu trabajo es que el asesor decida sabiendo.** Cuando cargues una comparación
contra benchmark, mirá **todas** las ventanas del fact sheet y decile cuáles
quedan afuera y qué dicen. Si él elige destacar una, listo. Lo que no puede
pasar es que la propuesta muestre tres de cinco ventanas y nadie se haya
enterado de las otras dos.

*Si se destaca una ventana, que se entienda por qué es esa.* "Desde el
reposicionamiento de marzo" se sostiene solo; "5 años" al lado de "desde inicio",
sin los períodos del medio, invita a la pregunta que no querés.

*Ojo con la versión disimulada:* sacar la palabra "alpha" y dejar `10,1%` al lado
de `Benchmark 8,9%` es la misma afirmación escrita distinto. El lector resta. Si
se saca la comparación, se saca entera —incluida la mención al benchmark en el
subtítulo—.

*Qué siempre se puede mostrar:* el rendimiento propio del producto, sin
comparación. Y las métricas de riesgo contra el benchmark, que son otra cosa:
describen el perfil, no reclaman haberle ganado a nadie.

*Cómo se rompió:* la lámina de CEDEARs de ETFs mostraba el alpha a 5 años
(+1,2pp) y desde inicio (+0,8pp). El de 3 años es **−1,2pp** y no figuraba. No
hubo intención de esconderlo, y ése es el punto: no hubo intención de nada. Al
avisarle, Pablo decidió sacar todas las comparaciones de rendimiento.

*Origen:* decisión de Pablo, 30/08/2026, y su corrección posterior el mismo día:
"tampoco tiene que ser algo tan rígido; si el asesor considera que hay un período
al que vale la pena meterle énfasis, está ok".

---

## 62. Ninguna slide desborda, y eso se mide en el navegador

**Antes de entregar, el generador mide cada slide y avisa si el contenido se
pasa.** `.slide` tiene `overflow:hidden`: lo que sobra se recorta o se encima con
el pie, y en las dos formas el defecto es invisible desde el JSON.

*Por qué no se puede estimar:* si entra o no depende de la fuente, del texto
real de cada etiqueta y de dónde cortó cada línea. Contar filas desde el JSON
falla siempre. La única medición honesta es sobre el documento ya maquetado, y
eso ya lo tenemos: el PDF se genera con Chromium, así que alcanza con preguntarle
al navegador antes de imprimir.

*Cómo funciona:* al generar un deck, el script compara el borde inferior de cada
elemento contra el techo del pie de página. Si algo se pasa, avisa por consola
con el número de slide, cuántos píxeles y **con qué texto empieza a encimarse**,
que es lo que permite encontrarlo sin abrir el PDF:

```
DESBORDE: slide 10 ('Mutual funds de renta fija') se pasa 10px del pie.
Empieza a encimarse en: "Por calificaciónAA29,0%BB18,9%B14,6%..."
```

*Qué hacer cuando salta:* sacar contenido o partir la slide en dos. **Nunca
achicar la tipografía hasta que entre** ni dejarlo recortado — ver criterio 35.
Lo más común es que sobre una tarjeta: seis KPIs envuelven a dos filas y empujan
todo lo de abajo.

*Cómo se rompió:* la lámina de mutual funds tenía seis tarjetas. La sexta pasó a
una segunda fila, corrió los gráficos hacia abajo y la distribución por
calificación terminó encimada con la nota al pie. Se generó el PDF sin que nada
avisara.

*Origen:* lo detectó Pablo en el primer deck completo, 30/08/2026.

---

## 63. Un trade no se cuenta como un rebalanceo

Hay dos clases de movimiento y no se argumentan igual.

Un **rebalanceo por estrategia** se justifica contra el mandato, posición por
posición: esto se vende porque pesa de más, esto se compra porque falta. Cada
línea se sostiene sola y el formato natural son las tres columnas de comprar /
vender / mantener del capítulo `cartera_actual`.

Un **trade** es un canje: sale este bono, entra este otro. El argumento no está en
ninguno de los dos por separado sino en la comparación —mismo segmento, por qué
el que entra es mejor que el que sale—, así que **la venta y la compra tienen que
leerse juntas**. Partidas en dos columnas, el cliente tiene que adivinar qué va
con qué.

*Cómo:* capítulo `trades`, que emite la tabla de movimientos emparejados y, si hay
razones, una lámina con una columna por movimiento. La razón nunca va como quinta
columna de la tabla: el texto largo parte las filas en dos y rompe el criterio 59.

*De dónde salió:* en el deck de canje se armó con comprar/vender, Pablo pidió
emparejarlo, y después hubo que recuperar los porqués en una slide aparte. Salió
bien y a mano; el catálogo no tenía el formato. 06/09/2026.

---

## 64. Dos números que contestan la misma pregunta no pueden convivir

Si el deck muestra dos cifras que el cliente va a leer como lo mismo, tienen que
coincidir o llamarse distinto. No alcanza con que cada una esté bien calculada en
su propio alcance.

*Caso:* la lámina de resumen decía "Resultado acumulado **+USD 9.319**" —el P&L de
tres años de toda la cartera, incluido lo ya cerrado— y dos slides después la
tabla de posiciones cerraba en "Resultado **+USD 11.205**", que es la ganancia no
realizada de lo que está hoy en cartera. Las dos correctas, con alcances
distintos, separadas por dos páginas y con el mismo rótulo.

*Qué hacer:* rotularlas por su alcance ("Resultado de las posiciones vigentes"
contra "Resultado acumulado"), o dejar una sola. Y si la diferencia importa,
pedirle al asesor los datos que faltan para reconciliarlas antes de emitir.

*Origen:* detectado en el deck de canje, 06/09/2026.

---

## 65. Un instrumento no se confirma de memoria

Cuando el asesor tira un ticker o un nombre de producto y pregunta si es ése,
**la respuesta no sale de la memoria**. Se verifica contra una fuente o se dice
que no se puede confirmar.

*Caso:* Pablo preguntó "creo que es VNUS el que necesito, ¿no?". VNUS no existe
como UCITS; lo que existe es VNRA, Vanguard FTSE North America, que va justo para
el lado contrario del que buscaba. Confirmarlo de memoria habría metido el ticker
equivocado en una orden.

*Y la distinción fina también se verifica:* "MSCI World ex-USA" y "FTSE All-World
ex-US" suenan igual y no lo son —el primero excluye emergentes—. Elegir mal deja
un casillero entero del mandato sin cubrir.

*Qué sí se puede afirmar:* el ISIN, que es unívoco. El ticker de pantalla cambia
según el mercado donde liste. Y **si el instrumento está disponible en la
plataforma es dato de la casa**, no se deduce: ver criterio 34.

*Origen:* el deck de canje, 06/09/2026.

---

## 66. La etiqueta de un gráfico no lleva puntos

Escribí "Acciones USA", no "Acciones EE.UU.", en cualquier `label` de donut o de
barras.

*Por qué:* hasta la v1.1 el generador pasaba el decimal a coma con un `replace`
sobre la cadena entera, etiqueta incluida, y "EE.UU." salía impreso "EE,UU,". El
bug está arreglado desde la v1.2 —`pct_coma()` formatea sólo el número— así que
hoy es seguro. Queda anotado porque el defecto pasó la validación, pasó la
generación del PDF y lo encontró Pablo mirando la lámina.

*El criterio general que deja:* cualquier formateo que se aplique a una cadena
armada tiene que tocar sólo la parte que corresponde. Si el `replace` está fuera
del `f-string` del número, está mal.

*Origen:* el deck de canje, 06/09/2026.

---

## 67. Cuando hay dos carteras, cada slide dice cuál está mostrando

Una propuesta que aplica un aporte nuevo tiene **dos carteras conviviendo en el
mismo PDF**: la de hoy y la que queda después. Y varias slides se ven iguales —una
tabla de posiciones, un donut por clase de activo, una fila de tarjetas—, así que
sin rótulo el cliente no sabe cuál está mirando.

**El rótulo va en el título, no en la bajada ni al pie.** Es donde el lector ya
tiene puesto el ojo, y es lo primero que necesita para leer el resto de la slide.

**Y el par tiene que usar la misma palabra en los dos lados.** "Hoy" contra
"Después de la operación" obliga a traducir de una slide a la otra; *pre aporte*
contra *post aporte* se lee sin pensar. Elegí un par y sostenelo.

*Por qué importa más de lo que parece:* con dos carteras cambia la base de los
porcentajes. En el deck de canje el oro pasó de **5,4% a 4,3% sin que se vendiera un
solo gramo** — la posición quedó igual en USD 5.207 y lo que creció fue el
denominador, de 95.547 a 120.547. Un cliente que compara las dos cifras sin saber
que son de carteras distintas lee una venta que nunca ocurrió.

*Lo mismo vale para el resultado.* Una cifra medida sobre la cartera vigente y
otra sobre la resultante no son comparables aunque se llamen igual — ver criterio
64.

*Origen:* pedido de Pablo, 06/09/2026: "las slides que son pre-aporte habría que
indicarlas también porque es un lío si no entender". Quedaron como "Cómo está
compuesta, pre aporte", "El detalle, pre aporte", "Cómo queda la cartera, post
aporte" y "El detalle, post aporte".

---

## 68. Un remate por deck, no uno por slide

Una frase de cierre debajo del contenido —en bajada, más chica, con aire
alrededor— es un recurso fuerte. **Usado una vez por deck golpea; usado en cada
slide es la firma de un texto escrito por una máquina.**

El primer borrador de la propuesta de servicio tenía doce slides y doce remates: "Para
nosotros fue la frase más importante de la reunión", "El fee lo ves todos los
meses. Esto no lo ves nunca. Por eso pesa más", "Un servicio flojo durante un año
es una molestia. Durante veinticinco, es un costo que se acumula solo". Cada una
funciona sola. Las doce juntas se leen como un tic.

*Cómo se reconoce:* si toda slide termina con una frase que no aporta un dato y
existe para dejar resonando algo, sobra en casi todas. Dejá la del capítulo que
más pesa y borrá el resto.

*Lo mismo con la antítesis y la tríada.* "Con los números, sin adjetivos", "Sin
fricción, sin pleitos, y sin que nadie tenga que adivinar qué querías". Una por
documento pasa; en cadena, delata.

*Qué sí queda:* el campo `remate` existe para esto y es uno por deck. Si el
capítulo cierra con un dato o una pregunta que el asesor va a hacer en la
reunión, va ahí. Si es sólo una frase linda, no va.

*Origen:* Pablo, 09/09/2026, sobre el borrador de la propuesta de servicio: "está MUY AI".

---

## 69. Nada de generalizar sobre el cliente

No se le explica al cliente cómo es él, ni qué se pregunta la gente como él.
Prohibidas las construcciones del tipo:

- "Las dos preguntas que se hace **todo el que se retiró a tu nivel**"
- "Hay algo que sabemos de **la gente que dirigió empresas**"
- "Con los ex CEO **nos pasa siempre lo mismo**"
- "**No importa cuántos ceros** tenga la cuenta"

*Por qué está mal:* la propuesta se apoya en lo que el cliente dijo en la
reunión, que es información propia y verificable. Una generalización sobre su
segmento es lo contrario: le informa que lo estamos leyendo desde un molde. A un
cliente sofisticado le suena a manual de ventas, y con razón.

*Qué sí se hace:* decir la misma cosa como observación de su caso. "Tenés por
delante veinte o treinta años de cartera" dice lo mismo que "todo el que se
retiró a tu nivel se pregunta si va a durar", sin el molde.

*Origen:* la propuesta de servicio, 09/09/2026. Es pariente del criterio 19 —escribir desde
la mirada del cliente— y del 46.

---

## 70. Una cita del cliente va una vez

Si la propuesta cita algo que el cliente dijo, aparece **en un solo lugar**. La
segunda vez deja de ser un dato de la reunión y pasa a ser un recurso retórico.

En la propuesta de servicio, "Para mí el servicio es muy importante" abría la slide de
perfil y volvía tres slides después como título de otra. La lección de sus años
en UBS —un costo chico se come una parte grande del interés— también estaba dos
veces. Repetir lo que alguien dijo hace que suene a que lo estamos usando.

*Dónde ponerla:* donde más pese. Normalmente al pie del capítulo de perfil, que
es el que devuelve lo escuchado.

*Origen:* la propuesta de servicio, 09/09/2026.

---

## 71. Un capítulo no repite lo que dijo el anterior

Cada slide tiene que agregar algo. **Si una slide vuelve a enumerar lo que el
lector leyó dos slides antes, se borra**, aunque el formato sea distinto.

El caso: el deck listaba los cuatro compromisos de servicio en una slide, y tres
slides después una tabla "lo que dijiste → lo que nos comprometemos" los volvía a
listar palabra por palabra, con la queja del cliente a la izquierda. El recurso
es bueno; el problema es que no traía nada nuevo.

*Cómo se detecta:* leé sólo los títulos y los bold del deck de corrido. Si dos
capítulos dicen lo mismo con otras palabras, uno sobra.

*Origen:* la propuesta de servicio, 09/09/2026. Es la razón por la que ese deck bajó de doce
páginas a ocho sin perder contenido.

---

## 72. Un descuento sin causa se lee como precio inflado

Cuando la propuesta muestra un fee bonificado al lado del estándar, **tiene que
decir por qué existe la bonificación**. Sin el motivo, el cliente no lee "me
están haciendo un precio": lee "el precio de lista estaba de más".

```
✅  Nos ajustamos sobre el fee estándar para que la estructura te resulte más
    eficiente, y para arrancar una relación de largo plazo.
❌  (la tabla sola, con una columna "fee con bonificación")
```

El motivo es una decisión comercial y se escribe en positivo: qué gana el cliente
y qué apuesta hace la casa. Nunca en disculpa, ni enumerando costos a la
defensiva antes de mostrar el número — eso es el criterio 47.

*Tampoco va lo que paga hoy en otro lado.* Traer el precio del competidor al
frente, justo antes del propio, invita a la comparación que la propuesta todavía
no ganó.

*Origen:* Pablo, 09/09/2026: "¿por qué me bajé los lompas si no?".

---

## 73. La portada la encabeza el cliente, no el tipo de documento

El nombre del cliente es el titular de la portada, en cuerpo grande. "Propuesta
de Inversión" baja a segunda línea. Arriba, la volanta "Preparado para".

*Por qué:* lo primero que tiene que leerse es **para quién está hecho esto**. El
tipo de documento el cliente ya lo sabe: se lo dijimos al mandárselo. Una portada
que grita "Propuesta de Inversión" se parece a todas las propuestas de
inversión; una que dice su nombre en 72px, no.

El generador elige el cuerpo según el largo del nombre —de 72px hasta 36px— así
que un nombre institucional largo entra igual en una línea. Al pie va la leyenda
de confidencialidad del `CONFIG`.

*Sin bloque de contacto:* una pieza genérica —una que usan varios asesores con
varios clientes— no lleva "Presentado por". Ahí el pie queda pegado a la
izquierda, y la fecha y la línea de confidencialidad se alinean por ese mismo eje.
Antes la fecha iba alineada a la derecha de su propio bloque y quedaba colgada,
sin nada contra qué alinearse.

*Origen:* referencia visual de Pablo, 09/09/2026. La portada sin contacto salió de
la pieza del plan de aportes, 20/09/2026.

---

## 74. El logo va en todas las slides, y esa esquina es de la marca

El logotipo va **arriba a la derecha en todas las slides**, siempre en el mismo
punto: `top:34px; right:32px`. Variante positiva sobre fondo claro, negativa
sobre fondo oscuro. Es la extensión del criterio 16.

**El punto es que no se mueva.** Dos slides seguidas con el logo desplazado
cuatro píxeles se nota aunque nadie sepa decir qué le pasa. Si un tipo de slide
necesita un logo distinto, cambia el tamaño, nunca el ancla.

*Consecuencia:* esa esquina es de la marca y de nadie más. Lo que antes vivía
ahí —la pill de nivel de riesgo, el monto destacado— va al renglón de encabezado,
alineado a la derecha, junto al número de slide y el nombre del cliente. La regla
es: **la marca en la esquina, los metadatos en el renglón.**

*Origen:* Pablo, 09/09/2026: "inadmisible que el logo de Max baile entre las
últimas dos slides".

---

## 75. Una tabla de pocas columnas no se estira al ancho de la slide

Con dos o tres columnas y pocas filas, el ancho completo separa tanto las celdas
que la fila deja de leerse como una unidad: el ojo pierde el renglón entre el
concepto y su número. **Esas tablas se angostan y suben de cuerpo.**

El generador lo aplica solo: hasta 3 columnas y 6 filas, la tabla va a 660px y de
9,4px pasa a 12,5px. No hay campo que tocar.

*Es lo contrario de lo que pide una tabla de cartera*, donde hay muchas columnas
y el ancho completo es lo que hace que entren. Por eso el umbral.

*Origen:* Pablo sobre la tabla de advisory fee de la propuesta de servicio, 09/09/2026:
"agrandale la letra y que sea menos ancha porque queda mucho aire al pedo".

---

## 76. Un recuadro destaca dos cosas, no cuatro

El recuadro gris con filete —`destacado` en el capítulo `perfil`— existe para que
el cliente vea **una o dos cosas antes que el resto de la slide**. Con cuatro
ítems adentro deja de destacar: es una lista más, con fondo gris.

En la propuesta de servicio los innegociables eran cuatro: nada más de riesgo argentino,
clases institucionales, Pershing y poder operar él. Entraron dos al recuadro —los
dos límites de fondo— y los otros dos bajaron a la ficha como un rasgo más, "Cómo
operás", porque describen la forma del mandato y no un límite.

*El criterio para elegir:* al recuadro va lo que, si se incumple, mata la
operación. El resto es dato.

*Qué va adentro son reglas del cliente*, no observaciones de la casa. Si el ítem
es una creencia suya ("en renta fija el costo importa"), se escribe como la regla
que se desprende de ella ("El costo, en renta fija").

*Origen:* Pablo, 09/09/2026.

---

## 77. No se corre el generador contra un cliente con propuesta enviada

Ni para regenerar, ni para probar, ni con salida al scratchpad. **Para verificar
un cambio de diseño se arma un JSON sintético**, que además es más rápido y
prueba mejor: se le ponen a mano los casos raros que ninguna propuesta real
tiene.

El caso: para confirmar que mover el logo no rompía nada, se corrió el generador
sobre los JSON de cuatro clientes con propuesta enviada. No se escribió ningún
archivo de esas carpetas y estuvo mal igual — la regla no es "no los rompas", es
"no los toques". El JSON sintético que se armó después, con pill de riesgo y
monto destacado, probó el caso que ninguna propuesta viva ejercitaba.

*Por qué la regla es tan dura:* el asesor revisa y aprueba antes de que algo
llegue al cliente. Un archivo que cambia solo se saltea ese control, y frente al
cliente la única referencia válida es lo que él recibió.

*Origen:* corrección de Pablo, 09/09/2026. Ver también el criterio 78.

---

## 78. Un cambio de la skill que afecta propuestas enviadas se avisa en el momento

Los PDF ya enviados quedan congelados en disco, pero **la fuente de la que
salieron se mueve con cada cambio de la skill**. Después de tocar la portada, el
logo y el encabezado, regenerar una propuesta vieja produce un documento distinto del que el
cliente tiene en la mano.

Eso hay que decirlo **cuando se hace el cambio**, no al final. El asesor decide
qué hacer con esa diferencia: puede no importarle, o puede ser motivo para
versionar antes de seguir.

**Y no es sólo diseño.** El 09/09/2026 legales corrigió la leyenda regulatoria de
"AN Propio" a "AN Integral": las tres propuestas ya enviadas describen mal la
licencia de la casa. Un cambio en el `CONFIG` legal es siempre un aviso, porque
deja de ser una cuestión de herramienta.

*Origen:* corrección de Pablo, 09/09/2026.

---

## 79. El esquema de comisiones no se nombra sin confirmación del asesor

**Nada sobre el esquema de cobro entra a la propuesta si el asesor no confirmó,
expresamente, que con este cliente ese tema ya se habló.** Ni "fee based", ni
"honorario de administración", ni "sin comisión por operación", ni "primer paso
hacia otro esquema". Ni en la portada, ni en la razón de una compra, ni en un
texto de cierre.

Se pregunta al arrancar, en el paso 0, igual que quiénes firman. Si la respuesta
no es un sí claro, el tema no existe para el documento.

*Por qué:* con muchos clientes el esquema de comisiones no se conversa, y no
hace falta. Se puede proponer un producto administrado —una cuenta administrada
es exactamente eso— **por el lado del producto**: qué hace, cómo diversifica,
quién lo gestiona, cómo le fue. Es una forma indirecta de llegar al mismo lugar,
y es la correcta. Un documento que plantea el cambio de esquema por su cuenta le
abre al asesor una conversación que él no eligió tener, y encima por escrito.

*Qué pasaba:* la skill decía, como política comercial, "empujá hacia fee based" y
"así hay que proponerlos", y ofrecía el argumento de cuentas administradas "tal
cual" para la propuesta. No distinguía entre la regla que decide qué productos
van y el mensaje al cliente, y la política interna terminó escrita en el
documento.

*Cómo se rompió:* el rebalanceo armado por otro asesor salió con este
subtítulo de portada:

> Un primer paso hacia el esquema de honorario de administración.

Y la razón de compra de la cuenta administrada decía "primer paso hacia el
esquema de honorario de administración: diversificación global, sin comisión por
operación". La misma idea contada desde el producto: *"Diversificación global en
una cartera de ETFs gestionada activamente."*

*Origen:* corrección de Pablo sobre un rebalanceo armado por otro asesor del
equipo con la skill, 16/09/2026.

---

## 80. La posición actual se muestra por clase de activo y por tipo de riesgo

Cuando la propuesta muestra la cartera vigente del cliente, lleva **dos gráficos
lado a lado**: la distribución por **clase de activo** y la distribución por
**tipo de riesgo**. Con las mismas categorías que usa su reporte de posición.

*Por qué dos:* cada una contesta otra pregunta. La clase de activo dice cuánto es
renta fija, cuánto renta variable, cuánto estructurado. El tipo de riesgo dice
**a qué está expuesto**: ON corporativa, soberano, provincial, equity argentino,
equity internacional, oro. Dos carteras con 60% de renta fija pueden tener
riesgos que no se parecen en nada.

*Por qué las categorías del reporte:* el cliente ya las ve todos los meses. Si la
propuesta usa otras, tiene que traducir, y cuando algo no coincide lo que piensa
es que un papel está mal. Ver criterio 64.

*Cómo se arma:* un capítulo `distribuciones` con los dos gráficos en `graficos`,
y si hacen falta, los números del reporte —aportes, resultado, valuación— como
`kpis` arriba. **No** un solo gráfico por activo en una lámina, la clase de
activo como tabla en otra y la custodia en una tercera: tres láminas flacas donde
entra una buena. La custodia rara vez es información para el cliente; si el
asesor la pide, que vaya como nota.

*Cómo se rompió:* la posición actual ocupaba tres láminas —un donut por
activo, una tabla por clase de activo, una tabla por custodia—, cada una casi
vacía, y nunca mostraba el tipo de riesgo.

*Origen:* corrección de Pablo sobre el rebalanceo de otro asesor, 16/09/2026.

---

## 81. La leyenda es una tabla, y el recuadro rodea el gráfico

Tres reglas para todo donut, en el deck y en el one-pager:

**Los porcentajes van en columna, alineados a la derecha.** No a continuación de
cada etiqueta, a distinta altura horizontal según lo que mida el texto.

**Esa columna queda cerca de las etiquetas.** Ni del otro lado de la tarjeta ni
pegada: la etiqueta más larga y su porcentaje llevan un aire fijo entre medio.

**El recuadro rodea el gráfico, no aire.** Un gráfico solo ocupa media fila, igual
que las tarjetas del criterio 85: la pieza conserva su tamaño y el sobrante queda
a la derecha. A ancho completo, un donut con su leyenda ocupa un tercio del
recuadro y el resto es vacío enmarcado.

*Cómo está hecho:* la leyenda es una `<table>` —etiqueta en una columna,
porcentaje en otra con `text-align:right`— que mide lo que su contenido.

*Por qué una tabla:* hubo dos intentos antes. Con `flex:1` la leyenda se estiraba
hasta el borde y el porcentaje quedaba a 576px de su etiqueta. Con flex y
`max-content` salía bien en el Chromium del generador, pero esa propuesta se armó
en un entorno donde eso no se resolvió igual: el porcentaje quedó pegado
al texto y el filete cruzó la tarjeta de lado a lado. Una tabla se dibuja igual
en cualquier motor.

*Ojo con los atajos de padding:* la compresión máxima del one-pager tenía
`padding:1.8px 0` sobre las celdas de la leyenda. Ese atajo también pone en cero
el margen izquierdo de la columna de porcentajes: salían "Estructurados10,0%".
En reglas que achican una tabla, tocar sólo `padding-top` y `padding-bottom`.

*Cómo se verifica:* lo mide el generador, en el deck y en el one-pager. Avisa si
la columna de porcentajes quedó a más de 60px de las etiquetas, si quedó pegada
(menos de 8px), si los porcentajes no están alineados a la derecha, y si el
gráfico ocupa menos del 55% del ancho de su recuadro.

*Cómo se rompió:* lámina "Posición actual" del rebalanceo de otro asesor, dos veces —
la segunda con la leyenda ya corregida en la v1.4, cuando Pablo la volvió a
generar—.

*Origen:* correcciones de Pablo, 16/09/2026.

---

## 82. Los productos se nombran con su nombre, y un paréntesis no se parte

**Nombre oficial, completo, en todos lados.** La cuenta administrada de CEDEARs
de ETFs es **"Cuenta Administrada CEDEARs de ETFs"** — en fichas, tablas y
columnas de comprar/vender. No "Cartera CEDEARs de ETFs (cuenta administrada)".
El detalle de nombres está en [`oferta.md`](oferta.md).

**Y un paréntesis corto nunca queda partido entre dos renglones.** "(cuenta /
administrada)" se lee como un error de maquetación, no como una aclaración.

*Cómo:* el generador convierte en no separables los espacios de todo paréntesis
de hasta 30 caracteres: si no entra, baja entero al renglón siguiente. Los más
largos sí pueden partir, porque forzarlos a una tira desbordaría la columna.
Pero la mejor solución sigue siendo no necesitar el paréntesis: un nombre que se
explica con una aclaración es un nombre que todavía no se eligió.

*Cómo se rompió:* en la columna "Comprar" de ese mismo rebalanceo el ítem salió
"Cartera CEDEARs de ETFs (cuenta" en un renglón y "administrada)" en el otro.

*Origen:* corrección de Pablo, 16/09/2026.

---

## 83. Un producto nuevo se presenta con su track record

**Cuando la propuesta suma un producto que el cliente no tiene, va una lámina con
cómo le fue**, además de lo que hace. Objetivo y estrategia describen; los números
convencen.

*Qué incluye:* los datos del fact sheet vigente — rendimiento anualizado en las
ventanas que el asesor elija, volatilidad, caída máxima y tiempo de recuperación,
y los retornos por año calendario si el fact sheet los trae. Se arma con un
capítulo `distribuciones` con `kpis` arriba y la composición abajo, o con `kpis`
más una `tabla` de retornos anuales.

*De dónde salen los números:* **del fact sheet vigente que aporta el asesor.**
Nunca de la memoria, de `oferta.md` ni de una propuesta anterior: cambian todos
los meses. Si no lo subió, pedíselo antes de armar la lámina — ver criterio 65.
Y las ventanas las elige él, mirando todas — ver criterio 61.

*Cómo se rompió:* una propuesta sumaba el saldo de una cuenta
administrada de CEDEARs de ETFs y le dedicaba una lámina entera: objetivo y
estrategia, sin un solo número de desempeño.

*Origen:* corrección de Pablo, 16/09/2026.

---

## 84. La cartera resultante se cuenta por tipo de riesgo, antes y después

La lámina de cómo queda la cartera —criterio 51— muestra **cómo varía cada tipo
de riesgo**, no sólo cada clase de activo.

*Por qué:* la clase de activo es demasiado gruesa para mostrar un movimiento. En
un rebalanceo que vende ON y compra una cuenta de ETFs, "renta fija −7,7 pp,
renta variable +8,2 pp" es cierto pero dice poco. Lo que el cliente necesita ver
es que baja la exposición a deuda corporativa argentina y sube la de equity
internacional, y eso vive en el tipo de riesgo.

*La mejor forma es una tabla con las dos cosas:* agrupada por clase de activo, con
una fila por tipo de riesgo y columnas **antes, después y variación**, con
subtotal por grupo y total. Es la misma lógica de la tabla de cartera final,
que agrupa por clase y detalla abajo.

```json
{"tipo": "cartera_sugerida", "titulo": "Así queda la cartera",
 "agrupar_por": "clase", "subtotales": true,
 "columnas": [
   {"clave": "clase", "titulo": "Clase de activo"},
   {"clave": "descripcion", "titulo": "Tipo de riesgo"},
   {"clave": "antes", "titulo": "Antes", "align": "r"},
   {"clave": "despues", "titulo": "Después", "align": "r"},
   {"clave": "variacion", "titulo": "Variación", "align": "r"}],
 "items": [
   {"clase": "Renta fija", "descripcion": "ON corporativa",
    "antes": "45,0%", "despues": "37,3%", "variacion": "−7,7 pp"}],
 "total": {"clase": "Total", "antes": "100,0%", "despues": "100,0%", "variacion": "0,0 pp"}}
```

Los subtotales suman solas las columnas de montos, porcentajes y puntos, cada
una en su formato.

**Variante preferida cuando hay que mover plata: "Gap a cubrir" en USD.** En vez
de la variación en puntos, una columna con cuánto hay que comprar o vender de
cada tipo de riesgo para llegar al objetivo. Es lo que el cliente necesita para
dimensionar la operación: "+USD 367.500 de equity internacional" dice más que
"+29,9 pp".

- **En el JSON, con signo:** `+USD 367.500` si hay que comprar, `−USD 656.000`
  si hay que vender, `USD 0` si no se toca. **En el PDF, el signo se vuelve
  color:** `USD 367.500` en verde, `USD 656.000` en rojo — sin el signo, ver
  criterio 89.
- **La base es la cartera que administramos**, no el patrimonio total del
  cliente.
- **La fila de total cierra en `USD 0`** cuando las compras salen de la liquidez
  de la misma cartera: lo que entra en un tipo de riesgo sale de otro.
- Los subtotales por grupo suman el gap con su signo y se pintan igual que las
  filas.

```json
{"clave": "gap", "titulo": "Gap a cubrir", "align": "r"}
```

con celdas como `"gap": "+USD 367.500"` y `"total": {"gap": "USD 0"}`. Las
columnas de antes y después se llaman como el caso lo pida —"Hoy" y "Objetivo"
en una revisión de posicionamiento—.

*Cómo se rompió:* la última lámina de ese rebalanceo era "Cómo queda distribuida la
cartera" con tres deltas y dos donuts **por clase de activo**, y el movimiento
real —salir de dos ON y entrar en ETFs— no se veía en ningún lado.

*Origen:* corrección de Pablo, 16/09/2026. La variante del gap en USD salió de la
el deck con captura de gráfico, 17/09/2026: la columna había quedado con
`"sumar": false` porque el subtotal no sabía sumar montos con signo.

---

## 85. Pocas tarjetas en una fila miden lo mismo que en una fila de cuatro

Una fila de deltas se divide siempre en **al menos cuatro columnas iguales**. Con
dos o tres tarjetas, cada una ocupa su cuarto de fila, alineada a la izquierda, y
el sobrante queda a la derecha.

*Por qué:* la tarjeta tiene un tamaño propio, el mismo en todo el deck. Si cambia
según cuántas haya, dos láminas del mismo documento muestran la misma pieza a dos
tamaños distintos, y el número —que es lo que importa— pierde presencia justo
cuando hay menos cosas compitiendo con él.

*Lo que no:* ni estirarlas a media lámina cada una —quedan huecas—, ni encogerlas
al ancho de su texto. La v1.2 hacía lo segundo: medían lo que su contenido y
llevaban el texto centrado. Dos tarjetas salían chicas, apretadas y sin aire.

*La referencia:* las cuatro tarjetas de "El efecto sobre la cartera" en la
del primer deck completo. Con dos tarjetas, tienen que medir lo mismo que
las dos primeras de esa fila.

*Cómo se rompió:* la lámina "Cómo queda distribuida" de otro deck, con dos
deltas.

*Origen:* corrección de Pablo, 16/09/2026.

---

## 86. Con tres gráficos en una fila, el donut se apila sobre su leyenda

Con tres gráficos por fila cada tarjeta mide un tercio de la lámina. El donut y su
leyenda **no entran uno al lado del otro**: la leyenda se pasa del borde y los
porcentajes quedan sobre el filete.

*Qué hace el generador:* con tres gráficos apila —**donut arriba, leyenda
debajo**— y el donut **crece** a 132px. Apilados no compiten por el ancho, así que
el tamaño del donut lo decide el alto disponible, no la leyenda.

*Por qué crecer y no achicar:* la primera versión de este criterio resolvía el
problema al revés, bajando el donut a 88px para que entrara al costado. Entraba,
pero la tarjeta más alta de una fila de tres suele ser una de barras largas —diez
u once sectores—, y todas las tarjetas se estiran a ese alto: un donut de 88px
dejaba el recuadro medio vacío. Apilado y grande, lo llena.

*Y el donut va centrado en su tarjeta* (`margin-top/bottom:auto`, como ya hacían
las barras): si no, queda colgado arriba con todo el aire junto abajo.

*La excepción: entre donuts hermanos, alinear gana.* En una fila de tres, el grid
estira las tarjetas al mismo alto, y centrar hace que la de leyenda corta baje su
donut y la de leyenda larga lo suba: ni los donuts ni el arranque de las leyendas
quedan a la misma altura, y la fila se lee desprolija. En ese caso van **alineados
arriba** (`.dist-wrap.n3 .donut-card .donut-row{margin-top:0;margin-bottom:auto}`).
El centrado queda para la tarjeta que no tiene con quién alinearse.

*Lo que el generador mide:* que la leyenda no termine más allá del ancho útil de
su tarjeta. **El control de "recuadro vacío" del criterio 81 no aplica a los
apilados** —ahí el gráfico no ocupa el ancho a propósito— y el generador lo saltea
cuando detecta el apilado.

*Si aun así avisa:* acortá etiquetas —"Equity Int" en vez de "Equity
Internacional"— o poné dos gráficos por fila.

*Cómo se rompió:* en el deck con captura de gráfico las tres tarjetas de una fila
tenían la leyenda pegada al filete, y con siete categorías era peor. La solución
de achicar el donut se reemplazó armando la pieza del plan de aportes, donde una
fila con once sectores dejó el defecto contrario a la vista.

*Origen:* el deck con captura de gráfico, 17/09/2026. Reescrito con la pieza del plan
de aportes, 20/09/2026.

---

## 87. Una captura va recortada al gráfico, con fuente y período

Cuando la propuesta lleva la captura de un gráfico —rendimiento de un ETF desde una
plataforma, un múltiplo de FactSet—:

**Se recorta al gráfico.** Sin pestañas, menús, selectores de período, botones ni
barras de la plataforma. Lo que queda es el eje, la serie y, si hace falta, la
escala. Una captura con la interfaz alrededor se lee como una foto de pantalla
pegada, no como parte de la propuesta.

**La nota dice de dónde sale y qué período muestra.** "Fuente: FactSet. SPY:
rendimiento del 31/05 al 16/09/2026." Sin eso, el cliente no puede saber si el
gráfico es de ayer o de hace un año, ni de quién es el dato. El validador avisa si
la lámina con imagen no tiene nota.

**Va dentro de la skill, no en un parche.** El campo `imagen` del capítulo `kpis`
la dibuja al lado de las tarjetas — ver [`capitulos.md`](capitulos.md). El
generador controla que no se deforme y que no desborde. Un parche fuera de la
skill se pierde la próxima vez que alguien regenera la propuesta.

*Si es muy alta:* una captura cuadrada o vertical desborda la lámina. Recortala a
algo apaisado — la proporción de un gráfico de serie temporal. El alto que la
lámina le deja lo fijan las tarjetas, no la imagen: ver criterio 98. Si en
cambio es muy apaisada, va a lo ancho — criterio 90.

*Cómo se rompió:* en el deck con captura de gráfico el de SPY se sumó con un
script aparte (`parche-grafico-spy.py`) que reemplazaba el cuerpo de la lámina en
el HTML. Regenerar con la skill borraba el gráfico.

*Origen:* el deck con captura de gráfico, 17/09/2026.

---

## 88. El flujo de fondos va sólo a pedido, sobre el calendario del asesor

La lámina de flujo de fondos —capítulo `flujo_de_fondos`— **se arma sólo si el
asesor la pide**. No es un capítulo por defecto de ninguna propuesta con bonos.

**El insumo lo trae él:** el flujo de fondos de cada bono —el xlsx que exporta la
plataforma— y los nominales de cada posición. Si pide la lámina sin traerlos,
pedíselos antes de armar nada. **Los cupones no se calculan de memoria** ni se
deducen de la tasa: un cronograma mal inferido es un número falso con formato de
dato, y el cliente lo va a contrastar contra lo que cobra.

**La cuenta la hace el generador.** Pago cada 100 VN × nominales ÷ 100, sumado por
mes de pago efectivo. Quien escribe el JSON sólo carga ruta y nominales.

**Vista mensual, doce meses.** Renta y amortización apiladas, el total del mes
arriba. Lo que se cobra después de los doce meses va en una tarjeta, nunca como una
barra más: en la misma escala aplasta el gráfico y los doce meses parecen iguales.
Si un bono amortiza dentro de la ventana, esa barra sí domina: es el dato real.

**Colores:** renta en azul y amortización en navy. Ni verde ni naranja —criterio
60—.

*Cómo se verifica:* el validador avisa si un bono no tiene archivo, pagos o
nominales, y si su amortización no suma 100 cada 100 VN. Las cuentas se probaron
contra un cálculo independiente con tres flujos reales (LUC5O, MCC3O y PQCRO) y
dieron exacto.

*Referencias:* la propuesta modelo en planilla de Max Capital ("Vencimientos por
año") y la de un competidor con barras mensuales, que ponía el total posterior a
12 meses como una barra que aplastaba el resto.

*Origen:* pedido de Pablo, 17/09/2026. Los xlsx de ejemplo están en
`material/flujos-de-fondos/`.

---

## 89. En una tabla, signo o color: no los dos

**Una celda que se pinta por su signo se imprime sin el signo.** `+USD 367.500`
sale como `USD 367.500` en verde; `−7,7 pp`, como `7,7 pp` en rojo.

*Por qué:* el signo y el color dicen lo mismo. Juntos, la celda repite la
información dos veces y se ve cargada — y en una tabla de diez filas con gaps y
variaciones, esa repetición es la mitad de la tinta de la columna.

*Cómo:* en el JSON el dato **conserva el signo**, porque es de donde sale el color
y lo que suman los subtotales. El generador lo saca recién al imprimir la celda.
Vale para las filas y los subtotales de `cartera_sugerida` y `cartera_actual`, y
para la `tabla` libre.

*Lo que no cambia:* las **tarjetas de KPI** y los **deltas** no se colorean, así que
conservan el signo: ahí es la única marca de la dirección. `−34,1 pp` en una
tarjeta sigue diciendo `−34,1 pp`. Tampoco cambia el **rótulo de una barra**: se
lee como número, lejos de su barra, y el criterio 97 le deja el signo escrito.

*La excepción, que es importante:* el criterio vale para columnas de
**resultado**, donde rojo significa "perdió". En una columna de **flujo**
—aportes netos, suscripciones y rescates, un flujo de caja— el color miente: un
retiro no es una pérdida. Y sin el signo, `USD 380.000` en una fila de aportes
netos se lee como un aporte cuando fue un retiro: el número dice exactamente lo
contrario de lo que pasó. Esas columnas **escriben el signo y no se pintan**, con
`"signo": ["Neto"]` en el capítulo `tabla` —o `"signo": true` para toda la
tabla—. **Un nombre de la lista selecciona la columna o la fila que se llame
así:** en un corte anual los años son las columnas y el concepto es la primera
celda de cada fila, así que la excepción cae sobre una fila. Nombrarla alcanza. Sigue habiendo una sola marca de la dirección, que es lo que el criterio
pide; lo que cambia es cuál.

*Cómo se rompió:* en un deck de rebalanceo una fila de aportes netos
salió con `−USD 380.000` impreso `USD 380.000` en rojo: sin signo se leía como
aporte y el rojo lo llamaba pérdida, justo al revés del mensaje de la lámina. Se
zafó con paréntesis contables y una nota, fuera de la skill.

*Cómo se rompió:* en el deck con captura de gráfico la columna "Gap a cubrir" salía
con `+USD` en verde y `−USD` en rojo. Se resolvió con una expresión regular en un
parche fuera de la skill, que se perdía al regenerar.

*Origen:* pedido de Pablo, 17/09/2026.

---

## 90. Una captura muy apaisada va a lo ancho, no en media lámina

Una serie temporal recortada al gráfico viene con proporción de **3:1 o más**. En
el layout de media lámina —captura a la izquierda, tarjetas 2×2 a la derecha— el
ancho disponible la reduce hasta volverla ilegible: la línea que el cliente tiene
que leer queda de tres milímetros.

*Cómo:* `"posicion": "abajo"` en el bloque `imagen` del capítulo `kpis`. Las
tarjetas pasan arriba, en una fila a lo ancho, y la captura ocupa toda la lámina
debajo. Ver [`capitulos.md`](capitulos.md).

*Cuándo cada uno:* de 3:1 para arriba, a lo ancho. Más cuadrada que eso, al
costado, que deja las tarjetas más grandes y legibles.

*Detalle:* si el bloque `imagen` no trae `titulo` ni `valor`, la captura va sin
recuadro interno — el recuadro sólo le robaría alto, y el marco ya se lo da el
borde de la propia imagen.

*Cómo se rompió:* la lámina de simulación de aportes tenía una captura de 3,5:1
en media lámina. Pasó de ilegible a ser el centro de la lámina.

*Origen:* pieza del plan de aportes, 20/09/2026.

---

## 91. Dos láminas seguidas con la misma estructura no pueden bailar

Cuando dos láminas consecutivas comparten layout —dos fichas de producto, dos
puntos de entrada, dos capturas con sus tarjetas— **todo lo que no es el dato
tiene que medir exactamente igual**: mismo alto de tarjetas, mismos rótulos, misma
cantidad de líneas, y las capturas del mismo tamaño en píxeles.

*Por qué:* al pasar de una a la otra, lo que se mueve se ve. Si un rótulo ocupa
dos líneas en una y una en la otra, o si una tarjeta lleva nota y la vecina no, el
bloque se rearma y el lector percibe un salto en vez de una comparación.

*El caso más traicionero son las capturas:* dos imágenes de distinta proporción
dan recuadros de distinto alto, y si las tarjetas se estiran al recuadro, cambian
de tamaño con ellas. Por eso las tarjetas al lado de una captura tienen **alto
fijo** y no se estiran — es la misma idea del criterio 26, pero entre láminas.

*Cómo igualar dos capturas:* **agregando margen blanco, nunca recortando**. Se
crea un lienzo del tamaño mayor y se pega la imagen centrada. Recortar pierde
parte del gráfico; el margen no pierde nada y las dos láminas quedan calcadas.

*Cómo se verifica:* renderizando las dos páginas y comparando posiciones — ver
criterio 62 y el método del criterio 92. Mirarlas no alcanza: en la pieza del plan
de aportes las tarjetas **nunca se habían movido**, y se perdieron dos vueltas
buscando el salto donde no estaba. Lo que bailaba era el contenido adentro.

*Origen:* láminas de punto de entrada de la pieza del plan de aportes, 20/09/2026.

---

## 92. Una regla que ajusta una tarjeta hero tiene que nombrar `.hero`

En `deck.css`, las tarjetas grandes se definen así:

```css
.kpi-grid.hero .kpi{padding:20px 18px;min-height:132px;}   /* 0,3,0 */
```

Cualquier regla escrita como `.mi-variante .kpi{...}` tiene especificidad 0,2,0 y
**pierde, aunque esté más abajo en el archivo**. La regla práctica: toda regla que
ajuste una tarjeta dentro de un grid hero se escribe
`.kpi-grid.hero.<variante> .kpi`. Lo mismo para `.k-label`, `.k-value` y
`.k-note`.

*Lo que costó:* fijar `grid-auto-rows:120px` no achicaba nada — la tarjeta
conservaba su `min-height:132px` y **se derramaba 12px sobre la fila de abajo**,
que se ve como tarjetas encimadas: peor que el problema original. Y cuatro reglas
escritas para otra variante no hacían absolutamente nada; las láminas se veían
bien con los valores por defecto. Se borraron: **un CSS que miente sobre lo que
hace es peor que no tenerlo.**

*El control que faltaba:* el generador ahora avisa cuando **dos cajas hermanas se
superponen**, en el deck y en el one-pager. Era el defecto más visible de todos en
un PDF terminado y pasaba en silencio: el control de desborde sólo mira el pie de
la lámina, y el de imagen sólo la proporción. Dice qué lámina, cuántos píxeles y
con qué textos empiezan las dos cajas.

*El método que resolvió el caso:* medir sobre el PDF renderizado en vez de
mirarlo. Rasterizar la página y buscar en una columna los tramos verticales no
blancos da dónde empieza y termina cada caja. Así apareció que la superposición
era de 12px exactos —justo `132 − 120`—, que llevó directo a la causa.

*Origen:* pieza del plan de aportes, 20/09/2026.

---

## 93. Las magnitudes van en dígitos, no en palabras

En una propuesta financiera los números se escriben con números: **5 puntos**,
**3 tramos**, **3 fichas**, **2 carteras**. También cuando abren la oración y
también en el título de una tarjeta, que es donde la regla gramatical de escribir
en letras los números chicos empuja para el otro lado.

*Por qué:* el lector escanea la lámina buscando cifras. "Cinco puntos por tramo"
obliga a leer la frase entera para encontrar la magnitud; "5 puntos por tramo" la
entrega en el primer golpe de vista. Y, como dijo Pablo, *"nadie en finance habla
de puntos en números escritos"*: la forma escrita suena a prosa, no a propuesta.

*Dónde no:* cuando el número no es una magnitud sino parte de una expresión
—"de una", "por un lado"—, y en los textos legales, que tienen su propia
convención.

*Cómo se rompió:* un deck de rebalanceo salió con "Cinco puntos por
tramo" y "Quince puntos de renta variable" en los títulos de las tarjetas.

*Origen:* corrección de Pablo sobre un deck de rebalanceo, 20/09/2026.

---

## 94. El fino de ejecución es del asesor, no del cliente

En la propuesta, **cómo se financia una compra se cuenta por clase de activo y
por monto agregado del tramo**: "se financia con la venta gradual de ONs
corporativas argentinas, USD 1,8M en el primer tramo". Nunca la lista de tickers
con sus nominales y sus precios.

> *"al cliente no le traslado esto, me sirve a mí pero al cliente le vamos con la
> estrategia a grandes rasgos, no con el fino, eso lo veo yo"*

*Por qué:* el fino lo decide el asesor al operar, contra precios que no son los
del informe. Escrito en la propuesta deja de ser un plan y pasa a ser un
compromiso, que después no se cumple al pie de la letra — y cada desvío hay que
explicarlo. El ladder de ventas, los nominales y el orden de ejecución se le
pasan al asesor por chat o en un anexo suyo, no van al PDF.

*Cómo se hace igual:* las tarjetas de comprar y vender del capítulo `trades`
funcionan por clase de activo — se pone la clase en `nombre` y el peso en
`monto`, sin nombrar un solo instrumento. Ver
[`capitulos.md`](capitulos.md). No hace falta descartar el bloque entero para
cumplir el criterio.

*Origen:* indicación de Pablo, reiterada sobre un deck de rebalanceo,
20/09/2026. Ver también criterio 79.

---

## 95. Una clase que viene adentro de un vehículo se abre una sola vez

Cuando un vehículo trae adentro una clase que la cartera no tenía —el oro dentro
de la cuenta administrada de CEDEARs de ETFs— hay que **decidir una sola vez** si
esa clase se abre como categoría propia, y **propagar la decisión a todos lados**:
a los dos gráficos de la lámina, a las tarjetas de delta y a cualquier texto que
cite el porcentaje.

*Por qué:* las dos opciones son defendibles por separado. El oro adentro de renta
variable es más simple de leer; abierto es más preciso. Lo que no se sostiene es
una de cada: dos gráficos de la misma lámina que contestan la misma pregunta con
dos números. Es el criterio 64 en su forma más difícil de ver, porque cada
gráfico está bien y el error sólo aparece al compararlos.

*El control:* el validador avisa cuando dos gráficos de un mismo capítulo
`distribuciones` usan la misma etiqueta con valores distintos. Dice la etiqueta,
los dos valores y en qué gráfico está cada uno.

*Cómo se rompió:* en un deck de rebalanceo el oro entró **dentro** de
renta variable en un gráfico y **aparte** en el otro, en la misma lámina: 16,4%
contra 14,4%. Y la tarjeta de delta decía "+15,0 pp" contando el oro dos veces.
Lo correcto quedó +13,0 pp de renta variable y +2,0 pp de oro, que suman los 15
del vehículo. Lo detectó Pablo, no el validador — de ahí el control.

*Origen:* un deck de rebalanceo, 20/09/2026.

---

## 96. Dos magnitudes distintas no comparten un gráfico

Un gráfico tiene **un solo eje vertical**. Si hay dos magnitudes que no se miden
en lo mismo —facturación y activos administrados, monto y rendimiento— van en
**dos gráficos**, o una va al lado como tarjeta.

*Por qué:* con dos escalas verticales el dibujo lo elige quien arma el gráfico.
Las dos escalas son arbitrarias, así que se las puede mover hasta que las curvas
se crucen donde a uno le conviene, y el cruce —que es lo único que el ojo
retiene— no significa nada. En una propuesta de inversión eso no es un problema
estético.

*Cuándo aparece la tentación:* cuando hay lugar para un gráfico y dos cosas para
contar. La respuesta es contar una y poner la otra en una tarjeta, no apretar las
dos en el mismo dibujo.

*Origen:* un gráfico de referencia que Pablo trajo del tablero del equipo,
20/09/2026. No se replicó, y conviene que quede escrito por qué.

---

## 97. Una serie con negativos se dibuja con eje en cero

Una serie que cruza el cero —aportes netos por año, un flujo de caja, variaciones
contra un período anterior— se dibuja con **el cero donde le corresponde según el
rango**, con las barras saliendo para los dos lados: verde para arriba, rojo para
abajo. En el JSON alcanza con que haya un valor negativo; también se puede pedir
con `"eje_cero": true`.

**La unidad la dice el gráfico.** `"unidad": "USD"` rotula las barras con la
magnitud abreviada —`USD 4,7M`, `−USD 380K`— en vez de tratar los valores como
porcentajes. Los millones llevan un decimal y los miles no.

**El negativo lleva su signo escrito; el positivo va pelado.** Un número sin
signo ya se lee como positivo, así que el `+` no agrega nada; el `−` es lo único
que no se puede perder, porque el rótulo se lee como número —lejos de su barra— y
ahí un retiro sin signo se lee como un aporte. Es la misma razón del criterio 89,
y el caso en que la regla de "signo o color" se resuelve del lado del signo.

**El verde es `#15803D`, no el de la marca.** El verde `#12A150` contra el rojo
`#F31260` da **ΔE 1,3 en deuteranopia**: para un daltónico son el mismo color, y
en un gráfico donde el color *es* el dato eso lo vuelve ilegible. `#15803D` es el
mismo verde un paso más oscuro, da ΔE 10,6 y a simple vista sigue siendo el verde
de Max Capital. Las pastillas de comprar y vender no cambian: ahí el color
acompaña a un texto que ya dice qué es.

**Horizontal o en columnas.** Por defecto salen barras horizontales, como el
resto de los gráficos del deck. `"orientacion": "vertical"` las dibuja como
columnas, que es la forma de leer una serie por año: el tiempo corre de izquierda
a derecha y el signo se ve como arriba o abajo de la línea. Es el dibujo del
tablero del equipo, y el que hay que usar cuando el eje horizontal es tiempo.

**Un donut no acepta negativos** — un gajo no tiene ángulo negativo. Si la serie
los tiene, el generador la manda a barras aunque entre en el máximo de
categorías.

*Si hace falta un gráfico que la skill no dibuja:* que entre por `imagen` como
**SVG**, no rasterizado. El generador inyecta el SVG como markup, así que hereda
el CSS del deck y sale con Inter. Dos trampas que costaron tiempo y ya están
resueltas: un `<img>` es un documento aparte y **no** ve el `@font-face` de la
página —por eso va inline—, y el MIME de un SVG es `image/svg+xml`, no
`image/svg`. Si igual hay que rasterizar con PyMuPDF, ojo: **no hereda
`font-family` de un `<g>`**, hay que ponerlo en cada `<text>` o el render cae a
serif, y eso recién se ve en el PDF terminado.

*Cómo se rompió:* `barras()` clampeaba el ancho a cero y rotulaba siempre en
porcentaje, así que una serie de aportes netos salía con **barra invisible y la
etiqueta "−4718200,0%"**. Para un deck de rebalanceo hubo que generar
un PNG aparte con un script fuera de la skill.

*Origen:* un deck de rebalanceo, 20/09/2026.

---

## 98. El alto de una lámina de KPIs con captura lo mandan las tarjetas

> *"que no exceda en altura a la suma de las cards, las cards te marcan los
> límites"*

En una lámina de `kpis` con `imagen`, **la altura de referencia es la de la
columna de tarjetas**. La captura entra ahí; no es la captura la que fija el alto
de la lámina.

*En números:* para una grilla de 4 tarjetas en 2×2, la imagen tiene que venir en
una proporción cercana a **0,5 (alto/ancho)** — 1200×600 es el caso que quedó
bien. Más alta que eso y empuja a las tarjetas o deja aire; más chata y el
recuadro queda con espacio muerto abajo.

*Por qué:* las tarjetas son el esqueleto de la lámina y se repiten entre láminas;
la captura cambia en cada una. Si el alto lo decide la imagen, dos láminas
seguidas con capturas de distinta proporción dan tarjetas de distinto tamaño y el
bloque salta al pasar — que es el criterio 91.

*Cómo se resuelve si no entra:* recortando la captura, no achicando las
tarjetas. Y si la imagen es mucho más apaisada que 0,5, va a lo ancho con
`"posicion": "abajo"` — criterio 90.

*Origen:* un deck de rebalanceo, 20/09/2026. Va junto al criterio 87.

---

## 99. "Riesgo argentino" es un dato, no una etiqueta para estresar

El dato neutro va: la barra de exposición por geografía con Argentina en 28,3%,
la tabla por tipo de riesgo. Lo que **no** se agrega por cuenta propia es la
etiqueta que lo califica —una tarjeta de delta que diga *"Riesgo argentino −15,0
pp"*, un subtítulo que diga *"15 puntos menos de riesgo argentino"*—.

> *"estamos estresando un concepto que no quiero"*

*Por qué:* el cliente eligió su exposición a la Argentina, muchas veces con el
mismo asesor. Titular la baja como "menos riesgo argentino" convierte una
decisión de asignación en un juicio sobre lo que tenía, y pone a la propuesta a
discutir con el pasado del cliente en vez de con su objetivo. La misma
diversificación se cuenta por lo que suma: más exposición internacional, más
moneda dura, más liquidez.

*Cuándo sí:* **cuando el asesor lo pide.** En el rebalanceo de otro asesor la pastilla
de riesgo argentino con su variación en pp fue un pedido explícito, y ahí va. La
regla es sobre la iniciativa, no sobre la existencia: no lo introduzcas vos.

*Cómo se rompió:* se probó la tarjeta de delta en un deck de rebalanceo y Pablo la
hizo revertir.

*Origen:* corrección de Pablo sobre un deck de rebalanceo, 20/09/2026.

---

## 100. La skill no lleva adentro nombres de clientes

Los criterios cuentan **de qué tipo de pieza** salió cada uno —"un deck de
rebalanceo", "la propuesta de servicio", "el primer one-pager"— con su fecha,
pero **sin el nombre del cliente**. Lo mismo vale para los ejemplos: el cliente
de ejemplo es `"Cliente Ejemplo S.A."`, acá, en `esquema.md`, en
`ejemplos/propuesta_ejemplo.json` y en los comentarios del CSS.

*Los asesores sí van.* `equipo.md` es el directorio de contacto y tiene que estar
completo; un criterio puede nombrar a quien lo pidió. La regla es sobre clientes,
no sobre el equipo.

*Por qué:* la skill la tiene instalada todo el equipo comercial y se reparte por
Drive. Que viaje adentro quién es cliente de quién es información que no necesita
para funcionar, y que no controlamos una vez que el archivo circula. El caso se
entiende igual sin el nombre: lo que enseña un criterio es la situación, no de
quién era la cartera.

*Cómo:* antes de empaquetar una versión, barrer la fuente con los nombres de las
carpetas de `clientes/` y de los archivos de `material/modelos/`, dejando pasar a
los asesores de `equipo.md`. Es un grep, tarda segundos, y es lo único que evita
que se vuelva a colar.

*Cómo se rompió:* la v1.7.1 despersonalizó `criterios.md` entero y aun así
quedaron cuatro casos con apellido y dos nombres de relleno que eran los de un
cliente real de la casa. El porqué de la despersonalización estaba sólo en el
changelog de esa versión, que se entierra a medida que se acumulan versiones.
Por eso pasa a criterio.

*Origen:* pedido de Pablo, 20/09/2026.
