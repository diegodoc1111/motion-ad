# -*- coding: utf-8 -*-
"""
motion-ad · VERIFICAR — revisa un render ANTES de decir "listo": formato, duración, volumen, y una hoja de
contacto con un cuadro cada N segundos para mirarla.

    python verificar.py <video.mp4> [--paso 0.5] [--columnas 8] [--ancho 480] [--salida snaps/hoja.jpg] [--esperado P]

  --esperado P   compara la duración con el "duracion" de P/plan.json
La hoja no lleva rótulos: el cuadro número n (contando desde 0, de izquierda a derecha y de arriba abajo)
corresponde al segundo n × paso.
"""
import sys, os, json, subprocess, math

def arg(nombre, defecto=None):
    if nombre in sys.argv:
        i = sys.argv.index(nombre); return sys.argv[i + 1] if i + 1 < len(sys.argv) else defecto
    return defecto

def main():
    if len(sys.argv) < 2: raise SystemExit(__doc__)
    v = sys.argv[1]
    if not os.path.exists(v): raise SystemExit('no existe ' + v)
    paso = float(arg('--paso', 0.5)); cols = int(arg('--columnas', 8)); ancho = int(arg('--ancho', 480))
    salida = arg('--salida', os.path.join(os.path.dirname(v) or '.', 'hoja-' + os.path.splitext(os.path.basename(v))[0] + '.jpg'))
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,pix_fmt',
                        '-of', 'json', v], capture_output=True, text=True)
    info = json.loads(r.stdout or '{}'); dur = float(info.get('format', {}).get('duration', 0))
    vid = next((s for s in info.get('streams', []) if s['codec_type'] == 'video'), None)
    aud = next((s for s in info.get('streams', []) if s['codec_type'] == 'audio'), None)
    fps = eval(vid['r_frame_rate']) if vid else 0
    print(f'video: {vid["width"]}x{vid["height"]} · {fps:.0f} fps · {vid["codec_name"]} {vid.get("pix_fmt", "")} · {dur:.3f} s' if vid else 'SIN VIDEO')
    print('audio:', (aud['codec_name'] if aud else 'SIN AUDIO (¿faltó la música o los cues?)'))
    if aud:
        r = subprocess.run(['ffmpeg', '-i', v, '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True)
        lineas = [l.split('] ')[-1] for l in r.stderr.splitlines() if 'mean_volume' in l or 'max_volume' in l]
        print('volumen:', ' · '.join(lineas))
        mv = next((float(l.split()[1]) for l in lineas if l.startswith('max_volume')), -99)
        if mv > -0.5: print('  [aviso] el pico está saturando: baja volúmenes en plan.json (música 0.6-0.75, efectos 0.4-0.6)')
    P = arg('--esperado')
    if P:
        esperada = float(json.load(open(os.path.join(P, 'plan.json'), encoding='utf-8'))['duracion'])
        print(f'duración esperada {esperada} s →', 'OK' if abs(esperada - dur) < 0.05 else f'DIFERENTE ({dur:.3f})')
    n = int(math.floor(dur / paso)); filas = max(1, math.ceil(n / cols))
    os.makedirs(os.path.dirname(salida) or '.', exist_ok=True)
    r = subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', v, '-vf', f'fps=1/{paso},scale={ancho}:-2,tile={cols}x{filas}', '-frames:v', '1', '-q:v', '3', salida])
    if r.returncode == 0: print(f'hoja: {salida}  ({n} cuadros, uno cada {paso} s, {cols} por fila: el cuadro n es el segundo n×{paso}; las celdas negras del final son relleno)')
    else: print('[aviso] no se pudo hacer la hoja de contacto')
    print('Mírala: ¿el último cuadro parece producto real (no dibujo)? ¿nada se monta ni se corta? ¿cada escena tiene algo nuevo?')

if __name__ == '__main__':
    main()
