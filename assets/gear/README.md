# Personal gear cutouts

These assets replace the generated object collage with cutouts based on Lasse's supplied photographs. Background extraction used the built-in `image_gen` editing tool. The PNG files are retained as master cutouts; the WebP files are compressed delivery assets for the website.

## Sources and prompt set

| Asset | Supplied source | Editing brief |
| --- | --- | --- |
| `acoustic-guitar.png` / `.webp` | `/Users/lasse/Downloads/IMG_0706.HEIC`, converted to `gear-inputs/IMG_0706.jpg` | Isolate the photographed acoustic guitar. Remove the room, stand and strap; preserve the instrument's appearance, proportions and visible details. |
| `electric-guitar.png` / `.webp` | `/Users/lasse/Downloads/IMG_1801.HEIC`, converted to `gear-inputs/IMG_1801.jpg` | Isolate the photographed electric guitar. Remove the background, stand and strap; preserve its shape, finish, hardware and visible details. |
| `bike.png` / `.webp` | `/Users/lasse/Downloads/IMG_4158.HEIC`, converted to `gear-inputs/IMG_4158.jpg` | Isolate the actual bicycle from the photograph. Remove the surroundings and retain the bicycle's proportions and visible components. |
| `microphone.png` / `.webp` | `/Users/lasse/Downloads/2L8A9163.JPEG` | Isolate the nearest, foreground microphone. Remove people, background, stand and other equipment; retain the microphone's photographic appearance. |
| `running-shoe.png` / `.webp` | `/Users/lasse/Desktop/Skærmbillede 2026-11-02 kl. 14.56.10.png` | Isolate the single foreground shoe only. Remove the background and the other shoe; retain its shape, colours and visible details. |

## Shared preservation constraints

The extraction prompts requested genuinely transparent backgrounds, original photographic objects, no illustrative or rendered styling, and no added objects. Both guitars are featured as distinct objects; only one running shoe is used. Backgrounds, stands and straps were to be removed where applicable.

These are image-model-assisted edits, so preservation of the supplied objects was the goal; exact pixel identity is not claimed. Original source photographs remain separate from the cutouts.

## Reversible website treatment

The website applies the restrained CSS filter `sepia(.28) saturate(.8)` to harmonise the gear with the warm palette. This does not bake the tint into the master or delivery files, so the original cutout colours remain available by removing the filter.

The hero fan uses the bicycle as a vertical centre, with two objects leaning each way. A narrow, layered white CSS drop-shadow on the outer object wrappers gives a soft contour glow without changing the image files or clipping it at the interactive hit areas.
