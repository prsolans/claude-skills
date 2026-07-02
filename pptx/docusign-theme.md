# Docusign Theme Reference

**Read-only reference.** Do not use these to hand-code slides. All presentations use template-based editing — these values are helpful when reading or debugging template XML.

## Font: DS Indigo

Docusign's custom typeface. Available weights: Light, Regular, Medium, Semi Bold, Bold.

**Weight mapping** (style guide name → font file):
- Normal → `DSIndigo-Regular`
- Medium → `DSIndigo-Medium`
- Semi Bold → `DSIndigo-SemiBold`
- Bold → `DSIndigo-Bold`
- Light → `DSIndigo-Light`

**Font files** are bundled with the skill at `templates/fonts/`:
- `DSIndigo-Light/DSIndigo-Light.otf`
- `DSIndigo-Regular/DSIndigo-Regular.otf`
- `DSIndigo-Medium/DSIndigo-Medium.otf`
- `DSIndigo-SemiBold/DSIndigo-SemiBold.otf`
- `DSIndigo-Bold/DSIndigo-Bold.otf`

Also available as `.ttf`, `.woff`, `.woff2` in the same directories.

**System install:** Copy `.otf` files to `~/Library/Fonts/` for macOS rendering (LibreOffice, Chrome, etc.).

**Fallback:** If DS Indigo is not available, use `Calibri`.

## Color Constants (JavaScript)

```javascript
// Primary palette
const DS_COBALT       = "4C00FF";  // Primary brand, CTAs, accent text
const DS_DEEP_VIOLET  = "26065D";  // Headers, cover backgrounds
const DS_INKWELL      = "130032";  // Deepest dark
const DS_POPPY        = "FF5252";  // Accent bars, emphasis
const DS_MIST         = "CBC2FF";  // Soft accent, borders
const DS_LIGHT_PURPLE = "EEEAFF";  // Card fills, tile backgrounds
const DS_ECRU         = "F8F3F0";  // Warm surface, placeholder areas
const DS_WHITE        = "FFFFFF";  // Content backgrounds

// Text colors
const DS_TEXT_DARK    = "111827";  // Primary body text
const DS_TEXT_MUTED   = "6B7280";  // Secondary/description text
const DS_TEXT_COVER   = "CCCCDD";  // Subtitle text on dark backgrounds

// Borders & utility
const DS_BORDER       = "E0D9FF";  // Card/divider borders
const DS_BORDER_GRAY  = "D1D5DB";  // Table cell borders
const DS_ROW_ALT      = "F8F3F0";  // Alternating table rows
```

## Color Constants (Python)

```python
from pptx.dml.color import RGBColor

C_COBALT        = RGBColor(0x4C, 0x00, 0xFF)
C_DEEP_VIOLET   = RGBColor(0x26, 0x06, 0x5D)
C_INKWELL       = RGBColor(0x13, 0x00, 0x32)
C_POPPY         = RGBColor(0xFF, 0x52, 0x52)
C_MIST          = RGBColor(0xCB, 0xC2, 0xFF)
C_LIGHT_PURPLE  = RGBColor(0xEE, 0xEA, 0xFF)
C_ECRU          = RGBColor(0xF8, 0xF3, 0xF0)
C_WHITE         = RGBColor(0xFF, 0xFF, 0xFF)

C_TEXT_DARK     = RGBColor(0x11, 0x18, 0x27)
C_TEXT_MUTED    = RGBColor(0x6B, 0x72, 0x80)
C_BORDER        = RGBColor(0xE0, 0xD9, 0xFF)
C_BORDER_GRAY   = RGBColor(0xD1, 0xD5, 0xDB)
C_ROW_ALT       = RGBColor(0xF8, 0xF3, 0xF0)
```

## Slide Dimensions

```
Layout: LAYOUT_WIDE (16:9 widescreen)
Width:  13.33 inches
Height: 7.5 inches
```
