# WinGreen collage redesign

Adapted from the user-supplied Ploy export, preserving its wine, espresso, cream and orange palette, Archivo and Hanken Grotesk typography, collage assets, paper edges, layout and motion direction.

The implementation uses static HTML/CSS and browser animations, compatible with the existing GitHub Pages deployment. It needs no build step or Ploy account. Danish is the default in index.html; en.html is English. Edit both when updating copy.

Motion includes opposite-side name entrances, scroll-linked hero movement on desktop, word-by-word statement emphasis, one-time section reveals, a quote sticker entrance and footer sticker movement. It respects prefers-reduced-motion; content also remains visible when JavaScript is unavailable. Video loads only when requested and the dialog returns focus to its opener.

The hero now features photograph-based transparent cutouts of Lasse’s acoustic guitar, electric guitar, bicycle, microphone and a single running shoe. These are stored in assets/gear/ with PNG masters, WebP delivery files and source/edit notes. A subtle CSS tint can be changed independently of the original cutouts.

Reference assets and fonts are stored in assets/ploy/. Ploy source attribution is in assets/ploy/LICENSE; font licenses are included beside the font files. The career pages remain separate and in English.

Verified in browser at desktop and mobile widths, including language switching and the performance video dialog. No external messages sent and no publication performed.

The five hero objects are now native interactive controls with silhouette-shaped hit areas and localised hover/focus labels. The microphone opens the existing performance dialog; the acoustic guitar opens Flow & Green in the matching language; electric guitar, bike and shoe jump to music, cycling and running. Their bases converge around the portrait opening (about 18–61% of its width), with the portrait blocking pointer interaction on concealed portions.
