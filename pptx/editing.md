# Editing Presentations

## Default Template

Unless another template is specified, use the **Docusign 2025 Corporate Deck Template (Light)**:

```
{skill_base_dir}/templates/2025 Corporate Deck Template - Light.pptx
```

The style guide is also available for reference:

```
{skill_base_dir}/templates/2025 Corporate Deck Template - Usage & Style Guide.pptx
```

These are the official corporate templates with proper slide masters, layouts, DS Indigo font, and brand assets.

**Note:** `{skill_base_dir}` is the base directory provided when the skill is invoked. Resolve to an absolute path at runtime.

---

## Slide Layout Catalog

The template contains 81 slides organized into categories. Use this catalog to choose the right layout for your content.

### Cover Slides (slides 6-12)
| Slide | Layout | Best For |
|-------|--------|----------|
| 6 | Title + subhead + 1 presenter (dark purple bg) | Standard presentations |
| 7 | Title + subhead + 1 presenter (variant) | Standard presentations |
| 8 | Title + subhead + 1 presenter (with badge) | Product/feature decks |
| 9 | Title + photo bg + 3 presenters | Team presentations, panels |
| 10 | Title + 2 presenters (vertical) | Co-presentations |
| 11 | Title + 2 presenters (horizontal) | Co-presentations |
| 12 | Title + right photo + 2 presenters | Customer-facing decks |

### Section Headers (slides 18-19, 23-24)
| Slide | Layout | Best For |
|-------|--------|----------|
| 18 | Section header + description (dark purple) | Topic transitions |
| 19 | Section header only (dark purple) | Clean transitions |
| 23 | Section header + full-bleed gradient | Visual impact |
| 24 | Section header + subtitle | Detailed sections |

### Content — Text (slides 20-22, 25-30)
| Slide | Layout | Best For |
|-------|--------|----------|
| 20 | Overview paragraph (white bg) | Introductory context |
| 21 | Large quote/statement (purple text) | Key messages |
| 22 | Large quote + page number | Key messages |
| 25 | Title + 2-column body text | Detailed explanations |
| 26 | Body text left + title right | Narrative flow |
| 27-28 | Title + 2-column text (variants) | Comparisons, details |
| 29 | Title + 2-column + bottom callout | Key point + supporting detail |
| 30 | Title + side-by-side bullets | Compact two-topic slide |

### Content — Image + Text (slides 31-37)
| Slide | Layout | Best For |
|-------|--------|----------|
| 31-32 | Title + photo + 3 topics | Feature highlights with visual |
| 33 | Title + photo + 4 stat percentages | Data-backed feature slides |
| 34 | Title + photo + 3 topics (vertical) | Feature deep-dives |
| 35 | Title + full-bleed photo + callout | Visual impact with message |
| 36-37 | Full-bleed photo layouts | Visual-first slides |

### Stats & Callouts (slides 39-41)
| Slide | Layout | Best For |
|-------|--------|----------|
| 39 | 4 stat callout boxes (XX%) | Metrics dashboards |
| 40 | 2 stat callout boxes (XX%) | Focused metrics |
| 41 | 2 large stats + title | Hero metrics |

### Case Studies & Comparisons (slides 42-45)
| Slide | Layout | Best For |
|-------|--------|----------|
| 42 | Case study (results + 3 stats) | Customer wins |
| 43 | Customer story (challenge/solution/products) | Customer narratives |
| 44 | Competitor analysis (2-column) | Head-to-head comparisons |
| 45 | Competitor analysis (with photo) | Competitive positioning |

### Timelines & Roadmaps (slides 46-48)
| Slide | Layout | Best For |
|-------|--------|----------|
| 46 | Roadmap (Gantt-style horizontal bars) | Project roadmaps |
| 47 | Project timeline (vertical milestones) | Linear timelines |
| 48 | Timeline (horizontal multi-year) | Long-range planning |

### Quotes (slides 49-51)
| Slide | Layout | Best For |
|-------|--------|----------|
| 49 | Quote + attribution (white bg) | Customer/exec quotes |
| 50 | Quote + attribution (light bg) | Customer/exec quotes |
| 51 | Quote + attribution (dark purple bg) | High-impact quotes |

### Demo & Closing (slides 52-58)
| Slide | Layout | Best For |
|-------|--------|----------|
| 52 | Demo slide | Live demo transitions |
| 53-56 | End/thank you slides (various) | Deck closings |
| 57-58 | Closing with DocuSign logo | Branded closings |

### Charts (slides 60-63)
| Slide | Layout | Best For |
|-------|--------|----------|
| 60 | Column bar chart + 2 topics | Bar chart data |
| 61 | Stacked bar chart + 2 topics | Composition data |
| 62 | Donut pie chart + 2 topics | Distribution data |
| 63 | Line graph + 2 topics | Trend data |

### Tables (slides 65-71)
| Slide | Layout | Best For |
|-------|--------|----------|
| 65 | 3-column product comparison | Feature matrices |
| 66 | 4-column simple table | Data grids |
| 67 | 2-column product comparison | Side-by-side |
| 68 | Dual comparison tables | A/B comparisons |
| 69 | Competitor feature table (checkmarks) | Competitive matrices |
| 70-71 | Detailed product/pricing tables | SKU comparisons |

### Workflow Diagrams (slides 73-77)
| Slide | Layout | Best For |
|-------|--------|----------|
| 73 | Process level diagram (3 steps) | Simple workflows |
| 74 | 1-to-3 funnel diagram | Diverging flows |
| 75 | 1-to-1 funnel diagram | Complex flows |
| 76 | Step diagram (3 numbered steps) | Sequential processes |
| 77 | Trail diagram (6 numbered steps) | Detailed processes |

### Utility (slides 1-5, 13, 78-81)

**EXTERNAL PRESENTATIONS: Always include slide 13 (Safe Harbor) immediately after the cover slide. This is a legal requirement for any customer-facing or external deck.**

| Slide | Layout | Best For |
|-------|--------|----------|
| 5 | Template overview/TOC | Skip (template instructions) |
| **13** | **Safe Harbor** | **Required for external presentations — insert after cover** |
| 14-15 | Agenda (1 or 2 sections) | Deck navigation |
| 16-17 | Speaker panel (3 or 6 speakers) | Team introductions |

---

## Template-Based Workflow

When using an existing presentation as a template:

1. **Analyze existing slides**:
   ```bash
   python scripts/thumbnail.py template.pptx
   python -m markitdown template.pptx
   ```
   Review `thumbnails.jpg` to see layouts, and markitdown output to see placeholder text.

2. **Plan slide mapping**: For each content section, choose a template slide.

   ⚠️ **USE VARIED LAYOUTS** — monotonous presentations are a common failure mode. Don't default to basic title + bullet slides. Actively seek out:
   - Multi-column layouts (2-column, 3-column)
   - Image + text combinations
   - Full-bleed images with text overlay
   - Quote or callout slides
   - Section dividers
   - Stat/number callouts
   - Icon grids or icon + text rows

   **Avoid:** Repeating the same text-heavy layout for every slide.

   Match content type to layout style (e.g., key points → bullet slide, team info → multi-column, testimonials → quote slide).

3. **Unpack**: `python scripts/office/unpack.py template.pptx unpacked/`

4. **Build presentation** (do this yourself, not with subagents):
   - Delete unwanted slides (remove from `<p:sldIdLst>`)
   - Duplicate slides you want to reuse (`add_slide.py`)
   - Reorder slides in `<p:sldIdLst>`
   - **Complete all structural changes before step 5**

5. **Edit content**: Update text in each `slide{N}.xml`.
   **Use subagents here if available** — slides are separate XML files, so subagents can edit in parallel.

6. **Clean**: `python scripts/clean.py unpacked/`

7. **Pack**: `python scripts/office/pack.py unpacked/ output.pptx --original template.pptx`

---

## Scripts

| Script | Purpose |
|--------|---------|
| `unpack.py` | Extract and pretty-print PPTX |
| `add_slide.py` | Duplicate slide or create from layout |
| `add_image.py` | Embed images into slides |
| `clean.py` | Remove orphaned files |
| `pack.py` | Repack with validation |
| `thumbnail.py` | Create visual grid of slides |

### unpack.py

```bash
python scripts/office/unpack.py input.pptx unpacked/
```

Extracts PPTX, pretty-prints XML, escapes smart quotes.

### add_slide.py

```bash
python scripts/add_slide.py unpacked/ slide2.xml      # Duplicate slide
python scripts/add_slide.py unpacked/ slideLayout2.xml # From layout
```

Prints `<p:sldId>` to add to `<p:sldIdLst>` at desired position.

### clean.py

```bash
python scripts/clean.py unpacked/
```

Removes slides not in `<p:sldIdLst>`, unreferenced media, orphaned rels.

### pack.py

```bash
python scripts/office/pack.py unpacked/ output.pptx --original input.pptx
```

Validates, repairs, condenses XML, re-encodes smart quotes.

### thumbnail.py

```bash
python scripts/thumbnail.py input.pptx [output_prefix] [--cols N]
```

Creates `thumbnails.jpg` with slide filenames as labels. Default 3 columns, max 12 per grid.

**Use for template analysis only** (choosing layouts). For visual QA, use `soffice` + `pdftoppm` to create full-resolution individual slide images—see SKILL.md.

### add_image.py

```bash
# Replace an existing image placeholder
python scripts/add_image.py unpacked/ slide9.xml photo.jpg --replace-idx 6

# Add a new image at specific coordinates (inches)
python scripts/add_image.py unpacked/ slide20.xml screenshot.png --x 1.0 --y 1.5 --w 6.0 --h 3.5
```

Embeds an image into a slide. Handles the full chain: copies to `ppt/media/`, registers the content type, creates the relationship, and updates the slide XML.

---

## Image Embedding

Use `add_image.py` to embed images into template slides. Two modes:

### Replacing Template Placeholders

Many template slides have image placeholders (photo slots). To find them:

```bash
# List placeholder indices in a slide
python3 -c "
import defusedxml.minidom
dom = defusedxml.minidom.parse('unpacked/ppt/slides/slide34.xml')
for pic in dom.getElementsByTagNameNS('http://schemas.openxmlformats.org/presentationml/2006/main', 'pic'):
    for ph in pic.getElementsByTagName('p:ph'):
        print(f'idx={ph.getAttribute(\"idx\")}')
"
```

Then replace:

```bash
python scripts/add_image.py unpacked/ slide34.xml photo.jpg --replace-idx 3
```

This swaps the placeholder's `<a:blip>` reference to point at the new image file while preserving the original position, size, and crop settings from the template.

### Adding New Images at Coordinates

For slides without image placeholders, or when adding supplementary images:

```bash
python scripts/add_image.py unpacked/ slide20.xml screenshot.png --x 1.0 --y 1.5 --w 6.0 --h 3.5
```

All values are in inches. The image is appended to the slide's shape tree as a new `<p:pic>` element.

### Screenshots Workflow

To embed a screenshot into a presentation:

1. Take the screenshot (or generate with a tool)
2. Unpack the template
3. Choose a slide — use an image+text layout (slides 31-37) or add to any slide
4. Run `add_image.py` with coordinates or placeholder replacement
5. Clean and pack

### Multiple Images Per Slide

Call `add_image.py` multiple times on the same slide. Each call assigns a new `rId` and media file — they don't conflict.

```bash
python scripts/add_image.py unpacked/ slide31.xml photo1.jpg --replace-idx 3
python scripts/add_image.py unpacked/ slide31.xml logo.png --x 10.5 --y 0.5 --w 2.0 --h 1.0
```

### Supported Formats

JPG, PNG, GIF, BMP, TIFF, WMF, EMF, SVG.

---

## Slide Operations

Slide order is in `ppt/presentation.xml` → `<p:sldIdLst>`.

**Reorder**: Rearrange `<p:sldId>` elements.

**Delete**: Remove `<p:sldId>`, then run `clean.py`.

**Add**: Use `add_slide.py`. Never manually copy slide files—the script handles notes references, Content_Types.xml, and relationship IDs that manual copying misses.

---

## Editing Content

**Subagents:** If available, use them here (after completing step 4). Each slide is a separate XML file, so subagents can edit in parallel. In your prompt to subagents, include:
- The slide file path(s) to edit
- **"Use the Edit tool for all changes"**
- The formatting rules and common pitfalls below

For each slide:
1. Read the slide's XML
2. Identify ALL placeholder content—text, images, charts, icons, captions
3. Replace each placeholder with final content

**Use the Edit tool, not sed or Python scripts.** The Edit tool forces specificity about what to replace and where, yielding better reliability.

### Formatting Rules

- **Bold all headers, subheadings, and inline labels**: Use `b="1"` on `<a:rPr>`. This includes:
  - Slide titles
  - Section headers within a slide
  - Inline labels like (e.g.: "Status:", "Description:") at the start of a line
- **Never use unicode bullets (•)**: Use proper list formatting with `<a:buChar>` or `<a:buAutoNum>`
- **Bullet consistency**: Let bullets inherit from the layout. Only specify `<a:buChar>` or `<a:buNone>`.

---

## Common Pitfalls

### Template Adaptation

When source content has fewer items than the template:
- **Remove excess elements entirely** (images, shapes, text boxes), don't just clear text
- Check for orphaned visuals after clearing text content
- Run visual QA to catch mismatched counts

When replacing text with different length content:
- **Shorter replacements**: Usually safe
- **Longer replacements**: May overflow or wrap unexpectedly
- Test with visual QA after text changes
- Consider truncating or splitting content to fit the template's design constraints

**Template slots ≠ Source items**: If template has 4 team members but source has 3 users, delete the 4th member's entire group (image + text boxes), not just the text.

### Multi-Item Content

If source has multiple items (numbered lists, multiple sections), create separate `<a:p>` elements for each — **never concatenate into one string**.

**❌ WRONG** — all items in one paragraph:
```xml
<a:p>
  <a:r><a:rPr .../><a:t>Step 1: Do the first thing. Step 2: Do the second thing.</a:t></a:r>
</a:p>
```

**✅ CORRECT** — separate paragraphs with bold headers:
```xml
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799" b="1" .../><a:t>Step 1</a:t></a:r>
</a:p>
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799" .../><a:t>Do the first thing.</a:t></a:r>
</a:p>
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799" b="1" .../><a:t>Step 2</a:t></a:r>
</a:p>
<!-- continue pattern -->
```

Copy `<a:pPr>` from the original paragraph to preserve line spacing. Use `b="1"` on headers.

### Smart Quotes

Handled automatically by unpack/pack. But the Edit tool converts smart quotes to ASCII.

**When adding new text with quotes, use XML entities:**

```xml
<a:t>the &#x201C;Agreement&#x201D;</a:t>
```

| Character | Name | Unicode | XML Entity |
|-----------|------|---------|------------|
| `“` | Left double quote | U+201C | `&#x201C;` |
| `”` | Right double quote | U+201D | `&#x201D;` |
| `‘` | Left single quote | U+2018 | `&#x2018;` |
| `’` | Right single quote | U+2019 | `&#x2019;` |

### Other

- **Whitespace**: Use `xml:space="preserve"` on `<a:t>` with leading/trailing spaces
- **XML parsing**: Use `defusedxml.minidom`, not `xml.etree.ElementTree` (corrupts namespaces)

---

## Design Tips (Avoid)

- **Don't use any colors outside the palette** — no generic blues, no random grays
- **Don't repeat the same layout** — vary tiles, cards, tables, and callouts across slides
- **Don't center body text** — left-align paragraphs and lists; center only titles and stats
- **Don't skimp on size contrast** — titles need 24pt+ to stand out from 13pt body
- **Don't mix spacing randomly** — choose 0.3" or 0.5" gaps and use consistently
- **Don't create text-only slides** — always add cards, tiles, tables, or visual shapes
- **Don't forget text box padding** — when aligning with shapes, set `margin: 0` on the text box
- **Don't use low-contrast elements** — ensure text is readable against its background
- **NEVER use accent lines under titles** — use the header bar pattern (dark purple + poppy) instead
