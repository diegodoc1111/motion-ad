# -*- coding: utf-8 -*-
"""
motion-ad · ENSAMBLAR — escribe P/index.html a partir de P/plan.json: un slot por escena (con el solape que
necesita su transición), las transiciones en el timeline raíz, la música y los efectos de sonido.

    python ensamblar.py <P>

plan.json:
{
  "duracion": 15, "lienzo": [1920, 1080], "fondo": "#121216",
  "musica": {"archivo": "assets/audio/bgm.mp3", "volumen": 0.72},          (opcional)
  "transicion_colores": {"borde": ["#FF4A3D", "#D6FF3F"], "flash": "#FFFFFF"},
  "escenas": [ {"id": "f01-gancho", "inicio": 0, "fin": 2.087, "entrada": "corte"}, … ],
  "sfx": [ [0.0, "whoosh-short", 0.5], [0.522, "click", 0.5], … ]           ([segundo, nombre, volumen])
}
"entrada" = cómo ENTRA esa escena: corte · zoom · barrido · cromatico · flash
Cada escena vive en compositions/frames/<id>.html (la construye construir.py desde frames-src/).
"""
import sys, os, json, subprocess

SOLAPE = {'corte': 0.0, 'zoom': 0.25, 'barrido': 0.30, 'cromatico': 0.36, 'flash': 0.0}

def dur_audio(p, cache={}):
    if p not in cache:
        r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True)
        cache[p] = float(r.stdout.strip() or 0)
    return cache[p]

def seam(tipo, A, B, T, W):
    if tipo == 'zoom':
        return (f'  tl.fromTo("#{A}", {{ scale: 1, filter: "blur(0px)", opacity: 1 }}, {{ scale: 1.22, filter: "blur(18px)", opacity: 0, duration: 0.25, ease: "power3.in" }}, {T});\n'
                f'  tl.fromTo("#{B}", {{ scale: 0.78, filter: "blur(16px)" }}, {{ scale: 1, filter: "blur(0px)", duration: 0.45, ease: "expo.out" }}, {T});\n')
    if tipo == 'barrido':
        return (f'  tl.fromTo("#{A}", {{ x: 0, filter: "blur(0px)" }}, {{ x: {-int(W*0.22)}, filter: "blur(22px)", duration: 0.3, ease: "power3.in" }}, {T});\n'
                f'  tl.fromTo("#{B}", {{ x: {int(W*0.22)}, filter: "blur(22px)" }}, {{ x: 0, filter: "blur(0px)", duration: 0.32, ease: "power3.out" }}, {T});\n')
    if tipo == 'cromatico':
        D = 0.36
        return (f'  tl.fromTo("#{B}", {{ clipPath: "inset(0px 0px 0px {W}px)" }}, {{ clipPath: "inset(0px 0px 0px 0px)", duration: {D}, ease: "power4.inOut" }}, {T});\n'
                f'  tl.fromTo("#{A}", {{ x: 0, filter: "blur(0px)" }}, {{ x: {-int(W*0.135)}, filter: "blur(14px)", duration: {D}, ease: "power3.in" }}, {T});\n'
                f'  tl.fromTo("#wipe-edge", {{ x: {W}, opacity: 1 }}, {{ x: -60, opacity: 1, duration: {D}, ease: "power4.inOut" }}, {T});\n'
                f'  tl.set("#wipe-edge", {{ opacity: 0 }}, {round(T + D, 3)});\n'
                f'  tl.fromTo("#flash", {{ opacity: 0 }}, {{ opacity: 0.85, duration: 1 / 30, ease: "none" }}, {round(T + D * 0.5, 3)});\n'
                f'  tl.to("#flash", {{ opacity: 0, duration: 2 / 30, ease: "none" }}, {round(T + D * 0.5 + 1 / 30, 3)});\n')
    if tipo == 'flash':
        return (f'  tl.fromTo("#flash", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.07, ease: "power2.in" }}, {round(T - 0.07, 3)});\n'
                f'  tl.to("#flash", {{ opacity: 0, duration: 0.22, ease: "power2.out" }}, {T});\n')
    return f'  // {A} → {B}: corte seco en {T}\n'

def main():
    if len(sys.argv) < 2: raise SystemExit(__doc__)
    P = sys.argv[1]; plan = json.load(open(os.path.join(P, 'plan.json'), encoding='utf-8'))
    W, H = plan.get('lienzo', [1920, 1080]); dur = float(plan['duracion']); fondo = plan.get('fondo', '#121216')
    esc = plan['escenas']; col = plan.get('transicion_colores', {}); borde = col.get('borde', ['#FF4A3D', '#D6FF3F']); flash = col.get('flash', '#FFFFFF')
    for e in esc:
        if e.get('entrada', 'corte') not in SOLAPE: raise SystemExit(f'entrada desconocida en {e["id"]}: {e["entrada"]}')
        if not os.path.exists(os.path.join(P, 'compositions', 'frames', e['id'] + '.html')):
            print(f'  [aviso] falta compositions/frames/{e["id"]}.html (corre construir.py)')
    slots, seams, zi = [], '', ''
    for i, e in enumerate(esc):
        sig = esc[i + 1] if i + 1 < len(esc) else None
        d = round(float(e['fin']) - float(e['inicio']) + (SOLAPE[sig.get('entrada', 'corte')] if sig else 0), 3)
        slots.append(f'      <div id="f{i+1}" data-composition-id="{e["id"]}" data-composition-src="compositions/frames/{e["id"]}.html" '
                     f'data-start="{e["inicio"]}" data-duration="{d}" data-track-index="{1 + i % 2}" data-width="{W}" data-height="{H}"></div>')
        zi += f' #f{i+1} {{ z-index: {i+1} }}'
        if i: seams += f'  // --- f{i} → f{i+1} : {e.get("entrada", "corte")} en {e["inicio"]}\n' + seam(e.get('entrada', 'corte'), f'f{i}', f'f{i+1}', e['inicio'], W)
    audio = []
    m = plan.get('musica')
    if m and os.path.exists(os.path.join(P, m['archivo'])):
        dm = round(min(dur, dur_audio(os.path.join(P, m['archivo']))), 3)
        if dm < dur - 0.05: print(f'  [aviso] la música dura {dm} s y el video {dur} s: vuelve a correr musica.py con --duracion {dur}')
        audio.append(f'      <audio id="bgm" src="{m["archivo"]}" data-start="0" data-duration="{dm}" data-track-index="10" data-volume="{m.get("volumen", 0.7)}"></audio>')
    elif m: print(f'  [aviso] no existe {m["archivo"]}: el video sale SIN música (corre musica.py)')
    pistas = {}  # pista → segundo en que queda libre
    for n, c in enumerate(sorted(plan.get('sfx', []), key=lambda c: c[0])):
        t, nombre, vol = float(c[0]), c[1], float(c[2]) if len(c) > 2 else 0.5
        f = next((os.path.join('assets', 'sfx', nombre + ext) for ext in ('.mp3', '.wav') if os.path.exists(os.path.join(P, 'assets', 'sfx', nombre + ext))), None)
        if not f: print(f'  [aviso] no existe assets/sfx/{nombre}.mp3: cue en {t} omitido'); continue
        dd = round(min(dur_audio(os.path.join(P, f)), dur - t), 3)
        if dd <= 0: continue
        pista = next((p for p in sorted(pistas) if pistas[p] <= t), None) or (max(pistas) + 1 if pistas else 11)
        pistas[pista] = t + dd
        audio.append(f'      <audio id="sfx{n:02d}-{nombre}" src="{f.replace(os.sep, "/")}" data-start="{t}" data-duration="{dd}" data-track-index="{pista}" data-volume="{vol}"></audio>')
    html = f'''<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width={W}, height={H}">
    <title>{plan.get("titulo", "motion-ad")}</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      body {{ margin: 0; background: {fondo}; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: {fondo}; }}
      #root > div[data-composition-src] {{ position: absolute; inset: 0; transform-origin: 50% 50%; will-change: transform, opacity, filter; }}
     {zi}
      #flash {{ position: absolute; inset: 0; background: {flash}; opacity: 0; z-index: 40; pointer-events: none; }}
      #wipe-edge {{ position: absolute; top: 0; bottom: 0; left: 0; width: 60px; z-index: 39; opacity: 0; pointer-events: none;
                   background: linear-gradient(90deg, {borde[0]}00 0%, {borde[0]} 30%, {borde[0]} 50%, {borde[1]} 50%, {borde[1]} 70%, {borde[1]}00 100%); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-width="{W}" data-height="{H}" data-duration="{dur}">
      <!-- escenas (generado por ensamblar.py desde plan.json; no editar a mano) -->
{chr(10).join(slots)}

      <div id="wipe-edge"></div>
      <div id="flash"></div>

      <!-- audio: música + efectos -->
{chr(10).join(audio)}
    </div>
    <script>
      // Timeline raíz: SOLO las transiciones entre escenas. El movimiento de cada escena vive en su propio archivo.
      const tl = gsap.timeline({{ paused: true }});
{seams}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
    open(os.path.join(P, 'index.html'), 'w', encoding='utf-8').write(html)
    print(f'index.html: {len(esc)} escenas · {len(audio)} pistas de audio · {dur} s · {W}x{H}')

if __name__ == '__main__':
    main()
