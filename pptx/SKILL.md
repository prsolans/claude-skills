---
name: pptx-prs
description: "Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill."
license: Proprietary. LICENSE.txt has complete terms
---

# PPTX Skill

## Quick Reference

| Task | Guide |
|------|-------|
| Read/analyze content | `python -m markitdown presentation.pptx` |
| **Create or edit presentations** | **Read [editing.md](editing.md) — always start from the corporate template** |
| Add images to slides | [editing.md](editing.md) — Image Embedding section |
| Docusign colors & fonts | [docusign-theme.md](docusign-theme.md) — read-only reference |

---

## Corporate Template (Required)

**All presentations start from the 2025 Corporate Deck Template.** The template lives in the skill directory:

```
templates/2025 Corporate Deck Template - Light.pptx    # 81 slide layouts — light/white backgrounds
templates/2026 Corporate Deck Template - Dark.pptx     # Dark variant — deep violet backgrounds
templates/2025 Corporate Deck Template - Usage & Style Guide.pptx  # Brand reference
templates/fonts/DSIndigo-{Light,Regular,Medium,SemiBold,Bold}/     # DS Indigo font files (.otf, .ttf, .woff, .woff2)
```

**Template selection:**
- **Light** (default): Clean, professional — virtual meetings, classrooms, meeting rooms, webinars
- **Dark**: Dramatic, confident — keynotes, executive-level presentations, large screens

Use absolute paths based on the skill base directory provided in the skill invocation header (`Base directory for this skill: <path>`).

**Each template contains 60+ layout options** — cover slides, section headers, content layouts, stat callouts, charts, tables, workflow diagrams, and more. There is almost always a template slide that fits your content.

---

## Reading Content

```bash
# Text extraction
python -m markitdown presentation.pptx

# Visual overview
python scripts/thumbnail.py presentation.pptx

# Raw XML
python scripts/office/unpack.py presentation.pptx unpacked/
```

---

## Primary Workflow: Template-Based Editing

**Read [editing.md](editing.md) for full details.**

1. Analyze corporate template with `thumbnail.py`
2. Choose layout slides that match your content
3. Unpack → delete unused slides → edit content → clean → pack

---

## Docusign Design System

**All presentations use Docusign branding.** The corporate template enforces the design system — typography, layout rules, and component patterns are baked into the template slides. See [editing.md](editing.md) for the slide layout catalog and design tips.

### Color Palette (Read-Only Reference)

Useful when reading template XML or debugging color values. Do not use these to hand-code slides.

| Token | Name | Hex | Usage |
|-------|------|-----|-------|
| `primary` | Cobalt | `4C00FF` | Primary brand, CTAs, accent text, interactive elements |
| `dark` | Deep Violet | `26065D` | Headers, nav bars, cover slide backgrounds |
| `darkest` | Inkwell | `130032` | Deepest dark, near-black text on dark surfaces |
| `accent` | Poppy | `FF5252` | Accent bars, alerts, emphasis |
| `mist` | Mist | `CBC2FF` | Soft accent, borders, light highlights |
| `light` | Light Purple | `EEEAFF` | Card fills, pill badges, tile backgrounds |
| `surface` | Ecru | `F8F3F0` | Warm surface backgrounds, placeholder areas |
| `white` | White | `FFFFFF` | Content slide backgrounds, card surfaces |
| `text` | Dark Text | `111827` | Primary body text |
| `muted` | Muted | `6B7280` | Secondary text, descriptions, captions |
| `border` | Border Light | `E0D9FF` | Card borders, dividers |

---

## QA (Required)

**Assume there are problems. Your job is to find them.**

Your first render is almost never correct. Approach QA as a bug hunt, not a confirmation step. If you found zero issues on first inspection, you weren't looking hard enough.

### Content QA

```bash
python -m markitdown output.pptx
```

Check for missing content, typos, wrong order.

**When using templates, check for leftover placeholder text:**

```bash
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"
```

If grep returns results, fix them before declaring success.

### Visual QA

**⚠️ USE SUBAGENTS** — even for 2-3 slides. You've been staring at the code and will see what you expect, not what's there. Subagents have fresh eyes.

Convert slides to images (see [Converting to Images](#converting-to-images)), then use this prompt:

```
Visually inspect these slides. Assume there are issues — find them.

Look for:
- Overlapping elements (text through shapes, lines through words, stacked elements)
- Text overflow or cut off at edges/box boundaries
- Decorative lines positioned for single-line text but title wrapped to two lines
- Source citations or footers colliding with content above
- Elements too close (< 0.3" gaps) or cards/sections nearly touching
- Uneven gaps (large empty area in one place, cramped in another)
- Insufficient margin from slide edges (< 0.5")
- Columns or similar elements not aligned consistently
- Low-contrast text (e.g., light gray text on cream-colored background)
- Low-contrast icons (e.g., dark icons on dark backgrounds without a contrasting circle)
- Text boxes too narrow causing excessive wrapping
- Leftover placeholder content

For each slide, list issues or areas of concern, even if minor.

Read and analyze these images:
1. /path/to/slide-01.jpg (Expected: [brief description])
2. /path/to/slide-02.jpg (Expected: [brief description])

Report ALL issues found, including minor ones.
```

### Verification Loop

1. Generate slides → Convert to images → Inspect
2. **List issues found** (if none found, look again more critically)
3. Fix issues
4. **Re-verify affected slides** — one fix often creates another problem
5. Repeat until a full pass reveals no new issues

**Do not declare success until you've completed at least one fix-and-verify cycle.**

---

## Converting to Images

Convert presentations to individual slide images for visual inspection:

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

This creates `slide-01.jpg`, `slide-02.jpg`, etc.

To re-render specific slides after fixes:

```bash
pdftoppm -jpeg -r 150 -f N -l N output.pdf slide-fixed
```

---

## Dependencies

- `pip install "markitdown[pptx]"` - text extraction
- `pip install Pillow` - thumbnail grids
- `pip install defusedxml` - safe XML parsing (used by all scripts)
- LibreOffice (`soffice`) - PDF conversion (auto-configured for sandboxed environments via `scripts/office/soffice.py`)
- Poppler (`pdftoppm`) - PDF to images
