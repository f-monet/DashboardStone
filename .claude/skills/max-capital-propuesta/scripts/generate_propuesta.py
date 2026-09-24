#!/usr/bin/env python3
"""
Max Capital — Generador de Propuestas de Inversión.

Toma un JSON normalizado (la "propuesta") y emite un PDF on-brand en uno de
tres formatos. La idea de fondo: el asesor y Claude discuten el CONTENIDO en
lenguaje natural, y este script se encarga de TODO el diseño. Nadie toca
colores, tipografías ni layout a mano.

    python generate_propuesta.py --json propuesta.json --formato deck      --out d.pdf
    python generate_propuesta.py --json propuesta.json --formato onepager  --out o.pdf
    python generate_propuesta.py --json propuesta.json --formato documento --out c.pdf

Flags:
    --design-html <ruta>  exporta el HTML con datos reales (para Claude Design)
    --validar             revisa el JSON y reporta problemas, sin renderizar
    --assets <dir>        carpeta de recursos (default: ../assets)

El contrato del JSON está documentado en reference/esquema.md y el catálogo de
capítulos en reference/capitulos.md.
"""

import argparse
import base64
import html
import json
import math
import os
import re
import sys
import tempfile

# ============================ CONFIG (criterios) ============================ #
# Los criterios del equipo viven acá. Cambiar un criterio = cambiar una línea.
CONFIG = {
    # --- Paginación automática -------------------------------------------- #
    # Una slide 16:9 no puede crecer: si un capítulo trae más filas/fichas que
    # esto, el generador lo parte en varias slides con "(cont.)" en el título,
    # en vez de dejar que el contenido se desborde fuera de la hoja.
    "FILAS_POR_SLIDE": 13,
    "FILAS_POR_SLIDE_DENSA": 19,
    "FICHAS_POR_SLIDE": 6,
    "PASOS_POR_SLIDE": 6,

    # A partir de esta cantidad de filas/fichas la slide entra en modo denso
    # (tipografía y padding proporcionalmente más chicos).
    "UMBRAL_DENSO": 9,

    # --- One-pager --------------------------------------------------------- #
    # El one-pager es UNA hoja. Según cuántas filas tenga la cartera, se aplica
    # compresión progresiva antes que permitir un desborde.
    # Umbrales más bajos que antes: desde que las distribuciones van debajo de la
    # tabla (y no al costado), el contenido se apila y la altura se consume más
    # rápido, así que la compresión tiene que entrar antes.
    "OP_FILAS_TIGHT": 7,
    "OP_FILAS_TIGHTER": 11,

    # La nota de instrumentos es una línea por vehículo: pasado este largo se
    # recorta, porque dos líneas por fondo empujan el bloque contra el pie.
    "OP_NOTA_MAX_CARACTERES": 150,
    # Más filas que esto no entran de forma legible en una sola hoja: el script
    # avisa y sugiere el deck. No trunca en silencio.
    "OP_FILAS_MAXIMO": 22,

    # --- Gráficos ---------------------------------------------------------- #
    # Paleta de las distribuciones. Es una escala de azules de marca + acentos;
    # el orden importa porque las categorías se pintan en el orden en que vienen.
    # Sólo azules, navies y grises. Nada de verde, rojo ni amarillo: son los
    # colores de positivo, negativo y atención, y en una serie de categorías se
    # aplican por orden, sin relación con el significado. En la distribución por
    # calificación crediticia el verde le tocó a "CCC y menor" —el peor rating
    # con el color de "bien"—. Ver criterio 60.
    "COLORES_GRAFICO": ["#006FEE", "#0B2545", "#6BA8F7", "#00396F", "#99C5FA",
                        "#71717A", "#CCE3FD", "#3F5A78", "#A1A1AA", "#D4D4D8"],
    # Con más categorías que esto, el donut se vuelve ilegible y conviene barras.
    "DONUT_MAX_CATEGORIAS": 7,

    # --- Textos fijos ------------------------------------------------------ #
    # ADAPTACIÓN del disclaimer oficial de informes de Max Capital S.A.
    # ------------------------------------------------------------------
    # El texto de informes arranca diciendo que el documento "no constituye
    # recomendación". Una PROPUESTA sí lo es: recomienda instrumentos concretos
    # para un cliente concreto. Sostener esa frase acá sería contradecir el
    # contenido del propio PDF.
    #
    # Cambios respecto del original, y son los únicos:
    #   1. El primer párrafo reconoce que hay recomendación y la funda en el
    #      perfil que aportó el cliente. Se conserva que no es oferta pública.
    #   2. "informe" -> "documento", por coherencia.
    #   3. Se agrega un párrafo sobre proyecciones: una propuesta proyecta
    #      rendimientos, un informe reporta lo ya ocurrido.
    # No se quitó ninguna cláusula del original.
    #
    # Este es el texto vigente para propuestas. No se edita por propuesta: si
    # hace falta un cambio, se cambia acá y vale para todas.
    "DISCLAIMER": (
        "La presente propuesta contiene recomendaciones de inversión elaboradas por Max Capital "
        "S.A. sobre la base de la información aportada por su destinatario respecto de sus "
        "objetivos de inversión, horizonte temporal y tolerancia al riesgo. La presente "
        "propuesta no constituye una oferta ni una invitación dirigida al público en general "
        "para la compra o venta de los valores negociables y/o de los instrumentos financieros "
        "mencionados en él, y no debe ser considerado un prospecto de emisión u oferta pública. "
        "El destinatario deberá evaluar por sí mismo la conveniencia de la inversión en los "
        "valores negociables o instrumentos financieros mencionados y deberá basarse en la "
        "investigación personal que considere pertinente realizar y consultar previamente a un "
        "asesor legal, impositivo y/o cambiario antes de tomar cualquier decisión de inversión. "
        "Algunos de los valores negociables bajo análisis pueden no estar autorizados a ser "
        "ofrecidos públicamente en la República Argentina. Aunque la información contenida en "
        "la presente propuesta ha sido obtenida de fuentes que Max Capital S.A. considera "
        "confiables, tal información puede ser incompleta o parcial y Max Capital S.A. no ha "
        "verificado en forma independiente la información contenida, ni garantiza la exactitud "
        "de la información, o que no se hayan producido cambios en la situación (económica, "
        "financiera o de otro tipo) relativa a los emisores descripta en este documento. Max "
        "Capital S.A. no asume responsabilidad alguna, explícita o implícita, en cuanto a la "
        "veracidad o suficiencia de la misma para efectuar la toma de decisión de su inversión. "
        "Ninguna persona ni funcionario de Max Capital S.A. ha sido autorizada a suministrar "
        "información adicional a la contenida en este documento. Los rendimientos y "
        "proyecciones expuestos constituyen estimaciones elaboradas sobre supuestos de mercado "
        "y no representan rendimientos garantizados ni resultados asegurados; los rendimientos "
        "pasados no garantizan rendimientos futuros. Todas las opiniones o estimaciones "
        "vertidas en la presente propuesta constituyen nuestro juicio y pueden ser modificadas "
        "sin previo aviso. Asimismo, bajo ningún concepto podrá entenderse que Max Capital S.A. "
        "asegura y/o garantiza resultado alguno con relación a posibles inversiones en valores "
        "negociables o instrumentos financieros mencionados en la presente propuesta, siendo el "
        "destinatario del mismo plenamente consciente de los riesgos inherentes a la actividad "
        "bursátil y/o financiera, incluida la pérdida del capital invertido. Consecuencia de lo "
        "reseñado, el destinatario desiste de realizar reclamo alguno a Max Capital S.A., y/o a "
        "cualquier entidad vinculada directa o indirectamente y a sus respectivos directores, "
        "funcionarios, colaboradores y/o agentes, por y contra eventuales daños y perjuicios "
        "que pudiera padecer, sustentando su reclamo en la información brindada por la presente "
        "propuesta. La reproducción o distribución total o parcial de esta propuesta a terceros "
        "está prohibida, salvo permiso. Todos los derechos reservados."),

    # Pie de cada slide: corto, porque se repite en todas.
    "FOOTER_BRAND": "Max Capital S.A. | ©2026 | Todos los derechos reservados.",

    # Área de los asesores. Es siempre la misma, así que no se carga por
    # propuesta ni se pregunta: se usa como valor por defecto del campo `cargo`.
    "AREA": "Wealth Management",

    # Leyenda de confidencialidad al pie de la portada del deck. Es texto de la
    # casa: se escribe una vez acá y no se redacta por propuesta.
    "CONFIDENCIALIDAD": "Estrictamente privado y confidencial",

    # Matrículas completas, texto oficial. Va una sola vez por documento, junto
    # al disclaimer: en el pie de cada slide no entra en una línea y repetirlo
    # nueve veces no agrega nada.
    "LEYENDA_REGULATORIA": (
        "Agente de Liquidación y Compensación y AN Integral N° 570/CNV. Agente de "
        "Administración de Productos de Inversión Colectiva - Fiduciario Financiero Nº 78/CNV. "
        "Agente de Colocación y Distribución Integral de Fondos Comunes de Inversión N° 13/CNV "
        "y Agente de Colocación y Distribución de Fondos Comunes de Inversión Nº 60/CNV."),
}

COLORES = CONFIG["COLORES_GRAFICO"]


# ============================== Utilidades ================================= #

# Paréntesis cortos: hasta este largo el contenido viaja entero de renglón.
PARENTESIS_MAX = 30


def _paren_entero(m):
    return "(" + m.group(1).replace(" ", "\u00a0") + ")"


def esc(s):
    """Escapa para HTML. None -> cadena vacía, para que un campo faltante no
    rompa el render ni imprima 'None' en el PDF.

    Además, un paréntesis corto no se parte: los espacios de adentro pasan a ser
    no separables. "Cartera CEDEARs de ETFs (cuenta / administrada)" dejaba media
    aclaración colgando en un renglón y la otra mitad en el siguiente, que se lee
    como un error. Si no entra, baja el paréntesis entero. Los largos —una
    aclaración de una línea completa— sí pueden partir: forzarlos a una sola
    tira desbordaría la columna. Ver criterio 82."""
    if s is None:
        return ""
    t = html.escape(str(s))
    return re.sub(r"\(([^()]{1,%d})\)" % PARENTESIS_MAX, _paren_entero, t)


def esc_md(s):
    """Como esc(), pero deja pasar **negrita**.

    Se escapa TODO primero y recién después se convierte el marcador, así que
    no hay forma de inyectar HTML desde el JSON: lo único que sobrevive es el
    <b>. Sirve para destacar la frase que sostiene un argumento sin partir el
    párrafo en dos.
    """
    t = esc(s)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t, flags=re.S)


def get(d, *claves, default=None):
    """Lee la primera clave presente. Los asesores (y Claude) escriben las
    claves de formas distintas ('valor'/'value', 'titulo'/'title'); aceptar
    sinónimos evita que la propuesta falle por un nombre."""
    if not isinstance(d, dict):
        return default
    for k in claves:
        if k in d and d[k] not in (None, ""):
            return d[k]
    return default


def a_numero(v):
    """Convierte '12,5%' / 'USD 20.000' / 20000 a float. Devuelve None si no
    hay número reconocible. Acepta formato español (1.234,56) e inglés."""
    if isinstance(v, (int, float)):
        return float(v)
    if v is None:
        return None
    s = str(v).strip()
    s = re.sub(r"[^\d,.\-]", "", s)
    if not s or s in ("-", ".", ","):
        return None
    # Si tiene ambos separadores, el último que aparece es el decimal.
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        # Coma sola: decimal si deja <=2 dígitos a la derecha, si no, de miles.
        ent, _, dec = s.rpartition(",")
        s = f"{ent.replace(',', '')}.{dec}" if len(dec) <= 2 else s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def clase_riesgo(v):
    """Mapea un nivel de riesgo a la pill correspondiente.

    Acepta las dos familias de vocabulario que conviven en el material del
    equipo: "Bajo / Medio / Alto" en las propuestas y "Conservador / Moderado /
    Agresivo" en los fact sheets. Sin esto, un fondo etiquetado "Moderado"
    salía como texto pelado, sin pastilla.
    """
    s = (str(v or "")).strip().lower()
    if s.startswith(("baj", "conserv")):
        return "bajo"
    if s.startswith(("med", "mod")):
        return "medio"
    if s.startswith(("alt", "agres")):
        return "alto"
    return ""


def pct_coma(pct):
    """Un porcentaje con un decimal y coma decimal: 52,3%.

    Existe para que la conversión toque sólo el número. Antes se hacía con un
    `.replace(".", ",")` sobre la cadena entera —etiqueta incluida— y cualquier
    punto del rótulo se convertía en coma: "EE.UU." salía impreso "EE,UU,"."""
    return f"{pct:.1f}%".replace(".", ",")


def celda_signo(v):
    """Clase de color y texto de una celda que se pinta por signo.

    Signo o color, no los dos: "+USD 367.500" en verde repite dos veces lo mismo.
    El color sale del signo que trae el dato y la celda se imprime sin él. Sólo
    aplica a celdas de tabla; las tarjetas de KPI no se colorean y conservan el
    signo, porque ahí es la única marca. Ver criterio 89."""
    clase = clase_signo(v)
    texto = str(v if v is not None else "")
    if clase:
        texto = texto.strip().lstrip("+-−").strip()
    return clase, esc(texto)


def clase_signo(v):
    """Colorea un valor según su signo, para que un resultado negativo se lea
    como negativo sin que nadie tenga que marcarlo."""
    s = str(v or "").strip()
    if s.startswith("-") or s.startswith("−"):
        return "neg"
    if s.startswith("+"):
        return "pos"
    return ""


MESES_ABREV = ["ene", "feb", "mar", "abr", "may", "jun",
               "jul", "ago", "sep", "oct", "nov", "dic"]


def mes_anio(fecha):
    """Convierte '27/08/2026' en 'ago/2026'.

    Una propuesta se fecha por mes: el día exacto en que se armó no le dice nada
    al cliente y envejece el documento más rápido de lo que corresponde. Si el
    valor no tiene formato de fecha se devuelve tal cual, así el asesor puede
    escribir directamente 'ago/2026' o un período propio.
    """
    if not fecha:
        return ""
    m = re.match(r"^\s*(\d{1,2})[/-](\d{1,2})[/-](\d{4})\s*$", str(fecha))
    if m:
        _, mes, anio = m.groups()
        if 1 <= int(mes) <= 12:
            return f"{MESES_ABREV[int(mes) - 1]}/{anio}"
    return str(fecha)


def asesores_de(p):
    """Los contactos de la propuesta, siempre como lista.

    Acepta `asesores` (lista) o `asesor` (uno solo). En Max Capital lo habitual
    es trabajar en dupla, así que el cliente tiene que poder escribirle a los
    dos: preguntá siempre quiénes van, no lo deduzcas de quién te habla.
    """
    lst = get(p, "asesores", "contactos", default=None)
    if lst:
        return lst if isinstance(lst, list) else [lst]
    uno = get(p, "asesor", default=None)
    return [uno] if uno else []


def trozos(lista, n):
    """Parte una lista en bloques de n. Base de la paginación automática."""
    return [lista[i:i + n] for i in range(0, len(lista), n)] or [[]]


# ============================ Gráficos (SVG) =============================== #

def donut(items, tamano=118, grosor=22):
    """Donut de distribución. `items` es [(label, valor)] donde valor puede ser
    número o texto con %. Los valores se normalizan sobre el total, así que
    funciona igual si vienen en % (suman 100) o en montos absolutos."""
    vals, labels = [], []
    for it in items:
        labels.append(get(it, "label", "etiqueta", "categoria", "nombre", default=""))
        vals.append(a_numero(get(it, "valor", "value", "pct", "peso", "monto")) or 0.0)
    total = sum(vals) or 1.0

    r = 70.0

    # Cada gajo es un arco <path> propio. Antes se dibujaban como circles con
    # stroke-dasharray, pero el último gajo terminaba justo sobre la costura
    # donde el path abre y cierra: el navegador lo trazaba cruzando ese punto y
    # le aplicaba un join, que salía como una punta hacia afuera del anillo.
    # Con arcos explícitos no hay costura que cruzar. Ver criterio 54.
    def punto(frac):
        ang = frac * 2 * math.pi - math.pi / 2     # 0 = las 12 en punto
        return f"{r * math.cos(ang):.4f} {r * math.sin(ang):.4f}"

    anillos = [f'<circle r="{r}" cx="0" cy="0" fill="none" stroke="#F4F4F5" '
               f'stroke-width="{grosor}"/>']
    acc = 0.0
    for i, v in enumerate(vals):
        f = (v / total) if total else 0.0
        color = COLORES[i % len(COLORES)]
        if f <= 0:
            continue
        if f >= 0.9999:
            # Un único gajo del 100%: un arco de 360° no dibuja nada porque
            # empieza y termina en el mismo punto. Va el círculo entero.
            anillos.append(f'<circle r="{r}" cx="0" cy="0" fill="none" '
                           f'stroke="{color}" stroke-width="{grosor}"/>')
        else:
            anillos.append(
                f'<path d="M {punto(acc)} A {r} {r} 0 {1 if f > 0.5 else 0} 1 '
                f'{punto(acc + f)}" fill="none" stroke="{color}" '
                f'stroke-width="{grosor}"/>')
        acc += f

    svg = (f'<svg viewBox="0 0 180 180" width="{tamano}" height="{tamano}" '
           f'xmlns="http://www.w3.org/2000/svg">'
           f'<g transform="translate(90,90)">{"".join(anillos)}</g></svg>')

    # Si los valores ya vienen en porcentaje —suman ~100— la leyenda muestra el
    # que escribió el asesor, no uno recalculado. Recalcular sobre el total
    # reintroduce el redondeo y hace que la leyenda contradiga al KPI de la
    # misma slide: 52,3% arriba y 52,2% abajo. Ver criterio 57.
    ya_es_pct = 99.0 <= total <= 101.0
    filas = []
    for i, (lb, v) in enumerate(zip(labels, vals)):
        pct = v if ya_es_pct else v / total * 100
        filas.append(
            f'<tr class="donut-legend-row"><td class="dl-lbl">'
            f'<span class="dot" style="background:{COLORES[i % len(COLORES)]};"></span>'
            # El decimal se pasa a coma SÓLO sobre el número: aplicarlo a toda la
            # cadena se comía los puntos de la etiqueta y "EE.UU." salía "EE,UU,".
            f'<span class="dl-txt">{esc(lb)}</span></td>'
            f'<td class="dl-val"><span>{pct_coma(pct)}</span></td></tr>')
    return svg, "".join(filas)


def _magnitud(v, unidad="%"):
    """El rótulo de una barra: porcentaje, o magnitud abreviada con M y K.

    `unidad` vacía o "%" da 12,3%. Cualquier otra —"USD", "ARS"— da la cifra
    abreviada: USD 4,7M, −USD 380K. Abreviada porque el rótulo de una barra se
    lee de un vistazo, igual que una tarjeta: ver criterio 25. Los millones
    llevan un decimal y los miles no: a esa escala el decimal no cambia ninguna
    decisión y suma tres caracteres a un rótulo que compite por ancho.

    **El negativo siempre lleva su signo; el positivo va pelado.** Un número sin
    signo se lee como positivo, así que el "+" no agrega nada y el "−" es lo
    único que no se puede perder: sin él, un retiro se lee como un aporte."""
    if unidad in (None, "", "%"):
        return pct_coma(v)
    a = abs(v)
    if a >= 1_000_000:
        cifra = f"{a / 1_000_000:.1f}".replace(".", ",") + "M"
    elif a >= 1_000:
        cifra = f"{a / 1_000:,.0f}".replace(",", ".") + "K"
    else:
        cifra = f"{a:,.0f}".replace(",", ".")
    return ("−" if v < 0 else "") + f"{unidad} {cifra}"


def columnas(labels, vals, unidad="%", alto=132):
    """Columnas verticales con el cero donde le toca según el rango.

    Es la forma en que el equipo ya mira una serie por año —el tablero de
    aportes netos—: el tiempo corre de izquierda a derecha y el signo se ve
    como arriba o abajo de la línea. Los alto se calculan acá en píxeles, como
    en el flujo de fondos, para que salga igual en cualquier motor de PDF: un
    alto en porcentaje depende de que el contenedor tenga altura resuelta, y en
    una tarjeta flexible eso no siempre pasa. Ver criterios 88 y 97."""
    vmin, vmax = min(min(vals), 0.0), max(max(vals), 0.0)
    rango = (vmax - vmin) or 1.0
    aire = 16                       # lugar para la cifra arriba y abajo
    y0 = round(vmax / rango * alto) + aire
    cols, rots = [], []
    for lb, v in zip(labels, vals):
        h = max(round(abs(v) / rango * alto), 2)
        arriba = (y0 - h) if v >= 0 else y0
        cifra_y = (arriba - 12) if v >= 0 else (arriba + h + 2)
        cols.append(
            f'<div class="cc-col">'
            f'<span class="cc-cifra" style="top:{cifra_y}px;">{_magnitud(v, unidad)}</span>'
            f'<div class="cc-barra {"pos" if v >= 0 else "neg"}" '
            f'style="top:{arriba}px;height:{h}px;"></div></div>')
        rots.append(f"<span>{esc(lb)}</span>")
    n = len(vals)
    rejilla = f"grid-template-columns:repeat({n},1fr);"
    return (f'<div class="cols-cero">'
            f'<div class="cc-grid" style="{rejilla}height:{alto + aire * 2}px;">'
            f'<div class="cc-eje" style="top:{y0}px;"></div>{"".join(cols)}</div>'
            f'<div class="cc-rot" style="{rejilla}">{"".join(rots)}</div></div>')


def barras(items, normalizar=True, eje_cero=False, unidad="%", orientacion=""):
    """Barras horizontales.

    `normalizar=True` (default) trata los valores como partes de un todo y los
    reparte sobre el total: es lo correcto para una distribución.

    `normalizar=False` los muestra tal cual, con la barra medida sobre 100. Hace
    falta cuando las barras comparan magnitudes INDEPENDIENTES —un antes contra
    un después, dos carteras distintas— donde sumarlas no significa nada.
    Normalizar ahí deforma los números: 63,9% y 38,8% se convertirían en 62,2% y
    37,8% sólo porque suman 102,7.

    `eje_cero=True` —o cualquier valor negativo en la serie— pone el cero donde
    le toca según el rango y dibuja las barras para los dos lados, en verde y
    rojo. Sin eso un negativo salía con barra de ancho cero: el ancho se
    clampeaba a 0 y la etiqueta imprimía el número crudo como porcentaje
    ("−4718200,0%"). Ver criterio 97.

    `unidad` es lo que dice el rótulo: "%" (default) o una moneda.

    `orientacion="vertical"` sobre un gráfico con eje en cero lo dibuja como
    columnas: el tiempo corre de izquierda a derecha, que es como se lee una
    serie por año.
    """
    vals, labels = [], []
    for it in items:
        labels.append(get(it, "label", "etiqueta", "categoria", "nombre", default=""))
        vals.append(a_numero(get(it, "valor", "value", "pct", "peso", "monto")) or 0.0)

    # Una serie con negativos no es una distribución: repartirla sobre un total
    # que mezcla signos no significa nada. Y una magnitud en moneda tampoco se
    # normaliza: si se la reparte sobre el total deja de ser lo que dice el
    # rótulo. En los dos casos los valores van tal cual.
    if any(v < 0 for v in vals):
        eje_cero = True
    if eje_cero or unidad not in (None, "", "%"):
        normalizar = False

    if eje_cero and orientacion.startswith(("vert", "col")):
        return columnas(labels, vals, unidad)

    if eje_cero:
        vmin, vmax = min(min(vals), 0.0), max(max(vals), 0.0)
        rango = (vmax - vmin) or 1.0
        cero = (0.0 - vmin) / rango * 100
        out = []
        for lb, v in zip(labels, vals):
            ancho = abs(v) / rango * 100
            izq = cero if v >= 0 else cero - ancho
            out.append(
                f'<div class="bar-row"><div class="bar-head"><span>{esc(lb)}</span>'
                f'<b>{_magnitud(v, unidad)}</b></div>'
                f'<div class="bar-track">'
                f'<div class="bar-eje" style="left:{cero:.2f}%;"></div>'
                f'<div class="bar-fill {"pos" if v >= 0 else "neg"}" '
                f'style="left:{izq:.2f}%;width:{ancho:.2f}%;"></div>'
                f'</div></div>')
        return f'<div class="bars bars-cero">{"".join(out)}</div>'

    total = sum(vals) or 1.0
    out = []
    for i, (lb, v) in enumerate(zip(labels, vals)):
        pct = (v / total * 100) if normalizar else v
        ancho = min(max(pct, 0), 100)
        out.append(
            f'<div class="bar-row"><div class="bar-head"><span>{esc(lb)}</span>'
            f'<b>{_magnitud(pct, unidad)}'
            f'</b></div><div class="bar-track"><div class="bar-fill" '
            f'style="width:{ancho:.2f}%;background:{COLORES[i % len(COLORES)]};">'
            f'</div></div></div>')
    return f'<div class="bars">{"".join(out)}</div>'


def grafico(g, tamano=118):
    """Elige donut o barras según lo que pidió el capítulo y cuántas categorías
    hay. Un donut de 12 gajos no se lee; en ese caso caen a barras solas."""
    titulo = get(g, "titulo", "title", default="")
    items = get(g, "items", "datos", default=[]) or []
    tipo = (get(g, "tipo", "type", default="") or "").lower()
    # Una serie con negativos no puede ser un donut: un gajo no tiene ángulo
    # negativo. Cae a barras con eje en cero aunque entre en el máximo de
    # categorías. Ver criterio 97.
    negativos = any((a_numero(get(it, "valor", "value", "pct", "peso", "monto")) or 0) < 0
                    for it in items)
    if not tipo:
        tipo = ("barras" if (negativos or len(items) > CONFIG["DONUT_MAX_CATEGORIAS"])
                else "donut")
    elif negativos and not tipo.startswith("barra"):
        tipo = "barras"
    # `normalizar: false` en el gráfico -> los valores se muestran tal cual.
    normalizar = get(g, "normalizar", default=None)
    normalizar = True if normalizar is None else bool(normalizar)
    eje_cero = bool(get(g, "eje_cero", "eje_en_cero", "cero", default=False))
    unidad = get(g, "unidad", "unit", "moneda", default="%") or "%"
    orientacion = str(get(g, "orientacion", "orientation", default="") or "").lower()
    cuerpo = (barras(items, normalizar, eje_cero, unidad, orientacion)
              if tipo.startswith("barra")
              # La leyenda es una <table>: etiqueta en una columna, porcentaje en
              # otra alineada a la derecha, y la tabla mide lo que su contenido.
              # Con flex y max-content dependía de cómo resolviera cada motor de
              # PDF el ancho intrínseco; una tabla se dibuja igual en todos.
              # Ver criterio 81.
              else '<div class="donut-row">%s<table class="donut-legend"><tbody>%s'
                   '</tbody></table></div>' % donut(items, tamano=tamano))
    return f'<div class="donut-card"><h4>{esc(titulo)}</h4>{cuerpo}</div>'


# ============================ Bloques reusables ============================ #

def kpi(item):
    label = get(item, "label", "etiqueta", "titulo", default="")
    valor = get(item, "valor", "value", default="")
    nota = get(item, "nota", "note", "detalle", default="")
    # Valor secundario: sirve para dar el equivalente nominal cuando la cifra
    # principal está en moneda constante. Sin él, un rendimiento real se lee
    # como flojo y nadie sabe que ya tiene la inflación descontada.
    secundario = get(item, "valor_nominal", "valor_secundario", default="")
    cls = " accent" if get(item, "accent", "destacado", default=False) else ""
    h = f'<div class="kpi{cls}"><span class="k-label">{esc(label)}</span>' \
        f'<span class="k-value">{esc(valor)}</span>'
    if secundario:
        h += f'<span class="k-alt">{esc(secundario)}</span>'
    if nota:
        h += f'<span class="k-note">{esc(nota)}</span>'
    return h + "</div>"


# Columnas por defecto del detalle de cartera. Sale del modelo "Propuesta de
# Inversión PH": son las que el equipo ya usa y el cliente ya sabe leer.
COLUMNAS_CARTERA = [
    ("clase", "Clase de Activo", "l"),
    ("descripcion", "Descripción", "l"),
    ("riesgo", "Nivel de Riesgo", "c"),
    ("rendimiento", "Rendimiento esperado", "r"),
    ("plazo", "Plazo de inversión", "c"),
    ("monto", "Monto a invertir", "r"),
]

# Encabezados y alineación de las columnas que el equipo usa además de las de
# arriba. Tenerlos acá evita títulos auto-generados sin tilde ("Ponderacion")
# y que una columna numérica salga alineada a la izquierda.
COLUMNAS_EXTRA = {
    "ponderacion": ("Ponderación", "r"),
    "geografia": ("Geografía", "c"),
    "custodia": ("Custodia", "c"),
    "duration": ("Duration", "r"),
    "vencimiento": ("Vencimiento", "c"),
    "tir": ("TIR", "r"),
    "moneda": ("Moneda", "c"),
    "precio": ("Precio", "r"),
    "nominal": ("Nominal", "r"),
    "trailer": ("Trailer", "r"),
}

SINONIMOS = {
    "clase": ("clase", "clase_activo", "asset_class", "tipo"),
    "descripcion": ("descripcion", "instrumento", "nombre", "detalle", "descripción"),
    "riesgo": ("riesgo", "nivel_riesgo", "nivel_de_riesgo"),
    "rendimiento": ("rendimiento", "rendimiento_esperado", "tir", "ytm", "retorno"),
    "plazo": ("plazo", "plazo_inversion", "horizonte", "vencimiento"),
    "monto": ("monto", "monto_a_invertir", "importe", "nominal"),
    "ponderacion": ("ponderacion", "peso", "ponderación", "participacion", "%"),
    "geografia": ("geografia", "geografía", "region", "país", "pais"),
    "custodia": ("custodia", "custodio"),
}


def celda(item, clave):
    return get(item, *SINONIMOS.get(clave, (clave,)), default="")


def _pct(v):
    """Lee '18,1%' o 18.1 y devuelve float. None si no parece un porcentaje."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    t = str(v).strip().replace("%", "").replace(".", "").replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def controlar_cierre(c, etiqueta, avisos):
    """Avisa cuando una tabla de cartera no cierra.

    El invariante no es "los porcentajes suman 100": es **que la tabla cierre
    con su propio total**. Una tabla de posiciones a vender es un subconjunto y
    sus pesos son sobre la cartera entera — ahí la suma correcta es 40,4%, no
    100%. Lo que nunca puede pasar es que las filas digan una cosa y la fila de
    total otra.

    No corrige solo. Rebasear sobre el total real o repartir la diferencia por
    resto mayor cambia números que el asesor eligió, y esa decisión es suya.
    Ver criterio 58."""
    items = get(c, "items", "posiciones", "instrumentos", default=[]) or []
    if not items:
        return
    total = get(c, "total", default=None)
    pcts = [_pct(get(it, "ponderacion", "peso", "pct", default=None)) for it in items]
    pcts = [x for x in pcts if x is not None]

    if len(pcts) >= 2:
        suma = round(sum(pcts), 1)
        esperado = _pct(get(total, "ponderacion", "peso", default=None)) if total else None
        if esperado is None:
            # Sin fila de total, el único cierre posible es el 100%.
            if abs(suma - 100.0) > 0.05:
                avisos.append(
                    f"{etiqueta}: los porcentajes suman {suma:.1f}% y la tabla no "
                    f"tiene fila de total. Agregá el total, o ajustá los pesos "
                    f"para que cierren en 100%.")
            else:
                avisos.append(f"{etiqueta}: la tabla no tiene fila de total. "
                              f"Una tabla con porcentajes siempre la lleva.")
        elif abs(suma - esperado) > 0.05:
            avisos.append(
                f"{etiqueta}: los porcentajes de las filas suman {suma:.1f}% pero "
                f"la fila de total dice {esperado:.1f}%. Preguntale al asesor si "
                f"ajusta —rebasear sobre el total real, o repartir la diferencia "
                f"por resto mayor—. No lo cambies por tu cuenta.")

    if total:
        montos = [_num(get(it, "monto", "valuacion", default=None)) for it in items]
        montos = [x for x in montos if x is not None]
        dec = _num(get(total, "monto", "valuacion", default=None))
        if montos and dec is not None and abs(sum(montos) - dec) > 0.5:
            avisos.append(
                f"{etiqueta}: la fila de total dice "
                f"{get(total, 'monto', default='')} pero las filas suman "
                f"{sum(montos):,.0f}".replace(",", ".") +
                ". Una tabla tiene que cerrar con su propio total.")


def _num(v):
    """Lee 'USD 1.300.056' y devuelve float. None si no hay número.

    Respeta el signo al principio de la celda: '+USD 367.500', '-USD 656.000' y
    '−USD 656.000' (menos tipográfico). Antes se quedaba sólo con dígitos,
    puntos, comas y el guion ASCII: el '+' se perdía sin consecuencias, pero el
    '−' también, y un monto a vender se leía como uno a comprar."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    crudo = str(v).strip()
    negativo = crudo[:1] in ("-", "−")
    t = "".join(ch for ch in crudo if ch.isdigit() or ch in ",.")
    t = t.replace(".", "").replace(",", ".")
    try:
        n = float(t)
    except ValueError:
        return None
    return -n if negativo else n


def _sumar_columna(valores):
    """Suma una columna de la tabla respetando su formato, o devuelve None si la
    columna no es sumable.

    Reconoce tres formatos: montos ("USD 245.869"), porcentajes ("18,9%") y
    puntos porcentuales con signo ("−7,7 pp"). El formato se toma de la primera
    celda con dato y la suma sale escrita igual —una columna de puntos no puede
    cerrar en porcentaje—. Si las celdas mezclan formatos, o alguna no es un
    número, la columna no se suma: un subtotal inventado es peor que uno vacío.
    """
    vals = [str(v).strip() for v in valores if str(v or "").strip()]
    if not vals:
        return None

    def formato(v):
        # El signo va delante del prefijo de moneda: "+USD 367.500", "−USD 656.000".
        if v.lstrip("+-−").strip().upper().startswith(("USD", "US$", "ARS", "$")):
            return "monto"
        if v.lower().endswith("pp"):
            return "pp"
        if v.endswith("%"):
            return "pct"
        return None

    f = formato(vals[0])
    if f is None or any(formato(v) != f for v in vals):
        return None
    if f == "monto":
        nums = [_num(v) for v in vals]
    else:
        nums = [_pct(v.replace("pp", "").replace("−", "-").strip()) for v in vals]
    if any(n is None for n in nums):
        return None
    total = sum(nums)
    if f == "monto":
        primero = vals[0].lstrip("+-−").strip()
        pref = primero.split()[0] if " " in primero else "USD"
        cifra = f"{pref} " + f"{abs(total):,.0f}".replace(",", ".")
        # Una columna con signo —un gap a cubrir, una variación en USD— devuelve
        # el subtotal con signo, y con el mismo menos que usen sus celdas. Cero
        # va sin signo: "USD 0". Una columna sin signos sigue saliendo sin signo.
        if not any(v[:1] in "+-−" for v in vals):
            return cifra
        if round(total) == 0:
            return f"{pref} 0"
        menos = "−" if any(v[:1] == "−" for v in vals) else "-"
        return ("+" if total > 0 else menos) + cifra
    if f == "pct":
        return pct_coma(total)
    signo = "+" if total > 0.05 else ("−" if total < -0.05 else "")
    return f"{signo}{abs(total):.1f} pp".replace(".", ",")


# Columnas que nunca se suman en un subtotal, aunque traigan "%": un rendimiento,
# una TIR o una duration de dos posiciones no se agregan sumando. Sumarlas daría
# un número con formato impecable y significado nulo. Las demás columnas con
# montos, porcentajes o puntos sí se suman —la ponderación, un "antes" y un
# "después"—. Una columna puede forzarlo con `"sumar": true` o `false`.
NO_SUMABLES = {"rendimiento", "rendimiento_esperado", "tir", "ytm", "retorno",
               "duration", "precio", "plazo", "vencimiento", "riesgo", "tna",
               "tea", "cupon", "volatilidad", "trailer", "rendimiento_anual"}


def _fila_subtotal(cols, grupo, agrupar, sumar=None):
    """Fila de subtotal de un grupo. Suma toda columna sumable de sus filas
    —montos, porcentajes, puntos—, no sólo monto y ponderación: una tabla de
    antes y después por tipo de riesgo tiene dos columnas de porcentaje y una de
    variación, y las tres tienen que cerrar por grupo.

    Un grupo de una sola línea no lleva subtotal: repetiría el mismo número dos
    veces seguidas. Lo decide quien llama."""
    if len(grupo) < 2:
        return ""
    etiqueta_puesta = False
    tds = []
    for clave, _, al in cols:
        base = f"{al} col-{esc(clave)}"
        if clave == agrupar:
            v = ""
        elif clave == "barra":
            v = ""
        elif not (sumar or {}).get(clave, clave not in NO_SUMABLES):
            v = ""
        else:
            v = _sumar_columna(celda(it, clave) for it in grupo)
            if v is None:
                # La primera columna de texto no sumable lleva el rótulo.
                v = "" if etiqueta_puesta else "Subtotal"
                etiqueta_puesta = True
        # El subtotal se pinta por signo igual que las filas: un gap a vender en
        # rojo, uno a comprar en verde.
        cls_s, txt_s = celda_signo(v)
        tds.append(f'<td class="{base} {cls_s}">{txt_s}</td>')
    return f'<tr class="subtotal">{"".join(tds)}</tr>'


def tabla_cartera(items, columnas=None, total=None, denso=False, agrupar=None,
                  subtotales=False):
    """Renderiza el detalle de la cartera. `columnas` permite al capítulo elegir
    qué mostrar (una propuesta de bonos quiere 'duration' y una de fondos
    'custodia'), pero por defecto usa el set que ya usa el equipo."""
    cols = []
    sumar = {}               # override por columna del subtotal: {"clave": bool}
    if columnas:
        for c in columnas:
            if isinstance(c, dict):
                cols.append((get(c, "clave", "key", default=""),
                             get(c, "titulo", "label", default=""),
                             get(c, "align", "alineacion", default="l")))
                if get(c, "sumar", default=None) is not None:
                    sumar[cols[-1][0]] = bool(get(c, "sumar"))
            else:
                match = next((x for x in COLUMNAS_CARTERA if x[0] == c), None)
                if match is None and c in COLUMNAS_EXTRA:
                    match = (c, COLUMNAS_EXTRA[c][0], COLUMNAS_EXTRA[c][1])
                cols.append(match or (c, c.replace("_", " ").capitalize(), "l"))
    else:
        cols = list(COLUMNAS_CARTERA)

    # La clave viaja como clase CSS (col-descripcion, col-monto…) para que la
    # hoja de estilos pueda dar ancho a la descripción y evitar que las columnas
    # numéricas cortas se partan en varias líneas.
    th = "".join(f'<th class="{al} col-{esc(k)}">{esc(tit)}</th>' for k, tit, al in cols)

    # La columna `barra` dibuja el peso de cada fila. Se escala contra la fila
    # más pesada y no contra 100%: con carteras de diez líneas ninguna pasa del
    # 20%, y contra 100% todas las barras quedarían igual de cortas y no se
    # compararían entre sí, que es justamente para lo que están.
    pesos = [_pct(get(it, "ponderacion", "peso", "pct", default=None)) or 0.0
             for it in items]
    tope = max(pesos) if pesos else 0.0

    filas = []
    grupo_acc = []           # filas del grupo en curso, para su subtotal
    previo = None            # último valor impreso de la columna agrupada
    for it in items:
        tds = []
        # `agrupar` escribe el valor sólo en la primera fila de cada corrida.
        # Diez filas que dicen "Renta fija" no informan diez veces: informan una
        # y ensucian nueve. Los ítems tienen que venir ya ordenados por esa
        # columna — la tabla no reordena, respeta el orden del asesor.
        arranca = agrupar and celda(it, agrupar) != previo
        if agrupar:
            previo = celda(it, agrupar)
        for clave, _, al in cols:
            v = celda(it, clave)
            base = f"{al} col-{esc(clave)}"
            if clave == agrupar:
                tds.append(f'<td class="{base} grupo">{esc(v) if arranca else ""}</td>')
                continue
            if clave == "barra":
                peso = _pct(get(it, "ponderacion", "peso", "pct", default=None)) or 0.0
                ancho = (peso / tope * 100) if tope else 0.0
                tds.append(f'<td class="{base}"><span class="tbar">'
                           f'<span style="width:{ancho:.1f}%"></span></span></td>')
                continue
            if clave == "riesgo" and clase_riesgo(v):
                tds.append(f'<td class="{base}"><span class="pill {clase_riesgo(v)}">'
                           f'{esc(v)}</span></td>')
            elif clave in ("clase", "descripcion"):
                tds.append(f'<td class="{base} strong">{esc(v)}</td>')
            else:
                cls_s, txt_s = celda_signo(v)
                tds.append(f'<td class="{base} {cls_s}">{txt_s}</td>')
        # Un grupo de una sola línea no lleva subtotal: repetiría el mismo número
        # dos veces seguidas. El grupo que cierra la tabla ya lo controlaba abajo;
        # los del medio no, y sacaban subtotal aunque tuvieran una fila sola.
        if arranca and filas and subtotales and len(grupo_acc) > 1:
            filas.append(_fila_subtotal(cols, grupo_acc, agrupar, sumar))
        if arranca:
            grupo_acc = []
        filas.append(f'<tr class="{"g-ini" if arranca and filas else ""}">'
                     f"{''.join(tds)}</tr>")
        grupo_acc.append(it)

    if subtotales and len(grupo_acc) > 1:
        filas.append(_fila_subtotal(cols, grupo_acc, agrupar, sumar))

    if total:
        tds = []
        # El rótulo "Total" se inyecta en la primera columna SÓLO si ninguna
        # columna lo trae ya. Si no, aparece dos veces: una en la columna que el
        # JSON completó y otra puesta por acá.
        rotulado = any(celda(total, k) for k, _, _ in cols)
        for i, (clave, _, al) in enumerate(cols):
            v = celda(total, clave) or (
                "" if rotulado else (get(total, "label", default="Total") if i == 0 else ""))
            tds.append(f'<td class="{al} col-{esc(clave)}">{esc(v)}</td>')
        filas.append(f'<tr class="total">{"".join(tds)}</tr>')

    return (f'<table class="mc"><thead><tr>{th}</tr></thead>'
            f'<tbody>{"".join(filas)}</tbody></table>')


def columnas_con_signo(headers, signo):
    """Qué columnas escriben el signo en vez de pintarse por él.

    `true` vale para la tabla entera; una lista nombra columnas por su
    encabezado o por su posición. Es la excepción del criterio 89: ahí donde la
    columna no es un resultado sino un flujo —aportes netos, suscripciones y
    rescates, un flujo de caja—, el rojo diría "perdió" sobre lo que en
    realidad es un retiro, y sin el signo un retiro se lee como un aporte."""
    if signo is True:
        return set(range(len(headers)))
    if not signo or signo is False:
        return set()
    cols = set()
    for s in (signo if isinstance(signo, (list, tuple)) else [signo]):
        if isinstance(s, bool):
            continue
        if isinstance(s, int):
            cols.add(s if s >= 0 else len(headers) + s)
            continue
        t = str(s).strip().lower()
        for i, h in enumerate(headers):
            if str(h).strip().lower() == t:
                cols.add(i)
    return cols


def filas_con_signo(filas, signo):
    """Qué filas escriben el signo en vez de pintarse por él.

    Hermana de `columnas_con_signo`, para la tabla que corre al revés: los años
    en las columnas y el concepto en la primera celda de cada fila. Esa es la
    forma natural de un corte anual —tenencia inicial, aportes netos, resultado,
    tenencia al cierre— y ahí la excepción del criterio 89 cae sobre una fila,
    no sobre una columna. Nombrar "Aportes netos" no seleccionaba nada y el
    retiro volvía a salir sin signo y en rojo.

    Los enteros siguen siendo posiciones de columna, como en la hermana: en una
    lista mezclada, el número nombra columna y el texto nombra las dos cosas.
    """
    if signo is True or not signo or signo is False:
        return set()          # `true` ya lo resuelve columnas_con_signo
    fil = set()
    for s in (signo if isinstance(signo, (list, tuple)) else [signo]):
        if isinstance(s, (bool, int)):
            continue
        t = str(s).strip().lower()
        for i, f in enumerate(filas):
            if len(f) and str(f[0]).strip().lower() == t:
                fil.add(i)
    return fil


def tabla_libre(headers, filas, alineacion=None, total_ultima=False, signo=None):
    """Escotilla de escape: cualquier tabla que el catálogo de capítulos no
    cubra. Sale con el mismo estilo que las demás, así que no rompe la unidad
    visual aunque el contenido sea arbitrario."""
    al = list(alineacion or "")
    while len(al) < len(headers):
        al.append("r" if al else "l")
    th = "".join(f'<th class="{a}">{esc(h)}</th>' for h, a in zip(headers, al))
    con_signo = columnas_con_signo(headers, signo)
    filas_signo = filas_con_signo(filas, signo)
    out = []
    for i, fila in enumerate(filas):
        cls = ' class="total"' if (total_ultima and i == len(filas) - 1) else ""
        tds = "".join(
            (f'<td class="{a}">{esc(str(c if c is not None else ""))}</td>'
             if (j in con_signo or i in filas_signo)
             else '<td class="{} {}">{}</td>'.format(a, *celda_signo(c)))
            for j, (c, a) in enumerate(zip(fila, al)))
        out.append(f"<tr{cls}>{tds}</tr>")
    return (f'<table class="mc"><thead><tr>{th}</tr></thead>'
            f'<tbody>{"".join(out)}</tbody></table>')


def ficha_instrumento(f):
    nombre = get(f, "nombre", "instrumento", "name", default="")
    tipo = get(f, "tipo", "clase", "kind", default="")
    texto = get(f, "que_hace", "descripcion", "texto", "rol", default="")
    datos = get(f, "datos", "metricas", default=[]) or []
    # Un dato puede venir como par (label + valor) o como texto suelto. El texto
    # suelto sale como etiqueta: sirve para clasificar la posición —"Largo
    # plazo", "Custodia USA"— donde no hay una cifra que mostrar.
    def _pill(d):
        if isinstance(d, str):
            return f'<span class="dato tag">{esc(d)}</span>'
        lb = get(d, "label", "etiqueta", default="")
        vl = get(d, "valor", "value", default="")
        if not lb:
            return f'<span class="dato tag">{esc(vl)}</span>'
        return f'<span class="dato">{esc(lb)} <b>{esc(vl)}</b></span>'
    pills = "".join(_pill(d) for d in datos)
    h = ['<div class="ficha"><div class="ficha-head"><div>'
         f'<span class="ficha-name">{esc(nombre)}</span>']
    if tipo:
        h.append(f'<span class="ficha-kind">{esc(tipo)}</span>')
    h.append("</div>")
    # La esquina de la ficha: el monto que se invierte y/o la pill de riesgo.
    # El monto va primero — es el número que el cliente busca en esta lámina.
    monto = get(f, "monto", "importe", default="")
    riesgo = get(f, "riesgo", "nivel_riesgo", default="")
    if monto or riesgo:
        h.append('<div class="ficha-esq">')
        if monto:
            h.append(f'<span class="ficha-monto">{esc(monto)}</span>')
        if riesgo:
            h.append(f'<span class="pill {clase_riesgo(riesgo)}">{esc(riesgo)}</span>')
        h.append("</div>")
    h.append("</div>")
    if texto:
        h.append(f"<p>{esc_md(texto)}</p>")
    if pills:
        h.append(f'<div class="ficha-datos">{pills}</div>')
    h.append("</div>")
    return "".join(h)


def bloque_acciones(acciones):
    """Qué comprar / qué vender / qué mantener. Es el capítulo que más valor
    tiene para un cliente con cartera vigente: convierte el análisis en algo
    accionable en vez de descriptivo."""
    cols = []
    # El orden por defecto es comprar → vender → mantener. `orden` lo cambia
    # cuando el relato de la slide pide otra secuencia: en un rebalanceo se
    # vende primero y recién después se coloca el producido, y leerlo al revés
    # obliga al cliente a reconstruir de dónde salió la plata.
    ROTULOS = {"comprar": "Comprar", "vender": "Vender", "mantener": "Mantener"}
    orden = get(acciones, "orden", "secuencia", default=None) \
        or ["comprar", "vender", "mantener"]
    for clave in orden:
        titulo = ROTULOS.get(clave)
        items = get(acciones, clave, default=[]) or []
        if titulo is None or not items:
            continue
        cuerpo = []
        for it in items:
            nombre = get(it, "nombre", "instrumento", "activo", default="")
            monto = get(it, "monto", "importe", "peso", default="")
            razon = get(it, "razon", "motivo", "por_que", "comentario", default="")
            cuerpo.append(
                f'<div class="accion-item"><div class="ai-top">'
                f'<span class="ai-name">{esc(nombre)}</span>'
                f'<span class="ai-amt">{esc(monto)}</span></div>'
                + (f'<div class="ai-why">{esc_md(razon)}</div>' if razon else "")
                + "</div>")
        cols.append(f'<div class="accion-col {clave}"><h4>{esc(titulo)}</h4>'
                    f'{"".join(cuerpo)}</div>')
    if not cols:
        return ""
    estilo = "" if len(cols) == 3 else f' style="grid-template-columns:repeat({len(cols)},1fr);"'
    return f'<div class="acciones"{estilo}>{"".join(cols)}</div>'


# ======================= Capítulos del DECK (16:9) ========================= #
# Cada función devuelve una LISTA de slides (HTML del cuerpo + metadatos), para
# que un capítulo largo pueda ocupar varias slides sin desbordar.

def esquina(destacado, riesgo):
    """La esquina superior derecha de una slide.

    Admite un dato destacado —típicamente el monto que se invierte— y/o la pill
    de nivel de riesgo. Si van los dos, el monto va primero: es el número que el
    cliente busca. Si no hay ninguno, la esquina no se dibuja."""
    piezas = []
    if destacado:
        if isinstance(destacado, str):
            destacado = {"valor": destacado}
        rotulo = get(destacado, "rotulo", "label", "titulo", default="")
        valor = get(destacado, "valor", "value", "monto", default="")
        if valor:
            piezas.append(
                (f'<span class="r-rotulo">{esc(rotulo)}</span>' if rotulo else "")
                + f'<span class="r-monto">{esc(valor)}</span>')
    if riesgo:
        piezas.append(f'<span class="r-rotulo">Nivel de riesgo</span>'
                      f'<span class="pill {clase_riesgo(riesgo)}">{esc(riesgo)}</span>')
    return f'<div class="slide-riesgo">{"".join(piezas)}</div>' if piezas else ""


def _slide(titulo, cuerpo, subtitulo=None, denso=False, nota=None, riesgo=None,
           destacado=None):
    return {"titulo": titulo, "subtitulo": subtitulo, "cuerpo": cuerpo,
            "denso": denso, "nota": nota, "clase": "", "riesgo": riesgo,
            "destacado": destacado}


def cap_texto(c):
    """Bloque de prosa en columnas. Es el capítulo de 'síntesis', 'contexto',
    'visión de mercado' — cualquier cosa que sea argumento y no tabla."""
    columnas = get(c, "columnas", "bloques", default=[]) or []
    if not columnas and get(c, "parrafos", "texto"):
        p = get(c, "parrafos", "texto")
        columnas = [{"parrafos": p if isinstance(p, list) else [p]}]
    n = min(max(len(columnas), 1), 4)
    # `formato: "tarjetas"` dibuja cada columna como una tarjeta gris con filete
    # navy arriba, en vez de prosa suelta. Es para cuando las columnas son piezas
    # de igual peso que se comparan entre sí, no un argumento que corre de
    # izquierda a derecha. Con `label` la tarjeta lleva volanta.
    tarjetas = get(c, "formato", "estilo", default="") == "tarjetas"
    partes = []
    for col in columnas:
        h = []
        lab = get(col, "label", "volanta", "etiqueta", default="")
        if lab:
            h.append(f'<span class="col-label">{esc(lab)}</span>')
        t = get(col, "titulo", "title", default="")
        if t:
            h.append(f"<h5>{esc(t)}</h5>")
        ps = get(col, "parrafos", "texto", "parrafo", default=[]) or []
        if isinstance(ps, str):
            ps = [ps]
        h += [f"<p>{esc_md(p)}</p>" for p in ps]
        partes.append(f'<div class="col">{"".join(h)}</div>')
    cuerpo = (f'<div class="cols c{n}{" tarjetas" if tarjetas else ""}">'
              f'{"".join(partes)}</div>')
    largo = sum(len(str(p)) for col in columnas
                for p in (get(col, "parrafos", "texto", default=[]) or []))
    return [_slide(get(c, "titulo", default=""), cuerpo,
                   get(c, "subtitulo", default=None), denso=largo > 1600)]


def cap_forma_trabajo(c):
    """Cómo trabajamos con el cliente. Va temprano en el deck porque ordena la
    expectativa de la relación antes de hablar de plata."""
    pasos = get(c, "pasos", "items", default=[]) or []
    slides = []
    grupos = trozos(pasos, CONFIG["PASOS_POR_SLIDE"])
    for i, grupo in enumerate(grupos):
        n = 2 if len(grupo) <= 4 else 3
        items = []
        for j, p in enumerate(grupo):
            idx = i * CONFIG["PASOS_POR_SLIDE"] + j + 1
            items.append(
                f'<div class="paso"><div class="paso-num">{idx}</div>'
                f'<div class="paso-body"><h5>'
                f'{esc(get(p, "titulo", "title", default=""))}</h5>'
                f'<p>{esc(get(p, "texto", "descripcion", default=""))}</p>'
                f"</div></div>")
        cuerpo = f'<div class="pasos p{n}">{"".join(items)}</div>'
        # `remate` cierra la slide con una línea sobre filete navy. Es donde va
        # lo que el asesor quiere que quede resonando o preguntado al cliente.
        rem = get(c, "remate", default=None) if i == len(grupos) - 1 else None
        if rem:
            cuerpo += f'<div class="remate">{esc_md(rem)}</div>'
        intro = get(c, "intro", "subtitulo", default=None) if i == 0 else None
        titulo = get(c, "titulo", default="Cómo trabajamos")
        slides.append(_slide(titulo + (" (cont.)" if i else ""), cuerpo, intro,
                             denso=len(grupo) > 4))
    return slides


def cap_perfil(c):
    """Quién es el cliente — no su perfil de riesgo, sino la persona.

    Sirve para devolverle al cliente lo que el asesor entendió de la charla y
    que lo confirme o lo corrija antes de discutir instrumentos. Una propuesta
    construida sobre un malentendido se cae en la reunión, y este capítulo hace
    barato descubrirlo temprano.
    """
    rasgos = get(c, "rasgos", "items", "datos", default=[]) or []
    parrafos = get(c, "notas", "parrafos", "texto", default=[]) or []
    if isinstance(parrafos, str):
        parrafos = [parrafos]
    # `puntos` es una lista con viñetas: sirve cuando lo que cambia la propuesta
    # se enumera en vez de argumentarse en prosa.
    puntos = get(c, "puntos", "bullets", "lista", default=[]) or []
    if isinstance(puntos, str):
        puntos = [puntos]

    # `destacado` es el recuadro gris al costado de la ficha: lo que no se
    # negocia, la condición del mandato, el límite que ordena todo lo que sigue.
    # Va aparte de los rasgos porque no es un dato más de la ficha — es el que
    # el cliente tiene que ver primero de un vistazo.
    destacado = get(c, "destacado", "recuadro", default=None)

    filas = "".join(
        f'<div class="rasgo"><span class="r-label">'
        f'{esc(get(r, "label", "etiqueta", "titulo", default=""))}</span>'
        f'<span class="r-valor">{esc(get(r, "valor", "value", default=""))}</span></div>'
        for r in rasgos)
    izq = f'<div class="rasgos">{filas}</div>' if filas else ""

    texto = "".join(f"<p>{esc_md(x)}</p>" for x in parrafos)
    if puntos:
        texto += "<ul>" + "".join(f"<li>{esc_md(x)}</li>" for x in puntos) + "</ul>"
    texto = f'<div class="perfil-texto">{texto}</div>' if texto else ""

    caja = ""
    if destacado:
        items = get(destacado, "items", "puntos", default=[]) or []
        cuerpo_caja = "".join(
            '<div class="d-item">'
            + (f'<h5>{esc(get(i, "titulo", "label", default=""))}</h5>'
               if get(i, "titulo", "label", default="") else "")
            + f'<p>{esc_md(get(i, "texto", "valor", "descripcion", default=""))}</p>'
            + "</div>"
            for i in items)
        t = get(destacado, "titulo", default="")
        # `perfil-destacado` y no `destacado` a secas: un nombre genérico choca
        # con `.delta.destacado`, que también existe, y la tarjeta de delta
        # heredaba el padding, el centrado vertical y el filete navy de este
        # recuadro. Ver criterio 26.
        caja = ('<div class="perfil-destacado">'
                + (f'<span class="d-titulo">{esc(t)}</span>' if t else "")
                + cuerpo_caja + "</div>")

    # Con recuadro, la prosa acompaña a la ficha en la columna izquierda: el
    # recuadro se queda solo en la derecha, que es lo que le da el peso.
    if caja:
        cuerpo = (f'<div class="split wide-left igual"><div>{izq}{texto}</div>'
                  f"<div>{caja}</div></div>")
    elif izq and texto:
        cuerpo = f'<div class="split wide-right"><div>{izq}</div>{texto}</div>'
    else:
        cuerpo = izq or texto
    return [_slide(get(c, "titulo", default="Perfil del inversor"), cuerpo,
                   get(c, "subtitulo", default=None),
                   denso=len(rasgos) > 7, nota=get(c, "nota", default=None))]


def cap_proyeccion(c):
    """Proyección de capital al retiro.

    Los números grandes arriba y los supuestos a la vista: una proyección sin
    sus supuestos visibles es una promesa, y acá lo que se muestra es el
    resultado de un modelo con parámetros discutibles.
    """
    items = get(c, "kpis", "items", default=[]) or []
    supuestos = get(c, "supuestos", default=[]) or []
    n = min(max(len(items), 1), 5)
    # En qué base están las cifras. Va arriba de los números y no en la bajada:
    # si la proyección es en moneda constante hay que decirlo donde se lee, no
    # en una línea que se saltea.
    base = get(c, "base", "aclaracion", "moneda", default=None)
    cuerpo = (f'<div class="proy-base">{esc(base)}</div>' if base else "")
    cuerpo += (f'<div class="kpi-grid hero k{n}" style="grid-template-columns:repeat({n},1fr);">'
              + "".join(kpi(i) for i in items) + "</div>")
    if supuestos:
        pills = "".join(
            f'<span class="dato">{esc(get(s, "label", "etiqueta", default=""))} '
            f'<b>{esc(get(s, "valor", "value", default=""))}</b></span>'
            for s in supuestos)
        cuerpo += ('<div class="supuestos"><span class="s-titulo">Supuestos</span>'
                   f'<div class="ficha-datos">{pills}</div></div>')
    return [_slide(get(c, "titulo", default="Proyección al retiro"), cuerpo,
                   get(c, "subtitulo", default=None), nota=get(c, "nota", default=None))]


def cap_glidepath(c):
    """Trayectoria de la asignación a lo largo del horizonte.

    Hace visible algo que el cliente no puede deducir de una tabla: cómo se va a
    mover su cartera con los años. Sirve tanto para mostrar un desarme gradual de
    riesgo como para mostrar que la asignación NO cambia — que también es una
    decisión, y conviene que esté dicha.

    Los tramos marcados `tentativo` se dibujan atenuados y punteados: son los que
    todavía no están decididos, y pintarlos igual que el resto los haría pasar
    por compromiso.
    """
    tramos = get(c, "tramos", "items", default=[]) or []
    et_rv = get(c, "etiqueta_variable", default="Renta variable")
    et_rf = get(c, "etiqueta_fija", default="Renta fija")

    cols = []
    for t in tramos:
        eq = a_numero(get(t, "acciones", "variable", "equity", default=0)) or 0.0
        eq = min(max(eq, 0), 100)
        lb = get(t, "label", "edad", "anio", default="")
        sub = get(t, "nota", "detalle", default="")
        cls = " tentativo" if get(t, "tentativo", default=False) else ""
        cols.append(
            f'<div class="gp-col{cls}"><div class="gp-bar">'
            f'<div class="gp-rv" style="height:{eq:.0f}%"><span>{eq:.0f}%</span></div>'
            f'<div class="gp-rf"><span>{100 - eq:.0f}%</span></div></div>'
            f'<div class="gp-foot"><div class="gp-label">{esc(lb)}</div>'
            + (f'<div class="gp-sub">{esc(sub)}</div>' if sub else "")
            + "</div></div>")

    leyenda = (f'<div class="gp-leyenda">'
               f'<span><i style="background:var(--blue)"></i>{esc(et_rv)}</span>'
               f'<span><i style="background:var(--navy)"></i>{esc(et_rf)}</span></div>')
    cuerpo = (f'<div class="glidepath"><div class="gp-chart">{"".join(cols)}</div>'
              f'{leyenda}</div>')
    return [_slide(get(c, "titulo", default="Trayectoria de la cartera"), cuerpo,
                   get(c, "subtitulo", default=None),
                   denso=len(tramos) > 9, nota=get(c, "nota", default=None))]


# Carpeta del JSON que se está generando. Las rutas de imágenes se buscan ahí:
# el asesor escribe "grafico-spy.png" pensando en la carpeta del cliente, no en
# el directorio desde el que se corre el script.
DIR_JSON = os.getcwd()


def ruta_recurso(ruta):
    """Resuelve una ruta del JSON: absoluta, relativa al directorio actual, o
    relativa a la carpeta del JSON, en ese orden. None si no existe."""
    if not ruta:
        return None
    for cand in (ruta, os.path.join(DIR_JSON, ruta)):
        if os.path.isfile(cand):
            return cand
    return None


def imagen_data_uri(ruta):
    """La imagen incrustada en base64, como la foto de portada: el PDF queda
    autocontenido y no depende de que el archivo siga en su lugar."""
    r = ruta_recurso(ruta)
    if not r:
        return None
    ext = os.path.splitext(r)[1].lstrip(".").lower() or "png"
    ext = "jpeg" if ext == "jpg" else ext
    # El MIME de un SVG es "image/svg+xml": con "image/svg" a secas el navegador
    # no reconoce el tipo y no dibuja nada. Ver criterio 97.
    ext = "svg+xml" if ext == "svg" else ext
    return f"data:image/{ext};base64," + base64.b64encode(open(r, "rb").read()).decode()


def etiqueta_imagen(ruta, clase="kpi-img", alt=""):
    """La imagen lista para pegar en el HTML. None si el archivo no está.

    Un SVG se inyecta como markup, no dentro de un `<img>`: un `<img>` es un
    documento aparte y no ve el `@font-face` de la página, así que el texto del
    gráfico cae a la fuente del sistema. Inline hereda el CSS del deck y sale
    con Inter, que es la razón por la que conviene traer un gráfico propio como
    SVG y no rasterizado. Ver criterio 97."""
    r = ruta_recurso(ruta)
    if not r:
        return None
    if os.path.splitext(r)[1].lower() == ".svg":
        texto = open(r, encoding="utf-8").read()
        m = re.search(r"<svg\b[^>]*>", texto, flags=re.S | re.I)
        if m:
            # La clase la pone el generador: si el archivo trae la suya, el
            # tamaño lo decidiría quien dibujó el SVG y no la lámina.
            tag = re.sub(r'\sclass\s*=\s*"[^"]*"', "", m.group(0), flags=re.I)
            tag = tag[:4] + f' class="{clase}"' + tag[4:]
            return texto[:m.start()] + tag + texto[m.end():]
    uri = imagen_data_uri(ruta)
    return f'<img class="{clase}" src="{uri}" alt="{esc(alt)}">' if uri else None


def cap_kpis(c):
    """Los números que resumen la propuesta. Se renderizan en modo 'hero'
    (tarjetas grandes) porque acá el número ES el contenido de la slide."""
    items = get(c, "items", "kpis", default=[]) or []
    n = min(max(len(items), 1), 5)
    img = get(c, "imagen", "grafico_imagen", default=None)
    ruta_img = get(img, "ruta", "path", "archivo", default=None) if img else None
    # Markup, no una URI: un SVG entra inline y el resto como <img> en base64.
    marca_img = etiqueta_imagen(ruta_img, "kpi-img",
                                get(img, "titulo", "title", default="")) if img else None
    if marca_img:
        # Una captura con su título y un valor destacado a la izquierda, y las
        # tarjetas en grilla de dos columnas a la derecha. El recuadro de la
        # imagen mide lo que mide la imagen —sin aire abajo— y las tarjetas se
        # estiran al alto de la fila. Ver criterio 87.
        titulo_img = get(img, "titulo", "title", default="")
        valor_img = get(img, "valor", "value", default="")
        recuadro = ('<div class="kpi-img-card">'
                    + (f'<h4>{esc(titulo_img)}</h4>' if titulo_img else "")
                    + (f'<div class="kpi-img-valor">{esc(valor_img)}</div>'
                       if valor_img else "")
                    + marca_img + '</div>')
        # Una captura muy apaisada —la serie de una simulación, por ejemplo—
        # queda diminuta en media slide. Con "posicion": "abajo" las tarjetas
        # van arriba, en una fila a lo ancho, y la captura debajo ocupando todo
        # el ancho de la lámina. Ver criterio 90.
        pos = str(get(img, "posicion", "layout", default="") or "").lower()
        if pos in ("abajo", "debajo", "ancho", "full", "completo"):
            # Sin título ni valor propios, la captura va a sangre y se queda con
            # todo el ancho: el recuadro sólo le robaría alto. El marco lo pone
            # el borde de la propia imagen.
            abajo = recuadro if (titulo_img or valor_img) else (
                '<div class="kpi-img-ancho">' + marca_img + "</div>")
            cuerpo = ('<div class="kpi-img-stack">'
                      f'<div class="kpi-grid hero k{n} kpi-img-fila" '
                      f'style="grid-template-columns:repeat({n},1fr);">'
                      + "".join(kpi(i) for i in items) + "</div>"
                      + abajo + "</div>")
        else:
            cuerpo = ('<div class="kpi-img-wrap">' + recuadro
                      + f'<div class="kpi-grid hero k4 kpi-img-grid">'
                      + "".join(kpi(i) for i in items) + "</div></div>")
    else:
        cuerpo = (f'<div class="kpi-grid hero k{n}" style="grid-template-columns:repeat({n},1fr);">'
                  + "".join(kpi(i) for i in items) + "</div>")
    extra = get(c, "texto", "nota_texto", default=None)
    if extra:
        cuerpo += f'<p class="lede" style="margin-top:18px;">{esc(extra)}</p>'
    return [_slide(get(c, "titulo", default=""), cuerpo,
                   get(c, "subtitulo", default=None), nota=get(c, "nota", default=None))]


def cap_cartera(c):
    """Cartera sugerida: KPIs de encabezado + tabla de detalle. Es el capítulo
    central de la propuesta y el que replica el modelo que el equipo ya usa."""
    items = get(c, "items", "posiciones", "instrumentos", default=[]) or []
    columnas = get(c, "columnas", default=None)
    total = get(c, "total", default=None)
    kpis = get(c, "kpis", default=[]) or []
    agrupar = get(c, "agrupar_por", "agrupar", default=None)
    graf = get(c, "grafico", default=None)

    cabecera = ""
    if kpis:
        n = min(max(len(kpis), 1), 5)
        cabecera = (f'<div class="kpi-grid" style="grid-template-columns:repeat({n},1fr);'
                    f'margin-bottom:14px;">' + "".join(kpi(k) for k in kpis) + "</div>")

    # La primera slide lleva los KPIs, así que le entran menos filas.
    denso = len(items) > CONFIG["UMBRAL_DENSO"]
    cupo = CONFIG["FILAS_POR_SLIDE_DENSA"] if denso else CONFIG["FILAS_POR_SLIDE"]
    cupo_primera = max(cupo - (3 if kpis else 0), 4)

    grupos = [items[:cupo_primera]]
    resto = items[cupo_primera:]
    while resto:
        grupos.append(resto[:cupo])
        resto = resto[cupo:]

    slides = []
    for i, grupo in enumerate(grupos):
        es_ultima = (i == len(grupos) - 1)
        tab = tabla_cartera(grupo, columnas, total if es_ultima else None,
                            denso, agrupar,
                            subtotales=bool(get(c, "subtotales", default=False)))
        # El gráfico acompaña a la tabla sólo si la cartera entra en una slide:
        # partido en dos no dice nada, y repetido en cada una miente sobre a qué
        # tramo corresponde.
        if graf and len(grupos) == 1:
            cuerpo = (cabecera + '<div class="cart-wrap">' + tab
                      + grafico(graf, tamano=150) + "</div>")
        else:
            cuerpo = (cabecera if i == 0 else "") + tab
        titulo = get(c, "titulo", default="Cartera sugerida")
        slides.append(_slide(titulo + (" (cont.)" if i else ""), cuerpo,
                             get(c, "subtitulo", default=None) if i == 0 else None,
                             denso=denso,
                             nota=get(c, "nota", default=None) if es_ultima else None))
    return slides


def cap_cartera_actual(c):
    """Cartera vigente + qué hacer con ella. Puede traer la foto de posiciones,
    el bloque de acciones, o ambos: se arma con lo que el asesor haya aportado."""
    slides = []
    posiciones = get(c, "posiciones", "items", default=[]) or []
    acciones = get(c, "acciones", "recomendaciones", default=None)
    titulo = get(c, "titulo", default="Cartera actual")

    if posiciones:
        columnas = get(c, "columnas", default=None)
        denso = len(posiciones) > CONFIG["UMBRAL_DENSO"]
        cupo = CONFIG["FILAS_POR_SLIDE_DENSA"] if denso else CONFIG["FILAS_POR_SLIDE"]
        for i, grupo in enumerate(trozos(posiciones, cupo)):
            es_ultima = (i == len(trozos(posiciones, cupo)) - 1)
            slides.append(_slide(
                titulo + (" (cont.)" if i else ""),
                tabla_cartera(grupo, columnas,
                              get(c, "total", default=None) if es_ultima else None, denso),
                get(c, "subtitulo", default=None) if i == 0 else None, denso=denso))

    if acciones:
        cuerpo = bloque_acciones(acciones)
        intro = get(c, "intro_acciones", default=None)
        slides.append(_slide(get(c, "titulo_acciones", default="Qué comprar y qué vender"),
                             cuerpo, intro, denso=True, nota=get(c, "nota", default=None)))
    return slides


def cap_trades(c):
    """Movimientos emparejados: qué sale y qué entra en cada uno.

    Es el hermano de `cartera_actual` y resuelve el caso contrario. En un
    rebalanceo por estrategia cada posición se justifica sola contra el mandato
    —esto se vende porque X, esto se compra porque Y— y las tres columnas de
    comprar / vender / mantener alcanzan. En un trade el argumento es la
    comparación entre dos instrumentos del mismo segmento: por qué el que entra
    es mejor que el que sale. Ahí la venta y la compra no se pueden leer por
    separado sin que el cliente tenga que adivinar qué va con qué.

    Salen dos slides: la tabla de movimientos y, si hay razones, una lámina con
    una columna por movimiento. La razón nunca va como quinta columna de la
    tabla: el texto largo parte las filas en dos y rompe el criterio 59."""
    items = get(c, "items", "movimientos", "trades", default=[]) or []
    if not items:
        return []
    slides = []

    filas = []
    for i, it in enumerate(items, 1):
        filas.append([
            get(it, "etiqueta", "label", default=f"Movimiento {i}"),
            get(it, "sale", "vender", "desde", default=""),
            get(it, "entra", "comprar", "hacia", default=""),
            get(it, "monto", "importe", default=""),
        ])
    slides.append(_slide(
        get(c, "titulo", default="Los movimientos"),
        tabla_libre(["", "Sale", "Entra", "Monto"], filas, "lllr", False),
        get(c, "subtitulo", default=None),
        denso=len(filas) > CONFIG["UMBRAL_DENSO"],
        nota=get(c, "nota", default=None)))

    # Las razones sólo si las hay: un trade sin porqué es una orden, pero a veces
    # el asesor quiere la tabla sola y desarrolla el argumento hablando.
    con_razon = [it for it in items
                 if get(it, "razon", "motivo", "por_que", default=None)]
    if con_razon:
        for j, grupo in enumerate(trozos(con_razon, 4)):
            partes = []
            for k, it in enumerate(grupo, 1):
                h = []
                t = get(it, "etiqueta", "label", default="")
                if t:
                    h.append(f"<h5>{esc(t)}</h5>")
                ps = get(it, "razon", "motivo", "por_que", default=[]) or []
                if isinstance(ps, str):
                    ps = [ps]
                h += [f"<p>{esc_md(p)}</p>" for p in ps]
                partes.append(f'<div class="col">{"".join(h)}</div>')
            n = min(max(len(grupo), 1), 4)
            titulo_r = get(c, "titulo_razones", default="Por qué cada movimiento")
            slides.append(_slide(
                titulo_r + (" (cont.)" if j else ""),
                f'<div class="cols c{n}">{"".join(partes)}</div>',
                get(c, "subtitulo_razones", default=None) if j == 0 else None))
    return slides


def cap_distribuciones(c):
    graficos = get(c, "graficos", "items", "distribuciones", default=[]) or []
    # Los deltas: lo que cambia entre el antes y el después, en una franja al
    # pie. Un par de donuts lado a lado obliga a restar de memoria; el número
    # que importa es cuánto se movió cada cosa, así que se escribe.
    deltas = get(c, "deltas", "cambios", default=[]) or []
    tira = ""
    if deltas:
        cajas = []
        for d_ in deltas:
            cls = " destacado" if get(d_, "destacado", "accent", default=False) else ""
            cajas.append(
                f'<div class="delta{cls}">'
                f'<span class="d-label">{esc(get(d_, "label", "etiqueta", default=""))}</span>'
                f'<span class="d-valor">{esc(get(d_, "valor", "value", default=""))}</span>'
                + (f'<span class="d-nota">{esc(get(d_, "nota", default=""))}</span>'
                   if get(d_, "nota", default="") else "")
                + "</div>")
        # La fila se divide siempre en al menos cuatro columnas iguales. Con dos
        # o tres tarjetas, cada una mide lo mismo que mediría en una fila de
        # cuatro y el sobrante queda a la derecha. Ni se estiran a media lámina
        # cada una, ni se encogen al tamaño de su texto: la v1.2 las hacía medir
        # lo que su contenido, y dos tarjetas salían chicas, centradas y con el
        # número apretado. Ver criterio 85.
        columnas = max(len(cajas), 4)
        tira = (f'<div class="deltas" style="grid-template-columns:repeat({columnas},1fr);">'
                + "".join(cajas) + "</div>")

    # Métricas de encabezado, opcionales: sirven para una slide de ficha de
    # portfolio, donde la distribución se lee mejor con el rendimiento y el
    # riesgo a la vista.
    kpis = get(c, "kpis", default=[]) or []
    cabecera = ""
    if kpis:
        nk = min(max(len(kpis), 1), 5)
        cabecera = (f'<div class="kpi-grid" style="grid-template-columns:repeat({nk},1fr);'
                    f'margin-bottom:16px;">' + "".join(kpi(k) for k in kpis) + "</div>")

    slides = []
    grupos = trozos(graficos, 3)
    for i, grupo in enumerate(grupos):
        n = len(grupo) if grupo else 1
        # Las tarjetas van ARRIBA de los gráficos: son la conclusión y es lo que
        # el lector tiene que ver primero. Debajo, el detalle que las sostiene.
        cuerpo = (cabecera if i == 0 else "")
        cuerpo += tira if i == 0 else ""
        # Un gráfico solo ocupa media fila, no la fila entera: el recuadro tiene
        # que rodear el gráfico, no una franja vacía de lado a lado. Es la misma
        # regla de las tarjetas (criterio 85): la pieza conserva su tamaño y el
        # sobrante queda a la derecha. Ver criterio 81.
        # Con tres gráficos por fila, cada tarjeta mide un tercio y la leyenda no
        # entra con el donut y los aires de siempre: se achica el donut y la
        # clase `n3` ajusta hueco, aire del porcentaje y letra. Ver criterio 86.
        # Con tres por fila el donut y la leyenda no entran uno al lado del otro,
        # así que se apilan —donut arriba, leyenda debajo— y el donut crece en vez
        # de achicarse: la tarjeta más alta de la fila suele ser una de barras
        # largas, y un donut chico dejaba el recuadro medio vacío. Criterio 86.
        tam = 132 if n >= 3 else 118
        cuerpo += (f'<div class="dist-wrap n{min(n, 3)}" style="grid-template-columns:repeat({max(n, 2)},1fr);">'
                  + "".join(grafico(g, tamano=tam) for g in grupo) + "</div>")
        slides.append(_slide(get(c, "titulo", default="Distribución de la cartera"),
                             cuerpo, get(c, "subtitulo", default=None),
                             denso=(bool(deltas) or bool(kpis)) and n >= 3,
                             riesgo=get(c, "riesgo", "nivel_riesgo", default=None),
                             destacado=get(c, "destacado", "monto", default=None),
                             # La nota va en la última slide del capítulo: si se
                             # repitiera en cada una parecería aplicar a cada
                             # gráfico por separado.
                             nota=(get(c, "nota", default=None)
                                   if i == len(grupos) - 1 else None)))
    return slides


def cap_instrumentos(c):
    """Qué hace cada componente de la cartera. Acá es donde entra el contenido
    de los fact sheets que aportó el asesor: una línea por instrumento sobre el
    rol que cumple, no una repetición de la ficha técnica."""
    fichas = get(c, "fichas", "items", "instrumentos", default=[]) or []
    slides = []
    grupos = trozos(fichas, CONFIG["FICHAS_POR_SLIDE"])
    for i, grupo in enumerate(grupos):
        n = 2 if len(grupo) <= 4 else 3
        cuerpo = (f'<div class="g{n}" style="grid-template-columns:repeat({n},1fr);">'
                  + "".join(ficha_instrumento(f) for f in grupo) + "</div>")
        titulo = get(c, "titulo", default="Los instrumentos de la cartera")
        slides.append(_slide(titulo + (" (cont.)" if i else ""), cuerpo,
                             get(c, "subtitulo", default=None) if i == 0 else None,
                             denso=len(grupo) > 4,
                             # La nota va en la última slide del capítulo. Antes no
                             # se pasaba: el campo validaba, se aceptaba y no se
                             # dibujaba, así que una aclaración desaparecía sin aviso.
                             nota=(get(c, "nota", default=None)
                                   if i == len(grupos) - 1 else None)))
    return slides


# ============================ Flujo de fondos ============================== #
# Sólo se arma si el asesor lo pide, y siempre sobre el calendario de pagos que
# él aporta: el xls de flujo de fondos de cada bono que exporta la plataforma, o
# los pagos cargados a mano. Los cupones nunca se calculan de memoria. La cuenta
# —pago cada 100 VN × nominales / 100, sumado por mes— la hace este código, no
# quien escribe el JSON. Ver criterio 88.

MESES_CORTOS = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep",
                "Oct", "Nov", "Dic"]


def _fecha(v):
    """Una fecha del JSON o del xls: date, datetime, 'dd/mm/aaaa' o 'mm/aaaa'."""
    import datetime as _dt
    if isinstance(v, _dt.datetime):
        return v.date()
    if isinstance(v, _dt.date):
        return v
    t = str(v or "").strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%m/%Y"):
        try:
            return _dt.datetime.strptime(t, fmt).date()
        except ValueError:
            pass
    return None


def leer_flujo_xlsx(ruta):
    """Lee la exportación de flujo de fondos de un bono.

    El formato es el de la plataforma: una fila de grupos ("Flujo de fondos
    c/100 vn") y una de encabezados ("Efectiva", "Amortización", "Interés"). Se
    toman la fecha de pago efectiva y la amortización y el interés cada 100 VN.
    No se usan las columnas de flujo simulado: dependen del nominal que haya
    cargado quien exportó, y el nominal de la propuesta es otro."""
    try:
        import openpyxl
    except ImportError:
        raise SystemExit("Para leer el flujo de fondos en xlsx hace falta openpyxl "
                         "(pip install openpyxl), o cargá los pagos en el JSON.")
    ws = openpyxl.load_workbook(ruta, data_only=True).worksheets[0]
    filas = [list(r) for r in ws.iter_rows(values_only=True)]
    es = lambda c, x: isinstance(c, str) and x in c.strip().lower()
    g = next(i for i, f in enumerate(filas) if any(es(c, "c/100") for c in f))
    h = next(i for i, f in enumerate(filas)
             if any(isinstance(c, str) and c.strip().lower() == "efectiva" for c in f))
    grupo, enc = filas[g], filas[h]
    c_fecha = next(j for j, c in enumerate(enc)
                   if isinstance(c, str) and c.strip().lower() == "efectiva")
    ini = next(j for j, c in enumerate(grupo) if es(c, "c/100"))
    fin = next((j for j in range(ini + 1, len(grupo)) if grupo[j] not in (None, "")),
               len(grupo))
    col = lambda pre: next(j for j in range(ini, fin)
                           if isinstance(enc[j], str) and enc[j].strip().lower().startswith(pre))
    c_am, c_in = col("amortiz"), col("inter")
    num = lambda v: float(str(v).replace(",", ".")) if v not in (None, "") else 0.0
    pagos = []
    for f in filas[h + 1:]:
        fe = _fecha(f[c_fecha]) if c_fecha < len(f) else None
        if fe:
            pagos.append({"fecha": fe, "amortizacion": num(f[c_am]), "renta": num(f[c_in])})
    return pagos


def pagos_de_posicion(pos):
    """Los pagos cada 100 VN de una posición, desde su xls o cargados a mano."""
    archivo = get(pos, "archivo", "flujo", "xlsx", default=None)
    if archivo:
        r = ruta_recurso(archivo)
        return leer_flujo_xlsx(r) if r else []
    out = []
    for x in get(pos, "pagos", default=[]) or []:
        fe = _fecha(get(x, "fecha", default=None))
        if fe:
            out.append({"fecha": fe,
                        "renta": a_numero(get(x, "renta", "interes", "cupon", default=0)) or 0.0,
                        "amortizacion": a_numero(get(x, "amortizacion", default=0)) or 0.0})
    return out


def calcular_flujo(c):
    """Agrega el flujo de la cartera por mes, para 12 meses desde `desde`."""
    import datetime as _dt
    base = _fecha(get(c, "desde", default=None)) or _fecha(get(c, "_fecha", default=None)) \
        or _dt.date.today()
    y0, m0 = base.year, base.month
    meses = [[(y0 + (m0 - 1 + k) // 12), (m0 - 1 + k) % 12 + 1, 0.0, 0.0] for k in range(12)]
    posterior = 0.0
    for pos in get(c, "posiciones", "bonos", default=[]) or []:
        vn = a_numero(get(pos, "nominales", "vn", default=0)) or 0.0
        for pg in pagos_de_posicion(pos):
            k = (pg["fecha"].year - y0) * 12 + pg["fecha"].month - m0
            renta = pg["renta"] * vn / 100
            amort = pg["amortizacion"] * vn / 100
            if 0 <= k < 12:
                meses[k][2] += renta
                meses[k][3] += amort
            elif k >= 12:
                posterior += renta + amort
    return {"meses": meses, "posterior": posterior,
            "renta": sum(m[2] for m in meses), "amort": sum(m[3] for m in meses)}


def _monto(v, moneda="USD"):
    return f"{moneda} " + f"{v:,.0f}".replace(",", ".")


def bloque_flujo(res, moneda="USD", alto=150):
    """Barras verticales por mes: amortización abajo, renta arriba, el total del
    mes encima. Todo en píxeles calculados acá, sin anchos intrínsecos, para que
    salga igual en cualquier motor de PDF. Los meses sin pagos quedan con la
    línea de base y sin número. Ver criterio 88."""
    tope = max((m[2] + m[3]) for m in res["meses"]) or 1.0
    cols = []
    for anio, mes, renta, amort in res["meses"]:
        total = renta + amort
        h_am = round(amort / tope * alto) if amort else 0
        h_re = round(renta / tope * alto) if renta else 0
        if renta and h_re < 2:
            h_re = 2
        if amort and h_am < 2:
            h_am = 2
        cifra = f"{total:,.0f}".replace(",", ".") if total else ""
        cols.append(
            f'<div class="ff-col"><div class="ff-area" style="height:{alto + 16}px;">'
            f'<span class="ff-cifra">{cifra}</span>'
            + (f'<div class="ff-renta" style="height:{h_re}px;"></div>' if h_re else "")
            + (f'<div class="ff-amort" style="height:{h_am}px;"></div>' if h_am else "")
            + f'</div><span class="ff-mes">{MESES_CORTOS[mes - 1]}\'{str(anio)[2:]}</span></div>')
    # La leyenda nombra sólo lo que aparece: si en los doce meses no hay
    # amortizaciones, rotularlas es describir algo que no está en el gráfico.
    leyenda = ('<div class="ff-leyenda">'
               + ('<span><i class="ff-renta"></i>Renta</span>' if res["renta"] else "")
               + ('<span><i class="ff-amort"></i>Amortización</span>' if res["amort"] else "")
               + f'<span class="ff-moneda">Montos en {esc(moneda)}</span></div>')
    return (f'<div class="ff-card"><div class="ff-barras">{"".join(cols)}</div>'
            f'{leyenda}</div>')


def kpis_flujo(res, moneda="USD"):
    return [{"label": "Renta próximos 12 meses", "valor": _monto(res["renta"], moneda),
             "accent": True},
            {"label": "Amortización próximos 12 meses", "valor": _monto(res["amort"], moneda)},
            {"label": "Total próximos 12 meses", "valor": _monto(res["renta"] + res["amort"], moneda)},
            {"label": "Después de 12 meses", "valor": _monto(res["posterior"], moneda)}]


def cap_flujo_de_fondos(c):
    moneda = get(c, "moneda", default="USD")
    res = calcular_flujo(c)
    kp = get(c, "kpis", default=None) or kpis_flujo(res, moneda)
    nk = min(max(len(kp), 1), 5)
    cuerpo = (f'<div class="kpi-grid" style="grid-template-columns:repeat({nk},1fr);'
              f'margin-bottom:16px;">' + "".join(kpi(k) for k in kp) + "</div>"
              + bloque_flujo(res, moneda))
    nota = get(c, "nota", default=None) or (
        f"Montos en {moneda} por mes de pago efectivo, sobre los nominales de cada "
        f"posición. Lo que se cobra después de los 12 meses va en la última tarjeta.")
    return [_slide(get(c, "titulo", default="Flujo de fondos de la cartera"), cuerpo,
                   get(c, "subtitulo", default=None), nota=nota)]


def cap_tabla(c):
    headers = get(c, "headers", "columnas", default=[]) or []
    filas = get(c, "filas", "rows", "datos", default=[]) or []
    denso = len(filas) > CONFIG["UMBRAL_DENSO"]
    cupo = CONFIG["FILAS_POR_SLIDE_DENSA"] if denso else CONFIG["FILAS_POR_SLIDE"]
    slides = []
    grupos = trozos(filas, cupo)
    for i, grupo in enumerate(grupos):
        es_ultima = (i == len(grupos) - 1)
        cuerpo = tabla_libre(headers, grupo, get(c, "alineacion", default=None),
                             get(c, "total_ultima_fila", default=False) and es_ultima,
                             get(c, "signo", "conservar_signo", default=None))
        # Una tabla de pocas columnas y pocas filas estirada al ancho de la slide
        # queda toda aire: las celdas se separan tanto que dejan de leerse como
        # fila. Se angosta y sube de cuerpo — ver criterio 68.
        if len(headers) <= 3 and len(filas) <= 6:
            cuerpo = f'<div class="tabla-chica">{cuerpo}</div>' 
        slides.append(_slide(get(c, "titulo", default="") + (" (cont.)" if i else ""),
                             cuerpo, get(c, "subtitulo", default=None) if i == 0 else None,
                             denso=denso,
                             nota=get(c, "nota", default=None) if es_ultima else None))
    return slides


def cap_hitos(c):
    """Línea de tiempo: qué pasa, en qué orden, y cuándo.

    Va sobre fondo navy y a ancho completo porque es la slide que el cliente se
    lleva: tres o cuatro momentos, cada uno con su fecha y una sola frase. No es
    `forma_de_trabajo` —eso describe cómo se trabaja, esto dice qué pasa cuándo—.
    """
    items = get(c, "hitos", "items", "pasos", default=[]) or []
    n = min(max(len(items), 1), 4)
    piezas = []
    for i, h in enumerate(items, 1):
        cuando = get(h, "cuando", "titulo", "label", default="")
        piezas.append(
            '<div class="hito">'
            f'<span class="hito-label"><span class="hito-num">{i:02d}</span>'
            f'{esc(cuando)}</span>'
            f'<p>{esc_md(get(h, "texto", "descripcion", "valor", default=""))}</p>'
            "</div>")
    cuerpo = f'<div class="hitos h{n}">{"".join(piezas)}</div>'
    s = _slide(get(c, "titulo", default="Qué pasa después"), cuerpo,
               get(c, "subtitulo", default=None), nota=get(c, "nota", default=None))
    s["clase"] = "oscura"
    return [s]


CAPITULOS_DECK = {
    "perfil": cap_perfil,
    "perfil_inversor": cap_perfil,
    "proyeccion": cap_proyeccion,
    "glidepath": cap_glidepath,
    "trayectoria": cap_glidepath,
    "proyeccion_retiro": cap_proyeccion,
    "texto": cap_texto,
    "sintesis": cap_texto,
    "vision_mercado": cap_texto,
    "forma_de_trabajo": cap_forma_trabajo,
    "hitos": cap_hitos,
    "timeline": cap_hitos,
    "proximos_pasos": cap_hitos,
    "kpis": cap_kpis,
    "resumen": cap_kpis,
    "cartera_sugerida": cap_cartera,
    "cartera": cap_cartera,
    "cartera_actual": cap_cartera_actual,
    "trades": cap_trades,
    "movimientos": cap_trades,
    "distribuciones": cap_distribuciones,
    "instrumentos": cap_instrumentos,
    "tabla": cap_tabla,
    "flujo_de_fondos": cap_flujo_de_fondos,
    "flujo": cap_flujo_de_fondos,
}


# ============================ Armado del DECK ============================== #

def slide_portada(p, logo_svg):
    cli = get(p, "cliente", default={}) or {}
    nombre_cli = get(cli, "nombre", "name", default="") if isinstance(cli, dict) else str(cli)
    portada = get(p, "portada", default={}) or {}
    asesor = get(p, "asesor", default={}) or {}
    imagen = get(portada, "imagen", "image", default=None)

    art_cls, art_style = "cover-art", ""
    veil = ""
    imagen = ruta_recurso(imagen)
    if imagen:
        ext = os.path.splitext(imagen)[1].lstrip(".").lower() or "jpeg"
        b64 = base64.b64encode(open(imagen, "rb").read()).decode()
        art_cls += " has-image"
        art_style = f' style="background-image:url(data:image/{ext};base64,{b64});"'
        veil = '<div class="cover-veil"></div>'

    anio = get(p, "anio", default=None) or (get(p, "fecha", default="") or "")[-4:]
    sub = get(p, "subtitulo", "subtitle", default="")
    fecha = get(p, "fecha", default="")

    ases = asesores_de(p)
    contacto = ""
    if ases:
        nombres = "".join(
            f'<span class="k-value">{esc(get(a, "nombre", default=""))}</span>' for a in ases)
        cargo = get(ases[0], "cargo", default=CONFIG["AREA"])
        contacto = (
            '<div class="cover-by"><span class="k-label">Presentado por</span>'
            + nombres
            + (f'<span class="k-note">{esc(cargo)}</span>' if cargo else "")
            + "</div>")

    n = len(nombre_cli)
    cuerpo_nombre = 72 if n <= 14 else 60 if n <= 22 else 46 if n <= 32 else 36

    return f'''<div class="slide cover">
<div class="{art_cls}"{art_style}></div>{veil}
<div class="cover-inner with-logo">
  <div class="cover-top">
    <div class="cover-top-left">
    {f'<span class="cover-year">{esc(anio)}</span>' if anio else ''}</div>
    <div class="cover-logo">{logo_svg}</div>
  </div>
  <div class="cover-hero">
    <span class="cover-eyebrow">Preparado para</span>
    <h1 class="cover-name" style="font-size:{cuerpo_nombre}px">{esc(nombre_cli)}</h1>
    <p class="cover-doc">{esc(get(p, "titulo", default="Propuesta de Inversión"))}</p>
    {f'<p class="cover-sub">{esc(sub)}</p>' if sub else ''}
  </div>
  <div class="cover-foot">{contacto}
    <div class="cover-meta">
      <div class="cover-conf">{esc(CONFIG["CONFIDENCIALIDAD"])}</div>
      {f'<div class="cover-date">Datos al {esc(fecha)}</div>' if fecha else ''}
    </div>
  </div>
</div>
</div>'''


def slide_divisor(c, nombre_cli, numero, logo=""):
    sub = get(c, "subtitulo", default="")
    return f'''<div class="slide divider">
<div class="divider-art"></div>
<div class="slide-logo">{logo}</div>
<div class="divider-inner">
  <div class="divider-num">{numero:02d}</div>
  <h2 class="divider-title">{esc(get(c, "titulo", default=""))}</h2>
  {f'<p class="divider-sub">{esc(sub)}</p>' if sub else ''}
</div>
<div class="divider-client">{esc(nombre_cli)}</div>
</div>'''


def slide_cierre(p, c, logo=""):
    contacto = []
    for a in asesores_de(p):
        lineas = []
        for clave in ("email", "telefono"):
            v = get(a, clave, default="")
            if v:
                lineas.append(f'<span class="k-dato">{esc(v)}</span>')
        contacto.append(
            '<div><span class="k-label">'
            f'{esc(get(a, "cargo", default=CONFIG["AREA"]))}</span>'
            f'<span class="k-value">{esc(get(a, "nombre", default=""))}</span>'
            + "".join(lineas) + "</div>")
    disc = get(c, "disclaimer", default=None) or CONFIG["DISCLAIMER"]
    # Sin URL por defecto: si el capítulo no la trae, la slide no la muestra.
    u = get(c, "url", default=None)
    url_cierre = f'<div class="closing-url">{esc(u)}</div>' if u else ""
    return f'''<div class="slide closing">
<div class="slide-logo">{logo}</div>
<div class="closing-inner">
  <h2 class="closing-title">{esc(get(c, "titulo", default="¡Muchas gracias!"))}</h2>
  {url_cierre}
  <div class="closing-contact">{"".join(contacto)}</div>
  <div class="disclaimer"><b>Información importante</b>{esc(disc)}
    <span class="matriculas">{esc(CONFIG["LEYENDA_REGULATORIA"])}</span></div>
</div>
</div>'''


def slide_contenido(s, nombre_cli, numero, logo_pos="", logo_neg=""):
    cls = "slide dense" if s["denso"] else "slide"
    if s.get("clase"):
        cls += " " + s["clase"]
    sub = s.get("subtitulo")
    pie = []
    if s.get("nota"):
        pie.append(f'<div class="fnote">{esc(s["nota"])}</div>')
    else:
        pie.append("<div></div>")
    pie.append(f'<div class="fbrand">{esc(CONFIG["FOOTER_BRAND"])}</div>')
    badge = esquina(s.get("destacado"), s.get("riesgo"))
    # El logo va en TODAS las slides y siempre en el mismo punto: la variante
    # negativa en las oscuras, la positiva en las claras.
    marca = logo_neg if "oscura" in cls else logo_pos
    art = f'<div class="slide-logo">{marca}</div>' if marca else ""
    return f'''<div class="{cls}">{art}
<div class="slide-top"><span class="slide-badge">{numero}</span>
<span class="slide-client">{esc(nombre_cli)}</span>{badge}</div>
<h2 class="slide-title">{esc(s["titulo"])}</h2>
{f'<p class="slide-sub">{esc(sub)}</p>' if sub else ''}
<div class="slide-body">{s["cuerpo"]}</div>
<div class="slide-foot">{"".join(pie)}</div>
</div>'''


def construir_deck(p, assets):
    cli = get(p, "cliente", default={}) or {}
    nombre_cli = get(cli, "nombre", default="") if isinstance(cli, dict) else str(cli)
    logo = leer_logo(assets, "negativo", 150)   # portada: arriba a la derecha, protagonista
    logo_chico = leer_logo(assets, "negativo", 84)  # divisores, cierre y slides oscuras
    logo_claro = leer_logo(assets, "positivo", 76)  # slides de contenido, fondo blanco

    out = [slide_portada(p, logo)]
    numero = 1          # numeración visible (la portada no cuenta)
    n_divisor = 0

    for c in get(p, "capitulos", "chapters", default=[]) or []:
        tipo = (get(c, "tipo", "type", default="texto") or "texto").lower()
        if tipo == "portada":
            continue
        if tipo == "divisor":
            n_divisor += 1
            out.append(slide_divisor(c, nombre_cli, n_divisor, logo_chico))
            continue
        if tipo == "cierre":
            out.append(slide_cierre(p, c, logo_chico))
            continue
        fn = CAPITULOS_DECK.get(tipo)
        if fn is None:
            # Un tipo desconocido no debe romper el render: se avisa por stderr
            # y se intenta como bloque de texto, que es el más permisivo.
            print(f"  aviso: capítulo de tipo '{tipo}' desconocido; "
                  f"se renderiza como texto.", file=sys.stderr)
            fn = cap_texto
        for s in fn(c):
            numero += 1
            out.append(slide_contenido(s, nombre_cli, numero,
                                       logo_claro, logo_chico))

    if not any('class="slide closing"' in s for s in out):
        out.append(slide_cierre(p, {}, logo_chico))
    return "\n".join(out)


# ========================== Armado del ONE-PAGER =========================== #

def buscar_capitulo(p, *tipos):
    for c in get(p, "capitulos", default=[]) or []:
        if (get(c, "tipo", "type", default="") or "").lower() in tipos:
            return c
    return None


def construir_onepager(p, assets):
    """El one-pager no compone capítulos libremente: es una hoja de estructura
    fija (KPIs · detalle · distribuciones) que toma lo esencial de la propuesta.
    Si el asesor cargó capítulos que no entran acá, se avisa cuáles se omiten
    para que la decisión de recortar sea explícita y no una sorpresa."""
    cli = get(p, "cliente", default={}) or {}
    nombre_cli = get(cli, "nombre", default="") if isinstance(cli, dict) else str(cli)
    logo = leer_logo(assets, "negativo", 96)    # banda negra del encabezado

    cap_cart = buscar_capitulo(p, "cartera_sugerida", "cartera")
    cap_dist = buscar_capitulo(p, "distribuciones")
    cap_k = buscar_capitulo(p, "kpis", "resumen")
    cap_inst = buscar_capitulo(p, "instrumentos")

    items = get(cap_cart, "items", "posiciones", default=[]) or [] if cap_cart else []
    kpis = (get(cap_k, "items", default=[]) if cap_k else None) or \
           (get(cap_cart, "kpis", default=[]) if cap_cart else []) or []

    if len(items) > CONFIG["OP_FILAS_MAXIMO"]:
        print(f"  aviso: la cartera tiene {len(items)} líneas; el one-pager rinde bien "
              f"hasta {CONFIG['OP_FILAS_MAXIMO']}. Se renderizan todas, pero revisá "
              f"la legibilidad o usá --formato deck.", file=sys.stderr)

    # La compresión mira el contenido total de la hoja, no sólo las filas: desde
    # que las distribuciones y la nota de instrumentos se apilan debajo de la
    # tabla, seis posiciones con seis fichas ocupan más que doce posiciones
    # peladas. Cada ficha pesa ~0,8 de una fila.
    n_fichas = len(get(cap_inst, "fichas", "items", default=[]) or []) if cap_inst else 0
    peso = len(items) + 0.8 * n_fichas
    cls = ""
    if peso > CONFIG["OP_FILAS_TIGHTER"]:
        cls = " tighter"
    elif peso > CONFIG["OP_FILAS_TIGHT"]:
        cls = " tight"

    n_k = min(max(len(kpis), 1), 6)
    bloque_kpis = (f'<div class="op-kpis k{n_k}" '
                   f'style="grid-template-columns:repeat({n_k},1fr);">'
                   + "".join(kpi(k) for k in kpis) + "</div>") if kpis else ""

    tabla = ""
    if items:
        tabla = ('<div class="section-heading">Detalle de la propuesta</div>'
                 + tabla_cartera(items, get(cap_cart, "columnas", default=None),
                                 get(cap_cart, "total", default=None)))
        nota = get(cap_cart, "nota", default=None)
        if nota:
            tabla += f'<div class="table-footnote">{esc(nota)}</div>'

    graficos = get(cap_dist, "graficos", "items", default=[]) or [] if cap_dist else []
    dist = ""
    if graficos:
        n_g = min(len(graficos), 3)
        dist = (f'<div class="op-dist g{n_g}" style="grid-template-columns:repeat({n_g},1fr);">'
                + "".join(grafico(g) for g in graficos[:3]) + "</div>")

    # Instrumentos al pie, como NOTA y no como tarjetas. En una hoja sola el
    # espacio se lo tienen que quedar la cartera y las distribuciones: qué hace
    # cada vehículo es contexto de apoyo, no un bloque protagonista. Si la ficha
    # trae `resumen` se usa eso (una cláusula); si no, se recorta `que_hace`.
    fichas = get(cap_inst, "fichas", "items", default=[]) or [] if cap_inst else []
    tira = ""
    if fichas:
        lineas = []
        for f in fichas:
            nombre = get(f, "nombre", "instrumento", default="")
            txt = get(f, "resumen", "que_hace", "descripcion", default="")
            # Si la ficha no trae `resumen`, `que_hace` viene con el texto largo
            # del deck. En una nota al pie eso desborda la hoja, así que se corta
            # en el límite de palabra. Lo correcto es cargar `resumen`; esto es
            # la red para que una propuesta no salga rota por no haberlo hecho.
            if txt and len(txt) > CONFIG["OP_NOTA_MAX_CARACTERES"]:
                corte = txt[:CONFIG["OP_NOTA_MAX_CARACTERES"]].rsplit(" ", 1)[0]
                txt = corte.rstrip(" .,;:") + "…"
            if txt:
                lineas.append(f'<span class="op-nota-item"><b>{esc(nombre)}</b> — '
                              f'{esc_md(txt)}</span>')
        if lineas:
            tira = f'<div class="op-nota-inst">{"".join(lineas)}</div>'

    # Las distribuciones van DEBAJO de la tabla, no en una columna al costado:
    # así la cartera ocupa el ancho completo (que es lo que el cliente lee) y no
    # queda media hoja vacía cuando hay un solo gráfico. La nota de instrumentos
    # cierra la hoja, apoyada contra el disclaimer (ver `margin-top:auto` en el
    # CSS): es contexto de lectura final, no parte del cuerpo de la propuesta.
    partes = []
    if dist:
        partes.append(f'<div class="op-bottom">{dist}</div>')
    if tira:
        partes.append(tira)
    bloque_inferior = "".join(partes)
    fecha_corta = get(p, "fecha_corta", default=None) or mes_anio(get(p, "fecha", default=""))
    objetivo = get(p, "objetivo", default=None) or \
        (get(cap_cart, "subtitulo", default=None) if cap_cart else None)

    meta = []
    for a in asesores_de(p):
        if get(a, "nombre", default=""):
            meta.append(f'<b>{esc(get(a, "nombre"))}</b>')
        for k in ("email", "telefono"):
            if get(a, k, default=""):
                meta.append(esc(get(a, k)))

    return f'''<div class="sheet{cls}">
<div class="op-header">
  <div class="op-header-left">
    <span class="op-eyebrow">{esc(nombre_cli)}{f'<span class="op-fecha">&nbsp;·&nbsp;{esc(fecha_corta)}</span>' if fecha_corta else ''}</span>
    <h1 class="op-title">{esc(get(p, "titulo", default="Propuesta de Inversión"))}</h1>
  </div>
  <div class="op-logo">{logo}</div>
</div>
{f'<div class="op-objetivo"><span class="lbl">Objetivo</span><span class="val">{esc(objetivo)}</span></div>' if objetivo else ''}
<div class="op-body">
  {bloque_kpis}
  {tabla}
  {bloque_inferior}
</div>
<div class="op-foot">
  <div class="disclaimer"><b>Información importante</b>{esc(CONFIG["DISCLAIMER"])}
    <span class="matriculas">{esc(CONFIG["LEYENDA_REGULATORIA"])}</span></div>
  <div class="op-meta">{"<br>".join(meta)}</div>
</div>
</div>'''


# ========================== Armado del DOCUMENTO =========================== #

def seccion_documento(c):
    """Traduce un capítulo al registro del documento largo: prosa primero,
    tablas y figuras como apoyo. El mismo dato que en el deck era una slide acá
    es una sección numerada."""
    tipo = (get(c, "tipo", "type", default="texto") or "texto").lower()
    titulo = get(c, "titulo", default="")
    h = [f'<div class="doc-sec"><h2>{esc(titulo)}</h2>']

    intro = get(c, "subtitulo", "intro", default=None)
    if intro:
        h.append(f'<div class="doc-callout">{esc(intro)}</div>')

    if tipo in ("texto", "sintesis", "vision_mercado"):
        for col in get(c, "columnas", "bloques", default=[]) or []:
            t = get(col, "titulo", default="")
            if t:
                h.append(f"<h3>{esc(t)}</h3>")
            ps = get(col, "parrafos", "texto", default=[]) or []
            h += [f"<p>{esc_md(x)}</p>" for x in ([ps] if isinstance(ps, str) else ps)]
        ps = get(c, "parrafos", "texto", default=[]) or []
        h += [f"<p>{esc_md(x)}</p>" for x in ([ps] if isinstance(ps, str) else ps)]

    elif tipo == "forma_de_trabajo":
        for p_ in get(c, "pasos", "items", default=[]) or []:
            h.append(f'<h3>{esc(get(p_, "titulo", default=""))}</h3>'
                     f'<p>{esc(get(p_, "texto", "descripcion", default=""))}</p>')

    elif tipo in ("kpis", "resumen"):
        items = get(c, "items", default=[]) or []
        n = min(max(len(items), 1), 4)
        h.append(f'<div class="kpi-grid" style="grid-template-columns:repeat({n},1fr);">'
                 + "".join(kpi(i) for i in items) + "</div>")
        if get(c, "texto", default=None):
            h.append(f'<p>{esc(get(c, "texto"))}</p>')

    elif tipo in ("cartera_sugerida", "cartera", "cartera_actual"):
        items = get(c, "items", "posiciones", default=[]) or []
        if items:
            h.append(tabla_cartera(items, get(c, "columnas", default=None),
                                   get(c, "total", default=None)))
        acciones = get(c, "acciones", default=None)
        if acciones:
            for clave, tit in (("comprar", "Comprar"), ("vender", "Vender"),
                               ("mantener", "Mantener")):
                lst = get(acciones, clave, default=[]) or []
                if not lst:
                    continue
                h.append(f"<h3>{tit}</h3><ul>")
                for it in lst:
                    razon = get(it, "razon", "motivo", default="")
                    h.append(f'<li><b>{esc(get(it, "nombre", default=""))}</b>'
                             f'{" — " + esc(razon) if razon else ""}</li>')
                h.append("</ul>")

    elif tipo == "distribuciones":
        gs = get(c, "graficos", "items", default=[]) or []
        h.append('<div class="dist-wrap">' + "".join(grafico(g) for g in gs) + "</div>")

    elif tipo == "instrumentos":
        fichas = get(c, "fichas", "items", default=[]) or []
        h.append('<div class="fichas-grid">'
                 + "".join(ficha_instrumento(f) for f in fichas) + "</div>")

    elif tipo == "tabla":
        h.append(tabla_libre(get(c, "headers", default=[]) or [],
                             get(c, "filas", "rows", default=[]) or [],
                             get(c, "alineacion", default=None),
                             get(c, "total_ultima_fila", default=False),
                             get(c, "signo", "conservar_signo", default=None)))

    elif tipo in ("flujo_de_fondos", "flujo"):
        res = calcular_flujo(c)
        moneda = get(c, "moneda", default="USD")
        kp = get(c, "kpis", default=None) or kpis_flujo(res, moneda)
        h.append('<div class="kpi-grid" style="grid-template-columns:repeat(4,1fr);'
                 'margin-bottom:14px;">' + "".join(kpi(k) for k in kp[:4]) + "</div>")
        h.append(bloque_flujo(res, moneda, alto=130))

    elif tipo in ("trades", "movimientos"):
        # En prosa el movimiento se lee mejor emparejado en una línea que como
        # tabla de cuatro columnas, y la razón va justo debajo de su movimiento.
        movs = get(c, "items", "movimientos", "trades", default=[]) or []
        for i, m in enumerate(movs, 1):
            et = get(m, "etiqueta", "label", default=f"Movimiento {i}")
            sale = get(m, "sale", "vender", "desde", default="")
            entra = get(m, "entra", "comprar", "hacia", default="")
            monto = get(m, "monto", "importe", default="")
            h.append(f"<h3>{esc(et)}</h3>")
            h.append(f"<p><b>{esc(sale)}</b> → <b>{esc(entra)}</b>"
                     + (f" · {esc(monto)}" if monto else "") + "</p>")
            ps = get(m, "razon", "motivo", "por_que", default=[]) or []
            if isinstance(ps, str):
                ps = [ps]
            h += [f"<p>{esc_md(x)}</p>" for x in ps]

    nota = get(c, "nota", default=None)
    if nota:
        h.append(f'<div class="doc-figcap">{esc(nota)}</div>')
    h.append("</div>")
    return "".join(h)


def construir_documento(p, assets):
    cli = get(p, "cliente", default={}) or {}
    nombre_cli = get(cli, "nombre", default="") if isinstance(cli, dict) else str(cli)
    asesor = get(p, "asesor", default={}) or {}
    logo = leer_logo(assets, "positivo", 132)  # portada sobre fondo blanco

    caps = [c for c in (get(p, "capitulos", default=[]) or [])
            if (get(c, "tipo", default="texto") or "").lower()
            not in ("portada", "divisor", "cierre")]

    meta = []
    for lbl, val in (("Preparado para", nombre_cli),
                     ("Preparado por", " · ".join(
                         get(a, "nombre", default="") for a in asesores_de(p))),
                     ("Fecha", get(p, "fecha", default="")),
                     ("Mandato", get(p, "mandato", default=""))):
        if val:
            meta.append(f'<div><span class="lbl">{lbl}</span>'
                        f'<span class="val">{esc(val)}</span></div>')

    toc = "".join(f'<li>{esc(get(c, "titulo", default=""))}</li>' for c in caps)
    sub = get(p, "subtitulo", default="")

    firma = []
    for a in asesores_de(p):
        datos = " · ".join(x for x in (get(a, "email", default=""),
                                       get(a, "telefono", default="")) if x)
        firma.append(f'<div><span class="lbl">{esc(get(a, "cargo", default=CONFIG["AREA"]))}</span>'
                     f'<span class="val">{esc(get(a, "nombre", default=""))}</span>'
                     + (f'<span class="lbl" style="margin-top:4px">{esc(datos)}</span>'
                        if datos else "") + "</div>")

    return f'''<div class="doc-wrap">
<div class="doc-cover">
  <div class="dc-logo">{logo}</div>
  <div class="dc-eyebrow">Wealth Management</div>
  <h1>{esc(get(p, "titulo", default="Propuesta de Administración de Cartera"))}</h1>
  <div class="dc-client">{esc(nombre_cli)}</div>
  <div class="dc-rule"></div>
  {f'<p style="margin-top:20px;max-width:480px;font-size:12px;line-height:1.6;">{esc(sub)}</p>' if sub else ''}
  <div class="dc-meta">{"".join(meta)}</div>
</div>
<div class="doc-toc"><h2>Contenido</h2><ol>{toc}</ol></div>
{"".join(seccion_documento(c) for c in caps)}
<div class="doc-legal">
  <h2>Información importante</h2>
  <div class="disclaimer"><b>Aviso legal</b>{esc(CONFIG["DISCLAIMER"])}
    <span class="matriculas">{esc(CONFIG["LEYENDA_REGULATORIA"])}</span></div>
  <div class="doc-firma">{"".join(firma)}</div>
  <p style="margin-top:18px;font-size:7.4px;color:#A1A1AA;">
    {esc(CONFIG["FOOTER_BRAND"])}</p>
</div>
</div>'''


# ============================ HTML + PDF =================================== #

def css_fuentes(assets):
    """Inter embebida en base64. Va inline para que el PDF sea autocontenido y
    se vea igual en cualquier máquina, sin depender de la red ni de fuentes
    instaladas."""
    pesos = {400: "inter-latin-400-normal.woff2", 500: "inter-latin-500-normal.woff2",
             600: "inter-latin-600-normal.woff2", 700: "inter-latin-700-normal.woff2"}
    out = []
    for peso, archivo in pesos.items():
        ruta = os.path.join(assets, "fonts", archivo)
        if not os.path.exists(ruta):
            continue
        b64 = base64.b64encode(open(ruta, "rb").read()).decode()
        out.append(f"@font-face{{font-family:'Inter';font-style:normal;"
                   f"font-weight:{peso};font-display:block;"
                   f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
    return "\n".join(out)


# Proporción del logotipo dentro del archivo oficial: el PNG trae incorporado el
# área de resguardo de la marca (el aire mínimo alrededor). Se usa tal cual viene
# —no se recorta— y el ancho se compensa con este factor para que el logotipo
# visible quede del tamaño buscado.
LOGO_PROPORCION = 0.648


def leer_logo(assets, variante="negativo", ancho=104):
    """Logotipo oficial de Max Capital, embebido en base64.

    `variante`: "negativo" (blanco, para fondos oscuros) o "positivo" (negro,
    para fondos claros). Son los archivos que provee marketing y se usan sin
    modificar: no se recolorean, no se les cambia la opacidad y no se recortan
    sus márgenes. Tintar el logotipo o bajarle la opacidad es una violación de
    marca, aunque quede lindo.
    """
    ruta = os.path.join(assets, f"logo_{variante}.png")
    if not os.path.exists(ruta):
        print(f"  aviso: falta el logotipo oficial {ruta}", file=sys.stderr)
        return ""
    b64 = base64.b64encode(open(ruta, "rb").read()).decode()
    w = round(ancho / LOGO_PROPORCION)
    return (f'<img class="logo-img" alt="Max Capital" style="width:{w}px" '
            f'src="data:image/png;base64,{b64}">')


def leer_css(assets, *nombres):
    out = []
    for n in nombres:
        ruta = os.path.join(assets, n)
        if os.path.exists(ruta):
            out.append(open(ruta, encoding="utf-8").read())
        else:
            print(f"  aviso: falta {n} en {assets}", file=sys.stderr)
    return "\n".join(out)


CONSTRUCTORES = {
    "deck": (construir_deck, "deck.css", ""),
    "onepager": (construir_onepager, "onepager.css", ""),
    "documento": (construir_documento, "documento.css", "doc"),
}


def construir_html(propuesta, formato, assets):
    # El flujo de fondos arranca, salvo que diga `desde`, en el mes de la
    # propuesta: el capítulo no ve la raíz del JSON, así que se le pasa la fecha.
    for _c in get(propuesta, "capitulos", default=[]) or []:
        if isinstance(_c, dict) and (_c.get("tipo") or "").lower() in ("flujo_de_fondos", "flujo"):
            _c.setdefault("_fecha", get(propuesta, "fecha", default=None))
    if formato not in CONSTRUCTORES:
        raise SystemExit(f"Formato desconocido: {formato}. "
                         f"Opciones: {', '.join(CONSTRUCTORES)}")
    fn, css_formato, body_cls = CONSTRUCTORES[formato]
    cuerpo = fn(propuesta, assets)
    css = css_fuentes(assets) + "\n" + leer_css(assets, "base.css", css_formato)
    titulo = get(propuesta, "titulo", default="Propuesta de Inversión")
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8">'
            f'<title>{esc(titulo)}</title><style>\n{css}\n</style></head>'
            f'<body class="{body_cls}">{cuerpo}</body></html>')


# Medidas de página por formato. El deck usa 10 x 5.625 in, que es exactamente
# el tamaño del deck de referencia (720 x 405 pt) y mapea 1:1 con los 960x540px
# del CSS.
PAGINA = {
    "deck": dict(width="10in", height="5.625in",
                 margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}),
    "onepager": dict(width="297mm", height="210mm",
                     margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}),
    "documento": dict(format="A4",
                      margin={"top": "20mm", "bottom": "18mm",
                              "left": "20mm", "right": "20mm"}),
}


# JS que corre en el navegador, con el documento ya maquetado. Es la única
# forma honesta de saber si algo desborda: depende de la fuente, del texto real
# y de cómo envolvió cada línea. Estimarlo desde el JSON siempre se equivoca.
_JS_DESBORDE = """
() => {
  const reportes = [];
  document.querySelectorAll('.slide').forEach((s, i) => {
    const sr = s.getBoundingClientRect();
    const cs = getComputedStyle(s);
    const pie = s.querySelector('.slide-foot');
    // El límite es el pie si existe —encimarse con él ya es un defecto— y si no
    // el borde interior de la slide.
    const limite = pie ? pie.getBoundingClientRect().top
                       : sr.bottom - parseFloat(cs.paddingBottom);
    let peor = 0, culpable = '';
    // Las capas de fondo ocupan la slide entera por definición: si no se
    // saltan, cada slide con arte de fondo se reporta como desborde con un
    // culpable vacío.
    const fondo = '.slide-art,.cover-art,.divider-art,.cover-veil';
    s.querySelectorAll('*').forEach(el => {
      if (pie && (el === pie || pie.contains(el))) return;
      if (el.matches(fondo)) return;
      const r = el.getBoundingClientRect();
      if (r.height === 0 || r.width === 0) return;
      const exceso = r.bottom - limite;
      if (exceso > peor) {
        peor = exceso;
        culpable = (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 46);
      }
    });
    if (peor > 1) {
      const t = s.querySelector('.slide-title');
      reportes.push({n: i + 1, titulo: t ? t.textContent.trim() : '',
                     exceso: Math.round(peor), culpable});
    }
  });
  return reportes;
}
"""


# Dos controles más sobre el documento maquetado. Los dos defectos que atacan se
# ven de lejos en la lámina y ninguno se ve en el JSON.
_JS_MAQUETA = """
() => {
  const r = [];
  // Láminas del deck y hojas del one-pager: los dos formatos llevan donuts.
  const slides = [...document.querySelectorAll('.slide, .sheet:not(.sheet-legal)')];
  const titulo = s => { const t = s.querySelector('.slide-title, .op-title');
                        return t ? t.textContent.trim() : ''; };
  slides.forEach((s, i) => {
    // 1. La leyenda, tres cosas:
    //    a) la columna de porcentajes pegada a la de etiquetas: se mide el
    //       hueco MÁS CHICO, el de la etiqueta más larga;
    //    b) los porcentajes alineados a la derecha: sus bordes derechos
    //       coinciden en todas las filas;
    //    c) el recuadro rodea el gráfico: el grupo donut + leyenda ocupa al
    //       menos 55% del ancho útil de la tarjeta.
    s.querySelectorAll('.donut-card').forEach(card => {
      const h = card.querySelector('h4');
      const base = {n: i + 1, titulo: titulo(s), grafico: h ? h.textContent.trim() : ''};
      let hueco = Infinity; const derechos = [];
      card.querySelectorAll('.donut-legend-row').forEach(row => {
        const a = row.querySelector('.dl-txt'), b = row.querySelector('.dl-val span');
        if (!a || !b) return;
        const ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
        hueco = Math.min(hueco, rb.left - ra.right);
        derechos.push(rb.right);
      });
      if (hueco !== Infinity && hueco > 60)
        r.push({...base, tipo: 'leyenda', px: Math.round(hueco)});
      if (hueco !== Infinity && hueco < 8)
        r.push({...base, tipo: 'pegado', px: Math.round(hueco)});
      if (derechos.length > 1 && Math.max(...derechos) - Math.min(...derechos) > 1)
        r.push({...base, tipo: 'alineacion'});
      //    d) la leyenda no toca el borde: termina dentro del ancho útil.
      const tabla = card.querySelector('table.donut-legend');
      if (tabla) {
        const cs0 = getComputedStyle(card);
        const limite = card.getBoundingClientRect().right - parseFloat(cs0.paddingRight);
        const exceso = tabla.getBoundingClientRect().right - limite;
        if (exceso > 0.5) r.push({...base, tipo: 'borde', px: Math.round(exceso)});
      }
      const fila = card.querySelector('.donut-row');
      // Apilado —donut arriba, leyenda debajo, en filas de tres— el gráfico no
      // ocupa el ancho a propósito, así que medirlo por ancho no dice nada.
      if (fila && fila.children.length &&
          getComputedStyle(fila).flexDirection !== 'column') {
        const cs = getComputedStyle(card);
        const util = card.getBoundingClientRect().width
                     - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
        const hijos = [...fila.children].map(x => x.getBoundingClientRect());
        const ocupado = Math.max(...hijos.map(x => x.right)) - Math.min(...hijos.map(x => x.left));
        if (util > 0 && ocupado / util < 0.55)
          r.push({...base, tipo: 'vacio', pct: Math.round(100 * ocupado / util)});
      }
    });
    // Una captura no se deforma: la proporción dibujada es la del archivo.
    s.querySelectorAll('img.kpi-img').forEach(im => {
      const b = im.getBoundingClientRect();
      if (!im.naturalWidth || !b.height) return;
      const dif = Math.abs((b.width / b.height) / (im.naturalWidth / im.naturalHeight) - 1);
      if (dif > 0.01) r.push({tipo: 'deformada', n: i + 1, titulo: titulo(s),
                              pct: Math.round(dif * 100)});
    });
    // 3. Cajas hermanas superpuestas. Es el defecto más visible de todos en un
    //    PDF terminado —una tarjeta encimada sobre otra— y hasta ahora pasaba en
    //    silencio: el control de desborde sólo mira el pie de la lámina. La causa
    //    típica es una regla que pierde por especificidad y deja una caja con su
    //    alto viejo dentro de una fila más baja. Ver criterio 92.
    const CONTENEDORES = '.kpi-grid, .deltas, .dist-wrap, .acciones, .fichas-grid,'
                       + '.cart-wrap, .kpi-img-wrap, .kpi-img-stack, .op-kpis, .op-dist';
    s.querySelectorAll(CONTENEDORES).forEach(cont => {
      const hijos = [...cont.children]
        .map(el => ({el, r: el.getBoundingClientRect()}))
        .filter(x => x.r.width > 0 && x.r.height > 0);
      for (let a = 0; a < hijos.length; a++) {
        for (let b = a + 1; b < hijos.length; b++) {
          const ra = hijos[a].r, rb = hijos[b].r;
          const ancho = Math.min(ra.right, rb.right) - Math.max(ra.left, rb.left);
          const alto = Math.min(ra.bottom, rb.bottom) - Math.max(ra.top, rb.top);
          if (ancho > 1 && alto > 1) {
            const texto = el => (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 28);
            r.push({tipo: 'superpuestas', n: i + 1, titulo: titulo(s),
                    px: Math.round(Math.min(ancho, alto)),
                    a: texto(hijos[a].el), b: texto(hijos[b].el)});
            return;
          }
        }
      }
    });
    // 2. Las tarjetas de una fila: el número arranca a la misma altura en todas.
    s.querySelectorAll('.deltas, .kpi-grid').forEach(fila => {
      const tops = [...fila.children].map(card => {
        const v = card.querySelector('.d-valor, .k-value');
        return v ? v.getBoundingClientRect().top - card.getBoundingClientRect().top
                 : null;
      }).filter(x => x !== null);
      if (tops.length > 1) {
        const dif = Math.max(...tops) - Math.min(...tops);
        if (dif > 2) r.push({tipo: 'tarjetas', n: i + 1, titulo: titulo(s),
                             px: Math.round(dif)});
      }
    });
  });
  return r;
}
"""


# One-pager: el texto legal nunca se encima con el contenido. Se decide midiendo
# el documento maquetado, porque el alto real depende del texto de cada celda y
# la compresión .tight/.tighter que elige Python cuenta filas, no píxeles. El
# orden es:
#   1. ajustar la reserva del pie al alto real del texto legal;
#   2. si no entra, subir la compresión de a un paso hasta .tighter;
#   3. si ni así entra, pasar el disclaimer entero a una segunda hoja, sola, y
#      volver a la compresión original: con el lugar liberado suele sobrar.
# Rompe la idea de una página, pero es la única salida que no esconde nada. Ver
# criterio 35.
_JS_ONEPAGER_LEGAL = """
() => {
  const PASOS = ['', 'tight', 'tighter'];
  const r = {comprimidas: [], movidas: [], siguen: []};
  const fondo = raiz => {
    let f = 0;
    raiz.querySelectorAll('*').forEach(el => {
      const b = el.getBoundingClientRect();
      if (b.width && b.height) f = Math.max(f, b.bottom);
    });
    return f;
  };
  const poner = (hoja, paso) => {
    hoja.classList.remove('tight', 'tighter');
    if (paso) hoja.classList.add(paso);
  };
  [...document.querySelectorAll('.sheet')].forEach((hoja, i) => {
    const pie = hoja.querySelector('.op-foot');
    const cuerpo = hoja.querySelector('.op-body');
    const legal = pie && pie.querySelector('.disclaimer');
    if (!pie || !cuerpo || !legal) return;
    const original = hoja.classList.contains('tighter') ? 'tighter'
                   : hoja.classList.contains('tight') ? 'tight' : '';
    const entra = techo => fondo(cuerpo) <= techo - 6;

    for (let k = PASOS.indexOf(original); k < PASOS.length; k++) {
      poner(hoja, PASOS[k]);
      cuerpo.style.paddingBottom = '';
      const hr = hoja.getBoundingClientRect(), pr = pie.getBoundingClientRect();
      cuerpo.style.paddingBottom = Math.ceil(hr.bottom - pr.top + 12) + 'px';
      if (entra(pie.getBoundingClientRect().top)) {
        if (PASOS[k] !== original) r.comprimidas.push(i + 1);
        return;
      }
    }

    // No entra ni con la compresión máxima: el legal va a una hoja propia.
    cuerpo.style.paddingBottom = '';
    const nueva = document.createElement('div');
    nueva.className = 'sheet sheet-legal';
    const caja = document.createElement('div');
    caja.className = 'op-legal';
    caja.appendChild(legal);
    nueva.appendChild(caja);
    hoja.after(nueva);
    hoja.classList.add('legal-aparte');
    r.movidas.push(i + 1);

    // Al pie de la primera hoja quedan sólo los contactos. Se vuelve a la
    // compresión original y se sube sólo si hace falta.
    const meta = hoja.querySelector('.op-meta');
    for (let k = PASOS.indexOf(original); k < PASOS.length; k++) {
      poner(hoja, PASOS[k]);
      if (!meta || entra(meta.getBoundingClientRect().top)) return;
    }
    r.siguen.push(i + 1);
  });
  return r;
}
"""

def render_pdf(html_str, out_path, formato, cliente=""):
    from playwright.sync_api import sync_playwright
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False,
                                     encoding="utf-8") as f:
        f.write(html_str)
        ruta = f.name
    opts = dict(PAGINA[formato])
    if formato == "documento":
        # El documento fluye y pagina solo, así que necesita pie corrido con
        # numeración. El deck y el one-pager tienen el pie dibujado en el CSS.
        opts.update(display_header_footer=True,
                    header_template="<div></div>",
                    footer_template=(
                        '<div style="width:100%;font-size:7px;color:#A1A1AA;'
                        'font-family:Arial,sans-serif;padding:0 20mm;'
                        'display:flex;justify-content:space-between;">'
                        f'<span>{html.escape(cliente)}</span>'
                        '<span class="pageNumber"></span></div>'))
    try:
        with sync_playwright() as pw:
            navegador = pw.chromium.launch()
            pagina = navegador.new_page()
            pagina.goto(f"file://{ruta}")
            pagina.wait_for_timeout(400)
            if formato == "deck":
                for r in pagina.evaluate(_JS_DESBORDE):
                    print(f"  DESBORDE: slide {r['n']} ('{r['titulo']}') se pasa "
                          f"{r['exceso']}px del pie. Empieza a encimarse en: "
                          f"\"{r['culpable']}\". Sacá contenido o partí la slide "
                          f"— no lo dejes recortado. Ver criterio 62.",
                          file=sys.stderr)
            if formato == "onepager":
                r = pagina.evaluate(_JS_ONEPAGER_LEGAL)
                if r["comprimidas"]:
                    print("  aviso: el one-pager no entraba con la compresión elegida; se "
                          "comprimió un paso más para que el texto legal no quede "
                          "encimado. Ver criterio 35.", file=sys.stderr)
                if r["movidas"]:
                    print("  AVISO: el contenido no deja lugar para el texto legal en la "
                          "hoja; el disclaimer pasó entero a una segunda hoja. Ver "
                          "criterio 35.", file=sys.stderr)
                for n in r["siguen"]:
                    print(f"  DESBORDE: hoja {n} del one-pager: aun sin el disclaimer, el "
                          f"contenido pisa los datos de contacto. Sacá contenido — no "
                          f"lo dejes recortado. Ver criterio 62.", file=sys.stderr)
            # Controles de maqueta: van después del ajuste del one-pager, que puede
            # haber cambiado la compresión y con ella el ancho de las leyendas.
            if formato in ("deck", "onepager"):
                for r in pagina.evaluate(_JS_MAQUETA):
                    if r["tipo"] == "leyenda":
                        print(f"  LEYENDA: slide {r['n']} ('{r['titulo']}'), gráfico "
                              f"'{r['grafico']}': la columna de porcentajes quedó a "
                              f"{r['px']}px de la de etiquetas. Tienen que leerse juntas. Ver "
                              f"criterio 81.", file=sys.stderr)
                    elif r["tipo"] == "pegado":
                        print(f"  LEYENDA: slide {r['n']} ('{r['titulo']}'), gráfico "
                              f"'{r['grafico']}': una etiqueta quedó pegada a su "
                              f"porcentaje ({r['px']}px). Ver criterio 81.", file=sys.stderr)
                    elif r["tipo"] == "superpuestas":
                        print(f"  SUPERPUESTAS: slide {r['n']} ('{r['titulo']}'): dos cajas "
                              f"hermanas se enciman {r['px']}px — \"{r['a']}\" y "
                              f"\"{r['b']}\". Suele ser una regla que pierde por "
                              f"especificidad. Ver criterio 92.", file=sys.stderr)
                    elif r["tipo"] == "deformada":
                        print(f"  IMAGEN: slide {r['n']} ('{r['titulo']}'): la captura se "
                              f"dibuja {r['pct']}% fuera de su proporción. Ver criterio "
                              f"87.", file=sys.stderr)
                    elif r["tipo"] == "borde":
                        print(f"  LEYENDA: slide {r['n']} ('{r['titulo']}'), gráfico "
                              f"'{r['grafico']}': la leyenda se pasa {r['px']}px del borde "
                              f"de la tarjeta. Acortá etiquetas o poné menos gráficos por "
                              f"fila. Ver criterio 86.", file=sys.stderr)
                    elif r["tipo"] == "alineacion":
                        print(f"  LEYENDA: slide {r['n']} ('{r['titulo']}'), gráfico "
                              f"'{r['grafico']}': los porcentajes no quedaron alineados "
                              f"a la derecha. Ver criterio 81.", file=sys.stderr)
                    elif r["tipo"] == "vacio":
                        print(f"  RECUADRO: slide {r['n']} ('{r['titulo']}'), gráfico "
                              f"'{r['grafico']}': el gráfico ocupa sólo {r['pct']}% de su "
                              f"recuadro. El recuadro tiene que rodear el gráfico, no "
                              f"aire. Ver criterio 81.", file=sys.stderr)
                    else:
                        print(f"  TARJETAS: slide {r['n']} ('{r['titulo']}'): el "
                              f"número de una tarjeta arranca {r['px']}px más abajo "
                              f"que el de otra de la misma fila. Tienen que ser "
                              f"iguales por dentro. Ver criterio 26.", file=sys.stderr)
            pagina.pdf(path=out_path, print_background=True, **opts)
            navegador.close()
    finally:
        os.unlink(ruta)


# ============================== Validación ================================= #

def controlar_distribucion(g, etiqueta, avisos):
    """Un gráfico de distribución tiene que cerrar en 100%.

    Se salta los que declaran `normalizar: false` —magnitudes independientes,
    como un antes/después de riesgo argentino, que no son partes de un todo— y
    los que vienen en montos absolutos, donde la suma no significa nada. El
    aviso salta sólo cuando los valores claramente quisieron ser porcentajes:
    suman cerca de 100 pero no 100. Ver criterio 58."""
    if get(g, "normalizar", default=True) is False:
        return
    # Una serie en moneda o con negativos no es una distribución: si sus montos
    # casualmente suman cerca de 100 el control avisaría de un agujero que no
    # existe. Ver criterio 97.
    if (get(g, "unidad", "unit", "moneda", default="%") or "%") not in ("%", ""):
        return
    vals = [_pct(get(it, "valor", "value", "pct", default=None))
            for it in (get(g, "items", "datos", default=[]) or [])]
    vals = [v for v in vals if v is not None]
    if len(vals) < 2 or any(v < 0 for v in vals):
        return
    # ±0,1 pp es el redondeo de la fuente, no un agujero: los pesos de un fact
    # sheet vienen con un decimal y sumados dan 99,9%. Avisar ahí convertía el
    # control en ruido fijo —saltaba en cada corrida de toda propuesta que usara
    # ese fact sheet— y un aviso que siempre salta deja de leerse.
    suma = round(sum(vals), 1)
    if 95.0 <= suma <= 105.0 and abs(suma - 100.0) > 0.105:
        avisos.append(
            f"{etiqueta}: el gráfico '{get(g, 'titulo', default='sin título')}' "
            f"suma {suma:.1f}%, no 100%. Si es una distribución tiene que cerrar; "
            f"si son magnitudes independientes marcalo con \"normalizar\": false.")


def controlar_etiquetas(c, etiqueta, avisos):
    """Dos gráficos de la misma lámina no pueden dar dos números a la misma
    etiqueta.

    Pasa cuando un vehículo trae adentro una clase que la cartera no tenía —el
    oro dentro de la cuenta administrada de CEDEARs de ETFs— y se abre en un
    gráfico pero no en el otro. Los dos quedan bien por separado y la lámina
    dice dos cosas. Ver criterios 64 y 95.

    Sólo mira pares de gráficos con **distinto juego de etiquetas**. Si los dos
    tienen exactamente las mismas categorías son un antes y un después, y que
    los valores cambien es justamente el contenido de la lámina: avisar ahí
    sería ruido en toda propuesta que compare dos carteras."""
    series = []
    for g in get(c, "graficos", "items", default=[]) or []:
        datos = {}
        for it in get(g, "items", "datos", default=[]) or []:
            lb = str(get(it, "label", "etiqueta", "categoria", "nombre",
                         default="") or "").strip()
            v = _pct(get(it, "valor", "value", "pct", default=None))
            if lb and v is not None:
                datos[lb.lower()] = (lb, v)
        if datos:
            series.append((get(g, "titulo", default="sin título"), datos))

    for i, (t1, d1) in enumerate(series):
        for t2, d2 in series[i + 1:]:
            if set(d1) == set(d2):
                continue
            # La categoría que uno abre y el otro no es la pista de qué pasó:
            # se nombra en el aviso para no dejar la corrección a la adivinanza.
            extra = sorted(set(d1) ^ set(d2))
            for clave in sorted(set(d1) & set(d2)):
                if abs(d1[clave][1] - d2[clave][1]) <= 0.05:
                    continue
                avisos.append(
                    f"{etiqueta}: '{d1[clave][0]}' vale {pct_coma(d1[clave][1])} "
                    f"en '{t1}' y {pct_coma(d2[clave][1])} en '{t2}', y "
                    f"'{d1.get(extra[0], d2.get(extra[0]))[0]}' está en uno solo "
                    f"de los dos. Decidí una sola vez si esa clase se abre y "
                    f"propagá a los dos gráficos, a los deltas y al texto.")
                break


def validar(p):
    """Revisa la propuesta antes de renderizar. La intención no es rechazar
    trabajo sino avisar temprano de lo que va a salir vacío o raro en el PDF,
    que es mucho más barato que descubrirlo mirando la hoja final."""
    problemas, avisos = [], []
    cli = get(p, "cliente", default=None)
    if not cli:
        problemas.append("Falta 'cliente'. La portada y el pie de cada slide lo usan.")
    if not get(p, "capitulos", default=None):
        problemas.append("Falta 'capitulos': la propuesta no tiene contenido.")

    for i, c in enumerate(get(p, "capitulos", default=[]) or []):
        tipo = (get(c, "tipo", "type", default="") or "").lower()
        et = f"capítulo {i + 1} ('{tipo or 'sin tipo'}')"
        if not tipo:
            problemas.append(f"{et}: falta 'tipo'.")
            continue
        if tipo not in CAPITULOS_DECK and tipo not in ("portada", "divisor", "cierre"):
            avisos.append(f"{et}: tipo desconocido, se renderiza como texto. "
                          f"Tipos válidos: {', '.join(sorted(CAPITULOS_DECK))}.")
        if tipo in ("cartera_sugerida", "cartera") and not get(c, "items", "posiciones"):
            problemas.append(f"{et}: no tiene 'items'; la tabla saldría vacía.")
        if tipo in ("cartera_sugerida", "cartera", "cartera_actual"):
            controlar_cierre(c, et, avisos)
        if tipo == "distribuciones":
            for g in get(c, "graficos", "items", default=[]) or []:
                if not (get(g, "items", "datos", default=[]) or []):
                    problemas.append(f"{et}: un gráfico no tiene 'items'.")
                controlar_distribucion(g, et, avisos)
            controlar_etiquetas(c, et, avisos)
        if tipo in ("kpis", "resumen") and get(c, "imagen", default=None):
            img = get(c, "imagen")
            if not ruta_recurso(get(img, "ruta", "path", "archivo", default=None)):
                problemas.append(f"{et}: no se encuentra la imagen "
                                 f"'{get(img, 'ruta', default='')}'. La ruta se busca "
                                 f"desde el directorio actual y desde la carpeta del JSON.")
            if not get(c, "nota", default=None):
                avisos.append(f"{et}: la captura no tiene nota. Tiene que decir de dónde "
                              f"sale y qué período muestra. Ver criterio 87.")
        if tipo in ("flujo_de_fondos", "flujo"):
            poss = get(c, "posiciones", "bonos", default=[]) or []
            if not poss:
                problemas.append(f"{et}: no tiene 'posiciones'. Pedile al asesor el "
                                 f"flujo de fondos de cada bono y los nominales.")
            for pos in poss:
                tk = get(pos, "ticker", "nombre", default="?")
                if not a_numero(get(pos, "nominales", "vn", default=None)):
                    problemas.append(f"{et}: {tk} no tiene nominales.")
                arch = get(pos, "archivo", "flujo", "xlsx", default=None)
                if arch and not ruta_recurso(arch):
                    problemas.append(f"{et}: no se encuentra el flujo de {tk}: '{arch}'.")
                    continue
                if not arch and not get(pos, "pagos", default=None):
                    problemas.append(f"{et}: {tk} no trae ni 'archivo' ni 'pagos'. El "
                                     f"calendario lo aporta el asesor — no se calcula.")
                    continue
                pagos = pagos_de_posicion(pos)
                am = sum(x["amortizacion"] for x in pagos)
                if pagos and abs(am - 100) > 0.5:
                    avisos.append(f"{et}: la amortización de {tk} suma {am:.1f} cada 100 "
                                  f"VN, no 100. El calendario puede estar incompleto.")
        if tipo == "instrumentos" and not get(c, "fichas", "items"):
            problemas.append(f"{et}: no tiene 'fichas'.")
        if tipo in ("trades", "movimientos"):
            movs = get(c, "items", "movimientos", "trades", default=[]) or []
            if not movs:
                problemas.append(f"{et}: no tiene 'items'; la tabla saldría vacía.")
            for j, m in enumerate(movs, 1):
                if not (get(m, "sale", "vender", "desde", default="")
                        and get(m, "entra", "comprar", "hacia", default="")):
                    avisos.append(f"{et}: el movimiento {j} no tiene los dos lados. "
                                  "Un trade se lee emparejado; si es una compra o una "
                                  "venta suelta, va en 'cartera_actual'.")
        if tipo == "tabla":
            headers = get(c, "headers", "columnas", default=[]) or []
            for j, fila in enumerate(get(c, "filas", "rows", default=[]) or []):
                if len(fila) != len(headers):
                    problemas.append(f"{et}: la fila {j + 1} tiene {len(fila)} celdas "
                                     f"y hay {len(headers)} columnas.")
                    break
    return problemas, avisos


# ================================= CLI ===================================== #

def main():
    ap = argparse.ArgumentParser(
        description="Genera el PDF de una propuesta de inversión de Max Capital.")
    ap.add_argument("--json", required=True, help="Ruta al JSON de la propuesta")
    ap.add_argument("--formato", default="deck",
                    choices=sorted(CONSTRUCTORES), help="deck | onepager | documento")
    ap.add_argument("--out", help="Ruta del PDF de salida")
    ap.add_argument("--design-html", dest="design_html",
                    help="Exporta el HTML con datos reales (para editar en Claude Design)")
    ap.add_argument("--validar", action="store_true",
                    help="Solo revisa el JSON y reporta problemas")
    ap.add_argument("--assets",
                    default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "..", "assets"))
    args = ap.parse_args()

    global DIR_JSON
    DIR_JSON = os.path.dirname(os.path.abspath(args.json))
    with open(args.json, encoding="utf-8") as f:
        propuesta = json.load(f)

    problemas, avisos = validar(propuesta)
    for a in avisos:
        print(f"  aviso: {a}", file=sys.stderr)
    if problemas:
        print("Problemas en la propuesta:", file=sys.stderr)
        for pr in problemas:
            print(f"  - {pr}", file=sys.stderr)
        if args.validar:
            raise SystemExit(1)
        raise SystemExit("Corregí el JSON y volvé a correr (o usá --validar "
                         "para ver el detalle).")
    if args.validar:
        print("OK: la propuesta es válida.")
        return

    if not args.out and not args.design_html:
        ap.error("Indicá --out (PDF) y/o --design-html (HTML para Claude Design)")

    assets = os.path.abspath(args.assets)
    html_str = construir_html(propuesta, args.formato, assets)

    if args.design_html:
        open(args.design_html, "w", encoding="utf-8").write(html_str)
        print(f"OK (design HTML) -> {args.design_html}")
    if args.out:
        cli = get(propuesta, "cliente", default={}) or {}
        nombre = get(cli, "nombre", default="") if isinstance(cli, dict) else str(cli)
        render_pdf(html_str, args.out, args.formato, nombre)
        print(f"OK (PDF {args.formato}) -> {args.out}")


if __name__ == "__main__":
    main()
