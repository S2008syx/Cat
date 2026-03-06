# Human Design Calculator — Documentation

A pure Python computation engine that calculates Human Design chart parameters from UTC birth time. Part 3 of a 4-part system:

```
[Part 2: Input Processing] → [Part 3: Calculator (this module)] → [Part 4: Interpreter]
```

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [API Reference](#api-reference)
  - [calculate()](#calculatebirth_utc-latitude-longitude--calculatoroutput)
  - [calculate_transit()](#calculate_transittransit_utc-natal_gates--dict)
  - [calculate_solar_return()](#calculate_solar_returnbirth_utc-year-latitude-longitude--dict)
- [Architecture](#architecture)
- [Calculation Pipeline](#calculation-pipeline)
- [Advanced Features](#advanced-features)
  - [Color / Tone / Base](#color--tone--base)
  - [Variables / Arrows](#variables--arrows)
  - [Transit Charts](#transit-charts)
  - [Solar Return Charts](#solar-return-charts)
- [Data Tables](#data-tables)
- [Algorithms](#algorithms)
- [Verification](#verification)
- [Testing](#testing)
- [References](#references)

---

## Quick Start

```python
from hd_calculator import calculate
from hd_calculator.transit import calculate_transit
from hd_calculator.solar_return import calculate_solar_return
from datetime import datetime, timezone

# --- Natal Chart ---
result = calculate(
    birth_utc=datetime(1990, 1, 15, 6, 30, tzinfo=timezone.utc),
    latitude=31.2304,
    longitude=121.4737,
)

print(result.type)          # "Generator"
print(result.profile)       # "4/6"
print(result.authority)     # "Emotional"
print(result.strategy)      # "To Respond"
print(result.definition_type)  # "Single"
print(result.defined_centers)  # ["sacral", "solar_plexus", ...]
print(result.variables)     # {"digestion": {"arrow": "Right", ...}, ...}

# Each activation now includes color/tone/base:
sun = result.personality_activations[0]
print(f"Sun: Gate {sun['gate']}.{sun['line']} Color={sun['color']} Tone={sun['tone']} Base={sun['base']}")

# --- Transit (daily planetary weather) ---
transit = calculate_transit(
    transit_utc=datetime(2026, 3, 6, 12, 0, tzinfo=timezone.utc),
    natal_gates=set(result.all_active_gates),
)
print(transit["active_gates"])        # Gates lit up right now
print(transit["completed_channels"])  # Channels completed by transit overlay

# --- Solar Return (annual theme chart) ---
sr = calculate_solar_return(
    birth_utc=datetime(1990, 1, 15, 6, 30, tzinfo=timezone.utc),
    year=2026,
    latitude=31.2304,
    longitude=121.4737,
)
print(sr["return_utc"])        # 2026-01-15 00:16:56 UTC
print(sr["chart"].type)        # Type for 2026
print(sr["chart"].profile)     # Profile for 2026
```

## Installation

```bash
pip install pyswisseph>=2.10.0
```

No other external dependencies. The module uses the **Moshier ephemeris** (built into pyswisseph), so no external ephemeris data files are needed.

## API Reference

### `calculate(birth_utc, latitude, longitude) → CalculatorOutput`

The primary public function. Takes birth data, returns a complete Human Design chart.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `birth_utc` | `datetime` | UTC birth time (must have `tzinfo=timezone.utc`) |
| `latitude` | `float` | Birth place latitude. **Reserved for future use** — does not affect results |
| `longitude` | `float` | Birth place longitude. **Reserved for future use** — does not affect results |

> **Note:** Human Design calculations depend only on UTC time. Latitude/longitude are accepted for interface completeness and potential future Local Sidereal Time features.

#### Returns: `CalculatorOutput`

| Field | Type | Description |
|-------|------|-------------|
| `type` | `str` | `"Generator"`, `"Manifesting Generator"`, `"Manifestor"`, `"Projector"`, or `"Reflector"` |
| `strategy` | `str` | `"To Respond"`, `"To Inform"`, `"To Wait for Invitation"`, or `"To Wait a Lunar Cycle"` |
| `authority` | `str` | `"Emotional"`, `"Sacral"`, `"Splenic"`, `"Ego Manifested"`, `"Ego Projected"`, `"Self-Projected"`, `"Lunar"`, or `"Mental"` |
| `profile` | `str` | Format `"X/Y"` (e.g. `"4/6"`, `"1/3"`) |
| `definition_type` | `str` | `"None"`, `"Single"`, `"Split"`, `"Triple Split"`, or `"Quadruple Split"` |
| `split_type` | `str \| None` | `"Small"` or `"Large"` when `definition_type == "Split"`, otherwise `None` |
| `incarnation_cross_type` | `str` | `"Right Angle"`, `"Juxtaposition"`, or `"Left Angle"` |
| `incarnation_cross_gates` | `list[int]` | `[p_sun_gate, p_earth_gate, d_sun_gate, d_earth_gate]` |
| `defined_centers` | `list[str]` | Centers with active channels passing through them |
| `undefined_centers` | `list[str]` | Centers with no active channels |
| `active_channels` | `list[dict]` | Each: `{"gate_a", "gate_b", "center_a", "center_b"}` |
| `variables` | `dict` | Four arrows: `{"digestion", "environment", "motivation", "perspective"}` each with `{"arrow", "color", "tone"}` |
| `personality_activations` | `list[dict]` | 13 conscious activations: `{"planet", "gate", "line", "color", "tone", "base", "longitude"}` |
| `design_activations` | `list[dict]` | 13 unconscious activations: same structure |
| `design_utc` | `datetime` | Computed design moment (88° Sun regression) |
| `all_active_gates` | `list[int]` | Deduplicated, sorted list of all activated gates |

### `calculate_transit(transit_utc, natal_gates=None) → dict`

Calculates planetary transit activations for any given moment. Import from `hd_calculator.transit`.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `transit_utc` | `datetime` | UTC time for the transit moment |
| `natal_gates` | `set[int] \| None` | Optional natal gate set for overlay analysis |

#### Returns

| Field | Type | Condition | Description |
|-------|------|-----------|-------------|
| `transit_utc` | `datetime` | Always | The transit moment used |
| `activations` | `list[dict]` | Always | 13 planetary activations with gate/line/color/tone/base |
| `active_gates` | `list[int]` | Always | Gates activated by current transits |
| `transit_channels` | `list[dict]` | Always | Channels formed by transit planets alone |
| `transit_defined_centers` | `list[str]` | Always | Centers defined by transit alone |
| `completed_channels` | `list[dict]` | With `natal_gates` | Channels completed by natal + transit overlay |
| `overlay_defined_centers` | `list[str]` | With `natal_gates` | All defined centers after overlay |
| `overlay_undefined_centers` | `list[str]` | With `natal_gates` | Centers still undefined after overlay |

### `calculate_solar_return(birth_utc, year, latitude, longitude) → dict`

Calculates a Solar Return chart — the full HD chart for the precise moment the Sun returns to its natal longitude. Import from `hd_calculator.solar_return`.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `birth_utc` | `datetime` | UTC birth time |
| `year` | `int` | Calendar year for the Solar Return |
| `latitude` | `float` | Birth place latitude (passed to `calculate()`) |
| `longitude` | `float` | Birth place longitude (passed to `calculate()`) |

#### Returns

| Field | Type | Description |
|-------|------|-------------|
| `return_utc` | `datetime` | Exact UTC moment of the Solar Return |
| `return_jd` | `float` | Julian Day of the Solar Return |
| `year` | `int` | Requested year |
| `natal_sun_longitude` | `float` | The natal Sun longitude (target) |
| `chart` | `CalculatorOutput` | Full HD chart for the return moment |

---

## Architecture

### File Structure

```
hd_calculator/
├── __init__.py           # Public API: calculate()
├── models.py             # Data models (CalculatorInput, CalculatorOutput, etc.)
├── ephemeris.py          # Layer 1: Swiss Ephemeris wrapper
├── gate_mapping.py       # Layer 2: Longitude → Gate/Line/Color/Tone/Base mapping
├── chart_properties.py   # Layers 3-6: Channels, Centers, Type, Authority, Variables, etc.
├── transit.py            # Transit chart calculation (daily planetary weather)
├── solar_return.py       # Solar Return chart calculation (annual theme)
├── data/
│   ├── gates.py          # 64-gate sequence table
│   ├── centers.py        # 9 centers with gate assignments
│   └── channels.py       # 36 channel definitions
└── tests/
    └── test_calculator.py  # 32 unit tests
```

### Module Boundary

Three public functions:
- `calculate()` — Natal chart (main entry point)
- `calculate_transit()` — Transit/daily chart (from `hd_calculator.transit`)
- `calculate_solar_return()` — Solar Return/annual chart (from `hd_calculator.solar_return`)

---

## Calculation Pipeline

The calculator runs a 6-layer pipeline:

```
┌─────────────────────────────────────────────────────────────┐
│ INPUT: birth_utc (datetime), latitude, longitude            │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────▼───────────────┐
         │  LAYER 1: Ephemeris           │
         │  UTC → Julian Day → Planets   │
         │  + 88° Sun Regression         │
         │  (Newton-Raphson)             │
         └───────────────┬───────────────┘
                         │ 13 personality positions
                         │ 13 design positions
         ┌───────────────▼───────────────┐
         │  LAYER 2: Gate Mapping        │
         │  Longitude → Gate (1-64)      │
         │           → Line (1-6)        │
         │           → Color (1-6)       │
         │           → Tone (1-6)        │
         │           → Base (1-5)        │
         └───────────────┬───────────────┘
                         │ 26 activations (with subdivisions)
         ┌───────────────▼───────────────┐
         │  LAYER 3: Pattern Matching    │
         │  Gates → Active Channels      │
         │  Channels → Defined Centers   │
         └───────────────┬───────────────┘
                         │ channels + centers
         ┌───────────────▼───────────────┐
         │  LAYER 4: Definition Type     │
         │  BFS Connected Components     │
         │  → None/Single/Split/Triple/  │
         │    Quadruple                  │
         └───────────────┬───────────────┘
                         │
         ┌───────────────▼───────────────┐
         │  LAYER 5: Derived Properties  │
         │  Type, Strategy, Authority,   │
         │  Profile, Incarnation Cross   │
         └───────────────┬───────────────┘
                         │
         ┌───────────────▼───────────────┐
         │  LAYER 6: Variables / Arrows  │
         │  Color/Tone → 4 Arrows        │
         │  (Digestion, Environment,     │
         │   Motivation, Perspective)    │
         └───────────────┬───────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│ OUTPUT: CalculatorOutput (20 fields)                        │
└─────────────────────────────────────────────────────────────┘
```

### Layer 1: Ephemeris (Time → Planet Positions)

**File:** `ephemeris.py`

Converts UTC birth time to planetary positions on the ecliptic using the Swiss Ephemeris (via `pyswisseph`).

**13 celestial bodies computed:**

| Body | Source | Method |
|------|--------|--------|
| Sun | Swiss Ephemeris | Direct query |
| Moon | Swiss Ephemeris | Direct query |
| Mercury–Pluto (8) | Swiss Ephemeris | Direct query |
| North Node | Swiss Ephemeris | Mean Node |
| Earth | Derived | Sun + 180° |
| South Node | Derived | North Node + 180° |

Two sets of positions are computed:
- **Personality** (conscious): Planets at the birth moment
- **Design** (unconscious): Planets at the 88° Sun regression moment

### Layer 2: Gate Mapping (Longitude → Gate/Line/Color/Tone/Base)

**File:** `gate_mapping.py`

Maps each planet's ecliptic longitude to a Human Design gate, line, and sub-line subdivisions.

- The ecliptic (360°) is divided into **64 gates** of **5.625°** each
- Each gate has **6 lines** of **0.9375°** each
- Each line has **6 colors** of **0.15625°** each
- Each color has **6 tones** of **~0.02604°** each
- Each tone has **5 bases** of **~0.00521°** each
- Starting point: **Gate 41 at 302°** (Aquarius 2°)

```
Longitude 302.0° → Gate 41, Line 1, Color 1, Tone 1, Base 1
Longitude 307.625° → Gate 19, Line 1, ...
...wraps around through all 64 gates...
Longitude 301.99° → Gate 60, Line 6, ...
```

### Layer 3: Channels & Centers

**File:** `chart_properties.py`

- **Channel activation:** A channel is defined when BOTH of its gates are activated (from any combination of personality + design planets)
- **Center definition:** A center is defined when at least one channel passes through it

### Layer 4: Definition Type

Uses **BFS connected components** on the graph of defined centers:

| Components | Definition Type |
|------------|----------------|
| 0 | None |
| 1 | Single |
| 2 | Split (Small or Large) |
| 3 | Triple Split |
| 4+ | Quadruple Split |

**Split Size:**
- **Small Split:** A single bridging channel exists in the channel table between the two components
- **Large Split:** No single channel can bridge the gap

### Layer 5: Type, Strategy, Authority, Profile, Cross

**Type determination** (evaluated in order):

| Priority | Condition | Type |
|----------|-----------|------|
| 1 | No defined centers | Reflector |
| 2 | Sacral defined + any motor→throat path | Manifesting Generator |
| 3 | Sacral defined | Generator |
| 4 | Non-sacral motor→throat path | Manifestor |
| 5 | Everything else | Projector |

**Motor centers:** Root, Sacral, Solar Plexus, Heart

**Authority priority chain** (first match wins):

| Priority | Condition | Authority |
|----------|-----------|-----------|
| 1 | Solar Plexus defined | Emotional |
| 2 | Sacral defined | Sacral |
| 3 | Spleen defined | Splenic |
| 4 | Heart defined + direct Throat connection | Ego Manifested |
| 5 | Heart defined | Ego Projected |
| 6 | G defined + direct Throat connection | Self-Projected |
| 7 | Reflector type | Lunar |
| 8 | Else | Mental |

**Strategy** is derived directly from Type:

| Type | Strategy |
|------|----------|
| Generator / Manifesting Generator | To Respond |
| Manifestor | To Inform |
| Projector | To Wait for Invitation |
| Reflector | To Wait a Lunar Cycle |

**Profile:** `"{personality_sun_line}/{design_sun_line}"` (e.g. `"4/6"`)

**Incarnation Cross type** (based on profile first digit):

| First digit | Cross Type |
|-------------|------------|
| 1, 2, 3 | Right Angle |
| 4 | Juxtaposition |
| 5, 6 | Left Angle |

---

## Advanced Features

### Color / Tone / Base

Each planetary activation is subdivided beyond Gate and Line into three additional levels of precision:

```
Gate (5.625°)
 └── Line (0.9375°)          ← 6 per gate
      └── Color (0.15625°)    ← 6 per line
           └── Tone (0.02604°) ← 6 per color
                └── Base (0.00521°) ← 5 per tone
```

These subdivisions are used in advanced Human Design analysis, particularly for deriving Variables (Arrows). The Swiss Ephemeris provides planetary positions with sub-arcsecond precision (~0.001°), which is more than sufficient for Base-level calculations (~0.005°).

### Variables / Arrows

Variables are four directional arrows displayed at the corners of a bodygraph. Each arrow points **Left** (strategic/focused/active) or **Right** (receptive/peripheral/passive).

| Arrow | Position | Source | Domain |
|-------|----------|--------|--------|
| Digestion | Top-Left | Design Sun Color | Body/nutrition |
| Environment | Bottom-Left | Design North Node Color | Physical space |
| Motivation | Top-Right | Personality Sun Color | Mental driver |
| Perspective | Bottom-Right | Personality North Node Color | Awareness |

**Direction rule:** Color 1-3 → Left, Color 4-6 → Right.

Each Variable also carries a Tone value (1-6) that further specifies the quality:

| Tone | Quality |
|------|---------|
| 1 | Smell / Certainty |
| 2 | Taste / Uncertainty |
| 3 | Outer Vision / Action |
| 4 | Inner Vision / Meditation |
| 5 | Feeling / Judgment |
| 6 | Touch / Acceptance |

### Transit Charts

Transit charts calculate the "daily planetary weather" — which gates and channels are activated by the current positions of the 13 celestial bodies.

**Standalone mode:** Shows which gates/channels/centers are collectively activated right now. This affects everyone — it is the background energy field.

**Overlay mode:** When combined with a natal chart, shows which dormant natal gates become "completed" by transiting planets, temporarily forming new channels and defining new centers.

Example: A person has natal Gate 6 (Solar Plexus) but not Gate 59 (Sacral). If transit Mars activates Gate 59, the 6-59 channel is temporarily completed, defining both centers for the duration of the transit.

### Solar Return Charts

A Solar Return chart is calculated for the precise moment each year when the Sun returns to its exact natal ecliptic longitude.

**How it works:**
1. Find the person's natal Sun longitude (e.g., 294.8449°)
2. Use Newton-Raphson iteration to find the exact Julian Day in the target year when the Sun reaches that longitude again
3. Calculate a full Human Design chart for that moment

**What changes year to year:**
- The Sun gate stays the same (same longitude), but its Line/Color/Tone/Base may differ slightly
- All other planets (Moon, Mercury, Venus, etc.) are at completely different positions
- This produces different channels, centers, Type, Authority, Profile, and Variables
- The resulting chart describes the energetic theme for that year

**Practical use:** Compare the Solar Return chart against the natal chart to identify which themes, centers, and channels are "active" for the year — similar to a detailed annual horoscope but based on Human Design mechanics.

---

## Data Tables

### Gate Order (64 gates)

The mandala wheel sequence starting at Gate 41 (302°):

```
41, 19, 13, 49, 30, 55, 37, 63,
22, 36, 25, 17, 21, 51, 42,  3,
27, 24,  2, 23,  8, 20, 16, 35,
45, 12, 15, 52, 39, 53, 62, 56,
31, 33,  7,  4, 29, 59, 40, 64,
47,  6, 46, 18, 48, 57, 32, 50,
28, 44,  1, 43, 14, 34,  9,  5,
26, 11, 10, 58, 38, 54, 61, 60,
```

### 9 Centers

| Center | Gates |
|--------|-------|
| Head | 64, 61, 63 |
| Ajna | 47, 24, 4, 17, 43, 11 |
| Throat | 62, 23, 56, 8, 31, 35, 45, 33, 20, 16, 12 |
| G | 1, 7, 13, 25, 46, 2, 15, 10 |
| Heart | 21, 51, 26, 40 |
| Sacral | 5, 14, 29, 34, 27, 42, 3, 9, 59 |
| Solar Plexus | 36, 6, 37, 49, 55, 30, 22 |
| Spleen | 57, 44, 50, 48, 18, 28, 32 |
| Root | 53, 60, 52, 19, 39, 41, 58, 38, 54 |

### 36 Channels

```
Head ↔ Ajna:           64-47, 61-24, 63-4
Ajna ↔ Throat:         17-62, 43-23, 11-56
Throat ↔ G:            8-1, 31-7, 33-13, 20-10
Throat ↔ Heart:        45-21
Throat ↔ Solar Plexus: 35-36, 12-22
Throat ↔ Sacral:       20-34
Throat ↔ Spleen:       20-57, 16-48
G ↔ Sacral:            15-5, 2-14, 46-29, 10-34
G ↔ Spleen:            10-57
G ↔ Heart:             25-51
Heart ↔ Spleen:        26-44
Heart ↔ Solar Plexus:  40-37
Sacral ↔ Solar Plexus: 59-6
Sacral ↔ Spleen:       27-50, 34-57
Sacral ↔ Root:         42-53, 3-60, 9-52
Solar Plexus ↔ Root:   49-19, 55-39, 30-41
Spleen ↔ Root:         18-58, 28-38, 32-54
```

---

## Algorithms

### 88° Sun Regression (Newton-Raphson)

Finds the moment when the Sun was exactly 88° behind its birth position:

```
1. target_lon = (birth_sun_lon − 88°) mod 360°
2. Initial estimate: birth_jd − 88 days
3. Iterate (max 50):
   a. Get Sun longitude & speed at current estimate
   b. diff = shortest_arc(current_lon, target_lon)
   c. If |diff| < 0.0001°: converged ✓
   d. Else: estimate += diff / sun_speed
```

Convergence precision: < 0.36 arcseconds. Typically converges in 3-5 iterations.

### Longitude → Gate/Line/Color/Tone/Base Mapping

```
1. offset = (longitude − 302°) mod 360°
2. gate_index = floor(offset / 5.625°)          → 0..63
3. remainder = offset − gate_index × 5.625°
4. line = floor(remainder / 0.9375°) + 1         → 1..6
5. remainder -= (line - 1) × 0.9375°
6. color = floor(remainder / 0.15625°) + 1       → 1..6
7. remainder -= (color - 1) × 0.15625°
8. tone = floor(remainder / 0.026042°) + 1       → 1..6
9. remainder -= (tone - 1) × 0.026042°
10. base = floor(remainder / 0.005208°) + 1      → 1..5
11. gate = GATE_ORDER[gate_index]                 → 1..64
```

### Variables / Arrows Derivation

```
1. Get Color value from Design Sun activation     → Digestion arrow
2. Get Color value from Design North Node          → Environment arrow
3. Get Color value from Personality Sun             → Motivation arrow
4. Get Color value from Personality North Node      → Perspective arrow
5. For each: Color 1-3 = Left, Color 4-6 = Right
```

### Connected Components (Definition Type)

Standard BFS on an adjacency graph built from active channels. Each connected component of defined centers forms one "definition."

### Solar Return (Newton-Raphson)

Finds the precise moment when the Sun returns to its natal longitude in a target year:

```
1. target_lon = natal Sun longitude
2. Initial estimate: birth_jd + (year − birth_year) × 365.2422
3. Iterate (max 50):
   a. Get Sun longitude & speed at current estimate
   b. diff = shortest_arc(current_lon, target_lon)
   c. If |diff| < 0.0001°: converged ✓
   d. Else: estimate += diff / sun_speed
```

Same convergence characteristics as the 88° regression: < 0.36 arcseconds, typically 3-5 iterations.

---

## Verification

Calculator results verified against published celebrity charts:

### Angelina Jolie
**Birth:** June 4, 1975, 9:09 AM, Los Angeles (PDT → 16:09 UTC)

| Property | Expected | Calculator |
|----------|----------|------------|
| Type | Manifesting Generator | Manifesting Generator ✓ |
| Profile | 3/5 | 3/5 ✓ |
| Authority | Emotional | Emotional ✓ |
| Definition | Split | Split ✓ |
| Cross Type | Right Angle | Right Angle ✓ |
| Cross Gates | 35/5 \| 63/64 | [35, 5, 63, 64] ✓ |

### Barack Obama
**Birth:** August 4, 1961, 7:24 PM, Honolulu (HST → 05:24 UTC Aug 5)

| Property | Expected | Calculator |
|----------|----------|------------|
| Type | Projector | Projector ✓ |
| Profile | 6/2 | 6/2 ✓ |
| Authority | Emotional | Emotional ✓ |
| Definition | Single | Single ✓ |
| Cross Type | Left Angle | Left Angle ✓ |
| Cross Gates | 33/19 \| 2/1 | [33, 19, 2, 1] ✓ |

---

## Testing

Run the test suite:

```bash
python -m pytest hd_calculator/tests/test_calculator.py -v
```

**32 tests** organized in 6 test classes:

| Class | Tests | Coverage |
|-------|-------|----------|
| `TestLongitudeToGateLine` | 7 | Gate/line mapping, boundaries, 0°/360° wrap |
| `TestDesignJD` | 2 | 88° regression timing and accuracy |
| `TestDetermineType` | 6 | All 5 types including indirect paths |
| `TestDetermineAuthority` | 8 | All 8 authority types |
| `TestDefinitionType` | 3 | None, Single, Split |
| `TestFullCalculation` | 6 | End-to-end with real dates, structure validation |

---

## References

### Open Source Projects Referenced

- [PyHD](https://pascal.polleunus.be/blog/learning-human-design-by-building-a-python-library) — 88° Sun regression algorithm
- [SharpAstrology.HumanDesign](https://github.com/CReizner/SharpAstrology.HumanDesign) — Type/Authority determination, channel/center data
- [hdkit](https://github.com/jdempcy/hdkit) — Gate order table, center definitions
- [humandesign_api](https://github.com/dturkuler/humandesign_api) — Gate mapping formula, incarnation cross logic
- [human_design_engine](https://github.com/MicFell/human_design_engine) — Gate mapping verification
- [MCP_Human_design](https://github.com/dvvolkovv/MCP_Human_design) — Type determination logic

### External Libraries

- [pyswisseph](https://github.com/astrorigin/pyswisseph) (≥2.10.0) — Python binding for the Swiss Ephemeris

---

## License

This calculator module is part of the Cat project.
