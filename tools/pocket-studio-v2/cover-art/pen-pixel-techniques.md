# Pen & Pixel Bling Techniques — Free-Tool Recipes

How to get the 90s diamond-encrusted rap cover look WITHOUT Adobe Photoshop. All recipes tested for Photopea (free, browser) and GIMP (free, desktop) unless noted.

## The Pen & Pixel formula (from Shawn Brauch interviews)
1. Sketch the concept on paper
2. Photograph/scan real objects from multiple angles (build a reusable asset library: chains, cars, watches, money)
3. Composite everything in layers — foreground subject, mid-ground props, background scene
4. Encrust text and objects in "diamonds"
5. More is more. Fill every pixel.

## Recipe 1: Diamond-encrusted text ("iced out" type)
The classic bling text effect. Original Photoshop technique (PhotoshopCAFE): clouds → glass distort → curves. Free-tool version:

**Photopea:**
1. Type your text, large and bold. Right-click layer → Rasterize.
2. Ctrl+click the text layer thumbnail to select the text shape.
3. Fill selection with 50% gray on a new layer.
4. Filter → Render → Clouds.
5. Filter → Distort → Glass. Choose the "Tiny Lens" texture, scale it down small, distortion ~7, smoothness ~3.
6. Image → Adjustments → Curves: drag the white point left until the facets go bright silver-white.
7. Optional: Layer Style → Bevel & Emboss (small, chisel hard) + Drop Shadow for depth.

**GIMP:**
1. Text tool → big bold text. Layer → "Discard Text Information" (rasterize).
2. Select by color the text, grow 0, fill with 50% gray on new layer.
3. Filters → Render → Clouds → Solid Noise (high detail).
4. Filters → Distort → Apply Lens / Glass Tile with tiny tile size — or use Filters → Map → Small Tiles then blur slightly.
5. Colors → Curves: crush whites up for sparkle.

## Recipe 2: Diamond sparkle / glints
- Create a small 4-point star brush (white cross with soft glow).
- Scatter manually on brightest reflection points — chains, teeth, watch faces.
- In Photopea: custom brush, spacing ~200%, scatter jitter on, paint on a Color Dodge layer at low opacity.
- Rule from jewelry retouchers: put flares ONLY on the brightest points. Subtle sells it.

## Recipe 3: Gold text
1. Rasterized text, fill with gold gradient (#8a5a00 → #ffdf80 → #b8860b).
2. Bevel & Emboss: chisel hard, depth ~200%, size ~5.
3. Inner Glow: warm yellow, low opacity.
4. Satin: dark brown, multiply — gives the metallic banding.

## Recipe 4: The full Pen & Pixel composite (no-budget version)
1. **Subject:** Phone photo of the artist, plain background. Cut out with remove.bg (free) or Photopea's Select → Subject.
2. **Background:** Dark gradient + lens flare + fire/cloud stock (Pexels, Pixabay — free). Pen & Pixel loved hellfire, luxury interiors, city skylines.
3. **Props:** Photograph your own chains/watches/money, or use free stock. Scatter with drop shadows.
4. **Text:** Diamond or gold recipe above. Slight arc (Warp Text) for that classic curve.
5. **Parental Advisory sticker:** Free PNGs online — completes the 90s look.
6. **Final:** Slight vignette + sharpen. Export 3000×3000 (streaming standard).

## Recipe 5: LONEWOLF-style mixed-media collage (the cheap path)
1. Print or hand-draw elements. Tear, don't cut clean.
2. Photograph with your phone in good light.
3. Composite in Photopea with Multiply/Overlay blend modes — let paper grain show.
4. Add scanned textures (coffee stains, notebook paper) at low opacity.
5. Hand-letter the title with your own fonts (Font Wizard catalog!).

## Typography — connect to Font Wizard
Pen & Pixel covers used heavy, condensed, chrome/metallic display type. The owner's custom fonts go here:
- Use his Trippy Drippy Wizard / Block Burner / Bush fonts for titles
- Diamond/gold recipes above work on ANY font — run his fonts through them
- House rule: generic neutral font for tracklist backs, custom font for the front cover (spice vs. backbone, per his font law)

## Canvas size
- Streaming: 3000×3000 px minimum (Spotify/Apple standard)
- Print vinyl: 12.375" × 12.375" @ 300 DPI = 3713×3713 px, CMYK
