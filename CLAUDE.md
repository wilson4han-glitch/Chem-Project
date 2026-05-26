# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Simulation

No build step required. Open `index.html` directly in a browser:

```
open index.html
```

There is no package manager, bundler, linter, or test framework.

## Architecture

The simulation is a vanilla JS + HTML Canvas app with no dependencies. Scripts must be loaded in order in `index.html` because they rely on globals from earlier files:

```
data.js → particles.js → cell.js → galvanic.js → electrolytic.js → main.js
```

### Class hierarchy

`CellRenderer` (cell.js) is the base class. It owns the canvas, animation loop (`requestAnimationFrame`), particle system, and all shared drawing methods. Subclasses override four getters (`getAnodeHR`, `getCathodeHR`, `getConcAnode`, `getConcCathode`) and `drawCircuitExtras()` to inject mode-specific rendering:

- `GalvanicCell` (galvanic.js) — draws a voltmeter and electron-flow arrow; also calls `_drawThermodynamicsPanel()` (inherited from `CellRenderer`) to display ΔG and K. Depletion (E ≤ 0.002 V) is detected in `CellRenderer._tickConcentrations()`, which sets `this._depleted = true`, stops the loop, and causes `draw()` to render a "BATTERY DEAD" overlay showing equilibrium stats.
- `ElectrolyticCell` (electrolytic.js) — draws a battery and reverses the electron path; overrides `_drawLabels()` to show the element being plated (symbol + full name) and mass deposited via Faraday's law; exposes `getCurrent()` which reads the `electro-current` slider.

`CellRenderer` also provides two shared helpers used by subclasses: `drawVoltmeter(x, y, voltage, label, warn)` (draws a circular gauge with a pulsing ring when voltage is near zero) and `_drawThermodynamicsPanel()` (draws the ΔG / K panel between the beakers).

### Data layer (data.js)

All chemistry lives here. `HALF_REACTIONS` is the global array of electrode data. `calcNernstPotential(cathode, anode, concCathode, concAnode)` handles the Nernst equation using LCM-balanced electron counts for mixed-charge pairs (e.g. Au³⁺ + Cu²⁺); concentrations are floored at `1e-15` internally to prevent `log(0)` when a galvanic cell fully depletes. `getHalfReactionString(hr, isAnode)` generates the display text for half-reactions, falling back to the optional `reductionStr`/`oxidationStr` fields when present (used by H₂).

### Particle system (particles.js)

`ParticleSystem` holds electrons and ions as arrays of `{path, t, speed, ...}` objects. Each particle's position is computed each frame by interpolating `t` (0–1) across its waypoint path. `initParticles()` is called by `CellRenderer.rebuildParticles()` whenever electrode selection changes; it recomputes the electron path (direction flips for electrolytic mode) and the two salt-bridge ion paths.

### Layout

All canvas coordinates are derived from the `LAYOUT` constant at the top of `cell.js`. Change beaker positions or sizes there — everything else derives from it.

### Control wiring (main.js)

`wireControls(cell, prefix)` (defined inside `DOMContentLoaded`) connects play/pause/reset/speed and electrode/concentration controls to a cell instance using the HTML id prefix (`galvanic-` or `electro-`). The electrolytic current slider (`electro-current`) is wired separately in `main.js` outside `wireControls` because it does not trigger a particle rebuild. Adding a new simulation tab means adding a canvas + controls in HTML, instantiating a `CellRenderer` subclass, and calling `wireControls`.

## Worksheet Generator (Python)

`auth_google.py` — run once to complete OAuth2 and save `token.json` (requires `credentials.json` from Google Cloud Console with Docs API enabled).

`write_worksheet.py` — uses the saved token to create a new Google Doc via the Docs API containing the AP Chemistry electrochemistry worksheet. Requires `google-api-python-client`, `google-auth-httplib2`, and `google-auth-oauthlib`.

## Adding a New Simulation

1. Add a new subclass in a new `js/*.js` file extending `CellRenderer`
2. Override `getAnodeHR()`, `getCathodeHR()`, `getConcAnode()`, `getConcCathode()`, `isElectrolytic()`, and `drawCircuitExtras()`
3. Add a `<canvas>` and controls section to `index.html` with a consistent id prefix
4. Add a tab button (`data-tab="<id>-panel"`) and load the new script before `main.js`
5. Instantiate the class in `main.js` and call `wireControls(cell, '<prefix>')`

## Adding a New Electrode

Add an entry to the `HALF_REACTIONS` array in `data.js`. Required fields: `id`, `label`, `E0` (standard reduction potential vs SHE), `ion`, `metal`, `name` (full element name, used in electroplating display), `charge`, `molarMass` (g/mol, used for Faraday mass calculation), `color` (hex, used for electrode bar), `solutionColor` (rgba, used for beaker fill). For gas-evolving electrodes (like H₂), add `type: 'gas'` to suppress electrode shrink/grow animation, and optionally `reductionStr`/`oxidationStr` to override the auto-generated half-reaction strings.
