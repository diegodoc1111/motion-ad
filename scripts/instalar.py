# -*- coding: utf-8 -*-
"""
motion-ad · INSTALAR  (se corre UNA vez por computador; se puede repetir sin problema)

    python instalar.py [--verificar]

  --verificar : solo revisa qué hay y qué falta, sin descargar nada.

Revisa Python 3.10+, ffmpeg/ffprobe y Node.js 20+ (npx); deja listo HyperFrames (el que renderiza) con su
navegador, e instala las skills oficiales de HyperFrames que esta skill usa por debajo (hyperframes, general-video…).
No crea entornos de Python ni descarga modelos: los scripts solo usan la librería estándar + ffmpeg.
"""
import sys, os, shutil, subprocess, platform

HF = 'hyperframes@0.8.153'
WIN = platform.system() == 'Windows'; MAC = platform.system() == 'Darwin'
como = lambda win, mac, lin: win if WIN else (mac if MAC else lin)
ok, falta = [], []

def hay(exe): return shutil.which(exe) or (WIN and shutil.which(exe + '.cmd'))

def corre(cmd, timeout):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)

def main():
    VERIF = '--verificar' in sys.argv
    print('motion-ad · ' + ('verificación' if VERIF else 'instalación'))
    if sys.version_info < (3, 10): raise SystemExit('Necesitas Python 3.10 o más nuevo.')
    ok.append(f'Python {sys.version.split()[0]}')
    for exe, nombre, ayuda in (('ffmpeg', 'ffmpeg', como('scoop install ffmpeg  (o winget install Gyan.FFmpeg)', 'brew install ffmpeg', 'sudo apt install ffmpeg')),
                               ('ffprobe', 'ffprobe (viene con ffmpeg)', como('scoop install ffmpeg', 'brew install ffmpeg', 'sudo apt install ffmpeg')),
                               ('npx', 'Node.js 20+ (npx)', como('scoop install nodejs-lts  (o winget install OpenJS.NodeJS.LTS)', 'brew install node', 'https://nodejs.org'))):
        if hay(exe): ok.append(nombre)
        else: falta.append(f'{nombre}  ->  instálalo con:  {ayuda}')
    if hay('node'):
        v = corre('node --version', 30).stdout.strip()
        try:
            if int(v.lstrip('v').split('.')[0]) < 20: falta.append(f'Node.js {v} es viejo: necesitas 20 o más nuevo')
        except Exception: pass
    if hay('npx'):
        print('preparando HyperFrames (la primera vez descarga el paquete y su navegador: unos minutos)…', flush=True)
        try:
            v = corre(f'npx --yes {HF} --version', 600)
            nav = v if VERIF else corre(f'npx --yes {HF} browser ensure', 900)
            if v.returncode == 0 and nav.returncode == 0: ok.append('HyperFrames ' + (v.stdout.strip().splitlines() or ['?'])[-1])
            else: falta.append(f'HyperFrames no quedó listo. Corre a mano:  npx --yes {HF} browser ensure')
        except Exception as e:
            falta.append(f'HyperFrames ({e}). Corre a mano:  npx --yes {HF} browser ensure')
        skills = os.path.expanduser('~/.claude/skills')
        tiene = all(os.path.isdir(os.path.join(skills, s)) for s in ('hyperframes', 'hyperframes-core', 'general-video'))
        if tiene: ok.append('skills oficiales de HyperFrames (hyperframes, hyperframes-core, general-video)')
        elif VERIF: falta.append('skills oficiales de HyperFrames (corre instalar.py sin --verificar)')
        else:
            print('instalando las skills oficiales de HyperFrames en ~/.claude/skills…', flush=True)
            r = corre(f'npx --yes {HF} skills update general-video', 600)
            tiene = all(os.path.isdir(os.path.join(skills, s)) for s in ('hyperframes', 'hyperframes-core', 'general-video'))
            (ok if tiene else falta).append('skills oficiales de HyperFrames' + ('' if tiene else f'  ->  corre a mano:  npx --yes {HF} skills update general-video'))
    print('\n=========== RESULTADO ===========')
    for x in ok: print('  [ok]    ', x)
    for x in falta: print('  [FALTA] ', x)
    print('\nListo para usar. Abre una conversación nueva de Claude Code para que cargue las skills.' if not falta else '\nArregla lo que dice FALTA y vuelve a correr este instalador.')
    sys.exit(1 if falta else 0)

if __name__ == '__main__':
    main()
