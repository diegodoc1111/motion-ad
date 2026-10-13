---
format: 1920x1080
duration: 15s
message: "MARCA MODELO: (la promesa en una frase) — y cada escena demuestra una técnica distinta de motion graphics"
arc: Gancho → Anatomía → Impacto → Variantes → Dato héroe → Prueba → Lockup → Cierre
music: "(pista) — (bpm) bpm, pulso (s), compás (s); el corte de musica.py pone un compás en t=0"
---

## Decisions

- **Columna vertebral:** un elemento que abre el video, lo atraviesa y lo cierra (en RÁFAGA: la línea de meta y el cronómetro).
- **Héroe:** `assets/producto.svg` — un solo dibujo vectorial, partes por `data-part`, recoloreado por variables CSS.
- **Grilla:** (bpm). Compases del video (de beats.json): 0.000 · … Cada corte cae en un compás o medio compás; cada golpe en un pulso.
- **Costuras:** una sola dirección (todo viaja a la IZQUIERDA). Tipos: corte · zoom · barrido · cromatico · flash (plan.json).
- **Audio:** música + cues de SFX por escena (lista `sfx:` abajo; van a plan.json). Sin narración.
- **Cuadro final sostenido:** la última escena deja ~0.45 s sin movimiento, con el producto de catálogo y su etiqueta.
- **Prohibido:** gradientes cian/morado, halos, tarjetas redondeadas, texto bajo 22px, líneas de 1px, marcas reales, salidas en escenas no finales.

## Frame 1 — Gancho

- scene: (qué pasa en una frase)
- duration: 2.087s
- transition_in: corte
- src: compositions/frames/f01-gancho.html
- técnica: (la técnica de motion que luce esta escena; ver catálogo §3 de la skill)
- focal: (qué domina el cuadro)
- sfx: 0.00 whoosh-short · 0.522 pop · 1.043 click
- assets: assets/producto.svg (colorway base)

Scene 1 (0.00–0.50s): (fondo, chrome, qué entra primero y cómo — ease, duración, desde dónde).
Scene 2 (0.50–1.50s): (el héroe: entrada, golpe, reacción).
Scene 3 (1.50–2.087s): (lo que llega en la segunda mitad; vector de salida para la transición).

## Frame 2 — Cierre

- scene: la línea barre y revela el producto terminado; entra la etiqueta de producto; todo se detiene
- duration: 2.087s
- transition_in: zoom
- src: compositions/frames/f02-cierre.html
- técnica: revelado por barrido (boceto → producto) + etiqueta de catálogo
- focal: el producto completo, quieto, con su etiqueta
- sfx: 0.00 whoosh · 0.40 chime · 0.52 pop
- assets: assets/producto.svg (wire-ink + base)

Scene 1 (0.00–0.40s): la línea entra por la derecha y barre hasta x=200; delante queda el boceto, detrás el producto.
Scene 2 (0.18–0.60s): la etiqueta (marca, modelo, 3 datos) se desliza desde la derecha con sombra dura.
Scene 3 (0.60–fin): NADA se mueve. Cuadro de catálogo.
