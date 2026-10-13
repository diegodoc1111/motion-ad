---
workflow: general-video
flow: automation
storyboard: no
message: "Un solo prompt y Claude entrega un anuncio de tenis con motion graphics de estudio: hecho para impresionar."
destination: instagram-reel-insert
aspect: 1920x1080
language: es
audience: "seguidores de @soydiegoosorio (marketers y dueños de negocio) que verán el anuncio incrustado en un reel"
length: 15s
angle: showreel
narration: no
---

## Intent

El prompt original (de un tutorial que Diego va a recrear en un reel):

> Make a dynamic 15-second motion graphics video of a sneaker ad that shows what an incredible motion graphic
> designer you are, like it's your showreel for a résumé. Go all out. Use not so common but high quality motion graphics.

Es un **showreel**: cada escena debe lucir una técnica distinta de motion graphics, poco común y de alta
calidad, alrededor de un tenis de una marca ficticia propia (nada de KYVO / KV-94, que es el ejemplo de otra
creadora). Sin narración; con música y efectos de sonido sincronizados ("hasta con el sonido").

Uso final: Diego lo monta debajo de su cara en un reel vertical donde dice que creó este anuncio con un solo
prompt en Claude (Fable 5.1), por eso el video tiene que ser 100 % original y sostener esa frase.

## Assets

- Ninguno del usuario. Tenis: ilustración vectorial propia (SVG por partes) creada en este proyecto.
- Música: una pista royalty-free de `Editor Videos/_music` (Pixabay), adoptada en `assets/`.
- Efectos: biblioteca incluida de media-use (`assets/sfx/`) + `Editor Videos/_sfx`.

## Customizations

- Cortes y golpes de cámara alineados al tempo de la música.
- 1–2 transiciones shader (glitch / chromatic split) en los momentos hero; el resto CSS.
- Marca ficticia con nombre y modelo propios; textos cortos, en español o neutros.

## Notes

- Decisiones tomadas en modo autónomo (señal "un solo prompt → MP4"): sin storyboard de revisión, una
  vista previa + render de borrador para Diego, export final 1080p60 solo con su OK.
- Evitar: gradientes cian/morado genéricos, texto con gradiente, tarjetas idénticas, todo centrado.
