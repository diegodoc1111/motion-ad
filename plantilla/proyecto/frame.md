---
version: 1
name: MARCA — Frame (anuncio animado, 1920×1080)
description: >
  La verdad de diseño de este anuncio: mundo, paleta, tipografía, componentes y reglas de movimiento.
  Todo lo que se dibuje en una escena sale de aquí. (Reemplaza MARCA / MODELO y ajusta colores y mundo.)
unit: el cuadro — 1920×1080
principle: un acento por cuadro · los números siempre en League Gothic · toda etiqueta en mono mayúscula

colors:
  ink: "#121216"        # casi negro, frío — fondo "laboratorio"
  paper: "#F3EFE4"      # blanco cálido — fondo "impreso"
  acento: "#D6FF3F"     # EL acento (uno solo; pon aquí el color de la marca si lo tiene)
  impacto: "#FF4A3D"    # segundo registro, racionado: golpes, sellos, un colorway
  graphite: "#2A2A31"   # superficies oscuras
  smoke: "#8E8C86"      # texto secundario sobre ink, reglas sobre paper
  white: "#FFFFFF"      # solo brillos y el flash

typography:
  display:   { fontFamily: "Archivo Black", weight: 400, upper: true, tracking: "-0.02em", lineHeight: 0.9 }
  numeral:   { fontFamily: "League Gothic", weight: 400, upper: true, tracking: "0.01em", lineHeight: 0.85 }
  chrome:    { fontFamily: "Space Mono", weight: 700, upper: true, tracking: "0.16em", size: "22-28px" }
  hero-word: { fontFamily: "Archivo Black", px: 260-360 }
  title:     { fontFamily: "Archivo Black", px: 120-180 }
  stat-big:  { fontFamily: "League Gothic", px: 420-560 }
  label:     { fontFamily: "Space Mono", px: 22-28, color: "smoke" }

spacing: { pad-frame: "72px", gutter: "40px", rule: "3px" }

components:
  ink-ground:   { background: "{colors.ink}",   texture: "grilla de carriles 1px rgba(243,239,228,.06) cada 120px" }
  paper-ground: { background: "{colors.paper}", texture: "grilla 60px rgba(18,18,22,.07) + grano del kit" }
  producto:
    source: "assets/producto.svg — se inyecta con {{PRODUCTO|colorway|ancho|id}}; partes direccionables por data-part"
    colorways: "ver diseno.json → colorways"
    description: "La estrella. Vista lateral/frontal clara. Trazos en ink. Nunca estirar salvo en un squash deliberado."
  stat-block:  { typography: "{typography.stat-big} + {typography.label} arriba", description: "cifra gigante con su etiqueta mono" }
  chip:        { border: "3px solid currentColor", padding: "8px 14px", typography: "{typography.chrome}", description: "etiqueta en caja, esquinas rectas" }
  leader-line: { stroke: "3px acento (sobre ink) / ink (sobre paper)", end: "punto de 14px sobre la parte, etiqueta al otro extremo" }
  stamp:       { border: "6px solid {colors.impacto}", typography: "chrome 34px impacto", transform: "rotate(-8deg)", description: "sello de caucho: entra con presión 1.6 → 1 y 2 cuadros de sacudida" }
  progress-strip: { size: "6px abajo", color: "{colors.acento}", description: "tira de tiempo que crece con el video" }
---

# MARCA — Frame

## El mundo
(Describe en 5 líneas el universo del anuncio: ¿laboratorio? ¿taller? ¿pista? ¿cocina de autor? Dos fondos que
alternan — uno oscuro y uno claro — y UN acento que manda en todos los cuadros. Un segundo color racionado a 2-3 golpes.)

## El cuadro
- Lienzo 1920×1080; el contenido vive dentro de 72px de margen; el héroe puede sangrar por UN borde a propósito.
- Se va a ver dentro de un celular (~720px de ancho): nada de texto bajo 22px, líneas bajo 3px ni decorativos bajo 12 % de opacidad.
- Prueba de entrecerrar los ojos: un solo héroe domina (el producto o una palabra/cifra), el chrome apoya, el acento se nota.
- Anclar a los bordes y partir el cuadro (cifra izquierda / producto derecha). Centrado y flotando solo en el lockup final.

## Movimiento (reglas para todas las escenas)
- Cortes y golpes en la grilla de la música (`beats.json`). Entradas con `fromTo`; eases variados (expo.out para slams,
  back.out(1.6) para pops, power3.out para deslizamientos, elastic UNA sola vez en todo el video). Nunca salidas: la
  transición es la salida (salvo la última escena).
- Cada escena tiene 2-4 decorativos ambientales moviéndose (grilla que deriva, tira que crece, número fantasma, anillos).
- El primer movimiento visible antes de 0.2 s; algo nuevo llega en la segunda mitad de cada escena.
- El ÚLTIMO cuadro del video es producto de catálogo: todo quieto, el producto completo, su etiqueta. Es lo que la gente recuerda.

## Prohibido
Gradientes cian/morado · halos de brillo · tarjetas redondeadas · texto centrado flotando · más de un acento por cuadro ·
etiquetas diminutas · marcas reales ajenas · copiar escenas de una referencia tal cual.
