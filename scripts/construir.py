# -*- coding: utf-8 -*-
"""
motion-ad · CONSTRUIR — arma compositions/frames/*.html a partir de frames-src/*.html:
inyecta el producto (assets/producto.svg) en cada colorway, el kit de densidad y la duración de cada escena.

    python construir.py <P> [--solo fNN]      (--solo: construye solo esa escena, para ver el producto antes de tener todas)

Marcadores que entiende dentro de frames-src/*.html:
  {{PRODUCTO|colorway|ancho_px|id|clases extra|atributos}}   el producto con las variables de ese colorway (diseno.json); 5.º campo opcional = atributos (p. ej. data-layout-allow-overflow)
  {{KIT|fNN|NN|NOMBRE|tono}}                        marcas de registro, slate arriba, "SC NN / total" abajo, número fantasma, puntos y grano
  {{DUR}}                                           duración del slot de esa escena (la escena + el solape de la transición que le sigue)
  /*COMMON*/   (en el <style>)                       CSS del producto, del kit, .shadow, .chip, .cota
  /*KITJS*/    (en el <script>)                      define kit(tl, id, dur) para animar el kit

El SVG del producto lleva grupos <g id="g-parte"> (se convierten en data-part para poder prender/apagar partes),
pinta con variables CSS (--c-upper, --c-sole, …) y usa las clases ln (rellenos), shade, hi, st (costuras).
"""
import sys, os, re, glob, json

def main():
    if len(sys.argv) < 2: raise SystemExit(__doc__)
    P = sys.argv[1]; solo = sys.argv[sys.argv.index('--solo') + 1] if '--solo' in sys.argv else None
    dis = json.load(open(os.path.join(P, 'diseno.json'), encoding='utf-8'))
    plan = json.load(open(os.path.join(P, 'plan.json'), encoding='utf-8'))
    W, H = plan.get('lienzo', dis.get('lienzo', [1920, 1080]))
    esc = plan['escenas']; total = len(esc)
    solape = {'corte': 0.0, 'zoom': 0.25, 'barrido': 0.30, 'cromatico': 0.36, 'flash': 0.0}
    duraciones = {}
    for i, e in enumerate(esc):
        sig = esc[i + 1] if i + 1 < len(esc) else None
        duraciones[e['id']] = round(float(e['fin']) - float(e['inicio']) + (solape[sig.get('entrada', 'corte')] if sig else 0), 3)

    svg_path = os.path.join(P, dis.get('producto', 'assets/producto.svg'))
    SVG = open(svg_path, encoding='utf-8').read()
    SVG = re.sub(r'<!--.*?-->\s*', '', SVG, flags=re.S)
    SVG = re.sub(r'<\?xml[^>]*\?>\s*', '', SVG)
    vb = re.search(r'viewBox="([\d.\s-]+)"', SVG)
    vw, vh = (float(vb.group(1).split()[2]), float(vb.group(1).split()[3])) if vb else (1200, 640)
    SVG = re.sub(r'\s(width|height)="[\d.]+(px)?"', '', SVG, count=2)             # el tamaño lo pone cada escena
    SVG = re.sub(r'<g id="g-([\w-]+)"', r'<g data-part="\1"', SVG)               # ids únicos por copia → data-part
    if 'style="display:block' not in SVG:
        SVG = SVG.replace('<svg ', '<svg style="display:block;overflow:visible" ', 1)
    CW = dis['colorways']
    def producto(m):
        cw, w, idv, cls, attrs = m.group(1), int(m.group(2)), m.group(3), (m.group(4) or '').strip(), (m.group(5) or '').strip()
        if cw not in CW: raise SystemExit(f'colorway "{cw}" no está en diseno.json (hay: {", ".join(CW)})')
        h = round(w * vh / vw)
        svg = SVG.replace('<svg ', f'<svg width="{w}" height="{h}" ', 1)
        wire = ' wire' if cw.startswith('wire') else ''
        vars_ = CW[cw] if isinstance(CW[cw], str) else ';'.join(f'{k}:{v}' for k, v in CW[cw].items())
        return f'<div id="{idv}" class="producto{wire} {cls}" {attrs} style="width:{w}px;height:{h}px;{vars_}">{svg}</div>'

    GRAIN = 'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'300\' height=\'300\'%3E%3Cfilter id=\'n\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.9\' numOctaves=\'2\' stitchTiles=\'stitch\'/%3E%3C/filter%3E%3Crect width=\'300\' height=\'300\' filter=\'url(%23n)\'/%3E%3C/svg%3E")'
    TONOS = dis.get('tonos') or {'ink': ['rgba(243,239,228,.7)', 'rgba(243,239,228,.07)'], 'paper': ['rgba(18,18,22,.7)', 'rgba(18,18,22,.07)']}
    reel = dis.get('reel', dis.get('marca', 'MOTION AD'))
    k = H / 1080.0
    def kit(m):
        fid, nn, name, tone = m.group(1), m.group(2), m.group(3), m.group(4)
        if tone not in TONOS: raise SystemExit(f'tono "{tone}" no está en diseno.json → tonos (hay: {", ".join(TONOS)})')
        c, g = TONOS[tone]
        pts = [(44, 44), (W - 44, 44), (44, H - 44), (W - 44, H - 44)]
        reg = ''.join('<path d="M%d %dH%dM%d %dV%d"/><circle cx="%d" cy="%d" r="9"/>' % (x - 16, y, x + 16, x, y - 16, y + 16, x, y) for x, y in pts)
        return ('<div id="%s-kit" class="kit" style="--kc:%s;--kg:%s">' % (fid, c, g)
                + '<div class="kit-dots"></div><div class="kit-grain"></div>'
                + '<svg class="kit-reg" viewBox="0 0 %d %d">' % (W, H) + reg + '</svg>'
                + '<div class="kit-top">%s</div>' % reel
                + '<div class="kit-br">SC %s / %02d · %s</div>' % (nn, total, name)
                + '<div class="kit-ghost" data-layout-allow-overflow data-layout-allow-occlusion>%s</div></div>' % nn)
    KIT_CSS = ('.kit{position:absolute;inset:0;pointer-events:none}'
               '.kit-dots{position:absolute;inset:0;background-image:radial-gradient(var(--kc) 1.3px,rgba(0,0,0,0) 1.8px);background-size:48px 48px;opacity:.28}'
               '.kit-grain{position:absolute;inset:0;background-image:' + GRAIN + ';background-size:300px 300px;mix-blend-mode:overlay;opacity:.18}'
               '.kit-reg{position:absolute;inset:0;width:' + str(W) + 'px;height:' + str(H) + 'px;fill:none;stroke:var(--kc);stroke-width:2px}'
               '.kit-top{position:absolute;left:50%;top:40px;margin-left:-260px;width:520px;text-align:center;font-family:"Space Mono";font-weight:700;font-size:20px;letter-spacing:.2em;color:var(--kc)}'
               '.kit-br{position:absolute;right:72px;bottom:28px;font-family:"Space Mono";font-weight:700;font-size:20px;letter-spacing:.2em;color:var(--kc)}'
               '.kit-ghost{position:absolute;right:-30px;bottom:-150px;font-family:"League Gothic";font-size:' + str(int(760 * k)) + 'px;line-height:1;color:var(--kg)}'
               '.shadow{position:absolute;height:54px;border-radius:50%;background:radial-gradient(ellipse at center,rgba(18,18,22,.55) 0%,rgba(18,18,22,0) 70%)}'
               '.chip{position:absolute;font-family:"Space Mono";font-weight:700;font-size:22px;letter-spacing:.14em;padding:8px 14px;border:3px solid currentColor;white-space:nowrap}'
               '.cota{position:absolute;font-family:"Space Mono";font-weight:700;font-size:20px;letter-spacing:.14em;white-space:nowrap}'
               '.cota i{position:absolute;display:block;background:currentColor}')
    KIT_JS = ('const kit=(tl,id,d)=>{tl.fromTo("#"+id+"-kit .kit-ghost",{y:0},{y:-24,duration:d,ease:"none"},0);'
              'tl.fromTo("#"+id+"-kit .kit-top",{opacity:0,y:-10},{opacity:1,y:0,duration:.3,ease:"power2.out"},.05);'
              'tl.fromTo("#"+id+"-kit .kit-br",{opacity:0,x:12},{opacity:1,x:0,duration:.3,ease:"power2.out"},.1);'
              'tl.fromTo("#"+id+"-kit .kit-reg",{opacity:0},{opacity:1,duration:.25},.02);};')
    COMMON_CSS = ('.producto{position:absolute;transform-origin:50% 100%}.producto svg{display:block;overflow:visible}'
                  '.wire svg .ln{fill:none!important;stroke-width:7px}.wire svg .shade,.wire svg .hi,.wire svg .st{display:none}')

    os.makedirs(os.path.join(P, 'compositions', 'frames'), exist_ok=True)
    n = 0
    for src in sorted(glob.glob(os.path.join(P, 'frames-src', '*.html'))):
        nombre = os.path.splitext(os.path.basename(src))[0]
        if nombre.startswith('_') or (solo and nombre != solo): continue
        s = re.sub(r'\s*data-hf-id="[^"]*"', '', open(src, encoding='utf-8').read())
        s = re.sub(r'\{\{PRODUCTO\|([\w-]+)\|(\d+)\|([\w-]+)\|?([^}|]*)\|?([^}]*)\}\}', producto, s)
        s = re.sub(r'\{\{KIT\|([\w-]+)\|(\d+)\|([^|]+)\|(\w+)\}\}', kit, s)
        s = s.replace('/*COMMON*/', COMMON_CSS + KIT_CSS).replace('/*KITJS*/', KIT_JS)
        if '{{DUR}}' in s:
            if nombre not in duraciones: raise SystemExit(f'{nombre} usa {{{{DUR}}}} pero no está en plan.json → escenas')
            s = s.replace('{{DUR}}', str(duraciones[nombre]))
        out = os.path.join(P, 'compositions', 'frames', nombre + '.html')
        open(out, 'w', encoding='utf-8').write(s); n += 1
        print('OK', nombre + '.html', len(s), 'bytes', f'· slot {duraciones.get(nombre, "?")} s')
    faltan = [e['id'] for e in esc if not os.path.exists(os.path.join(P, 'frames-src', e['id'] + '.html'))]
    if faltan and not solo: print('[aviso] escenas del plan sin archivo en frames-src/:', ', '.join(faltan))
    print(f'{n} escenas construidas')

if __name__ == '__main__':
    main()
