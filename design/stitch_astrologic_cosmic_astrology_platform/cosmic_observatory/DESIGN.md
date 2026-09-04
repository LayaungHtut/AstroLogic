---
name: Cosmic Observatory
colors:
  surface: '#121222'
  surface-dim: '#121222'
  surface-bright: '#38374a'
  surface-container-lowest: '#0c0c1d'
  surface-container-low: '#1a1a2b'
  surface-container: '#1e1e2f'
  surface-container-high: '#29283a'
  surface-container-highest: '#333345'
  on-surface: '#e3e0f8'
  on-surface-variant: '#ccc3d8'
  inverse-surface: '#e3e0f8'
  inverse-on-surface: '#2f2f40'
  outline: '#958da1'
  outline-variant: '#4a4455'
  surface-tint: '#d2bbff'
  primary: '#d2bbff'
  on-primary: '#3f008e'
  primary-container: '#7c3aed'
  on-primary-container: '#ede0ff'
  inverse-primary: '#732ee4'
  secondary: '#4cd7f6'
  on-secondary: '#003640'
  secondary-container: '#03b5d3'
  on-secondary-container: '#00424e'
  tertiary: '#cebdff'
  on-tertiary: '#381385'
  tertiary-container: '#6f54bf'
  on-tertiary-container: '#ebe1ff'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#eaddff'
  primary-fixed-dim: '#d2bbff'
  on-primary-fixed: '#25005a'
  on-primary-fixed-variant: '#5a00c6'
  secondary-fixed: '#acedff'
  secondary-fixed-dim: '#4cd7f6'
  on-secondary-fixed: '#001f26'
  on-secondary-fixed-variant: '#004e5c'
  tertiary-fixed: '#e8ddff'
  tertiary-fixed-dim: '#cebdff'
  on-tertiary-fixed: '#21005e'
  on-tertiary-fixed-variant: '#4f319c'
  background: '#121222'
  on-background: '#e3e0f8'
  surface-variant: '#333345'
typography:
  display-lg:
    fontFamily: sora
    fontSize: 48px
    fontWeight: '600'
    lineHeight: 56px
  display-lg-mobile:
    fontFamily: sora
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-lg:
    fontFamily: sora
    fontSize: 32px
    fontWeight: '500'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: sora
    fontSize: 24px
    fontWeight: '500'
    lineHeight: 32px
  headline-md:
    fontFamily: sora
    fontSize: 22px
    fontWeight: '500'
    lineHeight: 30px
  headline-sm:
    fontFamily: sora
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
  body-lg:
    fontFamily: inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
  body-md:
    fontFamily: inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
  body-sm:
    fontFamily: inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
  label-code-md:
    fontFamily: jetbrainsMono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
  label-code-sm:
    fontFamily: jetbrainsMono
    fontSize: 11px
    fontWeight: '400'
    lineHeight: 16px
  pill-tag:
    fontFamily: jetbrainsMono
    fontSize: 10px
    fontWeight: '600'
    lineHeight: 12px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  space-2xs: 0.25rem
  space-xs: 0.5rem
  space-sm: 0.75rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
  space-2xl: 3rem
  space-3xl: 4rem
  gutter-mobile: 1rem
  gutter-desktop: 1.5rem
  margin-mobile: 1.25rem
  margin-desktop: 3rem
---

## Brand & Style

This design system channels the precision of an ultra-modern celestial observatory combined with the mystique of esoteric divination. It is designed for an audience seeking elevated, analytical, and aesthetically profound astrological and tarot readings powered by artificial intelligence.

The visual style is **Glassmorphism fused with Cosmic Minimalist Futurism**. The interface evokes deep-space observation platforms: light-refracting optical lenses, low-illumination navigation displays, and hyper-refined luminous instrumentation. Surfaces mimic frosted telescope sight-glasses layered over infinite vacuum, preventing visual noise while framing ethereal data visualizations, AI-driven symbolic traces, and interactive celestial charts.

## Colors

The palette is rooted in the void of deep space, accented by chromatic nebulas and classical esoteric archetypes.

### Core Canvas & Accents
- **Canvas / Void Background**: `#0a0a1a` (deep navy-black)
- **Primary Mystic Indigo**: `#7c3aed` (symbolic insight, primary interactive state anchor)
- **Secondary Cyan Glow**: `#06b6d4` (clarity, celestial vector links)
- **Tertiary Nebula Violet**: `#a78bfa` (spiritual glow, luminous highlights)
- **Luminous Gradient Accent**: Linear from `#a78bfa` to `#06b6d4` (ambient strokes, active headers, glyph trails)
- **Interactive Action Gradient**: 135deg linear from `#7c3aed` to `#2563eb` (primary triggers, high-order decisions)

### Elemental Quadrants
To articulate astrological modalities and tarot suits with high specificity, four distinct elemental tokens govern contextual cards, glyphs, and micro-accents:
- **Fire**: `#FF6B35` (Aries, Leo, Sagittarius; Wands) — warm radiant solar energy.
- **Earth**: `#8B7355` (Taurus, Virgo, Capricorn; Pentacles) — grounded bronze-ochre mineral hue.
- **Air**: `#87CEEB` (Gemini, Libra, Aquarius; Swords) — ethereal atmospheric sky-glow.
- **Water**: `#4169E1` (Cancer, Scorpio, Pisces; Cups) — abyssal oceanic royal sapphire.

### Surface Tokens
- **Glass Base**: `rgba(255, 255, 255, 0.03)`
- **Glass Hover**: `rgba(255, 255, 255, 0.05)`
- **Glass Active / Selected**: `rgba(255, 255, 255, 0.08)`
- **Border Rim**: `rgba(255, 255, 255, 0.08)`
- **Border Rim Luminous**: `rgba(167, 139, 250, 0.25)`

## Typography

Typography establishes an intentional tension between cosmic grandeur and technical observability:

- **Display & Headlines (`Sora`)**: Curvature with geometric precision mirrors astronomical instruments, planetary rings, and clean optical charts. Large display headings employ soft, diffused text-shadow glows (`0 0 24px rgba(167, 139, 250, 0.35)`).
- **Body (`Inter`)**: High-legibility, distraction-free neutral sans-serif designed for continuous reading of complex astrological delineations, transit overviews, and card spread interpretations.
- **Symbolic Reasoning & Data (`JetBrains Mono`)**: Applied to transit coordinates, degree calculations, house classifications, ephemeris data, and AI chain-of-thought traces. Conveys computational fidelity and arcane logic.

## Layout & Spacing

The layout is built on a responsive 12-column dynamic grid system engineered for analytical dashboards and multi-pane spatial canvases.

### Rhythm & Proportions
- Spacing follows an absolute 4px/8px base cadence. 
- Component internal paddings default to `1.5rem` (`24px`) for primary observatory panels and `1rem` (`16px`) for micro-widgets.
- Card gaps maintain a rigid `1.5rem` (`24px`) interval on desktop displays to allow glass edge refraction to breathe without visual collisions.

### Responsive Behavior
- **Desktop (> 1200px)**: 12 columns, `1.5rem` gutters, `3rem` lateral safe margins. Sidebars for houses/aspects are anchored in fixed or collapsible utility columns.
- **Tablet (768px - 1199px)**: 8 columns, `1.25rem` gutters, `2rem` outer margins. Secondary symbolic traces collapse into tabbed navigation layers.
- **Mobile (< 768px)**: 4 columns, `1rem` gutters, `1.25rem` outer margins. Cards stretch edge-to-edge within margins; complex aspect tables convert into stacked vertical glass modules.

## Elevation & Depth

Visual hierarchy does not rely on opaque stacking or harsh drop shadows. Depth is achieved entirely through light diffusion, backdrop filters, and delicate ambient inner glows.

### Elevation Levels

1. **Floor (Base Void)**: `#0a0a1a` void surface, augmented by subtle radial background glows (`radial-gradient(ellipse at top, rgba(124, 58, 237, 0.08), transparent 70%)`).
2. **Level 1 (Glass Container Panels)**:
   - Background: `rgba(255, 255, 255, 0.03)`
   - Border: `1px solid rgba(255, 255, 255, 0.08)`
   - Backdrop Filter: `blur(12px)`
   - Box Shadow: `0 8px 32px 0 rgba(0, 0, 0, 0.37)`
3. **Level 2 (Active Cards & Floating Modules)**:
   - Background: `rgba(255, 255, 255, 0.05)`
   - Border: `1px solid rgba(167, 139, 250, 0.2)`
   - Backdrop Filter: `blur(16px)`
   - Box Shadow: `0 12px 40px 0 rgba(0, 0, 0, 0.5), inset 0 1px 1px 0 rgba(255, 255, 255, 0.1)`
4. **Level 3 (Modals, Overlays, Tarot Inspection Focus)**:
   - Background: `rgba(10, 10, 26, 0.85)`
   - Border: `1px solid rgba(6, 182, 212, 0.3)`
   - Backdrop Filter: `blur(24px)`
   - Box Shadow: `0 20px 60px -10px rgba(0, 0, 0, 0.7), 0 0 30px rgba(124, 58, 237, 0.15)`

### Transition Timing
All surface shifts, elevation changes, border highlight activations, and glow escalations follow a uniform curve:
`transition: all 300ms cubic-bezier(0.16, 1, 0.3, 1)`.

## Shapes

The design system employs a refined medium radius (`roundedness: 2`, `0.5rem` / `8px` base) across structural elements, paired intentionally with high-radius circular and pill geometries for data markers and celestial indices.

- **Standard Cards & Functional Tiles**: `1rem` (`rounded-lg`) corner radius, offering balanced architectural framing.
- **Large Observatory Screens & Modal Canvases**: `1.5rem` (`rounded-xl`) corner radius.
- **Badges, Status Nodes, Element Indicators, Buttons**: `9999px` (Full Pill) to evoke planetary bodies, talismanic stones, and modern luxury aerospace switchgear.
- **Tarot Aspect Cards**: Golden ratio proportions (1:1.618) with a constant `0.75rem` (`12px`) corner radius.

## Components

### Buttons
- **Primary CTA**: Background gradient of `linear-gradient(135deg, #7c3aed, #2563eb)`, text in pure white (`#ffffff`), border `1px solid rgba(255, 255, 255, 0.2)`. Padding `0.75rem 1.5rem`. Pill-shaped. On hover: shadow escalates to `0 0 20px rgba(124, 58, 237, 0.5)`. 300ms ease transition.
- **Ghost Glass Button**: Background `rgba(255, 255, 255, 0.03)`, border `1px solid rgba(255, 255, 255, 0.08)`. On hover: `background: rgba(255, 255, 255, 0.08)`, border color `rgba(167, 139, 250, 0.4)`.

### Elemental Badges & Chips
- Fully pill-shaped (`9999px`), padding `0.25rem 0.75rem`.
- Font: `JetBrains Mono`, uppercase, letter-spacing `0.08em`.
- Tinted glass backgrounds with low-opacity fills (`rgba(color, 0.12)`) and crisp borders (`1px solid rgba(color, 0.35)`). Text matches the respective elemental hex token:
  - *Fire*: Border/text `#FF6B35`
  - *Earth*: Border/text `#8B7355`
  - *Air*: Border/text `#87CEEB`
  - *Water*: Border/text `#4169E1`

### Input Fields & Prompts
- Background: `rgba(255, 255, 255, 0.02)`.
- Border: `1px solid rgba(255, 255, 255, 0.08)`.
- Border-radius: `0.5rem` (`8px`).
- Text color: `#ffffff`; Placeholder: `rgba(255, 255, 255, 0.3)`.
- Focus state: Border transitions to `#06b6d4`, subtle cyan field halo `0 0 16px rgba(6, 182, 212, 0.25)`. Outline is none.

### Checkboxes & Segmented Selectors
- Custom boxes: `18px x 18px`, `4px` border radius.
- Inactive: Border `1px solid rgba(255, 255, 255, 0.15)`, background `rgba(255, 255, 255, 0.02)`.
- Selected: Background `linear-gradient(135deg, #7c3aed, #06b6d4)`, checkmark rendered in clean stark white.

### Lists & Aspect Tables
- Borderless table rows separated by `1px solid rgba(255, 255, 255, 0.04)`.
- Hover state: Row illuminates with `background: rgba(255, 255, 255, 0.02)` and a left border accent `2px solid #a78bfa`.
- Monospace values right-aligned for clean astronomical reading.

### Cards & Observational Panels
- Glassmorphic architecture: Background `rgba(255, 255, 255, 0.03)`, border `1px solid rgba(255, 255, 255, 0.08)`, backdrop-filter `blur(12px)`.
- Top-edge subtle hairline highlight: Inset linear gradient simulating refraction (`inset 0 1px 0 rgba(255, 255, 255, 0.12)`).

### AI Symbolic Reasoning Stream
- Specialized terminal-style component displaying astrological calculation logs.
- Background: `rgba(5, 5, 15, 0.6)`.
- Font: `JetBrains Mono` sm.
- Glowing cyan pulse dot (`6px x 6px`, `#06b6d4`) signifying active real-time AI astronomical inference.