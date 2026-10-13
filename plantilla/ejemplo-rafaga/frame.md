---
version: 1
name: RÁFAGA — Frame (sneaker showreel, 1920×1080)
description: >
  Design truth for the RÁFAGA RF-27 sneaker ad. A race-lab world: ink-black track surfaces and warm
  paper sheets, one electric lime accent (the brand's "voltage") and one hot coral for impact beats.
  Heavy display type at poster scale, condensed numerals for data, mono chrome for labels. Flat planes,
  hard edges, no soft shadows; depth comes from scale, overlap, stroke and real 3D camera moves.
unit: the frame — 1920×1080
principle: one accent per frame · numbers are always set in League Gothic · every label is mono uppercase

colors:
  ink: "#121216"        # near-black, cool
  paper: "#F3EFE4"      # warm off-white sheet
  lime: "#D6FF3F"       # THE accent (voltage)
  coral: "#FF4A3D"      # impact / second register (rationed)
  graphite: "#2A2A31"   # dark surfaces, shoe outline fills
  smoke: "#8E8C86"      # secondary text on dark, rules on paper
  lime-dim: "#A6C92E"   # lime on paper when it must stay legible
  white: "#FFFFFF"      # highlights only (never a ground)

typography:
  display:   { fontFamily: "Archivo Black", weight: 400, upper: true, tracking: "-0.02em", lineHeight: 0.9 }
  numeral:   { fontFamily: "League Gothic", weight: 400, upper: true, tracking: "0.01em", lineHeight: 0.85 }
  chrome:    { fontFamily: "Space Mono", weight: 700, upper: true, tracking: "0.16em", size: "22-28px" }
  body:      { fontFamily: "Inter", weight: 400, size: "30-38px", lineHeight: 1.3 }
  # scale ramp (px on the 1920 canvas)
  hero-word: { fontFamily: "Archivo Black", px: 260-360 }   # one or two words, 60-80 % of frame width
  title:     { fontFamily: "Archivo Black", px: 120-180 }
  stat-big:  { fontFamily: "League Gothic", px: 420-560, color: "lime" }
  stat:      { fontFamily: "League Gothic", px: 160-240 }
  label:     { fontFamily: "Space Mono", px: 22-28, color: "smoke" }

spacing:
  pad-frame: "72px"
  gutter: "40px"
  rule: "3px"           # structural rules (never 1px: invisible on video)

components:
  ink-ground:
    background: "{colors.ink}"
    texture: "track-line grid: 1px rgba(243,239,228,.06) every 120px + faint lane numbers in chrome type at 8 % opacity"
    description: "The default ground for lab / speed frames."
  paper-ground:
    background: "{colors.paper}"
    texture: "fine grain (grain-overlay component at ~12 % opacity) + 3px ink rules"
    description: "The ground for print / poster / lockup frames."
  shoe:
    source: "assets/sneaker.svg — inline the markup; parts are addressable by id (see the file header)"
    colorways:
      carbon: { upper: "{colors.graphite}", sole: "{colors.paper}", accent: "{colors.lime}" }
      lima:   { upper: "{colors.lime}",     sole: "{colors.ink}",   accent: "{colors.ink}" }
      coral:  { upper: "{colors.coral}",    sole: "{colors.paper}", accent: "{colors.ink}" }
    description: "The hero prop. Side view, nose pointing RIGHT. Outline strokes stay ink. Never stretch non-uniformly except on a deliberate squash/stretch beat."
  stat-block:
    typography: "{typography.stat-big} + {typography.label} above"
    description: "A giant League Gothic figure with its mono label; label sits 12px above the figure's cap height, left-aligned to it."
  chrome-tag:
    border: "3px solid currentColor"
    padding: "10px 18px"
    typography: "{typography.chrome}"
    rounded: "0"
    description: "Boxed mono label (SKU, colorway, section number). Square corners always."
  leader-line:
    stroke: "3px {colors.lime} (on ink) or {colors.ink} (on paper)"
    end: "a 14px filled dot on the part, the label at the other end"
    description: "Callout line from a shoe part to its label. Draws on (svg-path-draw), label types after the line lands."
  rule:
    size: "3px"
    color: "{colors.lime} on ink · {colors.ink} on paper"
    description: "Structural divider; grows with scaleX from 0."
  stamp:
    border: "6px solid {colors.coral}"
    typography: "{typography.chrome} at 34px, color {colors.coral}"
    transform: "rotate(-8deg)"
    description: "Rubber-stamp box (edition, 'PROBADO', 'RF-27'). Lands with a press (scale 1.6 → 1) and a 2-frame shake."
  progress-strip:
    size: "6px tall, bottom edge"
    color: "{colors.lime}"
    description: "Optional timing strip at the very bottom; grows with the scene's progress."
---

# RÁFAGA — Frame

## Overview

A fictional running-sneaker brand, **RÁFAGA** (Spanish for a gust / burst), model **RF-27**. The ad's
world is a **race lab**: a black track with lane rules, photo-finish timing strips, measurement callouts,
and paper spec sheets — crossed with **poster-scale type**. The feeling: engineered speed, confident,
a little playful. Think a Nike Volt campaign shot by a print studio: every frame could be a poster, but
things move with real physics.

Two grounds alternate: **ink** (lab, speed, data) and **paper** (print, poster, lockup). **Lime** is the
voltage — the one color that pulls the eye on every frame. **Coral** is rationed to impact beats (a slam,
a stamp, a colorway) and never shares a frame with lime at equal weight.

## The Frame

- Canvas 1920×1080. Content lives inside `pad-frame` (72px); hero elements may bleed off one edge on purpose.
- The video will be shown **inside a phone reel at ~720px wide**: keep everything big. No text under 22px,
  no hairlines under 3px, decorative opacity ≥ 12 %. Big shapes, big type, high contrast.
- Squint test: one hero (the shoe or one word/figure) dominates; chrome supports; the accent is unmistakable.
- Anchor to edges and split the frame (stat left / shoe right; board top / shoe below). Centered-and-floating only
  for the final lockup.

## Colors

Tokens are exact. `ink` and `paper` are the only grounds. `lime` is the accent on ink; on paper use `lime-dim`
for text but full `lime` for fills/blocks. `coral` appears on at most 3 frames. `white` is for specular highlights
and the impact flash only. Tint everything warm (paper) or cool (ink) — no dead gray except `smoke` for chrome.

## Typography

- **Archivo Black** (400 only) — every hero word, title and the wordmark. Uppercase, tight tracking.
- **League Gothic** (400 only) — every number: timers, stats, counters, edition numbers. Tall and condensed, it
  can go enormous (560px) without crowding.
- **Space Mono 700** — chrome: labels, SKUs, section numbers, leader-line captions. Uppercase, tracked 0.16em.
- **Inter 400** — only if a sentence is needed (rare). Prefer a chrome label.
- No gradient text. No outlined text except the wordmark's ghost copy (stroke 3px lime, no fill) used as a background
  decorative.

## Depth & Surface

Flat planes. Depth from **scale contrast**, **overlap**, **3px ink/lime strokes**, and **real perspective** (3D
camera flights, preserve-3d stacks). No drop shadows on text. A hard 10px offset block shadow in `ink` under
paper cards is allowed (print feel). Motion blur / ghost trails are allowed on speed beats.

## Shapes

Square corners everywhere. Circles only for timing dots, eyelets and the pressure rings. The wordmark may sit
on a parallelogram skewed −12° (the brand's "gust").

## Motion language (guardrails for every frame)

- Cuts and hits land on the music grid (see `beats.json`: 114 bpm, beat 0.526s, bar 2.105s).
- Entrances: `fromTo`, varied eases (expo.out for slams, back.out(1.6) for pops, power3.out for slides,
  elastic only once in the whole film). Exits never (the transition is the exit) except the final frame.
- Every frame has 2–4 ambient decoratives moving (lane rules drifting, a timing strip growing, ghost type
  sliding, rings breathing).
- First visible motion within 0.2s of the frame start; something new arrives in the back half of every frame.

## Do / Don't

**Do** — giant League Gothic numbers · lime leader lines · chrome tags · the shoe big (≥ 55 % of frame width on
hero frames) · hard cuts on downbeats · paper grain on paper frames.

**Don't** — cyan/purple gradients · glow halos · rounded cards · centered floating text · more than one accent
per frame · tiny labels · any claim with a real brand name (RÁFAGA is fictional).
