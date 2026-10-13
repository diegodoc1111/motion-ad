# -*- coding: utf-8 -*-
"""
motion-ad · NUEVO — crea la carpeta de un anuncio nuevo a partir de la plantilla (o del ejemplo completo RÁFAGA).

    python nuevo.py <P> [--ejemplo] [--lienzo 1920x1080 | 1080x1920]

  <P>         carpeta del proyecto (se crea; si existe, solo se completa lo que falte sin pisar tus archivos)
  --ejemplo   copia el anuncio de ejemplo completo (8 escenas, tenis RÁFAGA) para estudiarlo o renderizarlo
  --lienzo    tamaño del video (por defecto 1920x1080; vertical: 1080x1920)
Deja: plan.json · diseno.json · frame.md · STORYBOARD.md · frames-src/ · assets/sfx/ · package.json · hyperframes.json
"""
import sys, os, shutil, json

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def copiar(src, dst):
    for raiz, dirs, archivos in os.walk(src):
        rel = os.path.relpath(raiz, src); destino = os.path.join(dst, rel) if rel != '.' else dst
        os.makedirs(destino, exist_ok=True)
        for a in archivos:
            d = os.path.join(destino, a)
            if not os.path.exists(d): shutil.copy2(os.path.join(raiz, a), d)

def main():
    if len(sys.argv) < 2 or sys.argv[1].startswith('--'): raise SystemExit(__doc__)
    P = os.path.abspath(sys.argv[1]); ejemplo = '--ejemplo' in sys.argv
    lienzo = sys.argv[sys.argv.index('--lienzo') + 1] if '--lienzo' in sys.argv else '1920x1080'
    W, H = [int(x) for x in lienzo.lower().split('x')]
    os.makedirs(P, exist_ok=True)
    copiar(os.path.join(SKILL, 'plantilla', 'ejemplo-rafaga' if ejemplo else 'proyecto'), P)
    copiar(os.path.join(SKILL, 'plantilla', 'base'), P)                       # package.json, hyperframes.json, CLAUDE.md, .gitignore
    os.makedirs(os.path.join(P, 'assets', 'sfx'), exist_ok=True); copiar(os.path.join(SKILL, 'recursos', 'sfx'), os.path.join(P, 'assets', 'sfx'))
    for d in ('assets/audio', 'compositions/frames', 'renders', 'snaps', '_work'): os.makedirs(os.path.join(P, d), exist_ok=True)
    meta = os.path.join(P, 'meta.json')
    if not os.path.exists(meta):
        json.dump({'id': os.path.basename(P), 'name': os.path.basename(P)}, open(meta, 'w', encoding='utf-8'))
    if not ejemplo:
        pj = os.path.join(P, 'plan.json'); plan = json.load(open(pj, encoding='utf-8'))
        plan['lienzo'] = [W, H]; json.dump(plan, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        dj = os.path.join(P, 'diseno.json'); dis = json.load(open(dj, encoding='utf-8'))
        dis['lienzo'] = [W, H]; json.dump(dis, open(dj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(os.path.join(P, '_work', 'skill.txt'), 'w', encoding='utf-8').write(SKILL)
    print('proyecto listo en', P)
    print('siguiente:', 'construir + ensamblar + check (el ejemplo ya trae todo; solo falta la música: musica.py)' if ejemplo
          else 'dibuja assets/producto.svg, completa diseno.json / frame.md / STORYBOARD.md y escribe las escenas en frames-src/')

if __name__ == '__main__':
    main()
