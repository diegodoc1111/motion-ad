# Proyecto de anuncio animado (skill motion-ad)

Este proyecto se arma con la skill **motion-ad** (`~/.claude/skills/motion-ad/SKILL.md`): léela antes de tocar nada.
Flujo corto: `frames-src/*.html` (escenas) + `diseno.json` + `plan.json` → `construir.py` → `ensamblar.py` →
`npx hyperframes check` → snapshot → render. Nunca edites `index.html` ni `compositions/frames/` a mano: se generan.

- Vista previa en vivo: `npx hyperframes preview --background` (detenla con `--stop` ANTES de editar frames-src).
- Revisión completa: `npx hyperframes check` (0 errores antes de renderizar).
- Render: ver §2.8 y §2.9 de la skill.
