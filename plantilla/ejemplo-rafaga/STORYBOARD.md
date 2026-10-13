---
format: 1920x1080
duration: 15s
message: "RÁFAGA RF-27: velocidad diseñada — y cada escena demuestra una técnica distinta de motion graphics"
arc: Hook (photo-finish) → Anatomía → Impacto → Colorways → Velocidad → Laboratorio → Lockup → Llegada
audience: seguidores de @soydiegoosorio que verán el anuncio incrustado (720px de ancho) dentro de un reel
mode: autonomous
music: "dance-playful-night.mp3 — 115 bpm, beat 0.5217s, bar 2.087s; the bed starts at media offset 1.615s so that a DOWNBEAT lands on video t=0.000"
---

## Decisions

- **Spine:** a photo-finish timing line. It opens the film (frame 1 reveals the shoe as a slit-scan), the timer runs
  through the film, and it closes it (frame 8: the line sweeps back, the clock stops at 00:15.00).
- **Hero prop:** `assets/sneaker.svg` — one vector shoe, parts addressable by id, recolored by CSS variables
  (colorways in `frame.md` → components.shoe). Every frame inlines that markup; never a raster.
- **Grid:** 115 bpm. Beat = 0.5217s. Downbeats (video time): 0.000 · 2.087 · 4.174 · 6.261 · 8.348 · 10.435 ·
  12.522 · 14.609. Every cut lands on a beat; every slam/pop lands on a beat or an eighth.
- **Seams:** one direction rule — motion travels LEFT (whip pans push left, zoom-throughs dive forward).
  Shader transitions are NOT used; the two hero seams are CSS (chromatic aberration wipe into the lockup, white flash
  into the finish). Hard cuts land on downbeats with an impact SFX.
- **Audio identity:** music bed + SFX cues (orchestrator-owned, listed per frame as `sfx:`). No narration.
- **Held frame:** frame 8 — after the scan, nothing moves for the last ~0.45s; the clock reads 00:15.00.
- **Bans:** no cyan/purple gradients, no glow halos, no rounded cards, no text under 22px, no 1px lines, no
  real brand names (RÁFAGA is fictional), no exits on non-final frames, no copying the KYVO reference beats
  (no Fourier circles, no CMYK misregistration, no capsule, no kaleidoscope, no lenticular, no box label).
- **Captions:** disabled. Keep-out relaxed: hero content stays above y=960; decoratives may bleed off any edge.
- **Canvas:** 1920×1080, 30fps authoring (final render 60fps).

## Frame 1 — Photo-finish

- scene: A lime finish line scans left→right and reveals the shoe as a slit-scan smear that snaps sharp; the race clock starts
- duration: 2.087s
- poster: 1.7s
- transition_in: cut
- status: outline
- src: compositions/frames/f01-photo-finish.html
- blueprint: compose
- rules: motion-blur-streak, svg-path-draw, counting-dynamic-scale, spring-pop-entrance
- focal: the shoe (carbon colorway) being revealed column by column behind the scan line
- roles: scan-line=driver · shoe=hero · clock=chrome · tags=accents
- sfx: 0.00 whoosh-short (scan starts) · 0.522 click (tag) · 1.043 click (tag) · 1.565 pop (outline lands) · 1.9 whoosh-cinematic (into the zoom-through)
- assets: assets/sneaker.svg (inline; colorway carbon: --c-upper #2A2A31 --c-sole #F3EFE4 --c-mid #F3EFE4 --c-accent #D6FF3F)

Scene 1 (0.00–0.20s): ink ground (`components.ink-ground`: lane grid 1px rgba(243,239,228,.06) every 120px, faint lane numerals "1 2 3 4" in Space Mono at 8% opacity drifting left 20px over the frame). Top-left chrome types in: "RÁFAGA · LAB". Top-right: the race clock, League Gothic 150px lime, "00:00.00" — tabular numerals — starts counting at 0.20 and reads real elapsed time (≈00:01.88 at the cut); its scale grows 1.0→1.06 as it counts (counting-dynamic-scale).
Scene 2 (0.20–1.30s): a vertical lime scan line (6px wide, full height, with a 40px soft lime haze to its right at 25%) travels from x=120 to x=1800 (power2.inOut, 1.1s). The shoe (1500px wide, centered, nose right, resting on a 3px lime ground rule at y=820) is revealed ONLY where the line has passed: a clip-path inset from the right follows the line's x. Preceding the reveal edge, a slit-scan smear: three echo copies of the shoe, scaleX 1.9 / 1.5 / 1.2 with transform-origin at the scan edge and opacity .18/.28/.4, that collapse into the sharp shoe as the line passes (motion-blur-streak, echo form, driven by the same tween). Chrome tags pop (spring-pop-entrance, back.out(1.6), 0.22s) on the beats: 0.522 "RF-27" (chrome-tag, lime border, under the clock) · 1.043 "PROTOTIPO 27" (bottom-left).
Scene 3 (1.30–2.087s): once the shoe is fully revealed, its wireframe (a second inline copy with `svg .ln{fill:none}`, strokes lime 4px) draws on over the shoe in 0.45s (svg-path-draw on the outline paths, staggered 0.03s) and holds at 60% opacity — a measurement scan. A 3px lime ground rule under the shoe grows scaleX 0→1 (0.4s). The bottom progress-strip (`components.progress-strip`) grows 0→14% of width across the frame. At 1.9s the scan line exits right, fast.
Exit vector: scan line leaving right at ~1800px/s; shoe + clock at rest (clock still counting).

## Frame 2 — Anatomía

- scene: The shoe's layers hang scattered in 3D space, the camera tilts down and they assemble into one shoe while lime leader lines label each part
- duration: 2.087s
- poster: 1.6s
- transition_in: zoom-through
- status: outline
- src: compositions/frames/f02-anatomia.html
- blueprint: compose
- rules: depth-scatter-assemble, 3d-camera-flight, svg-path-draw, waterfall-entry
- focal: the assembling shoe (carbon colorway), centered-right, ~1300px wide when assembled
- roles: shoe-layers=hero · leader-lines=connectors · labels=chrome · ghost-type=background
- sfx: 0.00 whoosh-cinematic (zoom lands) · 0.522 pop · 1.043 pop · 1.565 pop (each label lands) · 1.9 click
- assets: assets/sneaker.svg (inline SIX times, one part-group visible per copy via CSS: outsole / midsole / upper+toe / heel / tongue+laces+eyelets / mark; colorway carbon)

Scene 1 (0.00–0.30s): ink ground, lane grid. Chrome eyebrow top-left: "02 · ANATOMÍA". Right edge: ghost type "RF-27" in Archivo Black 520px, stroke-only lime 3px at 10% opacity, drifting up 30px over the frame. A perspective stage (perspective 1600px) holds a `.world` with preserve-3d; the six shoe layers sit in it as absolutely positioned 1300px-wide divs, each starting scattered (depth-scatter-assemble: index-derived translateZ −600…+400, rotateX ±18, rotateY ±26, offsets ±220px, opacity .9) — visible from the first frame.
Scene 2 (0.30–1.40s): the camera (3d-camera-flight, one pose object) flies from rotateX 24° / rotateY −22° / translateZ −380 to flat (0 / 0 / 0) with power4.out over 1.1s; meanwhile the layers assemble in order outsole → midsole → upper → heel → tongue/laces → mark, each 0.42s power3.out, staggered 0.12s (all landed by 1.25s). Each landing is a tiny settle (scale 1.02→1, 0.12s).
Scene 3 (0.52–2.087s): as the parts land, four leader lines (`components.leader-line`: 3px lime, 14px dot on the part, 45° elbow) draw on (svg-path-draw, 0.25s each) on the beats 0.522 / 1.043 / 1.565 / 1.9, each followed 0.1s later by its label typing/arriving (waterfall-entry for the label words): "MALLA 3D" (upper, top-left of the shoe) · "PLACA DE CARBONO" (midsole, bottom-left) · "SUELA REACTIVA" (outsole, bottom-right) · "MARCA RÁFAGA" (the streak, top-right). Labels are chrome (Space Mono 26px) with a chrome-tag box, lime on ink. A 3px lime rule under the eyebrow grows 0→1 at 0.3s.
Exit vector: camera still settling slowly (≤40px/s), labels at rest.

## Frame 3 — Pisa fuerte

- scene: "PISA" then "FUERTE." slam onto paper on consecutive beats; the shoe drops from above and stomps the ground rule with a squash, particles and a camera shake
- duration: 1.565s
- poster: 1.25s
- transition_in: cut
- status: outline
- src: compositions/frames/f03-pisa-fuerte.html
- blueprint: compose
- rules: kinetic-beat-slam, physics-press-reaction, particle-burst, motion-blur-streak
- focal: the stomp at beat 3 (1.043s) — shoe + ground + particles
- roles: PISA=beat1 · FUERTE=beat2 · shoe=beat3 hero · particles=punctuation · readout=chrome
- sfx: 0.00 impact-bass-1 (PISA) · 0.522 impact-bass-2 (FUERTE) · 1.043 thump + impact-bass-1 (stomp) · 1.25 pop (readout)
- assets: assets/sneaker.svg (inline; colorway carbon)

Scene 1 (0.00–0.52s): paper ground (`components.paper-ground`, grain-overlay at 12%). Beat 1 at 0.00: "PISA" (Archivo Black 330px, ink) slams in from scale 2.4 → 1 with expo.out 0.22s (kinetic-beat-slam scale-slam entrance), anchored top-left at x=96 y=120; a deterministic 3-frame stage shake follows (the whole content group jitters ±6px then settles). Chrome eyebrow "03 · IMPACTO" top-right. A 3px ink ground rule sits at y=880 across the frame.
Scene 2 (0.52–1.04s): beat 2 at 0.522: "FUERTE." (Archivo Black 330px, coral) side-snaps in from x=+900 with a motion-blur streak (motion-blur-streak, blur peaks mid-flight, resolves at the settle), landing at x=96 y=460. Both words stay.
Scene 3 (1.04–1.565s): beat 3 at 1.043: the shoe (1250px wide, right half of the frame, x≈620…1870) DROPS from y=−900 to the ground rule at y=880 with power4.in over 0.24s and lands: squash (scaleY .82, scaleX 1.12, transform-origin bottom center) for 2 frames then back.out(2) recovery (physics-press-reaction); on contact: 24 particles (particle-burst, ballistic, ink + lime chips 14–26px) launch from the sole's contact span and fall under gravity across the remaining frame; a dust ring (ellipse 420×60 at the sole, lime 3px stroke) scales 0→1.6 and fades; the ground rule bends (scaleY 1→2.4→1 in 0.18s); the camera shakes (content group y ±9px, 3 frames). At 1.25: a chrome readout pops bottom-left: "FUERZA 1.4 kN" (chrome-tag, coral border).
Exit vector: particles still falling (ballistic, ~400px/s), words and shoe at rest.

## Frame 4 — Colorways

- scene: A Solari split-flap board walks to CARBÓN, flips to LIMA, then CORAL on the beats, while the shoe swaps colorway in sync and a digit wheel counts 01/03 → 03/03
- duration: 2.609s
- poster: 2.0s
- transition_in: whip-pan
- status: outline
- src: compositions/frames/f04-colorways.html
- blueprint: compose
- rules: vertical-spring-ticker, spring-pop-entrance, sine-wave-loop
- focal: the shoe (≥55% of frame width, right-center) changing colorway on the beat
- roles: split-flap-board=driver (top band) · shoe=hero · number-wheel=counter (left) · sku-tag=chrome
- sfx: 0.00 whoosh (whip lands) · 0.00–0.35 key-press ×6 (flap cascade, 0.06s apart) · 0.522 pop (board locks CARBÓN) · 1.043 key-press ×6 + 1.30 pop (LIMA) · 2.087 key-press ×6 + 2.35 pop (CORAL)
- assets: assets/sneaker.svg (inline THREE times, one per colorway, stacked; carbon / lima / coral variables from frame.md components.shoe); mechanics reference: compositions/split-flap-board.html (copy its cell/drum mechanics into this frame, do NOT mount the block) and compositions/components/number-wheel.html (copy its strip mechanics)

Scene 1 (0.00–0.52s): ink ground. Top band (y 80–250): a Solari split-flap board of 7 cells (each 150×170px, graphite face, paper type Archivo Black 120px, a 3px ink split line across the middle, a lime rim on the active row). From 0.00 the cells walk forward through the alphabet (vertical-spring-ticker: masked column, stepped tweens 0.06s per step, deterministic) and land on "C A R B Ó N" by 0.52 (cells lock left→right). Left column: a number wheel "01/03" (League Gothic 230px lime; digits are masked vertical strips) already showing 01 / 03 with chrome label above "COLORWAY". The shoe (carbon) sits right-center, 1150px wide, with a subtle idle float (sine-wave-loop, ±6px, 1.3s period). Chrome tag bottom-left: "SKU RF-27-CB".
Scene 2 (0.52–1.57s): at 1.043 (beat) the board flips to "L I M A" (cells cascade 0.05s apart, two trailing cells go blank), the number wheel rolls 01→02 (strip tween 0.3s power3.out), the SKU tag swaps to "RF-27-LM" (hard swap), and the shoe changes to the LIMA colorway via a horizontal band wipe: the lima copy (stacked on top) reveals through 7 horizontal clip bands sweeping top→bottom over 0.3s (clip-path polygon steps or 7 stacked band divs with staggered scaleY), landing 1.30. A lime 3px rule under the board pulses once (scaleX 1→1.04→1).
Scene 3 (1.57–2.609s): at 2.087 (downbeat) the board flips to "C O R A L", the wheel rolls 02→03, SKU "RF-27-CR", and the coral copy band-wipes in (lands 2.35). Hold with the idle float. Exit vector: everything at rest except the ±6px float.

## Frame 5 — Velocidad

- scene: The camera flies down a lime perspective tunnel; the shoe rockets toward us with a ghost trail and the weight stat counts 0→275 in giant numerals
- duration: 2.087s
- poster: 1.75s
- transition_in: zoom-through
- status: outline
- src: compositions/frames/f05-velocidad.html
- blueprint: compose
- rules: 3d-camera-flight, motion-blur-streak
- focal: the stat "275" landing on the downbeat at 1.565s, with the shoe large at right
- roles: tunnel=background driver · shoe=hero (lima colorway) · stat=payoff · speed-lines=accents
- sfx: 0.00 whoosh-cinematic (dive) · 0.522 whoosh-short (shoe passes) · 1.565 thump + impact-bass-2 (stat lands) · 1.9 click
- assets: assets/sneaker.svg (inline; colorway lima)

Scene 1 (0.00–0.60s): ink ground. A perspective stage (perspective 900px, origin at x=1180 y=520 — right of center) holds a `.world` with preserve-3d containing 9 nested rectangles (1600×900, lime 3px outline, no fill) placed at translateZ −3600 … 0 in 450px steps, plus 6 lane lines converging to the vanishing point. The camera flies forward (3d-camera-flight: world translateZ 0 → +3600 over 1.9s, ease "none" so the rush is constant; rectangles that pass the camera are re-stepped with a finite repeat, or simply 18 rectangles so none run out). Short lime speed bars (8 of them, 3px × 120–260px) streak right→left across the frame at staggered times (each 0.18s, ease none, repeat a finite count).
Scene 2 (0.30–1.30s): the shoe (lima colorway) enters from far left-back: scale 0.25 → 1.0 and x −900 → +420 (final 1200px wide, right-center) with power3.out over 0.9s; a ghost trail of 3 echo copies (motion-blur-streak echo form: offsets −260/−170/−90px in x, scaleX 1.35/1.2/1.08, opacity .15/.25/.4) collapses into the lead as it settles at 1.20; a slight settle overshoot (back.out(1.4)).
Scene 3 (1.04–2.087s): left third: stat-block — chrome label "PESO · GRAMOS" (Space Mono 26px, smoke) arrives at 1.04; the figure (League Gothic 520px, lime, tabular) counts 0 → 275 from 1.09 to 1.565 (a plain-object proxy tween with onUpdate writing Math.round(v), tabular-nums, ease power2.out) with its scale growing 0.9 → 1.0 on the same timeline position, landing on the downbeat with a 2-frame scale punch (1.06 → 1). At 1.9 a chrome-tag "0,275 KG" clicks in under it. The tunnel keeps rushing; the shoe idles (sine-wave-loop ±4px). Exit vector: tunnel rushing at ~1900px/s in Z, shoe/stat at rest.

## Frame 6 — Laboratorio

- scene: On a paper spec sheet the shoe presses down and a pressure map blooms under the sole while two bars fill — REBOTE 94%, AGARRE 98% — and a coral stamp slams: PROBADO EN PISTA
- duration: 2.087s
- poster: 1.85s
- transition_in: cut
- status: outline
- src: compositions/frames/f06-laboratorio.html
- blueprint: compose
- rules: stat-bars-and-fills, sine-wave-loop, press-release-spring, spring-pop-entrance
- focal: the pressure map blooming under the shoe on the downbeat, then the stamp
- roles: shoe=hero (carbon) · pressure-rings=reaction · bars=data (left) · stamp=punctuation · eyebrow=chrome
- sfx: 0.00 impact-bass-1 (cut + press) · 0.08 pop (rings) · 0.522 pop (bar 1) · 1.043 pop (bar 2) · 1.30 thump (stamp) · 1.565 click (chip)
- assets: assets/sneaker.svg (inline; colorway carbon)

Scene 1 (0.00–0.40s): paper ground, grain-overlay 12%, 3px ink rules framing a sheet (inset 48px). Chrome eyebrow "04 · LABORATORIO" top-left; chrome "RF-27 · HOJA 06" top-right. The shoe (carbon, 1150px wide) sits top-right on a 3px ink baseline at y=760 and PRESSES at 0.00: scaleY 1 → .94 (origin bottom) over 0.08s then springs back (press-release-spring). Under the sole, at the heel and forefoot contact points, two sets of 5 concentric contour rings (ellipses, 3px strokes, coral innermost → lime outermost, no fill) bloom: scale 0 → 1 staggered 0.05s, back.out(1.8), each ring then breathes (sine-wave-loop, ±3%, phase offset by index).
Scene 2 (0.40–1.30s): left column (x 96…780): two data bars (stat-bars-and-fills: 3px ink outline track 640×64, lime fill scaleX from 0, origin left) — "REBOTE" fills to 94% by 0.522 with its League Gothic 150px figure "94%" counting up alongside; "AGARRE" fills to 98% by 1.043 with "98%". Labels in chrome above each bar.
Scene 3 (1.30–2.087s): at 1.30 a coral stamp (`components.stamp`: 6px coral border, Space Mono 34px, "PROBADO EN PISTA", rotate −8°) presses in over the shoe's heel area: scale 1.6 → 1 power4.in 0.14s + a 2-frame shake + ink offset shadow 10px appearing. At 1.565 a chip pops bottom-left: "RETORNO DE ENERGÍA +31%" (chrome-tag, ink border, lime-dim text). Rings keep breathing. Exit vector: rings breathing (≤20px/s), rest.

## Frame 7 — Lockup

- scene: The wordmark RÁFAGA slams in with a lime ring and one white frame; the shoe flips in from 3D; the tagline ROMPE EL AIRE. waterfalls in; a chromatic glitch burst punctuates the beat
- duration: 1.565s
- poster: 1.3s
- transition_in: chromatic-wipe
- status: outline
- src: compositions/frames/f07-lockup.html
- blueprint: compose
- rules: orbit-3d-entry, waterfall-entry, chromatic-glitch, spring-pop-entrance
- focal: the wordmark RÁFAGA (Archivo Black 300px, paper) across the top; the shoe bottom-right
- roles: wordmark=hero · shoe=secondary hero (lima) · tagline=payoff · ghost-outlines=background · ring+flash=impact
- sfx: 0.00 glitch-1 (wipe) · 0.05 impact-bass-2 (wordmark lands) · 0.522 pop ×3 (tagline words, 0.08 apart) · 1.043 glitch-2 (emphasis burst) · 1.3 click
- assets: assets/sneaker.svg (inline; colorway lima); mechanics reference: compositions/components/logo-sting.html (copy the slam + ring + single white impact frame mechanics; do NOT mount it)

Scene 1 (0.00–0.55s): ink ground. Behind everything, three ghost copies of the wordmark (stroke-only lime 3px, no fill, 300px) offset +40/+80/+120px down-right at 12% opacity, drifting slowly left. The wordmark "RÁFAGA" (Archivo Black 300px, paper, letter-spacing −0.02em, left-anchored x=96 y=150, width ~1500px) lands from scale 1.15 → 1 with expo.out 0.4s (logo-sting mechanics); on landing (0.45): one lime ring (3px, from the wordmark's center) scales 0.7 → 2.6 fading .9 → 0 over 0.5s, and EXACTLY one frame of white full-bleed (opacity 1 for 1/30s) at 0.45.
Scene 2 (0.30–1.00s): the shoe (lima, 1050px wide, bottom-right, x≈820…1870, baseline y=960) flips in from 3D (orbit-3d-entry entry form: rotateY −80 → 0, translateZ −500 → 0, opacity 0 → 1, 0.6s power3.out starting 0.30), then idles with a ±5px float.
Scene 3 (0.52–1.565s): tagline bottom-left (x=96 y=720): "ROMPE EL AIRE." in Archivo Black 120px lime — three words whip in from below (waterfall-entry, binary opacity, 0.08s stagger) starting 0.522; under it, chrome "RF-27 · 2026 · RAFAGA.CO" tracks in (letter-spacing from 0.6em → 0.16em, 0.4s) at 0.75. At 1.043 (beat) the wordmark gets a chromatic glitch emphasis burst (chromatic-glitch: red/cyan copies jitter ±14px on a quantized-time hash for 0.2s, then snap clean). Exit vector: shoe floating ±5px, text at rest.

## Frame 8 — Llegada

- scene: The finish line sweeps back right→left turning the shoe into its lime outline; the clock stops at 00:15.00, the tag LLEGADA pops, and the frame holds dead still
- duration: 0.913s
- poster: 0.8s
- transition_in: flash
- status: outline
- src: compositions/frames/f08-llegada.html
- blueprint: compose
- rules: motion-blur-streak, svg-path-draw, spring-pop-entrance
- focal: the clock "00:15.00" freezing, and the outlined shoe
- roles: scan-line=driver · shoe=hero (carbon → lime outline) · clock=payoff · tag=chrome · progress-strip=closure
- sfx: 0.00 whoosh-short (scan back) · 0.40 chime (clock stops) · 0.52 pop (tag)
- assets: assets/sneaker.svg (inline TWICE: carbon colorway + wireframe copy with strokes lime 5px)

Scene 1 (0.00–0.40s): ink ground, same layout as Frame 1 (clock top-right reading 00:14.09 at t=0 and counting, "RÁFAGA · LAB" top-left, the shoe 1500px centered on the lime ground rule, progress-strip at 93%). The lime scan line enters from the RIGHT edge and sweeps to x=120 in 0.40s (power3.out); where it passes, the filled shoe is replaced by its lime wireframe (clip-path inset from the left following the line; a brief 2-echo smear ahead of the edge — motion-blur-streak). At 0.40 the clock freezes at "00:15.00" and flashes lime→paper→lime over 3 frames; the progress-strip completes to 100% (scaleX, 0.3s).
Scene 2 (0.40–0.913s): at 0.522 a chrome-tag pops bottom-left: "LLEGADA · 15.00 s" (spring-pop-entrance). Then the HELD FRAME: nothing moves until the end. (Final frame: a 0.2s fade of the lane grid to 0 at 0.70 is allowed; nothing else exits.)
Entry vector: scan line entering at ~4500px/s from the right.
