# Areafitness S.A. — Análisis de la cartera actual (Max Capital, comitente 21519)

Estado de cuenta al 17/09/2026. Total: ARS 593.785.104,43 ≈ **USD 386.150**
(dólar MEP de referencia del propio estado de cuenta: 1.537,56).

## Composición por clase

| Clase | % | ARS |
|---|---:|---:|
| FCI | 37,6% | 222.977.943 |
| Renta Variable (acciones + CEDEARs) | 36,9% | 218.934.490 |
| Renta Fija (ONs/bonos) | 23,0% | 136.705.510 |
| Monedas/cash | 2,6% | 15.164.160 |

Coincide con el 38/37/23/3 redondeado que ya muestra el propio reporte de Max — el
estado de cuenta es internamente consistente.

**69 posiciones de inversión** (sin contar cash): 9 en renta fija, 50 en renta
variable, 10 en FCI. Confirma lo que contás: es una cartera muy fragmentada.

## No es fragmentación pareja: es un ancla enorme + una cola larga de apuestas chicas

**El fondo MAX RENTA FIJA DÓLARES (Clase B MEP) es, solo, el 20,1% de toda la
cartera** (≈USD 77.622) — la posición más grande con una diferencia enorme sobre
cualquier otra. Y está la misma familia de fondo duplicada en otra clase: **MAX
RENTA FIJA DÓLARES Clase D (Cable), apenas 0,32%**. Vale la pena preguntarle a
Nicolás si tiene sentido mantener las dos clases separadas o si conviene
consolidarlas en una sola.

Descontado ese fondo grande, el resto de la cartera (80% del total) se reparte en
68 posiciones bastante más chicas — ahí está la fragmentación real.

## Solapamiento con índices — el pedido específico

**SPY (CEDEAR del S&P 500) convive con 15 de sus propios componentes grandes
sostenidos en forma directa**: GOOGL, MSFT, NVDA, AVGO, AMZN, TSLA, NFLX, V,
ORCL, QCOM, PFE, MCD, LLY, RTX, LMT. Juntas, SPY + esas 15 posiciones son el
**13,7% de la cartera en 16 líneas** — una parte importante es la misma
exposición a la bolsa de EE.UU. contada dos veces: una vez por el índice, otra
por cada acción suelta que ya está adentro del índice.

Mismo patrón, más chico, con **SMH (CEDEAR de semiconductores) + AVGO + NVDA +
ASML + QCOM** (4,4% en 5 líneas — AVGO y NVDA ya se cuentan también en el grupo
de SPY).

## Otros clusters temáticos, spread en posiciones chicas

- **Commodities/minería** (oro, plata, cobre x2, uranio, litio x2): GLD, SLV,
  COPX, URA, FCX, SCCO, VALE, LAC, LAR — 5,6% repartido en 9 posiciones, ninguna
  con peso individual relevante.
- **Brasil/LatAm**: EWZ (ETF Brasil) + VALE + STNE + NU — 4,1% en 4 posiciones,
  con superposición similar a SPY (EWZ ya incluye a VALE).
- **Energía limpia/nuclear**: ICLN, FSLR, OKLO, CEG — 1,8% en 4 posiciones.
- **Utilities**: XLU + CEG — 1,3%, con CEG apareciendo en dos clusters a la vez.
- **Aeroespacial/defensa**: ITA, LMT, RTX — 0,7% en 3 posiciones.
- **Energía/utilities locales**: PAMP, TGSU2, YPFD, TRAN — 3,9% en 4 posiciones.
  Mismo patrón sectorial que vimos con Isaac Nicolay, acá bastante más chico.

## Posiciones chicas de verdad

**19 posiciones están por debajo del 0,3% de la cartera cada una** (algunas por
debajo del 0,1%: ECOG, LAC, LMT, OKLO). Individualmente no mueven la aguja, y
son las que más ensucian el seguimiento día a día.

## Primera poda posible — candidatos, no una propuesta todavía

Con lo que hay a mano, sin entrar en fundamentos (eso lo hacés vos), tres
frentes de reducción de posiciones que no necesitan análisis de research:

1. **Las 19 posiciones por debajo de 0,3%** — candidatas directas a salir o
   consolidarse, aportan poco por su tamaño.
2. **El fondo duplicado en dos clases** — consolidar Clase D en Clase B MEP (o
   al revés), si no hay una razón operativa para tenerlo separado.
3. **Reconsiderar SPY y SMH en simultáneo con sus propios componentes** — no
   necesariamente sacar todo, pero merece la conversación: ¿la convicción está
   en el índice o en los nombres puntuales?

## Lo que no tocamos

No armé un `cartera_actual`/`trades` todavía. Decime con cuáles de estos tres
frentes arrancamos (o si preferís esperar tu análisis de valuación y
crecimiento antes de definir qué sale) y armamos la propuesta.
