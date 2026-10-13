# -*- coding: utf-8 -*-
"""
motion-ad · MÚSICA — detecta el tempo de la pista, la recorta para que un COMPÁS (downbeat) caiga en el
segundo 0 del video, normaliza el volumen, le pone un fade final y escribe la grilla de compases con la que
se cortan las escenas.

    python musica.py <pista.mp3> <P> [--duracion 15] [--desde 0] [--bpm 0] [--loudness -14] [--solo-analisis]

  <P>            carpeta del proyecto: deja  P/assets/audio/bgm.mp3  y  P/beats.json
  --duracion     largo del video (por defecto el "duracion" de P/plan.json; si no, 15)
  --desde        segundo de la pista antes del cual NO se usa nada (para saltar una intro floja);
                 el corte se hace en el primer compás después de ese segundo
  --bpm          fuerza el tempo cuando la detección se equivoca (lo normal es que se equivoque al doble o a la mitad)
  --solo-analisis  imprime tempo, compases y energía por compás, sin escribir nada

Solo necesita ffmpeg (nada de librerías de Python).
"""
import sys, os, json, math, subprocess
from array import array

HOP = 0.01  # segundos por cuadro de análisis (100 por segundo)

def arg(nombre, defecto=None):
    if nombre in sys.argv:
        i = sys.argv.index(nombre)
        return sys.argv[i + 1] if i + 1 < len(sys.argv) else defecto
    return defecto

def decodificar(pista):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', pista, '-ac', '1', '-ar', '8000', '-f', 's16le', '-'], capture_output=True)
    if r.returncode != 0: raise SystemExit('ffmpeg no pudo leer la pista: ' + r.stderr.decode(errors='replace'))
    a = array('h'); a.frombytes(r.stdout[: len(r.stdout) // 2 * 2]); return a

def envolvente(a, sr=8000):
    n = int(sr * HOP); env = []
    for i in range(0, len(a) - n, n):
        s = 0
        for v in a[i:i + n]: s += v * v
        env.append(math.sqrt(s / n) + 1.0)
    # "onset": cuánto SUBE el volumen de un cuadro al siguiente (solo subidas)
    on = [0.0] + [max(0.0, math.log(env[i]) - math.log(env[i - 1])) for i in range(1, len(env))]
    # suavizado corto
    return [sum(on[max(0, i - 1): i + 2]) / 3 for i in range(len(on))]

def tempo(on):
    """autocorrelación de los onsets entre 60 y 200 bpm, con preferencia suave por tempos entre 90 y 150"""
    n = len(on); mejor = (0, 0)
    lmin, lmax = int(60 / 200 / HOP), int(60 / 60 / HOP)
    puntajes = {}
    for lag in range(lmin, lmax + 1):
        s = 0.0
        for i in range(n - lag): s += on[i] * on[i + lag]
        bpm = 60 / (lag * HOP)
        peso = math.exp(-((bpm - 120) / 45) ** 2 / 2) * 0.6 + 0.4
        puntajes[lag] = s / (n - lag) * peso
        if puntajes[lag] > mejor[0]: mejor = (puntajes[lag], lag)
    lag = mejor[1]
    # afinar el lag con una parábola sobre los vecinos (precisión por debajo del cuadro)
    y0, y1, y2 = puntajes.get(lag - 1, 0), puntajes[lag], puntajes.get(lag + 1, 0)
    d = (y0 - y2) / (2 * (y0 - 2 * y1 + y2)) if (y0 - 2 * y1 + y2) != 0 else 0
    return 60 / ((lag + max(-0.5, min(0.5, d))) * HOP)

def afinar(on, T):
    """segunda pasada: prueba tempos a ±1.5 % del detectado y se queda con el que mejor encaja en los golpes
    (la autocorrelación sola deja un error de ~0.3 %, que al cabo de 15 s ya se nota)"""
    n = len(on); mejor = (0.0, T)
    for k in range(-60, 61):
        Tp = T * (1 + k * 0.00025); s_best = 0.0
        for ph_i in range(int(Tp / HOP)):
            s = 0.0; t = ph_i * HOP
            while t < n * HOP:
                s += on[int(t / HOP)]; t += Tp
            if s > s_best: s_best = s
        if s_best > mejor[0]: mejor = (s_best, Tp)
    return mejor[1]

def fase(on, T):
    """desplazamiento (0..T) donde mejor caen los golpes, y cuál de los 4 pulsos es el compás"""
    n = len(on); mejor = (0, 0.0)
    pasos = int(T / 0.005)
    for k in range(pasos):
        ph = k * 0.005; s = 0.0; t = ph
        while t < n * HOP:
            s += on[int(t / HOP)]; t += T
        if s > mejor[0]: mejor = (s, ph)
    ph = mejor[1]
    mejor_d = (0, 0)
    for d in range(4):
        s = 0.0; t = ph + d * T
        while t < n * HOP:
            s += on[int(t / HOP)]; t += 4 * T
        if s > mejor_d[0]: mejor_d = (s, d)
    return ph, mejor_d[1]

def main():
    if len(sys.argv) < 3 or sys.argv[1].startswith('--'): raise SystemExit(__doc__)
    pista, P = sys.argv[1], sys.argv[2]
    plan = os.path.join(P, 'plan.json')
    dur_plan = json.load(open(plan, encoding='utf-8')).get('duracion') if os.path.exists(plan) else None
    dur = float(arg('--duracion', dur_plan or 15))
    desde = float(arg('--desde', 0)); loud = float(arg('--loudness', -14)); bpm_forzado = float(arg('--bpm', 0))

    print('analizando', os.path.basename(pista), '…', flush=True)
    on = envolvente(decodificar(pista))
    T = 60 / bpm_forzado if bpm_forzado else afinar(on, 60 / tempo(on))
    bpm = 60 / T
    ph, d = fase(on, T)
    primer = ph + d * T                      # primer compás de la pista
    compases = []
    t = primer
    while t < len(on) * HOP - dur - 0.1:
        e = sum(on[int(t / HOP): int((t + 4 * T) / HOP)])
        compases.append((round(t, 3), round(e, 2))); t += 4 * T
    if not compases: raise SystemExit('La pista es más corta que el video. Usa otra o baja --duracion.')
    cands = [c for c in compases if c[0] >= desde] or compases[-1:]
    inicio = cands[0][0]
    print(f'tempo: {bpm:.1f} bpm · pulso {T:.4f} s · compás {4*T:.4f} s')
    print('compases de la pista (segundo → energía; más energía = más golpe):')
    print('  ' + '  '.join(f'{c[0]}→{c[1]}' for c in compases[:24]))
    print(f'corte elegido: {inicio} s de la pista cae en el segundo 0 del video' + (f' (--desde {desde})' if desde else ''))
    grilla = [round(i * 4 * T, 3) for i in range(int(dur / (4 * T)) + 1)]
    mitades = [round(i * 2 * T, 3) for i in range(int(dur / (2 * T)) + 1)]
    print('compases del VIDEO (corta las escenas aquí):', ' '.join(map(str, grilla)))
    print('medios compases (para escenas cortas):      ', ' '.join(map(str, mitades)))
    if '--solo-analisis' in sys.argv: return

    out = os.path.join(P, 'assets', 'audio', 'bgm.mp3'); os.makedirs(os.path.dirname(out), exist_ok=True)
    cola = 0.4
    r = subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', pista, '-ss', f'{inicio:.3f}', '-t', f'{dur + cola:.3f}',
                        '-af', f'loudnorm=I={loud}:TP=-1.5:LRA=11,afade=t=out:st={dur - 0.5:.3f}:d={0.5 + cola:.3f}',
                        '-ar', '48000', '-b:a', '192k', out])
    if r.returncode != 0: raise SystemExit('ffmpeg falló al recortar la pista.')
    json.dump({'pista': os.path.basename(pista), 'bpm': round(bpm, 2), 'pulso': round(T, 4), 'compas': round(4 * T, 4),
               'inicio_en_pista': inicio, 'duracion': dur, 'compases': grilla, 'medios': mitades,
               'pulsos': [round(i * T, 3) for i in range(int(dur / T) + 1)]},
              open(os.path.join(P, 'beats.json'), 'w', encoding='utf-8'), indent=1)
    print('listo:', out, 'y', os.path.join(P, 'beats.json'))
    print('Si el tempo salió al doble o a la mitad de lo que oyes, repite con --bpm <el correcto>.')

if __name__ == '__main__':
    main()
