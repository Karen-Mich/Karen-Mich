"""Genera los SVG animados del perfil en <out>/assets."""
import os
import sys

OUT = os.path.join(sys.argv[1], "assets")
os.makedirs(OUT, exist_ok=True)

GREEN, TEAL, PURPLE = "#6FDA44", "#00C9A7", "#845EC2"
BG, BG2, BORDER, TXT, MUTED = "#0d1117", "#161b22", "#30363d", "#e6edf3", "#8b949e"
SANS = "font-family:'Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif"
MONO = "font-family:'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

BASE_CSS = f"""
.sans{{{SANS}}} .mono{{{MONO}}}
.blink{{animation:blink 1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
"""


def svg(w, h, body, css=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
        f"<style>{BASE_CSS}{css}</style>\n{body}\n</svg>\n"
    )


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("ok", name)


def appear(name, start, hold=88, frm="translate(0px,12px)", extra_on=""):
    """Keyframes: oculto hasta start%, visible hasta hold%, oculto al final (bucle)."""
    s2 = min(start + 4, hold)
    return (
        f"@keyframes {name}{{0%,{start}%{{opacity:0;transform:{frm}}}"
        f"{s2}%,{hold}%{{opacity:1;transform:translate(0px,0px) scale(1){extra_on}}}"
        f"{min(hold + 4, 100)}%,100%{{opacity:0;transform:{frm}}}}}\n"
    )


def browser(w, h, url, inner):
    return f"""
<defs><clipPath id="win"><rect width="{w}" height="{h}" rx="16"/></clipPath></defs>
<g clip-path="url(#win)">
  <rect width="{w}" height="{h}" fill="{BG}"/>
  <rect width="{w}" height="40" fill="{BG2}"/>
  <circle cx="22" cy="20" r="6" fill="#ff5f56"/><circle cx="42" cy="20" r="6" fill="#ffbd2e"/><circle cx="62" cy="20" r="6" fill="#27c93f"/>
  <rect x="100" y="9" width="{w - 200}" height="22" rx="11" fill="{BG}" stroke="{BORDER}"/>
  <path d="M116 17 v-2 a4 4 0 0 1 8 0 v2 M114 17 h12 v8 h-12z" fill="none" stroke="{MUTED}" stroke-width="1.5"/>
  <text x="134" y="25" class="mono" font-size="12" fill="{MUTED}">{url}</text>
  {inner}
</g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16" fill="none" stroke="{BORDER}"/>
"""


# ───────────────────────── CABECERA ─────────────────────────
def header():
    W, H = 1000, 300
    css = """
.float{animation:float 8s ease-in-out infinite}
@keyframes float{0%,100%{transform:translate(0px,0px)}50%{transform:translate(0px,-16px)}}
.d1{animation-delay:-2s}.d2{animation-delay:-4s}.d3{animation-delay:-6s}
.in{animation:in 1.2s ease-out both}
@keyframes in{from{opacity:0;transform:translate(0px,14px)}to{opacity:1;transform:translate(0px,0px)}}
.i2{animation-delay:.3s}.i3{animation-delay:.6s}.i4{animation-delay:.9s}
"""
    # líneas de código abstractas del editor (segmentos: color, ancho)
    lines = [
        (0, [(PURPLE, 44), (GREEN, 80), (MUTED, 20)]),
        (16, [(TEAL, 56), (TXT, 70)]),
        (16, [(PURPLE, 30), (GREEN, 96)]),
        (32, [(TEAL, 40), (MUTED, 60), ("#e3b341", 30)]),
        (16, [(MUTED, 24)]),
        (0, [(PURPLE, 70), (GREEN, 40)]),
    ]
    ex, ey = 680, 62
    defs, code = [], []
    T = 7.0
    for i, (indent, segs) in enumerate(lines):
        y = ey + 56 + i * 24
        total = sum(w for _, w in segs) + 6 * (len(segs) - 1)
        a, b = 0.06 + i * 0.1, 0.06 + i * 0.1 + 0.08
        defs.append(
            f'<clipPath id="cl{i}"><rect x="{ex + 22 + indent}" y="{y - 6}" height="12" width="0">'
            f'<animate attributeName="width" dur="{T}s" repeatCount="indefinite" '
            f'values="0;0;{total};{total};0" keyTimes="0;{a:.3f};{b:.3f};0.92;1"/></rect></clipPath>'
        )
        x = ex + 22 + indent
        parts = []
        for color, w in segs:
            parts.append(f'<rect x="{x}" y="{y - 4}" width="{w}" height="8" rx="4" fill="{color}"/>')
            x += w + 6
        code.append(
            f'<text x="{ex + 10}" y="{y + 4}" class="mono" font-size="10" fill="{BORDER}">{i + 1}</text>'
            f'<g clip-path="url(#cl{i})">{"".join(parts)}</g>'
        )

    pills = [("Node.js · Express", GREEN, 150), ("Angular · React", TEAL, 140), ("MySQL", PURPLE, 76)]
    px, pill_svg = 60, []
    for label, color, w in pills:
        pill_svg.append(
            f'<rect x="{px}" y="226" width="{w}" height="30" rx="15" fill="{color}" fill-opacity=".14" stroke="{color}" stroke-opacity=".6"/>'
            f'<text x="{px + w / 2}" y="246" text-anchor="middle" class="sans" font-size="14" font-weight="600" fill="{color}">{label}</text>'
        )
        px += w + 12

    body = f"""
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="#151b26"/></linearGradient>
  <linearGradient id="name" x1="0" x2="1"><stop offset="0" stop-color="{GREEN}"/><stop offset=".5" stop-color="{TEAL}"/><stop offset="1" stop-color="{PURPLE}"/></linearGradient>
  <filter id="blur" x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation="45"/></filter>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="{BORDER}"/></pattern>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  {''.join(defs)}
</defs>
<g clip-path="url(#card)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#dots)" opacity=".55"/>
  <circle cx="140" cy="30" r="120" fill="{GREEN}" opacity=".22" filter="url(#blur)">
    <animate attributeName="cx" values="140;260;140" dur="14s" repeatCount="indefinite"/></circle>
  <circle cx="900" cy="280" r="150" fill="{PURPLE}" opacity=".35" filter="url(#blur)">
    <animate attributeName="cy" values="280;200;280" dur="12s" repeatCount="indefinite"/></circle>
  <circle cx="560" cy="-20" r="100" fill="{TEAL}" opacity=".2" filter="url(#blur)">
    <animate attributeName="cx" values="560;460;560" dur="16s" repeatCount="indefinite"/></circle>

  <text x="545" y="80" class="mono float" font-size="26" fill="{TEAL}" opacity=".35">{{ }}</text>
  <text x="590" y="270" class="mono float d1" font-size="24" fill="{PURPLE}" opacity=".45">&lt;/&gt;</text>
  <text x="630" y="215" class="mono float d2" font-size="20" fill="{GREEN}" opacity=".3">;</text>
  <text x="840" y="44" class="mono float d3" font-size="16" fill="{MUTED}" opacity=".5">SELECT *</text>

  <text x="60" y="92" class="mono in" font-size="18" fill="{GREEN}">&gt; hola, mundo. soy</text>
  <text x="58" y="158" class="sans in i2" font-size="58" font-weight="800" fill="url(#name)">Karen Guatumillo</text>
  <text x="60" y="200" class="sans in i3" font-size="21" fill="#c9d1d9">Estudiante de Ingeniería en Software</text>
  <g class="in i4">{''.join(pill_svg)}</g>

  <g class="float d1">
    <rect x="{ex}" y="{ey}" width="280" height="200" rx="12" fill="{BG}" fill-opacity=".92" stroke="{BORDER}"/>
    <circle cx="{ex + 16}" cy="{ey + 16}" r="4.5" fill="#ff5f56"/><circle cx="{ex + 30}" cy="{ey + 16}" r="4.5" fill="#ffbd2e"/><circle cx="{ex + 44}" cy="{ey + 16}" r="4.5" fill="#27c93f"/>
    <text x="{ex + 268}" y="{ey + 20}" text-anchor="end" class="mono" font-size="11" fill="{MUTED}">karen.java</text>
    <line x1="{ex}" y1="{ey + 32}" x2="{ex + 280}" y2="{ey + 32}" stroke="{BORDER}"/>
    {''.join(code)}
  </g>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{BORDER}"/>
"""
    save("header.svg", svg(W, H, body, css))


# ───────────────────────── TERMINAL (sobre mí) ─────────────────────────
def terminal():
    W, H = 900, 366
    T = 16.0
    prompt = f'<tspan fill="{GREEN}">karen@dev</tspan><tspan fill="{MUTED}"> ~ $ </tspan>'
    pw = 150  # ancho aproximado del prompt
    lines = [
        ("cmd", f'{prompt}<tspan fill="{TXT}">whoami</tspan>', 230, 0.3, 1.1),
        ("out", f'<tspan fill="{TXT}" font-weight="700">Karen Guatumillo</tspan><tspan fill="#c9d1d9"> · Estudiante de Ingeniería en Software</tspan>', 860, 1.4, 0),
        ("cmd", f'{prompt}<tspan fill="{TXT}">cat enfoque.txt</tspan>', 330, 2.2, 3.2),
        ("out", f'<tspan fill="{TEAL}">Back-End  ·  APIs REST  ·  Facturación electrónica</tspan>', 860, 3.5, 0),
        ("cmd", f'{prompt}<tspan fill="{TXT}">ls proyectos/</tspan>', 310, 4.3, 5.3),
        ("out", f'<tspan fill="#b39ddb">facturacion-angular/  sri-invoice-signer/  api-usuarios/  front-usuarios/</tspan>', 860, 5.6, 0),
        ("cmd", f'{prompt}<tspan fill="{TXT}">echo $FRASE</tspan>', 300, 6.4, 7.3),
        ("out", f'<tspan fill="#e3b341">"Siempre buscando nuevas formas de innovar"</tspan>', 860, 7.6, 0),
        ("cmd", f'{prompt}', 160, 8.2, 0),
    ]
    defs, texts = [], []
    y0, lh = 84, 32
    for i, (kind, content, width, start, end) in enumerate(lines):
        y = y0 + i * lh
        a = start / T
        if kind == "cmd" and end:
            b = end / T
            values = f"0;0;{pw};{width};{width};0"
            kt = f"0;{a:.4f};{a + 0.002:.4f};{b:.4f};0.97;1"
        else:
            values = f"0;0;{width};{width};0"
            kt = f"0;{a:.4f};{a + 0.002:.4f};0.97;1"
        defs.append(
            f'<clipPath id="t{i}"><rect x="28" y="{y - 22}" height="{lh}" width="0">'
            f'<animate attributeName="width" dur="{T}s" repeatCount="indefinite" values="{values}" keyTimes="{kt}"/>'
            f"</rect></clipPath>"
        )
        texts.append(
            f'<text x="30" y="{y}" class="mono" font-size="17" clip-path="url(#t{i})" xml:space="preserve">{content}</text>'
        )
    cy = y0 + (len(lines) - 1) * lh
    cursor = (
        f'<rect x="{30 + pw}" y="{cy - 16}" width="10" height="20" fill="{GREEN}" class="blink" opacity="0">'
        f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" values="0;0;1;1;0" '
        f'keyTimes="0;{8.2 / T:.4f};{8.25 / T:.4f};0.97;1" calcMode="discrete"/></rect>'
    )
    body = f"""
<defs><clipPath id="win"><rect width="{W}" height="{H}" rx="14"/></clipPath>{''.join(defs)}</defs>
<g clip-path="url(#win)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="38" fill="{BG2}"/>
  <circle cx="22" cy="19" r="6" fill="#ff5f56"/><circle cx="42" cy="19" r="6" fill="#ffbd2e"/><circle cx="62" cy="19" r="6" fill="#27c93f"/>
  <text x="{W / 2}" y="24" text-anchor="middle" class="mono" font-size="13" fill="{MUTED}">karen@dev: ~ — zsh</text>
  {''.join(texts)}
  <g class="blink">{cursor}</g>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{BORDER}"/>
"""
    save("terminal.svg", svg(W, H, body))


# ───────────────────────── PROYECTO: FACTURACIÓN ─────────────────────────
def facturacion():
    W, H = 800, 440
    rows = [
        ("Laptop Lenovo IdeaPad", "2", "$450.00", "$900.00"),
        ("Mouse inalámbrico", "3", "$18.50", "$55.50"),
        ('Monitor 24"', "1", "$189.00", "$189.00"),
        ("Teclado mecánico", "1", "$64.00", "$64.00"),
    ]
    css = "".join(appear(f"r{i}", 8 + i * 8, frm="translate(-24px,0px)") for i in range(len(rows)))
    css += appear("tot", 44)
    css += (
        "@keyframes stamp{0%,58%{opacity:0;transform:scale(2.6)}64%{opacity:1;transform:scale(.92)}"
        "68%,88%{opacity:1;transform:scale(1)}92%,100%{opacity:0;transform:scale(1)}}\n"
        ".anim{transform-box:fill-box;transform-origin:center}\n"
    )
    css += "".join(f".r{i}{{animation:r{i} 9s ease-out infinite}}" for i in range(len(rows)))
    css += ".tot{animation:tot 9s ease-out infinite}.stamp{animation:stamp 9s ease-out infinite}"

    row_svg = []
    for i, (p, q, u, s) in enumerate(rows):
        y = 236 + i * 34
        row_svg.append(
            f'<g class="r{i} anim">'
            f'<rect x="100" y="{y - 20}" width="670" height="30" rx="6" fill="{BG2 if i % 2 else BG}"/>'
            f'<text x="115" y="{y}" class="sans" font-size="14" fill="{TXT}">{p}</text>'
            f'<text x="480" y="{y}" class="mono" font-size="13" fill="{MUTED}" text-anchor="middle">{q}</text>'
            f'<text x="620" y="{y}" class="mono" font-size="13" fill="{MUTED}" text-anchor="end">{u}</text>'
            f'<text x="755" y="{y}" class="mono" font-size="13" fill="{TXT}" text-anchor="end">{s}</text></g>'
        )
    icons = "".join(
        f'<rect x="20" y="{70 + i * 50}" width="30" height="30" rx="8" fill="{GREEN if i == 0 else BORDER}" fill-opacity="{1 if i == 0 else .7}"/>'
        for i in range(5)
    )
    inner = f"""
<rect x="0" y="40" width="70" height="{H - 40}" fill="#11161d"/>
{icons}
<path d="M28 80 h14 M28 85 h14 M28 90 h9" stroke="{BG}" stroke-width="2.2" stroke-linecap="round"/>
<text x="100" y="85" class="sans" font-size="22" font-weight="700" fill="{TXT}">Factura</text>
<text x="190" y="85" class="mono" font-size="18" fill="{GREEN}">#000128</text>
<rect x="660" y="63" width="110" height="30" rx="8" fill="{GREEN}"/>
<text x="715" y="83" text-anchor="middle" class="sans" font-size="14" font-weight="700" fill="{BG}">+ Nueva</text>

<rect x="100" y="105" width="325" height="58" rx="10" fill="{BG2}" stroke="{BORDER}"/>
<circle cx="128" cy="134" r="15" fill="{PURPLE}"/><text x="128" y="139" text-anchor="middle" class="sans" font-size="13" font-weight="700" fill="#fff">CA</text>
<text x="152" y="128" class="sans" font-size="12" fill="{MUTED}">Cliente</text>
<text x="152" y="148" class="sans" font-size="15" font-weight="600" fill="{TXT}">Comercial Andina S.A.</text>
<rect x="445" y="105" width="325" height="58" rx="10" fill="{BG2}" stroke="{BORDER}"/>
<text x="465" y="128" class="sans" font-size="12" fill="{MUTED}">Fecha de emisión</text>
<text x="465" y="148" class="sans" font-size="15" font-weight="600" fill="{TXT}">25 nov 2026</text>
<text x="755" y="148" text-anchor="end" class="sans" font-size="12" fill="{TEAL}">Vence en 30 días</text>

<text x="115" y="196" class="sans" font-size="12" font-weight="700" fill="{MUTED}">PRODUCTO</text>
<text x="480" y="196" class="sans" font-size="12" font-weight="700" fill="{MUTED}" text-anchor="middle">CANT.</text>
<text x="620" y="196" class="sans" font-size="12" font-weight="700" fill="{MUTED}" text-anchor="end">PRECIO</text>
<text x="755" y="196" class="sans" font-size="12" font-weight="700" fill="{MUTED}" text-anchor="end">SUBTOTAL</text>
<line x1="100" y1="205" x2="770" y2="205" stroke="{BORDER}"/>
{''.join(row_svg)}

<g class="tot anim">
  <line x1="540" y1="360" x2="770" y2="360" stroke="{BORDER}"/>
  <text x="560" y="382" class="sans" font-size="13" fill="{MUTED}">Subtotal</text><text x="755" y="382" text-anchor="end" class="mono" font-size="13" fill="{TXT}">$1,208.50</text>
  <text x="560" y="402" class="sans" font-size="13" fill="{MUTED}">IVA 15%</text><text x="755" y="402" text-anchor="end" class="mono" font-size="13" fill="{TXT}">$181.28</text>
  <text x="560" y="426" class="sans" font-size="16" font-weight="700" fill="{TXT}">Total</text><text x="755" y="426" text-anchor="end" class="mono" font-size="17" font-weight="700" fill="{GREEN}">$1,389.78</text>
</g>
<g transform="translate(250 395) rotate(-10)">
  <g class="stamp anim">
    <rect x="-85" y="-26" width="170" height="52" rx="8" fill="none" stroke="{GREEN}" stroke-width="3.5"/>
    <rect x="-79" y="-20" width="158" height="40" rx="5" fill="none" stroke="{GREEN}" stroke-width="1.2"/>
    <text x="0" y="9" text-anchor="middle" class="sans" font-size="26" font-weight="800" fill="{GREEN}" letter-spacing="4">EMITIDA</text>
  </g>
</g>
"""
    save("proyecto-facturacion.svg", svg(W, H, browser(W, H, "localhost:4200/facturas/000128", inner), css))


# ───────────────────────── PROYECTO: USUARIOS (React + Express) ─────────────────────────
def usuarios():
    W, H = 800, 440
    D = 10
    rows = [
        ("Karen Guatumillo", "karen@correo.com", "admin", PURPLE, "KG"),
        ("Luis Pérez", "luis@correo.com", "usuario", TEAL, "LP"),
        ("María Gómez", "maria@correo.com", "usuario", "#e3b341", "MG"),
        ("Diego Ruiz", "diego@correo.com", "usuario", GREEN, "DR"),
    ]
    css = ".anim{transform-box:fill-box;transform-origin:center}\n"
    css += appear("req", 15, frm="translate(-14px,0px)") + appear("res", 23, frm="translate(14px,0px)")
    css += f".req{{animation:req {D}s ease-out infinite}}.res{{animation:res {D}s ease-out infinite}}\n"
    for i in range(len(rows)):
        css += appear(f"u{i}", 32 + i * 6, frm="translate(0px,14px)")
        css += f".u{i}{{animation:u{i} {D}s ease-out infinite}}\n"
    css += (
        "@keyframes press{0%,12%{transform:scale(1)}13.5%{transform:scale(.93)}15%,100%{transform:scale(1)}}"
        f".press{{animation:press {D}s ease-out infinite}}\n"
    )

    def clip(id_, x, y, w, a, b):
        return (
            f'<clipPath id="{id_}"><rect x="{x}" y="{y}" height="26" width="0">'
            f'<animate attributeName="width" dur="{D}s" repeatCount="indefinite" values="0;0;{w};{w};0" '
            f'keyTimes="0;{a};{b};0.95;1"/></rect></clipPath>'
        )

    row_svg = []
    for i, (name, mail, rol, color, ini) in enumerate(rows):
        y = 146 + i * 52
        rc = PURPLE if rol == "admin" else TEAL
        row_svg.append(f"""
<g class="u{i} anim">
  <rect x="320" y="{y}" width="450" height="46" rx="8" fill="{BG if i % 2 == 0 else BG2}"/>
  <circle cx="346" cy="{y + 23}" r="15" fill="{color}"/>
  <text x="346" y="{y + 28}" text-anchor="middle" class="sans" font-size="11" font-weight="800" fill="{BG}">{ini}</text>
  <text x="370" y="{y + 20}" class="sans" font-size="14" font-weight="600" fill="{TXT}">{name}</text>
  <text x="370" y="{y + 36}" class="mono" font-size="10.5" fill="{MUTED}">id: {i + 1}</text>
  <text x="510" y="{y + 28}" class="mono" font-size="12" fill="{MUTED}">{mail}</text>
  <rect x="664" y="{y + 12}" width="62" height="22" rx="11" fill="{rc}" fill-opacity=".18" stroke="{rc}" stroke-opacity=".6"/>
  <text x="695" y="{y + 27}" text-anchor="middle" class="sans" font-size="11" font-weight="700" fill="{rc}">{rol}</text>
  <path d="M740 {y + 29} l2 -6 l8 -8 l4 4 l-8 8z" fill="none" stroke="{MUTED}" stroke-width="1.6" stroke-linejoin="round"/>
  <path d="M758 {y + 17} h10 M760 {y + 17} v12 h6 v-12 M762 {y + 15} h2" fill="none" stroke="#ff7b72" stroke-width="1.6" stroke-linecap="round"/>
</g>""")

    inner = f"""
<defs>
  {clip("mail", 50, 196, 140, 0.02, 0.09)}
  {clip("pass", 50, 258, 90, 0.095, 0.12)}
</defs>
<rect x="20" y="58" width="280" height="364" rx="14" fill="{BG2}" stroke="{BORDER}"/>
<circle cx="160" cy="100" r="22" fill="{PURPLE}" fill-opacity=".22"/>
<path d="M153 99 v-5 a7 7 0 0 1 14 0 v5" fill="none" stroke="{PURPLE}" stroke-width="2.4"/>
<rect x="149" y="98" width="22" height="15" rx="3" fill="{PURPLE}"/>
<text x="160" y="148" text-anchor="middle" class="sans" font-size="18" font-weight="700" fill="{TXT}">Iniciar sesión</text>
<text x="40" y="180" class="sans" font-size="12" fill="{MUTED}">Correo</text>
<rect x="40" y="188" width="240" height="34" rx="8" fill="{BG}" stroke="{BORDER}"/>
<text x="52" y="210" class="sans" font-size="14" fill="{TXT}" clip-path="url(#mail)">karen@correo.com</text>
<text x="40" y="242" class="sans" font-size="12" fill="{MUTED}">Contraseña</text>
<rect x="40" y="250" width="240" height="34" rx="8" fill="{BG}" stroke="{BORDER}"/>
<text x="52" y="273" class="mono" font-size="16" fill="{TXT}" clip-path="url(#pass)" letter-spacing="2">••••••••</text>
<g class="press anim">
  <rect x="40" y="298" width="240" height="36" rx="8" fill="{GREEN}"/>
  <text x="160" y="321" text-anchor="middle" class="sans" font-size="14" font-weight="700" fill="{BG}">Ingresar</text>
</g>
<rect x="40" y="348" width="240" height="60" rx="8" fill="{BG}" stroke="{BORDER}"/>
<text class="req mono anim" x="52" y="372" font-size="11" fill="{TEAL}">→ POST /api/usuarios/login</text>
<text class="res mono anim" x="52" y="394" font-size="11" fill="{GREEN}">← 200 OK · token JWT ✓</text>

<rect x="310" y="58" width="470" height="364" rx="14" fill="{BG2}" stroke="{BORDER}"/>
<text x="330" y="94" class="sans" font-size="20" font-weight="700" fill="{TXT}">Usuarios</text>
<rect x="424" y="77" width="118" height="22" rx="11" fill="{PURPLE}" fill-opacity=".18"/>
<path d="M436 82 l6 -2 l6 2 v5 c0 4 -3 6 -6 7 c-3 -1 -6 -3 -6 -7z" fill="{PURPLE}"/>
<text x="454" y="92" class="sans" font-size="11" font-weight="600" fill="#b39ddb">Ruta protegida</text>
<rect x="684" y="74" width="82" height="28" rx="8" fill="{GREEN}"/>
<text x="725" y="93" text-anchor="middle" class="sans" font-size="13" font-weight="700" fill="{BG}">+ Nuevo</text>
<text x="370" y="132" class="sans" font-size="11" font-weight="700" fill="{MUTED}">NOMBRE</text>
<text x="510" y="132" class="sans" font-size="11" font-weight="700" fill="{MUTED}">CORREO</text>
<text x="695" y="132" text-anchor="middle" class="sans" font-size="11" font-weight="700" fill="{MUTED}">ROL</text>
<line x1="320" y1="140" x2="770" y2="140" stroke="{BORDER}"/>
{''.join(row_svg)}
<text x="330" y="400" class="sans" font-size="12" fill="{MUTED}">Mostrando 4 usuarios</text>
<text x="764" y="400" text-anchor="end" class="mono" font-size="11" fill="{TEAL}">GET /api/usuarios · Bearer</text>
"""
    save("proyecto-usuarios.svg", svg(W, H, browser(W, H, "front-usuarios-psi.vercel.app/dashboard", inner), css))


# ───────────────────────── PROYECTO: FIRMA SRI ─────────────────────────
def firma():
    import re
    W, H = 800, 440
    D = 10
    TAG, ATTR = "#7ee787", "#79c0ff"

    def xml(line):
        out = []
        for part in re.split(r"(<[^>]+>)", line):
            if not part:
                continue
            esc = part.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            if part.startswith("<"):
                esc = re.sub(r'(\w[\w:]*)=(&quot;|")([^"]*)"', rf'<tspan fill="{ATTR}">\1</tspan>=<tspan fill="#a5d6ff">"\3"</tspan>', esc)
                out.append(f'<tspan fill="{TAG}">{esc}</tspan>')
            else:
                out.append(f'<tspan fill="#c9d1d9">{esc}</tspan>')
        return "".join(out)

    base = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<factura id="comprobante" version="1.1.0">',
        "  <infoTributaria>",
        "    <ambiente>1</ambiente>",
        "    <claveAcceso>2511202601179…</claveAcceso>",
        "  </infoTributaria>",
        "  <infoFactura>…</infoFactura>",
        "  <detalles>…</detalles>",
    ]
    sig = [
        '  <ds:Signature Id="Signature">',
        "    <ds:SignedInfo>…</ds:SignedInfo>",
        "    <ds:SignatureValue>kF3x…Qw==</ds:SignatureValue>",
        "    <ds:KeyInfo>…</ds:KeyInfo>",
        "    <ds:Object>xades:SignedProperties</ds:Object>",
        "  </ds:Signature>",
    ]
    y0, lh = 104, 21
    css = ".anim{transform-box:fill-box;transform-origin:center}\n"
    css += (
        f"@keyframes close{{0%,16%{{transform:translate(0px,-{lh * len(sig)}px)}}20%,90%{{transform:translate(0px,0px)}}"
        f"94%,100%{{transform:translate(0px,-{lh * len(sig)}px)}}}}.close{{animation:close {D}s ease-in-out infinite}}\n"
    )
    lines = []
    for i, l in enumerate(base):
        y = y0 + i * lh
        lines.append(f'<text x="34" y="{y}" class="mono" font-size="11" fill="{BORDER}" text-anchor="end">{i + 1}</text>')
        lines.append(f'<text x="46" y="{y}" class="mono" font-size="12.5" xml:space="preserve">{xml(l)}</text>')
    for j, l in enumerate(sig):
        i = len(base) + j
        y = y0 + i * lh
        css += appear(f"s{j}", 20 + j * 4, frm="translate(-10px,0px)") + f".s{j}{{animation:s{j} {D}s ease-out infinite}}\n"
        lines.append(
            f'<g class="s{j} anim"><rect x="40" y="{y - 15}" width="456" height="{lh}" fill="{GREEN}" fill-opacity=".1"/>'
            f'<rect x="40" y="{y - 15}" width="3" height="{lh}" fill="{GREEN}"/>'
            f'<text x="34" y="{y}" class="mono" font-size="11" fill="{GREEN}" text-anchor="end">+</text>'
            f'<text x="46" y="{y}" class="mono" font-size="12.5" xml:space="preserve">{xml(l)}</text></g>'
        )
    yc = y0 + (len(base) + len(sig)) * lh
    lines.append(
        f'<g class="close"><text x="34" y="{yc}" class="mono" font-size="11" fill="{BORDER}" text-anchor="end">{len(base) + len(sig) + 1}</text>'
        f'<text x="46" y="{yc}" class="mono" font-size="12.5">{xml("</factura>")}</text></g>'
    )

    css += (
        "@keyframes seal{0%,50%{opacity:0;transform:scale(.3) rotate(-30deg)}55%{opacity:1;transform:scale(1.15) rotate(6deg)}"
        "59%,90%{opacity:1;transform:scale(1) rotate(0deg)}94%,100%{opacity:0;transform:scale(.3) rotate(-30deg)}}"
        f".seal{{animation:seal {D}s ease-out infinite}}\n"
        "@keyframes flow{to{stroke-dashoffset:-24}}.flow{animation:flow 1s linear infinite}\n"
    )
    for k in range(3):
        css += appear(f"t{k}", 62 + k * 5, frm="translate(0px,8px)") + f".t{k}{{animation:t{k} {D}s ease-out infinite}}\n"

    inner = f"""
<rect x="20" y="56" width="480" height="368" rx="12" fill="{BG2}" stroke="{BORDER}"/>
<path d="M20 68 a12 12 0 0 1 12 -12 h108 v28 h-120z" fill="{BG}"/>
<text x="36" y="75" class="mono" font-size="12" fill="{TXT}">factura.xml</text>
<circle cx="126" cy="70" r="3.5" fill="{GREEN}"/>
<line x1="20" y1="84" x2="500" y2="84" stroke="{BORDER}"/>
{''.join(lines)}

<rect x="520" y="56" width="260" height="88" rx="12" fill="{BG2}" stroke="{BORDER}"/>
<rect x="536" y="74" width="40" height="52" rx="6" fill="{PURPLE}" fill-opacity=".2" stroke="{PURPLE}"/>
<circle cx="556" cy="94" r="7" fill="none" stroke="{PURPLE}" stroke-width="2.4"/>
<path d="M556 101 v14 m0 -5 h5 m-5 4 h4" stroke="{PURPLE}" stroke-width="2.4" fill="none"/>
<text x="590" y="94" class="mono" font-size="13" font-weight="700" fill="{TXT}">signature.p12</text>
<text x="590" y="114" class="sans" font-size="11.5" fill="{MUTED}">Certificado PKCS#12</text>
<text x="590" y="130" class="sans" font-size="11.5" fill="{MUTED}">node-forge · sin OpenSSL</text>

<path class="flow" d="M650 150 V196" stroke="{TEAL}" stroke-width="2.5" stroke-dasharray="6 6"/>
<path d="M644 192 l6 8 l6 -8" fill="none" stroke="{TEAL}" stroke-width="2.5" stroke-linejoin="round"/>
<text x="662" y="178" class="mono" font-size="12" fill="{TEAL}">signInvoiceXml()</text>

<g class="seal anim">
  <circle cx="650" cy="250" r="44" fill="{GREEN}" fill-opacity=".14" stroke="{GREEN}" stroke-width="2.5" stroke-dasharray="5 4"/>
  <circle cx="650" cy="250" r="32" fill="{GREEN}"/>
  <path d="M636 250 l10 10 l18 -20" fill="none" stroke="{BG}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
</g>
<text x="650" y="318" text-anchor="middle" class="sans" font-size="15" font-weight="800" fill="{TXT}">Firma XAdES-BES</text>
<text x="650" y="336" text-anchor="middle" class="sans" font-size="12" fill="{MUTED}">lista para enviar al SRI</text>

<rect x="520" y="350" width="260" height="74" rx="10" fill="{BG}" stroke="{BORDER}"/>
<text class="t0 anim mono" x="534" y="372" font-size="11.5" fill="{TXT}"><tspan fill="{GREEN}">$</tspan> npm test</text>
<g class="t1 anim"><rect x="534" y="381" width="36" height="16" rx="3" fill="{GREEN}"/><text x="552" y="393" text-anchor="middle" class="mono" font-size="10" font-weight="700" fill="{BG}">PASS</text>
<text x="578" y="393" class="mono" font-size="11" fill="#c9d1d9">signature.test.ts</text></g>
<g class="t2 anim"><rect x="534" y="401" width="36" height="16" rx="3" fill="{GREEN}"/><text x="552" y="413" text-anchor="middle" class="mono" font-size="10" font-weight="700" fill="{BG}">PASS</text>
<text x="578" y="413" class="mono" font-size="11" fill="#c9d1d9">c14n.test.ts</text></g>
"""
    save("proyecto-firma-sri.svg", svg(W, H, browser(W, H, "sri-invoice-signer · TypeScript", inner), css))


# ───────────────────────── RECORRIDO (línea de tiempo) ─────────────────────────
def recorrido():
    W, H = 1000, 220
    hitos = [
        ("2023", "Primeros pasos", "HTML · CSS · Git", TEAL),
        ("2023", "POO con Java", "Java · NetBeans", "#e3b341"),
        ("2024", "Back-End y APIs", "PHP · Laravel · Python", PURPLE),
        ("2025", "Facturación", "Angular · TS · SRI", GREEN),
        ("2025", "Full-Stack", "React · Express · JWT", TEAL),
        ("HOY", "¿Qué sigue?", "abierta a nuevos retos", GREEN),
    ]
    xs = [90 + i * 164 for i in range(len(hitos))]
    ly = 104
    css = (
        "@keyframes draw{from{stroke-dashoffset:100}to{stroke-dashoffset:0}}"
        ".line{stroke-dasharray:100;animation:draw 2.4s ease-out both}\n"
        "@keyframes pop{0%{opacity:0;transform:scale(.2)}70%{opacity:1;transform:scale(1.2)}100%{opacity:1;transform:scale(1)}}\n"
        "@keyframes up{from{opacity:0;transform:translate(0px,10px)}to{opacity:1;transform:translate(0px,0px)}}\n"
        ".anim{transform-box:fill-box;transform-origin:center}\n"
    )
    nodes = []
    for i, ((year, title, sub, color), x) in enumerate(zip(hitos, xs)):
        d = 0.2 + i * 0.4
        last = i == len(hitos) - 1
        ring = (
            f'<circle cx="{x}" cy="{ly}" r="10" fill="none" stroke="{color}" stroke-width="2">'
            f'<animate attributeName="r" values="10;26" dur="1.6s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="1;0" dur="1.6s" repeatCount="indefinite"/></circle>'
            if last else ""
        )
        nodes.append(f"""
<g class="anim" style="animation:pop .6s ease-out {d:.1f}s both">
  {ring}
  <circle cx="{x}" cy="{ly}" r="16" fill="{color}" fill-opacity=".15"/>
  <circle cx="{x}" cy="{ly}" r="8" fill="{color}" stroke="{BG}" stroke-width="3"/>
</g>
<g style="animation:up .6s ease-out {d + .15:.2f}s both">
  <text x="{x}" y="{ly - 30}" text-anchor="middle" class="mono" font-size="13" font-weight="700" fill="{color}">{year}</text>
  <text x="{x}" y="{ly + 44}" text-anchor="middle" class="sans" font-size="15" font-weight="700" fill="{TXT}">{title}</text>
  <text x="{x}" y="{ly + 64}" text-anchor="middle" class="mono" font-size="11" fill="{MUTED}">{sub}</text>
</g>""")
    body = f"""
<defs><linearGradient id="tl" gradientUnits="userSpaceOnUse" x1="{xs[0]}" y1="0" x2="{xs[-1]}" y2="0"><stop offset="0" stop-color="{TEAL}"/><stop offset=".5" stop-color="{PURPLE}"/><stop offset="1" stop-color="{GREEN}"/></linearGradient></defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="{BG}" stroke="{BORDER}"/>
<text x="28" y="32" class="mono" font-size="12" fill="{MUTED}">// git log --reverse --oneline karen</text>
<line x1="{xs[0]}" y1="{ly}" x2="{xs[-1]}" y2="{ly}" stroke="{BORDER}" stroke-width="3" stroke-linecap="round"/>
<line class="line" pathLength="100" x1="{xs[0]}" y1="{ly}" x2="{xs[-1]}" y2="{ly}" stroke="url(#tl)" stroke-width="3" stroke-linecap="round"/>
<circle r="4" fill="#fff" opacity="0">
  <animateMotion dur="5s" begin="2.6s" repeatCount="indefinite" path="M{xs[0]} {ly} H{xs[-1]}"/>
  <animate attributeName="opacity" values="0;0;.9;.9;0" keyTimes="0;.01;.05;.9;1" dur="5s" begin="2.6s" repeatCount="indefinite"/>
</circle>
{''.join(nodes)}
"""
    save("recorrido.svg", svg(W, H, body, css))


# ───────────────────────── TECH STACK (cuadrícula uniforme) ─────────────────────────
def stack():
    """Descarga los iconos de skillicons.dev y los incrusta (las imágenes de GitHub no cargan recursos externos)."""
    import re
    import urllib.request

    cats = {
        "Lenguajes": TEAL,
        "Frontend": PURPLE,
        "Back-End y BD": GREEN,
        "Herramientas": "#e3b341",
    }
    items = [
        ("ts", "TypeScript", "Lenguajes"), ("js", "JavaScript", "Lenguajes"), ("java", "Java", "Lenguajes"),
        ("php", "PHP", "Lenguajes"), ("py", "Python", "Lenguajes"), ("html", "HTML", "Lenguajes"),
        ("css", "CSS", "Lenguajes"),
        ("angular", "Angular", "Frontend"), ("react", "React", "Frontend"), ("vite", "Vite", "Frontend"),
        ("bootstrap", "Bootstrap", "Frontend"),
        ("nodejs", "Node.js", "Back-End y BD"), ("express", "Express", "Back-End y BD"),
        ("laravel", "Laravel", "Back-End y BD"), ("mysql", "MySQL", "Back-End y BD"),
        ("git", "Git", "Herramientas"), ("github", "GitHub", "Herramientas"), ("vscode", "VS Code", "Herramientas"),
        ("vercel", "Vercel", "Herramientas"), ("postman", "Postman", "Herramientas"), ("jest", "Jest", "Herramientas"),
    ]

    def icon(key, n):
        req = urllib.request.Request(f"https://skillicons.dev/icons?i={key}", headers={"User-Agent": "Mozilla/5.0"})
        raw = urllib.request.urlopen(req, timeout=20).read().decode("utf-8")
        start = raw.index("<svg", raw.index("<svg") + 4)
        end = raw.rindex("</svg>", 0, raw.rindex("</svg>")) + len("</svg>")
        inner = raw[start:end]
        inner = re.sub(r'id="([^"]+)"', lambda m: f'id="i{n}-{m.group(1)}"', inner)
        inner = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#i{n}-{m.group(1)})", inner)
        inner = re.sub(r'href="#([^"]+)"', lambda m: f'href="#i{n}-{m.group(1)}"', inner)
        return inner

    W, cols = 1000, 7
    tw, th, gap = 120, 116, 16
    x0 = (W - (cols * tw + (cols - 1) * gap)) / 2
    y0 = 78
    rows = (len(items) + cols - 1) // cols
    H = y0 + rows * th + (rows - 1) * gap + 30
    css = (
        "@keyframes pop{0%{opacity:0;transform:translate(0px,14px) scale(.9)}100%{opacity:1;transform:translate(0px,0px) scale(1)}}\n"
        ".anim{transform-box:fill-box;transform-origin:center}\n"
        "@keyframes glow{0%,100%{opacity:.35}50%{opacity:1}}\n"
    )
    tiles = []
    for n, (key, label, cat) in enumerate(items):
        r, c = divmod(n, cols)
        x = x0 + c * (tw + gap)
        y = y0 + r * (th + gap)
        color = cats[cat]
        d = 0.1 + n * 0.06
        tiles.append(f"""
<g class="anim" style="animation:pop .5s ease-out {d:.2f}s both">
  <rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="14" fill="{BG2}" stroke="{BORDER}"/>
  <rect x="{x + 34}" y="{y + th - 4}" width="{tw - 68}" height="3" rx="1.5" fill="{color}" style="animation:glow 3s ease-in-out {n * 0.15:.2f}s infinite"/>
  <svg x="{x + (tw - 56) / 2}" y="{y + 16}" width="56" height="56" viewBox="0 0 256 256">{icon(key, n)}</svg>
  <text x="{x + tw / 2}" y="{y + 94}" text-anchor="middle" class="sans" font-size="13.5" font-weight="600" fill="{TXT}">{label}</text>
</g>""")

    legend, lx = [], W - 32
    for name, color in reversed(list(cats.items())):
        w = len(name) * 7.4 + 22
        lx -= w
        legend.append(
            f'<circle cx="{lx + 6}" cy="38" r="5" fill="{color}"/>'
            f'<text x="{lx + 16}" y="43" class="sans" font-size="13" fill="{MUTED}">{name}</text>'
        )
        lx -= 14
    body = f"""
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{BG}" stroke="{BORDER}"/>
<text x="32" y="43" class="mono" font-size="13" fill="{MUTED}">// lo que uso para construir</text>
{''.join(legend)}
{''.join(tiles)}
"""
    save("stack.svg", svg(W, H, body, css))


header()
terminal()
facturacion()
usuarios()
firma()
recorrido()
stack()
