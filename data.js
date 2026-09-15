// ============================================================================
// Base de datos de la discografía — Rolling Stones + solistas.
// Investigado y cruzado con Wikipedia/Discogs. Es un punto de partida (v1):
// se va a seguir completando/corrigiendo con lo que encontremos.
//
// category: "Estudio" | "Vivo" | "Recopilatorio" | "Single/EP" | "Bootleg" | "Box"
// region: "UK" | "US" | "Global" | "" (no aplica / solista)
// artist: "The Rolling Stones" o el nombre del integrante/solista
// ============================================================================

const APP_VERSION = "1.9";

function slug(...parts) {
  return parts
    .join("-")
    .toLowerCase()
    .normalize("NFD").replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

function album(artist, year, title, category, region, label, note) {
  return {
    id: slug(artist, year, title, category, region || ""),
    artist,
    year,
    title,
    category,
    region: region || "",
    label: label || "",
    note: note || "",
  };
}

const RS = "The Rolling Stones";

// ---------------------------------------------------------------------------
// ÁLBUMES DE ESTUDIO — con ediciones UK/US separadas donde el título/tracklist
// difiere (era Decca/London Records, 1964-1971).
// ---------------------------------------------------------------------------
const STUDIO_ALBUMS = [
  album(RS, 1964, "The Rolling Stones", "Estudio", "UK", "Decca", "Debut UK. 12 temas, no incluye \"Not Fade Away\" (sí \"Mona\")."),
  album(RS, 1964, "England's Newest Hit Makers", "Estudio", "US", "London Records", "Equivalente US del debut; tracklist distinto, \"Not Fade Away\" reemplaza a \"Mona\"."),
  album(RS, 1964, "12 X 5", "Estudio", "US", "London Records", "Sin equivalente UK; compilado de EPs UK + grabaciones nuevas."),
  album(RS, 1965, "The Rolling Stones No. 2", "Estudio", "UK", "Decca"),
  album(RS, 1965, "The Rolling Stones, Now!", "Estudio", "US", "London Records", "Equivalente US de No. 2; agrega \"Heart of Stone\", \"Surprise, Surprise\"."),
  album(RS, 1965, "Out of Our Heads", "Estudio", "US", "London Records", "Editado julio 1965; incluye \"(I Can't Get No) Satisfaction\"."),
  album(RS, 1965, "Out of Our Heads", "Estudio", "UK", "Decca", "Editado sept. 1965; tracklist distinto, sin \"Satisfaction\", abre con \"She Said Yeah\"."),
  album(RS, 1965, "December's Children (And Everybody's)", "Estudio", "US", "London Records", "Sin equivalente UK; incluye \"Get Off of My Cloud\"."),
  album(RS, 1966, "Aftermath", "Estudio", "UK", "Decca", "14 temas, sin \"Paint It Black\"."),
  album(RS, 1966, "Aftermath", "Estudio", "US", "London Records", "11 temas; abre con \"Paint It Black\", se sacan 4 temas UK."),
  album(RS, 1967, "Between the Buttons", "Estudio", "UK", "Decca", "Incluye \"Back Street Girl\", \"Please Go Home\"."),
  album(RS, 1967, "Between the Buttons", "Estudio", "US", "London Records", "Cambia esos dos por \"Let's Spend the Night Together\"/\"Ruby Tuesday\"."),
  album(RS, 1967, "Their Satanic Majesties Request", "Estudio", "Global", "Decca / London Records", "Mismo tracklist en ambos territorios."),
  album(RS, 1968, "Beggars Banquet", "Estudio", "Global", "Decca / London Records"),
  album(RS, 1969, "Let It Bleed", "Estudio", "Global", "Decca / London Records", "Último álbum de estudio de la era Decca/London."),
  album(RS, 1971, "Sticky Fingers", "Estudio", "Global", "Rolling Stones Records", "Primer álbum en el sello propio de la banda."),
  album(RS, 1972, "Exile on Main St.", "Estudio", "Global", "Rolling Stones Records"),
  album(RS, 1973, "Goats Head Soup", "Estudio", "Global", "Rolling Stones Records"),
  album(RS, 1974, "It's Only Rock 'n Roll", "Estudio", "Global", "Rolling Stones Records"),
  album(RS, 1976, "Black and Blue", "Estudio", "Global", "Rolling Stones Records"),
  album(RS, 1978, "Some Girls", "Estudio", "Global", "Rolling Stones Records"),
  album(RS, 1980, "Emotional Rescue", "Estudio", "Global", "Rolling Stones Records"),
  album(RS, 1981, "Tattoo You", "Estudio", "Global", "Rolling Stones Records"),
  album(RS, 1983, "Undercover", "Estudio", "Global", "Rolling Stones Records"),
  album(RS, 1986, "Dirty Work", "Estudio", "Global", "Rolling Stones Records / CBS"),
  album(RS, 1989, "Steel Wheels", "Estudio", "Global", "Rolling Stones Records / Columbia"),
  album(RS, 1994, "Voodoo Lounge", "Estudio", "Global", "Virgin"),
  album(RS, 1997, "Bridges to Babylon", "Estudio", "Global", "Virgin"),
  album(RS, 2005, "A Bigger Bang", "Estudio", "Global", "Virgin"),
  album(RS, 2016, "Blue & Lonesome", "Estudio", "Global", "Polydor (UK) / Interscope (US)"),
  album(RS, 2023, "Hackney Diamonds", "Estudio", "Global", "Polydor (UK) / Interscope (US)"),
  album(RS, 2026, "Foreign Tongues", "Estudio", "Global", "Polydor / Capitol", "25to álbum de estudio UK / 27mo US. Producido por Andrew Watt. 14 temas (15 en la Bonus Track Edition)."),
];

// ---------------------------------------------------------------------------
// ÁLBUMES EN VIVO
// ---------------------------------------------------------------------------
const LIVE_ALBUMS = [
  album(RS, 1966, "Got Live If You Want It!", "Vivo", "US", "London Records", "Editado solo en US; algunas tomas con overdubs de estudio."),
  album(RS, 1970, "Get Yer Ya-Ya's Out! The Rolling Stones in Concert", "Vivo", "Global", "Decca / London Records", "Grabado en la gira US de 1969."),
  album(RS, 1977, "Love You Live", "Vivo", "Global", "Rolling Stones Records"),
  album(RS, 1982, "Still Life (American Concert 1981)", "Vivo", "Global", "Rolling Stones Records"),
  album(RS, 1991, "Flashpoint", "Vivo", "Global", "Rolling Stones Records / Columbia"),
  album(RS, 1995, "Stripped", "Vivo", "Global", "Virgin", "Mayormente acústico, en vivo en estudio/salas chicas."),
  album(RS, 1998, "No Security", "Vivo", "Global", "Virgin"),
  album(RS, 2004, "Live Licks", "Vivo", "Global", "Virgin"),
  album(RS, 2008, "Shine a Light", "Vivo", "Global", "Interscope / Polydor", "Soundtrack del documental de Scorsese."),
  album(RS, 2013, "Sweet Summer Sun: Hyde Park Live", "Vivo", "Global", "Interscope / Eagle Vision"),
  album(RS, 2014, "From the Vault: Hampton Coliseum – Live in 1981", "Vivo", "Global", "Eagle Rock / Eagle Vision", "Grabado el 18/12/1981, Hampton VA (gira Tattoo You)."),
  album(RS, 2014, "From the Vault: L.A. Forum – Live in 1975", "Vivo", "Global", "Eagle Rock / Eagle Vision", "Grabado el 12/7/1975, The Forum, Inglewood (primera gira con Ronnie Wood)."),
  album(RS, 2015, "From the Vault: The Marquee Club – Live in 1971", "Vivo", "Global", "Eagle Rock / Eagle Vision", "Grabado el 26/3/1971, Marquee Club, Londres (show chico/especial de TV, previo a Sticky Fingers)."),
  album(RS, 2015, "From the Vault: Hyde Park Live, 1969", "Vivo", "Global", "Eagle Rock / Eagle Vision", "Grabado el 5/7/1969, Hyde Park, Londres (recital gratuito, debut de Mick Taylor)."),
  album(RS, 2015, "From the Vault: Live in Leeds 1982", "Vivo", "Global", "Eagle Rock / Eagle Vision", "Grabado el 25/7/1982, Roundhay Park, Leeds (cierre de la gira europea 1982, último show de Ian Stewart)."),
  album(RS, 2015, "From the Vault: Live at the Tokyo Dome 1990", "Vivo", "Global", "Eagle Rock / Eagle Vision", "Grabado en febrero de 1990, Tokyo Dome (cierre de la gira Steel Wheels)."),
  album(RS, 2017, "From the Vault: Sticky Fingers Live at the Fonda Theatre", "Vivo", "Global", "Eagle Rock / Eagle Vision", "Grabado el 20/5/2015 (arranque de la gira Zip Code, Sticky Fingers completo en vivo); editado en 2017."),
  album(RS, 2018, "From the Vault: No Security – San Jose 1999", "Vivo", "Global", "Eagle Rock / Eagle Vision", "Grabado el 19-20/4/1999, San Jose Arena (gira No Security)."),
  album(RS, 2016, "Havana Moon", "Vivo", "Global", "Eagle Vision / Universal", "Show gratuito en La Habana, Cuba."),
  album(RS, 2020, "Steel Wheels Live", "Vivo", "Global", "Eagle Rock / Universal", "Grabado en Atlantic City, 1989."),
  album(RS, 2022, "Live at the El Mocambo", "Vivo", "Global", "Mercury Studios / Universal", "Grabado el 4-5/3/1977 en el club El Mocambo, Toronto."),
  album(RS, 2022, "Licked Live in NYC", "Vivo", "Global", "Mercury Studios", "Grabado en el Madison Square Garden, 2003."),
  album(RS, 2023, "GRRR Live!", "Vivo", "Global", "Mercury Studios / Polydor", "Grabado en la O2 Arena de Londres, 2012."),
  album(RS, 2021, "A Bigger Bang: Live on Copacabana Beach", "Vivo", "Global", "Eagle Vision / Universal", "Show gratuito en la playa de Copacabana, Río de Janeiro, 18/2/2006 (gira A Bigger Bang). ~1.5 millones de asistentes."),
  album(RS, 2024, "Live at the Wiltern", "Vivo", "Global", "Mercury Studios / Universal", "Grabado el 4/11/2002 en el Wiltern Theatre, LA (era gira Forty Licks)."),
  album(RS, 2024, "Live At Racket, NYC", "Vivo", "Global", "Rolling Stones Records", "EP en vivo, show sorpresa en el club Racket NYC, 19/10/2023, víspera del lanzamiento de Hackney Diamonds (con Lady Gaga en \"Sweet Sounds of Heaven\"). Exclusivo Record Store Day, vinilo blanco limitado a 7.000 copias."),
  album(RS, 2024, "Welcome to Shepherd's Bush", "Vivo", "Global", "Mercury Studios", "Grabado el 8/6/1999 en el Shepherd's Bush Empire, Londres (gira No Security), ~2.000 personas. Publicado 25 años después."),
  album(RS, 1970, "Gimme Shelter", "Vivo", "Global", "Criterion / Maysles Films", "Documental de 1970 sobre la gira US 1969 y Altamont. No es sello propio de la banda, pero es un film autorizado."),
  album(RS, 1972, "Ladies and Gentlemen: The Rolling Stones", "Vivo", "Global", "Eagle Vision", "Filmada en 1972 (gira US de Exile on Main St., 4 noches en Texas). Estreno en cines 1974; restaurada y editada en DVD/Blu-ray recién en 2010."),
  album(RS, 1989, "25x5: The Continuing Adventures of the Rolling Stones", "Vivo", "Global", "CBS/Fox Video", "Documental de toda la carrera de la banda hasta Steel Wheels. Solo salió en VHS/LaserDisc, nunca tuvo edición en DVD."),
  album(RS, 1991, "Rolling Stones: Live at the Max", "Vivo", "Global", "Eagle Vision", "Grabado en 1990 (gira Steel Wheels/Urban Jungle). Primer film de concierto IMAX de la historia. VHS/LaserDisc 1991; reeditado en DVD/Blu-ray en 2009."),
  album(RS, 1995, "Voodoo Lounge Live", "Vivo", "Global", "Eagle Vision", "Grabado el 25/11/1994, Joe Robbie Stadium, Miami. Versión editada del show (17 de 27 temas); VHS 1995, DVD 1998. Distinto de \"Voodoo Lounge Uncut\" (2018), que es el show completo."),
  album(RS, 2003, "Four Flicks", "Vivo", "Global", "Eagle Vision", "Box de 4 DVD de la gira Licks (2002-03): The Wiltern Theatre (LA), Madison Square Garden (NY), Twickenham Stadium (Londres) y Olympia (París), más documental y extras."),
  album(RS, 2007, "The Biggest Bang", "Box", "Global", "Eagle Vision", "Box de 4 DVD con recortes de varias etapas de la gira A Bigger Bang (2005-06): Zilker Park Austin, Copacabana Rio, Japón/China/Argentina, y documental \"Salt of the Earth\". Se superpone parcialmente con otros discos ya cargados (Copacabana completo, Sweet Summer Sun, GRRR Live!)."),
  album(RS, 2011, "Some Girls: Live in Texas '78", "Vivo", "Global", "Eagle Vision", "Grabado el 18/7/1978, Fort Worth, Texas (gira Some Girls)."),
  album(RS, 2012, "Light the Fuse: Bigger Bang", "Vivo", "Global", "Google Play Music", "Grabado el 10/8/2005 en el Phoenix Concert Theatre, Toronto (show chico previo a la gira A Bigger Bang). Ojo: solo se editó como descarga digital de audio (2012) — nunca tuvo DVD/Blu-ray oficial; los DVD que circulan de este show son bootlegs no oficiales."),
  album(RS, 2016, "Totally Stripped", "Vivo", "Global", "Eagle Vision", "Documental + 3 shows completos de la era Stripped (1995): Amsterdam, París y Brixton Academy (Londres)."),
  album(RS, 2012, "Crossfire Hurricane", "Vivo", "Global", "Eagle Rock / Eagle Vision / HBO", "Documental de toda la carrera (1962-1981) por el 50 aniversario, dirigido por Brett Morgen."),
  album(RS, 2017, "Olé Olé Olé! A Trip Across Latin America", "Vivo", "Global", "Eagle Vision", "Documental de la gira América Latina Olé (2016), con 7 temas en vivo de bonus. Distinto de \"Havana Moon\", que es el show completo de La Habana."),
  album(RS, 2019, "Bridges to Buenos Aires", "Vivo", "Global", "Eagle Vision", "Grabado el 5/4/1998 en el Estadio River Plate, Buenos Aires (última noche de la gira Bridges to Babylon en Argentina), con Bob Dylan invitado en \"Like a Rolling Stone\"."),
  album(RS, 2010, "Stones in Exile", "Vivo", "Global", "Eagle Rock / Eagle Vision", "Documental sobre la grabación de Exile on Main St. (1972), dirigido por Stephen Kijak. Venta standalone y también incluido en la reedición deluxe del álbum (2010)."),
  album(RS, 2012, "Charlie Is My Darling (edición estándar)", "Vivo", "Global", "ABKCO", "Edición simple en DVD/Blu-ray de la gira Irlanda 1965, distinta del box Super Deluxe (que trae además 2CD, vinilo 10\" y libro)."),
  album(RS, 2022, "My Life as a Rolling Stone", "Vivo", "Global", "BBC", "Serie documental de 4 episodios (uno por Jagger, Richards, Wood y un homenaje póstumo a Watts)."),
];

// ---------------------------------------------------------------------------
// RECOPILATORIOS
// ---------------------------------------------------------------------------
const COMPILATION_ALBUMS = [
  album(RS, 1966, "Big Hits (High Tide and Green Grass)", "Recopilatorio", "US", "London Records", "Editado marzo 1966."),
  album(RS, 1966, "Big Hits (High Tide and Green Grass)", "Recopilatorio", "UK", "Decca", "Editado nov. 1966, tracklist distinto al US."),
  album(RS, 1967, "Flowers", "Recopilatorio", "US", "London Records", "Solo US, sin edición UK."),
  album(RS, 1969, "Through the Past, Darkly (Big Hits Vol. 2)", "Recopilatorio", "UK", "Decca", "Portada hexagonal, 12 temas."),
  album(RS, 1969, "Through the Past, Darkly (Big Hits Vol. 2)", "Recopilatorio", "US", "London Records", "10 temas, distinto al UK."),
  album(RS, 1971, "Stone Age", "Recopilatorio", "UK", "Decca", "Primer recopilatorio post-contrato; la banda se opuso a su edición."),
  album(RS, 1971, "Gimme Shelter", "Recopilatorio", "UK/NZ", "Decca", "Rarezas/outtakes de estudio 1968-69."),
  album(RS, 1971, "Hot Rocks 1964-1971", "Recopilatorio", "US", "London Records", "Doble LP, el más vendido de su carrera."),
  album(RS, 1972, "Milestones", "Recopilatorio", "UK", "Decca", "Editado sin consentimiento de la banda."),
  album(RS, 1972, "Rock 'n' Rolling Stones", "Recopilatorio", "UK", "Decca", "Foco en covers de Chuck Berry."),
  album(RS, 1972, "More Hot Rocks (Big Hits & Fazed Cookies)", "Recopilatorio", "US", "London Records", "Complemento de Hot Rocks."),
  album(RS, 1973, "No Stone Unturned", "Recopilatorio", "UK", "Decca", "Lados B / temas de EP, no autorizado."),
  album(RS, 1975, "Metamorphosis", "Recopilatorio", "Global", "ABKCO", "Demos/outtakes inéditos, no autorizado por la banda."),
  album(RS, 1975, "Made in the Shade", "Recopilatorio", "US/Global", "Rolling Stones Records", "Autorizado; cubre la era 1971-74."),
  album(RS, 1975, "Rolled Gold: The Very Best of the Rolling Stones", "Recopilatorio", "UK", "Decca", "Doble LP no autorizado."),
  album(RS, 1977, "Get Stoned (30 Greatest Hits)", "Recopilatorio", "UK", "Arcade Records", "Doble LP de venta por TV; también circuló como \"30 Greatest Hits\"."),
  album(RS, 1978, "20 Golden Greats", "Recopilatorio", "AU/NZ/SA", "Decca", "Solo mercados regionales."),
  album(RS, 1979, "A Slice of Rock 'n' Roll", "Recopilatorio", "AU/NZ", "Decca", "Solo mercados regionales."),
  album(RS, 1980, "Solid Rock", "Recopilatorio", "UK", "Decca", "No autorizado, foco rock and roll."),
  album(RS, 1981, "Sucking in the Seventies", "Recopilatorio", "Global", "Rolling Stones Records", "Autorizado; mezcla hits, remixes, vivo y lados B (1974-80)."),
  album(RS, 1981, "Slow Rollers", "Recopilatorio", "UK", "Decca", "No autorizado, foco baladas."),
  album(RS, 1982, "Story of the Stones", "Recopilatorio", "UK", "Decca", "Doble LP."),
  album(RS, 1984, "Rewind (1971-1984)", "Recopilatorio", "UK/Europa", "Rolling Stones Records / CBS", "Autorizado; tracklist distinto al US."),
  album(RS, 1984, "Rewind (1971-1984)", "Recopilatorio", "US", "Rolling Stones Records / Columbia", "Tracklist distinto al UK/Europa."),
  album(RS, 1989, "Singles Collection: The London Years", "Recopilatorio", "Global", "ABKCO", "3CD/4LP con todos los lados A y B de la era Decca/London, 1963-71."),
  album(RS, 1993, "Jump Back: The Best of The Rolling Stones '71-'93", "Recopilatorio", "UK/Europa/Mundo", "Rolling Stones Records / Virgin", "Primer recopilatorio de la era CD; cubre Sticky Fingers-Steel Wheels."),
  album(RS, 2004, "Jump Back: The Best of The Rolling Stones '71-'93", "Recopilatorio", "US", "Virgin", "Edición US tardía del comp. de 1993."),
  album(RS, 2002, "Forty Licks", "Recopilatorio", "Global", "ABKCO / Virgin / Decca", "2CD, toda la carrera 1963-2002."),
  album(RS, 2005, "Rarities 1971-2003", "Recopilatorio", "Global", "Virgin / Rolling Stones Records", "Versiones en vivo, remixes y rarezas de estudio."),
  album(RS, 2012, "GRRR!", "Recopilatorio", "Global", "ABKCO / Polydor / Interscope", "50 aniversario; toda la carrera + 2 temas nuevos."),
  album(RS, 2019, "Honk", "Recopilatorio", "Global", "Polydor / Interscope", "Recopilatorio ligado a la gira No Filter."),
  album(RS, 2017, "The Rolling Stones: On Air", "Recopilatorio", "Global", "Polydor / UMe", "Sesiones de radio BBC 1963-1965. Edición estándar: 1CD, 18 temas."),
  album(RS, 2017, "The Rolling Stones: On Air (Deluxe Edition)", "Recopilatorio", "Global", "Polydor / UMe", "2CD, 32 temas (18 de la estándar + 14 adicionales)."),
];

// ---------------------------------------------------------------------------
// BOOTLEGS — selección curada de los más relevantes para coleccionistas
// (no exhaustivo; se puede seguir ampliando).
// ---------------------------------------------------------------------------
const BOOTLEGS = [
  album(RS, 1969, "Live'r Than You'll Ever Be", "Bootleg", "", "", "Oakland Coliseum, 9/11/1969. Uno de los primeros bootlegs de rock ampliamente distribuidos; su éxito empujó a la banda a editar \"Get Yer Ya-Ya's Out!\" en 1970."),
  album(RS, 1969, "Get Yer Alternate Ya-Ya's Out", "Bootleg", "", "", "Madison Square Garden, 27-28/11/1969. Tomas fuente sin overdubs usadas para armar el álbum oficial."),
  album(RS, 1969, "Altamont Free Concert (Complete)", "Bootleg", "", "", "Altamont Speedway, 6/12/1969. Grabación completa del recital donde murió Meredith Hunter."),
  album(RS, 1971, "Get Your Leeds Lungs Out", "Bootleg", "", "", "Leeds University, 13/3/1971. Era Mick Taylor; muy valorado desde \"Midnight Rambler\" en adelante."),
  album(RS, 1972, "Necrophilia", "Bootleg", "", "", "Outtakes de estudio de la era Decca/London (1963-1970), pensado originalmente como sucesor de Hot Rocks."),
  album(RS, 1968, "Rock and Roll Circus", "Bootleg", "", "", "Filmado el 11-12/12/1968; Jagger frenó su edición ~30 años; oficializado en 1996."),
  album(RS, 1972, "Cocksucker Blues", "Bootleg", "", "", "Audio ligado al documental suprimido de Robert Frank sobre la gira US de 1972."),
  album(RS, 1972, "Very Ancient, Thank You Kindly", "Bootleg", "", "", "Gira americana 1972 (Exile on Main St. tour), documento casi completo show por show."),
  album(RS, 1973, "Brussels Affair", "Bootleg", "", "", "Forest National, Bruselas, 17/10/1973. Referencia de soundboard; oficializado en 2011 (From the Vault)."),
  album(RS, 1973, "Nasty Music (The Lost Live Album)", "Bootleg", "", "", "Cintas soundboard de la gira europea 1973 (Bruselas, Wembley, Newcastle, Rotterdam)."),
  album(RS, 1975, "L.A. Forum / L.A. Friday", "Bootleg", "", "", "The Forum, Inglewood, julio 1975. Parcialmente oficializado en 2023 como \"L.A. Friday (Live 1975)\"."),
  album(RS, 1976, "Knebworth Fair", "Bootleg", "", "", "Knebworth Park, 21/8/1976. También circula como \"Hot August Night\" / \"Complete Knebworth\"."),
  album(RS, 1977, "El Mocambo 1977", "Bootleg", "", "", "El Mocambo, Toronto, 4-5/3/1977. Grabado por Eddie Kramer; oficializado recién en 2022."),
  album(RS, 1978, "Handsome Girls (King Biscuit Flower Hour)", "Bootleg", "", "", "Gira Some Girls 1978, transmisión FM sindicada."),
  album(RS, 1978, "Oakland (audience recording)", "Bootleg", "", "", "Oakland Coliseum, 26/7/1978. Considerada la mejor grabación de público de la gira."),
  album(RS, 1981, "Hampton Coliseum", "Bootleg", "", "", "Hampton, VA, 18/12/1981. Primer show en vivo transmitido por pay-per-view; oficializado en 2012."),
  album(RS, 1965, "Charlie Is My Darling (Ireland tapes)", "Bootleg", "", "", "Gira Irlanda, sept. 1965. Oficializado como box deluxe en 2012."),
  album(RS, 1969, "Bright Lights, Big City", "Bootleg", "", "", "Outtakes/versiones alternativas de la era Brian Jones (1963-1969), 2CD."),
  album(RS, 1970, "The Trident Mixes", "Bootleg", "", "", "Acetatos de Trident Studios de la era Beggars Banquet/Let It Bleed/Sticky Fingers."),
  album(RS, 1968, "Beggars Banquet Sessions", "Bootleg", "", "", "Olympic Studios, marzo-mayo 1968. Tomas alternativas de Beggars Banquet y Let It Bleed."),
  album(RS, 1976, "Place Pigalle", "Bootleg", "", "", "Outtakes de estudio 1972-1981 (Nellcôte, Musicland, Dynamic Sound, Pathé Marconi, Compass Point)."),
  album(RS, 1997, "The Double Door (Chicago)", "Bootleg", "", "", "Show sorpresa en el club Double Door, Chicago, 26/9/1997, previo a la gira Bridges to Babylon. Bootleg en video profesional muy valorado por coleccionistas."),
  album(RS, 1998, "Rio '98", "Bootleg", "", "", "Show gratuito al aire libre en Río de Janeiro (gira Bridges to Babylon), con más de 1 millón de asistentes según reportes. Bootleg de la transmisión, filmado profesionalmente."),
  album(RS, 1976, "Tour of Europe '76 – Earls Court", "Bootleg", "", "", "Earls Court, Londres, mayo de 1976 (gira europea, era Black and Blue). Bootleg de filmación de TV/venue, nunca editado oficialmente."),
];

// ---------------------------------------------------------------------------
// BOX SETS — cada uno con checkbox separado del álbum original que reedita.
// ---------------------------------------------------------------------------
const BOX_SETS = [
  album(RS, 1978, "The Rolling Stones (5xLP box, RS 30.001-005)", "Box", "", "Decca (Francia)", "Box temprano de la era Decca, un disco por integrante + reedición de Get Yer Ya-Ya's Out."),
  album(RS, 1980, "The Rolling Stones Story", "Box", "", "Decca (Alemania)", "12xLP, compila todo el catálogo Decca UK 1964-1975."),
  album(RS, 1989, "Singles Collection: The London Years", "Box", "Global", "ABKCO", "3CD/4LP con todos los lados A y B 1963-1971."),
  album(RS, 2002, "Forty Licks (Box)", "Box", "Global", "ABKCO/Virgin", "2CD/4LP, edición box del recopilatorio del 40 aniversario."),
  album(RS, 2004, "Singles 1963-1965", "Box", "", "ABKCO", "Box de réplicas de simples 7\", vol. 1 de 3."),
  album(RS, 2004, "Singles 1965-1967", "Box", "", "ABKCO", "Box de réplicas de simples 7\", vol. 2 de 3."),
  album(RS, 2005, "Singles 1968-1971", "Box", "", "ABKCO", "Box de réplicas de simples 7\", vol. 3 de 3."),
  album(RS, 2010, "The Rolling Stones 1964-1969", "Box", "", "ABKCO", "13xLP remasterizado, catálogo Decca UK en mono."),
  album(RS, 2010, "The Rolling Stones 1971-2005", "Box", "", "Universal", "Vinilo remasterizado del catálogo post-1970 hasta A Bigger Bang."),
  album(RS, 2010, "Exile on Main St. (Deluxe/Super Deluxe)", "Box", "Global", "Universal", "Reedición del álbum de 1972 + disco extra de 10 temas inéditos."),
  album(RS, 2011, "Some Girls (Deluxe/Super Deluxe)", "Box", "Global", "Universal", "Reedición del álbum de 1978 con disco extra de outtakes."),
  album(RS, 2011, "The Singles 1971-2006", "Box", "Global", "Universal", "45xCD, réplicas de simples de Sticky Fingers a A Bigger Bang."),
  album(RS, 2012, "Charlie Is My Darling - Ireland 1965 (Super Deluxe)", "Box", "", "ABKCO", "DVD/Blu-ray + 2CD + vinilo 10\" + libro."),
  album(RS, 2012, "GRRR! (Super Deluxe)", "Box", "Global", "ABKCO/Polydor/Interscope", "Box del 50 aniversario, 5CD/vinilo + libro."),
  album(RS, 2015, "Sticky Fingers (Super Deluxe)", "Box", "Global", "Universal", "Reedición del álbum de 1971 con tomas alternativas y disco en vivo extra."),
  album(RS, 2016, "The Rolling Stones in Mono", "Box", "", "ABKCO", "16CD con las mezclas mono originales del catálogo 1964-1969."),
  album(RS, 2017, "Their Satanic Majesties Request (50th Anniversary)", "Box", "", "ABKCO", "Reedición con portada lenticular 3D restaurada, mezclas estéreo y mono."),
  album(RS, 2018, "Beggars Banquet (50th Anniversary Edition)", "Box", "", "Universal", "Reedición en vinilo con \"Sympathy for the Devil\" mono en 12\" y flexi-disc réplica."),
  album(RS, 2018, "Studio Albums Vinyl Collection 1971-2016", "Box", "Global", "Universal", "20xLP, sucesor ampliado del box 1971-2005."),
  album(RS, 2018, "Voodoo Lounge Uncut", "Box", "", "Eagle Vision", "Blu-ray/DVD/2CD/LP del show completo de Miami, gira Voodoo Lounge."),
  album(RS, 2019, "Let It Bleed (50th Anniversary Deluxe)", "Box", "Global", "Universal", "Reedición con vinilo estéreo/mono, SACD, simple 7\" réplica y libro."),
  album(RS, 2020, "Goats Head Soup (Super Deluxe)", "Box", "Global", "Universal", "Reedición del álbum de 1973 con mezclas nuevas, rarezas y \"Brussels Affair\" 1973."),
  album(RS, 2020, "Steel Wheels Live (Deluxe)", "Box", "Global", "Eagle Rock/Universal", "6 discos CD/DVD/Blu-ray de la gira Steel Wheels 1989."),
  album(RS, 2021, "Tattoo You (40th Anniversary Super Deluxe)", "Box", "Global", "Universal", "Reedición del álbum de 1981 con disco \"Lost & Found\" (9 inéditos) + \"Still Life: Wembley 1982\"."),
  album(RS, 2022, "The Rolling Stones Singles 1963-1966", "Box", "", "ABKCO", "18x7\" vinilo, réplicas de simples, vol. 1 de la nueva serie."),
  album(RS, 2023, "Hackney Diamonds (Limited Edition Box)", "Box", "Global", "Polydor/Interscope", "CD+Blu-ray con audio hi-res/Dolby Atmos, libro y portada lenticular."),
  album(RS, 2024, "The Rolling Stones 7\" Singles 1966-1971", "Box", "", "ABKCO", "18x7\" vinilo, réplicas de simples, vol. 2 de la nueva serie."),
  album(RS, 2026, "Foreign Tongues (Box Set)", "Box", "Global", "Polydor / Capitol", "2xVinilo + Blu-ray (Dolby Atmos/5.1/Hi-Res Stereo). También existe una versión \"CD Boxset\" con digisleeve, folleto de letras de 16 páginas, print 7\" y póster desplegable."),
  album(RS, 2019, "The Rolling Stones Rock and Roll Circus (Deluxe Edition)", "Box", "Global", "ABKCO", "Restauración 4K/Dolby Vision del film de 1968 (editado por primera vez en 1996). Incluye 2CD + Blu-ray + DVD."),
];

// ---------------------------------------------------------------------------
// SINGLES / EPs — 1963-2025. Para la era Decca/London (1963-1969) se listan
// UK y US por separado cuando el sello/catálogo difiere.
// ---------------------------------------------------------------------------
const SINGLES_EPS = [
  album(RS, 1963, "Come On", "Single/EP", "UK", "Decca"),
  album(RS, 1963, "I Wanna Be Your Man", "Single/EP", "UK", "Decca"),
  album(RS, 1964, "The Rolling Stones (EP)", "Single/EP", "UK", "Decca"),
  album(RS, 1964, "Not Fade Away", "Single/EP", "UK", "Decca"),
  album(RS, 1964, "Not Fade Away", "Single/EP", "US", "London Records"),
  album(RS, 1964, "Tell Me", "Single/EP", "US", "London Records"),
  album(RS, 1964, "It's All Over Now", "Single/EP", "UK", "Decca"),
  album(RS, 1964, "It's All Over Now", "Single/EP", "US", "London Records"),
  album(RS, 1964, "Time Is on My Side", "Single/EP", "US", "London Records"),
  album(RS, 1964, "Five by Five (EP)", "Single/EP", "UK", "Decca"),
  album(RS, 1964, "Little Red Rooster", "Single/EP", "UK", "Decca"),
  album(RS, 1964, "Heart of Stone", "Single/EP", "US", "London Records"),
  album(RS, 1965, "The Last Time", "Single/EP", "UK", "Decca"),
  album(RS, 1965, "The Last Time", "Single/EP", "US", "London Records"),
  album(RS, 1965, "(I Can't Get No) Satisfaction", "Single/EP", "US", "London Records"),
  album(RS, 1965, "(I Can't Get No) Satisfaction", "Single/EP", "UK", "Decca"),
  album(RS, 1965, "Got Live If You Want It! (EP)", "Single/EP", "UK", "Decca"),
  album(RS, 1965, "Get Off of My Cloud", "Single/EP", "UK", "Decca"),
  album(RS, 1965, "Get Off of My Cloud", "Single/EP", "US", "London Records"),
  album(RS, 1965, "As Tears Go By", "Single/EP", "US", "London Records"),
  album(RS, 1966, "19th Nervous Breakdown", "Single/EP", "UK", "Decca"),
  album(RS, 1966, "19th Nervous Breakdown", "Single/EP", "US", "London Records"),
  album(RS, 1966, "Paint It Black", "Single/EP", "UK", "Decca"),
  album(RS, 1966, "Paint It Black", "Single/EP", "US", "London Records"),
  album(RS, 1966, "Mother's Little Helper", "Single/EP", "US", "London Records"),
  album(RS, 1966, "Have You Seen Your Mother, Baby, Standing in the Shadow?", "Single/EP", "UK", "Decca"),
  album(RS, 1966, "Have You Seen Your Mother, Baby, Standing in the Shadow?", "Single/EP", "US", "London Records"),
  album(RS, 1967, "Let's Spend the Night Together", "Single/EP", "UK", "Decca"),
  album(RS, 1967, "Let's Spend the Night Together", "Single/EP", "US", "London Records"),
  album(RS, 1967, "Dandelion", "Single/EP", "US", "London Records"),
  album(RS, 1967, "We Love You", "Single/EP", "UK", "Decca"),
  album(RS, 1967, "She's a Rainbow", "Single/EP", "US", "London Records"),
  album(RS, 1967, "In Another Land", "Single/EP", "US", "London Records"),
  album(RS, 1968, "Jumpin' Jack Flash", "Single/EP", "UK", "Decca"),
  album(RS, 1968, "Jumpin' Jack Flash", "Single/EP", "US", "London Records"),
  album(RS, 1968, "Street Fighting Man", "Single/EP", "US", "London Records"),
  album(RS, 1969, "Honky Tonk Women", "Single/EP", "UK", "Decca"),
  album(RS, 1969, "Honky Tonk Women", "Single/EP", "US", "London Records"),

  album(RS, 1971, "Brown Sugar", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1971, "Wild Horses", "Single/EP", "US", "Rolling Stones Records"),
  album(RS, 1972, "Tumbling Dice", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1972, "Happy", "Single/EP", "US", "Rolling Stones Records"),
  album(RS, 1973, "Angie", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1973, "Doo Doo Doo Doo Doo (Heartbreaker)", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1974, "It's Only Rock 'n Roll (But I Like It)", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1974, "Ain't Too Proud to Beg", "Single/EP", "US", "Rolling Stones Records"),
  album(RS, 1976, "Hot Stuff", "Single/EP", "US", "Rolling Stones Records"),
  album(RS, 1976, "Fool to Cry", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1978, "Miss You", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1978, "Respectable", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1978, "Beast of Burden", "Single/EP", "US", "Rolling Stones Records"),
  album(RS, 1978, "Shattered", "Single/EP", "US", "Rolling Stones Records"),
  album(RS, 1980, "Emotional Rescue", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1980, "She's So Cold", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1981, "Start Me Up", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1981, "Waiting on a Friend", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1982, "Hang Fire", "Single/EP", "US", "Rolling Stones Records"),
  album(RS, 1982, "Going to a Go-Go (Live)", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1982, "Time Is on My Side (Live)", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1983, "Undercover of the Night", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1984, "She Was Hot", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1984, "Too Much Blood", "Single/EP", "US", "Rolling Stones Records"),
  album(RS, 1986, "Harlem Shuffle", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1986, "One Hit (To the Body)", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1989, "Mixed Emotions", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1989, "Rock and a Hard Place", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1990, "Almost Hear You Sigh", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1990, "Terrifying", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1991, "Highwire", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1991, "Ruby Tuesday (Live)", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1991, "Sex Drive", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1994, "Love Is Strong", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1994, "You Got Me Rocking", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1994, "Out of Tears", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1995, "I Go Wild", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1995, "Like a Rolling Stone (Live)", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1997, "Anybody Seen My Baby?", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1998, "Saint of Me", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 1998, "Out of Control", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 2002, "Don't Stop", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 2003, "Sympathy for the Devil (Fatboy Slim Remix)", "Single/EP", "UK", "ABKCO"),
  album(RS, 2005, "Rough Justice / Streets of Love", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 2005, "Rain Fall Down", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 2006, "Biggest Mistake", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 2010, "Plundered My Soul", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 2012, "Doom and Gloom", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 2012, "One More Shot", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 2016, "Just Your Fool", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 2016, "Hate to See You Go", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 2016, "Ride 'Em on Down", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 2020, "Living in a Ghost Town", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 2020, "Scarlet", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 2020, "Criss Cross", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 2021, "Troubles a Comin'", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 2021, "Living in the Heart of Love", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 2023, "Angry", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 2023, "Sweet Sounds of Heaven", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 2023, "Mess It Up", "Single/EP", "UK", "Rolling Stones Records"),
  album(RS, 2026, "In the Stars", "Single/EP", "UK", "Polydor / Capitol", "Del álbum Foreign Tongues. Lado B: \"Rough and Twisted\" (antes solo en un single físico ultra limitado bajo el seudónimo \"The Cockroaches\")."),
  album(RS, 2026, "Jealous Lover", "Single/EP", "UK", "Polydor / Capitol", "Del álbum Foreign Tongues. Lado B: \"Divine Intervention\"."),
];

// ---------------------------------------------------------------------------
// DISCOGRAFÍA SOLISTA
// ---------------------------------------------------------------------------
const SOLO_ALBUMS = [
  // --- Mick Jagger ---
  album("Mick Jagger", 1985, "She's the Boss", "Estudio", "", "", "Debut solista."),
  album("Mick Jagger", 1987, "Primitive Cool", "Estudio"),
  album("Mick Jagger", 1993, "Wandering Spirit", "Estudio"),
  album("Mick Jagger", 2001, "Goddess in the Doorway", "Estudio"),
  album("Mick Jagger", 2011, "SuperHeavy", "Estudio", "", "", "Proyecto SuperHeavy (Jagger, Joss Stone, Dave Stewart, A.R. Rahman, Damian Marley)."),
  album("Mick Jagger", 2001, "Being Mick", "Vivo", "", "", "Documental para TV (ABC), dirigido por Kevin Macdonald y Jim Gable."),

  // --- Keith Richards ---
  album("Keith Richards", 1988, "Talk Is Cheap", "Estudio", "", "", "Con los X-Pensive Winos."),
  album("Keith Richards", 1991, "Live at the Hollywood Palladium, December 15, 1988", "Vivo", "", "", "Con los X-Pensive Winos."),
  album("Keith Richards", 1992, "Main Offender", "Estudio", "", "", "Con los X-Pensive Winos."),
  album("Keith Richards", 2015, "Crosseyed Heart", "Estudio", "", "", "Con los X-Pensive Winos."),
  album("Keith Richards", 2019, "Talk Is Cheap (30th Anniversary Deluxe Edition)", "Box", "", "", "Reedición deluxe del álbum de 1988."),
  album("Keith Richards", 2026, "Main Offender (30th Anniversary Edition)", "Box", "", "BMG", "Reedición del álbum de 1992."),
  album("Keith Richards", 2015, "Keith Richards: Under the Influence", "Vivo", "", "", "Documental dirigido por Morgan Neville, Netflix."),

  // --- Bill Wyman ---
  album("Bill Wyman", 1974, "Monkey Grip", "Estudio", "", "", "Debut solista."),
  album("Bill Wyman", 1976, "Stone Alone", "Estudio"),
  album("Bill Wyman", 1982, "Bill Wyman", "Estudio", "", "", "Álbum homónimo."),
  album("Bill Wyman", 1992, "Stuff", "Estudio", "", "", "Edición limitada, solo Japón/Argentina."),
  album("Bill Wyman", 1997, "Struttin' Our Stuff", "Estudio", "", "", "Bill Wyman's Rhythm Kings."),
  album("Bill Wyman", 1999, "Anyway the Wind Blows", "Estudio", "", "", "Bill Wyman's Rhythm Kings, con Keith Richards."),
  album("Bill Wyman", 2000, "Groovin'", "Estudio", "", "", "Bill Wyman's Rhythm Kings."),
  album("Bill Wyman", 2001, "Double Bill", "Estudio", "", "", "Bill Wyman's Rhythm Kings."),
  album("Bill Wyman", 2004, "Just for a Thrill", "Estudio", "", "", "Bill Wyman's Rhythm Kings."),
  album("Bill Wyman", 2005, "Live", "Vivo", "", "", "Bill Wyman's Rhythm Kings, grabado en Berlín 2004."),
  album("Bill Wyman", 2015, "Back to Basics", "Estudio"),
  album("Bill Wyman", 2018, "Studio Time", "Estudio", "", "", "Bill Wyman's Rhythm Kings."),
  album("Bill Wyman", 2024, "Drive My Car", "Estudio", "", "", "9no álbum solista."),
  album("Bill Wyman", 2025, "Treasury", "Box", "", "", "Box 7CD que abarca 1974-2024, con rarezas/demos."),
  album("Bill Wyman", 2019, "The Quiet One", "Vivo", "", "", "Documental sobre su vida, dirigido por Oliver Murray, armado con su propio archivo personal. Ojo: el apodo \"el callado\" también se usa para Charlie Watts, pero esta película es sobre Wyman."),

  // --- Charlie Watts ---
  album("Charlie Watts", 1986, "Live at Fulham Town Hall", "Vivo", "", "", "Charlie Watts Orchestra."),
  album("Charlie Watts", 1991, "From One Charlie", "Estudio", "", "", "Charlie Watts Quintet, tributo a Charlie Parker."),
  album("Charlie Watts", 1992, "A Tribute to Charlie Parker with Strings", "Vivo", "", "", "Charlie Watts Quintet, grabado en vivo en Ronnie Scott's, Birmingham."),
  album("Charlie Watts", 1993, "Warm & Tender", "Estudio", "", "", "Charlie Watts Quintet."),
  album("Charlie Watts", 1996, "Long Ago & Far Away", "Estudio", "", "", "Charlie Watts Quintet."),
  album("Charlie Watts", 2000, "Charlie Watts/Jim Keltner Project", "Estudio", "", "", "Colaboración con el baterista Jim Keltner."),
  album("Charlie Watts", 2004, "Watts at Scott's", "Vivo", "", "", "Charlie Watts Tentet, en vivo en Ronnie Scott's, Londres."),
  album("Charlie Watts", 2012, "The ABC&D of Boogie Woogie – Live in Paris", "Vivo", "", "", "Grabado 2010, editado 2012."),
  album("Charlie Watts", 2017, "Charlie Watts Meets the Danish Radio Big Band", "Vivo", "", "", "Grabado en vivo en 2010, editado en 2017."),

  // --- Ron Wood ---
  album("Ron Wood", 1974, "I've Got My Own Album to Do", "Estudio", "", "", "Debut solista."),
  album("Ron Wood", 1975, "Now Look", "Estudio"),
  album("Ron Wood", 1976, "Mahoney's Last Stand", "Estudio", "", "", "Soundtrack, co-crédito con Ronnie Lane."),
  album("Ron Wood", 1979, "Gimme Some Neck", "Estudio"),
  album("Ron Wood", 1981, "1234", "Estudio"),
  album("Ron Wood", 1988, "Live at the Ritz", "Vivo", "", "", "Grabado nov. 1987, NYC."),
  album("Ron Wood", 1992, "Slide on This", "Estudio"),
  album("Ron Wood", 1993, "Slide on Live: Plugged in and Standing", "Vivo"),
  album("Ron Wood", 2000, "Live & Eclectic", "Vivo", "", "", "Grabado 1992; reeditado 2002 como \"Live at Electric Ladyland\"."),
  album("Ron Wood", 2001, "Not for Beginners", "Estudio"),
  album("Ron Wood", 2006, "Ronnie Wood Anthology: The Essential Crossexion", "Box", "", "", "2CD antología de toda su carrera."),
  album("Ron Wood", 2025, "Fearless: Anthology 1965-2025", "Box", "", "", "Antología doble de toda su carrera (solista + Faces + Jeff Beck Group), con 4 grabaciones nuevas incluidas (su primer material solista inédito desde 2010), entre ellas una nueva versión de \"You're So Fine\" con Imelda May."),
  album("Ron Wood", 2019, "Somebody Up There Likes Me", "Vivo", "", "", "Documental sobre su vida y carrera, dirigido por Mike Figgis."),
  album("Ron Wood", 2007, "The First Barbarians: Live from Kilburn", "Vivo", "", "", "Grabado 1974, con Keith Richards, Ian McLagan, Kenney Jones, Willie Weeks."),
  album("Ron Wood", 2010, "I Feel Like Playing", "Estudio", "", "", "Con Slash, Billy Gibbons, Flea."),
  album("Ron Wood", 2019, "Mad Lad: A Live Tribute to Chuck Berry", "Vivo"),
  album("Ron Wood", 2021, "Mr. Luck – A Tribute to Jimmy Reed: Live at the Royal Albert Hall", "Vivo"),
  album("Ron Wood", 2006, "Buried Alive: Live in Maryland", "Vivo", "", "", "New Barbarians (proyecto paralelo con Keith Richards), grabado 1979."),

  // --- Mick Taylor ---
  album("Mick Taylor", 1979, "Mick Taylor", "Estudio", "", "", "Álbum homónimo, tras dejar los Stones."),
  album("Mick Taylor", 1990, "Stranger in This Town", "Vivo", "", "", "Con Carla Olson."),
  album("Mick Taylor", 1991, "Too Hot for Snakes", "Vivo", "", "", "Con Carla Olson, grabado en el Roxy, Hollywood."),
  album("Mick Taylor", 1995, "Live at the 14 Below", "Vivo", "", "", "También circula como \"Coastin' Home\"."),
  album("Mick Taylor", 2000, "A Stone's Throw", "Estudio"),
  album("Mick Taylor", 2003, "Shadow Man", "Estudio", "", "", "Origen/crédito comercialmente discutido."),

  // --- Andrew Loog Oldham (productor, no intérprete) ---
  album("Andrew Loog Oldham", 1964, "16 Hip Hits", "Estudio", "", "", "Andrew Oldham Orchestra & Chorus."),
  album("Andrew Loog Oldham", 1964, "Lionel Bart's Maggie May", "Estudio", "", "", "Andrew Oldham Orchestra."),
  album("Andrew Loog Oldham", 1965, "East Meets West", "Estudio", "", "", "Andrew Oldham Orchestra."),
  album("Andrew Loog Oldham", 1966, "The Rolling Stones Songbook", "Estudio", "", "", "Andrew Oldham Orchestra, covers instrumentales de temas de los Stones."),

  // --- Brian Jones ---
  album("Brian Jones", 1971, "Brian Jones Presents the Pipes of Pan at Jajouka", "Estudio", "", "Rolling Stones Records", "Póstumo, grabado en Marruecos en 1968. Único lanzamiento a su nombre."),
];

const ALL_ALBUMS = [
  ...STUDIO_ALBUMS,
  ...LIVE_ALBUMS,
  ...COMPILATION_ALBUMS,
  ...SINGLES_EPS,
  ...BOOTLEGS,
  ...BOX_SETS,
  ...SOLO_ALBUMS,
];

const SOLO_ARTISTS = [
  "Mick Jagger",
  "Keith Richards",
  "Bill Wyman",
  "Charlie Watts",
  "Ron Wood",
  "Mick Taylor",
  "Andrew Loog Oldham",
  "Brian Jones",
];
