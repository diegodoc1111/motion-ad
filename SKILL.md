---
name: motion-ad
description: >-
  Crea un ANUNCIO ANIMADO de producto hecho 100 % con código (HyperFrames + GSAP), sin presentador ni narración:
  el producto dibujado por partes que se desarma, cambia de color, cae, corre y se revela, con tipografía de
  póster, cifras gigantes, etiquetas técnicas, cortes al compás de la música y efectos de sonido en cada golpe.
  Entrega un MP4 1920×1080 (o 1080×1920) de 10-30 s con aspecto de showreel de estudio. Úsala cuando pidan
  "un anuncio animado de mi producto", "motion graphics de 15 segundos", "un showreel", "como el anuncio de los
  tenis", "un anuncio sin que yo aparezca", o invoquen /motion-ad. NO es para animar a una persona hablando
  (eso es reel-motion), NI para editar un video grabado (video-ad-editing), NI para explicadores narrados con
  voz de IA (video-explainer / anuncios-animados).
---

# motion-ad — el anuncio animado de producto, hecho con código

**Qué entrega:** un MP4 de 10-30 s donde TODO es diseño animado: un producto vectorial propio (dibujado por
partes y recoloreable), 6-9 escenas que cada una luce una técnica distinta de motion graphics, cortes en los
compases de la música, 40-60 efectos de sonido sincronizados y un cuadro final de catálogo. Se ve como un
showreel de un estudio, no como una plantilla.

**Cuál skill de video usar** (no confundirlas):

| Skill | El presentador | Úsala cuando |
|---|---|---|
| **motion-ad** (esta) | **No hay** persona ni voz | "anuncio animado de mi producto", "showreel", "motion graphics de N segundos" |
| reel-motion | Grabado y **recortado** dentro de un diseño | "anímalo", "ponme recortado sobre color" |
| video-ad-editing | Grabado, a pantalla completa | "edítame este video": zooms, b-roll, subtítulos |
| video-explainer / anuncios-animados | No hay, pero SÍ hay voz de IA y guion | explicadores narrados estilo documental |
| hyperframes (oficial) | — | el motor que renderiza; dudas de bajo nivel (`/hyperframes-core`, `/hyperframes-animation`, `/hyperframes-keyframes`) |

**Entrada que necesita:** un brief de producto (qué es, marca, colores, 3-4 datos, un lema). Opcional: una foto
del producto para dibujarlo parecido, una pista de música y un video de referencia (para medir calidad, NUNCA
para copiar sus escenas).

Rutas en este documento: `SKILL` = la carpeta de esta skill. `P` = la carpeta del proyecto del anuncio.
`PY` = tu Python 3.10+ (Windows: `python -X utf8`; Mac/Linux: `python3`). Rutas con espacios SIEMPRE entre comillas.

---

## 0. Instalación (una sola vez por computador)

```bash
PY "SKILL/scripts/instalar.py"
```

(`--verificar` solo revisa.) Comprueba Python 3.10+, ffmpeg y Node.js 20+, deja listo HyperFrames con su
navegador e instala las skills oficiales de HyperFrames (`hyperframes`, `hyperframes-core`, `general-video`, …)
en `~/.claude/skills`. Si algo dice `[FALTA]`, instálalo con el comando que imprime y vuelve a correrlo hasta
que diga "Listo para usar"; luego abre una conversación nueva. No hace falta ningún entorno de Python: los
scripts usan solo la librería estándar + ffmpeg. Las fuentes de Google Fonts se descargan solas en el primer
render (necesita internet esa primera vez).

## 1. Qué preguntarle al usuario (una sola ronda, solo lo que falte)

1. **El producto**: qué es y cómo se ve (foto o referencia si tiene). Si no hay marca real, inventa una ficticia
   (nombre corto + modelo tipo "RF-27") y dilo.
2. **Colores**: el de la marca (será EL acento) y 2-3 variantes/colorways del producto.
3. **3-4 datos cortos** que presumir (peso, %, cifra, precio, material) y **un lema** de 2-3 palabras.
4. **Duración y formato**: 15 s y 1920×1080 por defecto (va incrustado en un reel); 1080×1920 si se publica solo.
5. **Música**: la skill NO trae música (derechos). Pide una pista libre de derechos (Pixabay Music) o la ruta de
   una que ya tenga. Sin pista, el anuncio sale con efectos y se avisa. Nunca descargues música por tu cuenta.
6. **CTA / cierre**: ¿qué debe quedar en el último cuadro? (marca + modelo + dato, una web, un precio).

No preguntes nada técnico: técnicas, escenas, tipografía, tiempos y sonidos los decides tú.

## 2. Flujo de trabajo

### 2.1 Crear el proyecto

```bash
PY "SKILL/scripts/nuevo.py" "<P>" [--lienzo 1920x1080 | 1080x1920]
PY "SKILL/scripts/nuevo.py" "<P>" --ejemplo        # el anuncio completo de ejemplo (RÁFAGA, 8 escenas) para estudiar o probar
```

Deja `plan.json` (escenas, transiciones, música, cues), `diseno.json` (marca, lienzo, colorways, tonos del kit),
`frame.md` y `STORYBOARD.md` (plantillas para llenar), `frames-src/` (dos escenas de muestra: gancho y cierre),
`assets/sfx/` (la biblioteca de efectos), `assets/producto.svg` (una botella de muestra que vas a reemplazar).
Todos los comandos de HyperFrames se corren DENTRO de `P`. Lee `frame.md` y `STORYBOARD.md` del ejemplo
(`SKILL/plantilla/ejemplo-rafaga/`) una vez: son el nivel de detalle que se espera.

### 2.2 Dibujar el producto (`assets/producto.svg`)

El producto es un **SVG propio por partes**, el mismo dibujo en todas las escenas. Contrato (míralo en
`SKILL/plantilla/ejemplo-rafaga/assets/producto.svg`, un tenis de 41 KB):

- `viewBox` con la proporción real del producto; vista lateral o frontal clara; "la nariz" apunta a la DERECHA.
- Un `<g id="g-parte">` por parte, **de atrás hacia adelante** (suela → cuerpo → tapa → etiqueta → logo…). `construir.py`
  los convierte en `data-part="parte"` para prender/apagar partes en una escena (explosión, anatomía).
- Rellenos con variables: `fill="var(--c-cuerpo)"` etc. (los nombres los defines tú y los repites en
  `diseno.json → colorways`); trazo `var(--c-ink)` de 7 px con `stroke-linejoin:round`, clase `ln`.
- Sombras internas clase `shade` (`var(--c-shade)`), brillos clase `hi` (`var(--c-hi)`), costuras y detalles
  finos clase `st` (`var(--c-stitch)`). Con `.wire` se apagan y queda el boceto en línea.
- **Nivel de detalle = producto real**: paneles, costuras, perforaciones, halftone, texturas, relieve. Un dibujo
  plano de seis trazos se ve "caricatura" (fue el veredicto de un juez independiente en la primera versión del
  ejemplo). Si hay foto, dibújalo a partir de ella; nunca incrustes la foto salvo que el usuario lo pida.
- Colorways en `diseno.json`: la base (la de la marca), 1-2 variantes, y siempre `wire` (líneas en acento) y
  `wire-ink` (líneas en tinta) con todos los rellenos en `none`.

Para verlo: pon el producto grande en la escena `f01` (`{{PRODUCTO|base|1300|f01-prod}}`), corre 2.6 + 2.7 y
`npx hyperframes snapshot . --at 0.9 --no-end -o snaps`. Itera 2-3 veces hasta que parezca el producto. Si quieres
comparar variantes, dibuja 2-3 candidatos (`producto-1.svg`, `-2`, `-3`), mira sus capturas y elige uno.

### 2.3 Música y grilla

```bash
PY "SKILL/scripts/musica.py" "<pista.mp3>" "<P>" [--duracion 15] [--desde 8] [--bpm 128]
```

Detecta el tempo, recorta la pista para que un **compás caiga exacto en el segundo 0**, normaliza (−14 LUFS),
pone un fade final y escribe `beats.json` + `assets/audio/bgm.mp3`. Imprime los compases de la pista con su
energía (usa `--desde` para arrancar donde entra el golpe y saltar la intro) y **los compases del video**: ahí
van los cortes de escena. Si el tempo salió al doble o a la mitad de lo que se oye, repite con `--bpm`.
Sin música: pon `"musica": null` en `plan.json` y usa una grilla de 2.0 s.

### 2.4 Diseño y guion (antes de escribir código)

1. **`frame.md`**: el mundo del anuncio (laboratorio, taller, pista, cocina de autor…), DOS fondos que alternan
   (uno oscuro, uno claro), UN acento (el color de la marca) y un color de impacto racionado a 2-3 golpes.
   Tipografías por defecto: Archivo Black (titulares), League Gothic (toda cifra), Space Mono 700 (etiquetas).
2. **`STORYBOARD.md`**: 6-9 escenas para 15 s. Las hero de 1 compás (~2 s), las de golpe de medio compás. Cada
   escena: una técnica DISTINTA del catálogo (§3), qué domina el cuadro, qué entra en la segunda mitad, sus cues
   de sonido, y cómo "sale" (la transición es la salida). Arco probado: gancho (revelado) → anatomía →
   impacto → variantes → cifra héroe → prueba/laboratorio → lockup → cierre.
3. **Columna vertebral**: un elemento que abre, atraviesa y cierra el video (en el ejemplo: la línea de meta y el
   cronómetro). Da unidad.
4. **El último cuadro es producto de catálogo**: producto completo, sombra real, etiqueta (marca, modelo, datos),
   NADA moviéndose en los últimos ~0.45 s. Es lo que la gente recuerda; un cierre "animado" se percibe barato.
5. Nunca copies las escenas de una referencia: toma su nivel de calidad, no sus ideas.

### 2.5 Escribir las escenas (`frames-src/fNN-nombre.html`)

Una escena = un archivo. Copia la estructura de `f01-gancho.html` / `f02-cierre.html` (o de cualquier escena
del ejemplo) y respeta:

- `<template>` con `<style>` (incluye `/*COMMON*/`), el `<div id="root" data-composition-id="fNN-nombre">`
  (el id = nombre del archivo = `id` en `plan.json`), el clip de fondo
  `<div id="fNN-bg" class="clip" data-start="0" data-duration="{{DUR}}">`, `{{KIT|fNN|NN|NOMBRE|tono}}`, los
  elementos, y el `<script>` con `/*KITJS*/`, `const tl = gsap.timeline({ paused: true }); kit(tl, "fNN", {{DUR}});`
  y al final `window.__timelines["fNN-nombre"] = tl;`.
- Todos los ids de la escena con prefijo `fNN-` (ids únicos en todo el proyecto; **nunca empiezan por dígito**).
- El producto: `{{PRODUCTO|colorway|ancho_px|fNN-id|clases}}`; su posición va en CSS (`#fNN-id{left:…;top:…}`).
  Para mostrar solo una parte: `#fNN-x svg > g:not([data-part="suela"]){display:none}`. Para el boceto: colorway `wire`.
- Movimiento solo con `fromTo` sobre `x y scale rotation opacity clipPath xPercent yPercent rotateX/Y z`
  (nunca `top/left/width/height`); sin transiciones CSS; nada aleatorio ni dependiente del reloj.
- Segundo tween sobre la misma propiedad → `immediateRender: false`. Partículas y cosas que aparecen después:
  `opacity: 0` en t ≤ 0.
- Tiempos en pulsos de `beats.json` (`const B = 0.5217`): los golpes caen en `k * B`, las entradas terminan en un pulso.
- Decorativos: `{{KIT}}` (registro, slate, "SC NN / total", número fantasma, puntos, grano) + 2-4 ambientales
  moviéndose + chips (`.chip`), cotas (`.cota`), sombra (`.shadow`). Cuadros "vacíos" = amateur.
- Mecánicas de bloques del registro (split-flap, number-wheel, logo-sting…): `npx hyperframes add <bloque>` para
  LEER cómo lo hacen y copiar la mecánica en tu escena; no los montes tal cual.

### 2.6 Plan, construcción y ensamble

`plan.json`: `duracion`, `lienzo`, `musica`, `escenas` (`id`, `inicio`, `fin` en la grilla, `entrada` = cómo
entra ESA escena: `corte` · `zoom` · `barrido` · `cromatico` · `flash`) y `sfx` (`[segundo, nombre, volumen]`).
Regla de dirección: todo viaja a la IZQUIERDA. Máximo 2 transiciones "grandes" (cromatico/flash) por video.

```bash
PY "SKILL/scripts/construir.py" "<P>"     # frames-src → compositions/frames (inyecta producto, kit y {{DUR}})
PY "SKILL/scripts/ensamblar.py" "<P>"     # plan.json → index.html (slots con solape, transiciones, música, cues)
```

**Cues de sonido** (biblioteca en `assets/sfx/`): `whoosh-short` / `whoosh` / `whoosh-cinematic` (barridos,
entradas, zooms) · `pop` (algo aparece) · `click` / `click-soft` (etiquetas, chips) · `key-press` (cascadas de
letras, 0.06 s entre sí) · `impact-bass-1/2` + `thump` (slams, caídas, cifras) · `glitch-1/2` (bursts) · `chime`
/ `sparkle` / `ping` (revelación, cierre). Un cue por evento visual; impacto en los compases; volúmenes 0.4-0.6
(bajos 0.7-0.9); música 0.65-0.75. `ensamblar.py` reparte pistas para que no se pisen.

### 2.7 Revisar ANTES de mostrar (obligatorio)

```bash
npx hyperframes check                                                   # 0 errores (avisos normales: composition_file_too_large y el contraste del número fantasma .kit-ghost)
npx hyperframes snapshot . --at <mitad de cada escena>,<último cuadro de cada escena> --no-end --timeout 120000 -o snaps
```

Abre `snaps/contact-sheet.jpg` y **mírala**. Lista de control: nada se monta sobre otra cosa ni se corta por un
borde · cada escena tiene su héroe y algo nuevo en la segunda mitad · cifras en League Gothic gigantes · un solo
acento por cuadro · el producto parece el producto · el último cuadro es de catálogo y está quieto · tildes y
ortografía. Para que el usuario vea en vivo: `npx hyperframes preview --background` (abre
`http://127.0.0.1:<puerto>/#project/<carpeta>`); **detenlo con `npx hyperframes preview --stop` antes de editar
`frames-src/`** (el preview reescribe atributos en TODOS los .html del proyecto).

### 2.8 Borrador para aprobación

```bash
npx hyperframes render --quality draft --fps 30 --output renders/borrador.mp4
PY "SKILL/scripts/verificar.py" renders/borrador.mp4 --esperado "<P>" --paso 0.5
```

`verificar.py` imprime formato, duración, volumen y deja `renders/hoja-borrador.jpg` (un cuadro cada 0.5 s):
míralo. Entrega el borrador y ajusta lo que pida. **No exportes el final sin el OK del usuario.**

### 2.9 Final

```bash
npx hyperframes render --fps 60 --quality high --crf 16 --sdr --video-frame-format png --workers 2 --output renders/<nombre>-FINAL.mp4
PY "SKILL/scripts/verificar.py" renders/<nombre>-FINAL.mp4 --esperado "<P>" --paso 1
```

(Si el render se queda sin memoria: `NODE_OPTIONS=--max-old-space-size=8192`.) Verifica antes de decir "listo":
resolución, 60 fps, duración exacta, audio presente, pico bajo −1 dB, y la hoja final mirada.

### 2.10 Juez independiente (opcional; obligatorio si hay un video de referencia)

Lanza UN agente sin contexto con: *"Mira estos dos videos (hojas de cuadros A y B). Como director de arte
independiente: ¿cuál se ve más profesional y por qué? ¿El producto de B parece producto real o dibujo animado?
¿Qué 3 cosas concretas le faltan a B para estar al nivel de A? Solo diagnóstico."* Si el veredicto es
"caricatura" o "cuadros vacíos", la cura es: más detalle en el SVG (paneles, costuras, texturas), más densidad
(kit + chips + cotas + fondos con grilla/color por escena) y un cierre de catálogo.

---

## 3. Catálogo de técnicas (una distinta por escena; el ejemplo muestra cómo se hace cada una)

| Técnica | Qué se ve | Dónde verla | SFX |
|---|---|---|---|
| Revelado slit-scan | una línea barre y "revela" el producto, con 3 ecos estirados que se contraen | ejemplo f01 | whoosh-short + clicks |
| Cronómetro vivo | cifra League Gothic que cuenta tiempo real y crece 1→1.06 | f01 / f08 | chime al parar |
| Boceto que se dibuja | copia `wire` del producto, trazos que se dibujan (`strokeDashoffset`) | f01 | pop |
| Anatomía 3D | partes del producto esparcidas en profundidad (`translateZ`, `rotateX/Y`) que se ensamblan con vuelo de cámara | f02 | pops por pieza |
| Líneas guía + etiquetas | leader lines que se dibujan y etiquetas que llegan en cascada | f02 | pop |
| Slam tipográfico | palabra de 330 px entra de escala 2.4 → 1 con `expo.out` + sacudida de 3 cuadros | f03 | impact-bass |
| Caída con squash | el producto cae (`power4.in`), aplasta (scaleY .82) y rebota (`back.out(2)`) | f03 | thump + impact |
| Partículas balísticas | 24 esquirlas con gravedad desde el punto de contacto | f03 | — |
| Tablero split-flap | letras que giran en celdas (`steps()`), cambian en los compases | f04 | key-press ×6 + pop |
| Cambio de colorway por bandas | copias apiladas del producto reveladas con `clip-path` en 7 bandas (`steps(7)`) | f04 | pop |
| Rueda de números | dígitos en tiras verticales enmascaradas (01/03 → 03/03) | f04 | click |
| Túnel de velocidad | 18 rectángulos en Z + rayos desde el punto de fuga + barras de velocidad | f05 | whoosh-cinematic |
| Estela / ecos | el producto entra desde lejos con 3 copias desplazadas que se contraen | f05 | whoosh-short |
| Cifra contadora héroe | 0 → 275 en 460 px con golpe de escala en el compás | f05 | thump + impact |
| Presión y anillos | el producto presiona (scaleY .94) y anillos concéntricos "respiran" bajo él | f06 | impact + pops |
| Barras de dato | barras con relleno `scaleX` y su cifra contando al lado | f06 | pop |
| Sello de caucho | caja girada −8° que entra 1.6 → 1 con sacudida de 2 cuadros | f06 | thump |
| Inset macro | ventana con el producto ×2 recorriendo un detalle | f06 | click |
| Lockup con flash | wordmark slam + anillo + UN cuadro blanco + copias glitch en 2 colores | f07 | impact + glitch |
| Volteo 3D | el producto entra con `rotateY −80 → 0` y `translateZ` | f07 | whoosh |
| Cascada de palabras | lema palabra por palabra desde abajo (`waterfall`) y meta con tracking por glifo | f07 | pop ×3 |
| Cierre de catálogo | barrido que convierte el boceto en producto terminado + etiqueta con código de barras + nada se mueve | f08 | whoosh-short + chime |

Transiciones (en `plan.json`): `zoom` (zoom-through con blur), `barrido` (whip pan a la izquierda), `cromatico`
(barrido con borde bicolor y flash de 1 cuadro), `flash` (corte bajo blanco), `corte` (seco, en el compás).

## 4. Reglas de diseño (lo que hace que se vea de estudio)

1. **Densidad**: kit en toda escena + chips/cotas/sombra + fondo con grilla o color por escena (ink, papel, teal,
   violeta, coral…). Dos escenas seguidas no comparten fondo.
2. **Un acento por cuadro**; el color de impacto en máximo 3 escenas; nunca gradientes cian/morado ni halos.
3. **Escala**: héroe ≥ 55 % del ancho; palabras héroe 260-360 px; cifras 420-560 px; etiquetas 22-28 px; líneas ≥ 3 px.
4. **Ritmo**: cortes en compases, golpes en pulsos; primer movimiento antes de 0.2 s; algo nuevo en la segunda
   mitad de cada escena; cada escena una técnica distinta; eases variados (elastic UNA vez en todo el video).
5. **Dirección**: todo viaja a la izquierda (barridos, cámaras, estelas).
6. **Sonido**: un cue por evento; impactos en los compases; nunca más de 2 cues por pulso; la música por debajo.
7. **Cierre de catálogo**: último cuadro quieto con producto + etiqueta; el pico de la música cae antes.
8. **Prueba de entrecerrar los ojos** en cada captura: un héroe, chrome de apoyo, acento inconfundible.

## 5. Reglas técnicas y errores comunes

- `construir.py` y `ensamblar.py` GENERAN `compositions/frames/` e `index.html`: nunca los edites a mano; edita
  `frames-src/`, `plan.json` y `diseno.json` y vuelve a correrlos.
- El preview de Studio reescribe `data-hf-id` y normaliza atributos en todos los .html: `preview --stop` antes de
  editar; `construir.py` limpia los `data-hf-id` de `frames-src`.
- Lint: ids no pueden empezar por dígito · `letterSpacing` no se anima (reparte los glifos en `<span>` y anima `x`)
  · texto `color: transparent` + text-stroke falla `text_not_painted` (usa un relleno rgba tenue) · contraste
  WCAG 3:1 en texto (chrome sobre ink `#A9A79F`, sobre papel `#6E6A63`; decorativos grandes como el número
  fantasma dan aviso, no error) · dos tweens sobre la misma propiedad en el mismo instante = error (usa
  `immediateRender:false` y tiempos distintos) · `transform` en CSS + GSAP sobre el mismo elemento = conflicto
  (pon la posición base con `left/top` y deja los transforms a GSAP).
- Sangrados a propósito (algo que sale del cuadro): `data-layout-allow-overflow`; capas intencionales encima de
  texto decorativo: `data-layout-allow-occlusion`.
- El aviso `composition_file_too_large` es normal (el SVG del producto va inline en cada escena).
- `snapshot` se queda sin tiempo → `--timeout 120000` y menos segundos por llamada.
- Formato 1080×1920: `nuevo.py --lienzo 1080x1920`; el kit se adapta solo; reparte el cuadro en vertical
  (producto abajo, titular arriba) y sube tamaños de texto un 15 %.
- No lances agentes en paralelo para escribir escenas: cuestan más tokens que escribirlas tú y pierden el
  contexto del diseño. Un juez independiente (2.10) sí vale la pena.
- Windows: `python -X utf8`; archivos guardados en UTF-8; parches grandes en un `.py`, no en heredocs.

## 6. Qué entregar

1. El borrador (`renders/borrador.mp4`) y, tras el OK, el final (`renders/<nombre>-FINAL.mp4`) verificado con
   `verificar.py` y con su hoja mirada.
2. Dos líneas: qué técnica luce cada escena y qué puede cambiar el usuario (colores, datos, lema, música, duración).
3. Nunca publiques ni subas nada por tu cuenta: publicar es decisión del usuario.

Créditos y licencias: ver `README.md`.
