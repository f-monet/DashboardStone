# Rolling Stones — Dashboard de Discografía

Página para controlar la colección de discos de The Rolling Stones. Versión actual: **v1.9** (visible al pie de la página).

## Qué es

Página web estática (HTML + CSS + JS, sin backend) con dos vistas:

**The Rolling Stones (banda)**
- Álbumes de estudio 1964-2026, con ediciones UK/US separadas cuando el título o tracklist difiere (Decca, London Records, ABKCO, Rolling Stones Records, etc.)
- Álbumes en vivo 1966-2024, incluyendo lanzamientos "de archivo" editados muchos años después del show
- Recopilatorios, desde el primero (1966) hasta On Air (2017)
- Singles y EPs, 1963-2026
- Bootlegs de interés para coleccionistas (selección curada, ampliable)
- Box sets, cada uno con su propio checkbox aunque reedite un álbum ya cargado

**Discografía Solista** — Mick Jagger, Keith Richards, Bill Wyman, Charlie Watts, Ron Wood, Mick Taylor, Andrew Loog Oldham y Brian Jones, con sus álbumes de estudio, en vivo y box sets.

Cada disco tiene: checkbox de "lo tengo", región, sello discográfico (para la banda), formato (podés tildar varios a la vez: Vinilo/CD/Digital/Cassette/DVD/Blu-ray, para los casos que lo tenés en más de un soporte) y notas. Hay buscador, filtros por tipo (también multi-selección: por ejemplo "Estudio" + "Box" a la vez), y estadísticas de progreso (total, en colección, faltantes, % completado) calculadas sobre la vista/filtro actual.

Los datos del catálogo están en `data.js`. El estado de "tengo/no tengo" (owned/formato/notas) se guarda en **Firebase Firestore** (`firebase-config.js`), así que es el mismo desde cualquier dispositivo/navegador.

## Cómo verla

Abriendo `index.html` en cualquier navegador (no necesita instalación ni servidor).

Para acceder desde el celular vía internet, se puede publicar con **GitHub Pages**:
1. En GitHub → Settings → Pages.
2. Source: Deploy from a branch → elegir la rama y carpeta `/ (root)`.
3. GitHub genera una URL pública (tipo `https://usuario.github.io/proyectocoder/`) accesible desde cualquier dispositivo.

## Historial de versiones

- **v1.9**: los filtros de categoría (Estudio, Vivo, Recopilatorio, etc.) pasan a ser multi-selección — se puede tildar, por ejemplo, "Estudio" y "Box" al mismo tiempo para verlos juntos, en vez de tener que elegir uno solo por vez.
- **v1.8**: agrega documentales de la banda y de integrantes: "Stones in Exile" (2010), "Charlie Is My Darling" en su edición estándar (distinta del box Super Deluxe ya cargado), "My Life as a Rolling Stone" (2022, serie BBC), "Being Mick" de Mick Jagger, "Keith Richards: Under the Influence", "The Quiet One" y "Somebody Up There Likes Me" de Ron Wood. Corrección importante: **"The Quiet One" es sobre Bill Wyman, no sobre Charlie Watts** (ambos comparten el apodo "el callado"), así que quedó cargado en la discografía de Wyman. "Crossfire Hurricane", "25x5" y "Olé Olé Olé!" ya estaban cargados desde la v1.7.
- **v1.7**: agrega los films/documentales en vivo autorizados que faltaban (Ladies and Gentlemen, Gimme Shelter, 25x5, Live at the Max, Voodoo Lounge Live original, Four Flicks, The Biggest Bang, Some Girls Live in Texas '78, Light the Fuse: Bigger Bang, Totally Stripped, Crossfire Hurricane, Olé Olé Olé!, Bridges to Buenos Aires) y el box deluxe 2019 de Rock and Roll Circus. Se suman 3 bootlegs en video de alto interés (The Double Door 1997, Rio '98, Earls Court '76). Correcciones: "12x5" ya estaba cubierto por el álbum de estudio de 1964, no es un DVD aparte; "Light the Fuse: Bigger Bang" nunca tuvo DVD oficial (solo descarga digital de audio, 2012) — se aclara en la nota del disco.
- **v1.6**: completa la serie oficial "From the Vault" (Eagle Rock/Eagle Vision), que solo tenía un disco cargado. Se agregan los 7 que faltaban: Hampton Coliseum 1981, L.A. Forum 1975, The Marquee Club 1971, Hyde Park 1969, Live in Leeds 1982 (el que faltaba y disparó la revisión), Tokyo Dome 1990 y No Security San Jose 1999. También se corrige el año de "Sticky Fingers Live at the Fonda Theatre" (grabado en 2015, editado en 2017 — antes estaba mal cargado como 2015) y se agrega "Live at the El Mocambo" (2022), la edición oficial del show de 1977 que solo estaba cargado como bootleg.
- **v1.5**: el formato pasa de ser un dropdown de una sola opción a checkboxes múltiples (Vinilo, CD, Digital, Cassette, DVD, Blu-ray), para poder marcar que un mismo disco se tiene en varios soportes. Los datos viejos (un solo formato guardado como texto) se siguen leyendo bien, se migran solos la primera vez que se tocan.
- **v1.4**: reemplaza la guitarra 🎸 por el emoji de lengua 👅 en el título y como ícono de la pestaña del navegador (favicon). No se usa el logo oficial de la banda por ser una marca registrada (diseño de John Pasche, propiedad de Musidor B.V.).
- **v1.3**: el estado de "tengo/no tengo" pasa de `localStorage` a **Firebase Firestore**, así que ahora se comparte entre dispositivos/navegadores en tiempo real. Las reglas de Firestore están abiertas (lectura/escritura pública) — bajo riesgo dado el uso personal, pero cualquiera con el link técnicamente podría modificar los datos.
- **v1.2**: agrega "Foreign Tongues" (2026, álbum de estudio nuevo + singles + box), "On Air" (2017, estándar y deluxe), "A Bigger Bang: Live on Copacabana Beach" (2021), "Live at the Wiltern" (2024), "Live At Racket, NYC" (2024), "Welcome to Shepherd's Bush" (2024), la reedición de "Main Offender" de Keith Richards (2026) y "Fearless: Anthology 1965-2025" de Ron Wood. Se agrega el número de versión visible al pie de la página.
- **v1.1**: primera carga completa — discografía de la banda (estudio, vivo, recopilatorios, singles/EPs, bootlegs, box sets) + discografía solista de los 8 integrantes/afines.
- **v1.0**: primera aproximación del dashboard, con datos de ejemplo.

## Próximos pasos

- v1.10 (posible): agregar login simple para que solo el dueño pueda editar, y así cerrar las reglas de Firestore.
- Revisar y corregir la data cargada (puede tener errores u omisiones).
- La lista de bootlegs es una selección curada, no exhaustiva — se puede seguir ampliando.
- Podría faltar alguna edición regional muy específica (compilados solo-mercado, variantes de vinilo de los 70s/80s, etc.) — se agregan a medida que se detecten.

