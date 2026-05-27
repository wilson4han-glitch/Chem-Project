document.addEventListener('DOMContentLoaded', () => {
  // Populate electrode dropdowns
  ['galvanic-anode', 'galvanic-cathode', 'electro-anode', 'electro-cathode'].forEach(id => {
    const sel = document.getElementById(id);
    HALF_REACTIONS.forEach(hr => {
      const opt = document.createElement('option');
      opt.value = hr.id;
      opt.textContent = `${hr.metal}  (${hr.label}, E°=${hr.E0 >= 0 ? '+' : ''}${hr.E0} V)`;
      sel.appendChild(opt);
    });
  });

  // Default selections: Zn | Cu for both tabs
  document.getElementById('galvanic-anode').value   = 'zn';
  document.getElementById('galvanic-cathode').value = 'cu';
  document.getElementById('electro-anode').value    = 'cu';
  document.getElementById('electro-cathode').value  = 'zn';

  // --- Galvanic cell setup ---
  const galvControls = {
    anodeSelect:  document.getElementById('galvanic-anode'),
    cathodeSelect: document.getElementById('galvanic-cathode'),
    concAnode:    document.getElementById('galvanic-conc-anode'),
    concCathode:  document.getElementById('galvanic-conc-cathode'),
    tempSlider:   document.getElementById('galvanic-temp'),
  };
  const galvCanvas = document.getElementById('galvanic-canvas');
  const galvCell = new GalvanicCell(galvCanvas, galvControls);

  // --- Electrolytic cell setup ---
  const electroControls = {
    anodeSelect:  document.getElementById('electro-anode'),
    cathodeSelect: document.getElementById('electro-cathode'),
    concAnode:    document.getElementById('electro-conc-anode'),
    concCathode:  document.getElementById('electro-conc-cathode'),
    current:      document.getElementById('electro-current'),
    tempSlider:   document.getElementById('electro-temp'),
  };
  const electroCanvas = document.getElementById('electro-canvas');
  const electroCell = new ElectrolyticCell(electroCanvas, electroControls);

  // Active cell tracking
  let activeCell = galvCell;

  function rebuildAndDraw(cell) {
    cell.rebuildParticles();
    cell.draw();
  }

  // Initial draw
  galvCell.rebuildParticles();
  galvCell.draw();
  electroCell.rebuildParticles();
  electroCell.draw();

  // Tab switching
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.tab;
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(target).classList.add('active');

      // Stop previous cell, switch active
      activeCell.stop();
      activeCell = target === 'galvanic-panel' ? galvCell : electroCell;
      // Don't auto-start; let user click Play
    });
  });

  // Shared button wiring helper
  function wireControls(cell, prefix) {
    document.getElementById(`${prefix}-play`).addEventListener('click', () => {
      cell.start();
    });
    document.getElementById(`${prefix}-pause`).addEventListener('click', () => cell.stop());
    document.getElementById(`${prefix}-reset`).addEventListener('click', () => {
      cell.stop();
      cell.reset();
      cell.speed = 1.0;
      const speedSlider = document.getElementById(`${prefix}-speed`);
      speedSlider.value = '1.0';
      document.getElementById(`${prefix}-speed-label`).textContent = '1.0×';
      const tempSlider = document.getElementById(`${prefix}-temp`);
      if (tempSlider) {
        tempSlider.value = '25';
        document.getElementById(`${prefix}-temp-label`).textContent = '25°C (298 K)';
      }
      cell.draw();
    });
    document.getElementById(`${prefix}-speed`).addEventListener('input', e => {
      cell.speed = parseFloat(e.target.value);
      document.getElementById(`${prefix}-speed-label`).textContent = parseFloat(e.target.value).toFixed(1) + '×';
    });

    // Rebuild on any control change
    const tempEl  = document.getElementById(`${prefix}-temp`);
    const tempLbl = document.getElementById(`${prefix}-temp-label`);
    if (tempEl && tempLbl) {
      tempEl.addEventListener('input', () => {
        const c = parseInt(tempEl.value);
        tempLbl.textContent = `${c}°C (${c + 273} K)`;
        if (!cell.running) cell.draw();
      });
    }

    [`${prefix}-anode`, `${prefix}-cathode`,
     `${prefix}-conc-anode`, `${prefix}-conc-cathode`].forEach(id => {
      const el = document.getElementById(id);
      if (!el) return;
      el.addEventListener('change', () => { if (cell._depleted) cell.reset(); rebuildAndDraw(cell); if (cell.running) { cell.stop(); cell.start(); } });
      el.addEventListener('input',  () => {
        if (id.includes('conc')) {
          cell._concAccAnode = null;
          cell._concAccCathode = null;
        }
        if (!cell.running) cell.draw();
      });
    });
  }

  wireControls(galvCell,   'galvanic');
  wireControls(electroCell, 'electro');

  // Electrolytic cell: only allow cathodes with lower E° than the anode so the
  // reaction is non-spontaneous and actually requires external power.
  function filterElectroCathodeOptions() {
    const anodeSel   = document.getElementById('electro-anode');
    const cathodeSel = document.getElementById('electro-cathode');
    const anodeHR    = getById(anodeSel.value);
    const prevValue  = cathodeSel.value;

    // Repopulate cathode select — only elements with E0 strictly below the anode's E0.
    cathodeSel.innerHTML = '';
    HALF_REACTIONS
      .filter(hr => !anodeHR || hr.E0 < anodeHR.E0)
      .forEach(hr => {
        const opt = document.createElement('option');
        opt.value = hr.id;
        opt.textContent = `${hr.metal}  (${hr.label}, E°=${hr.E0 >= 0 ? '+' : ''}${hr.E0} V)`;
        cathodeSel.appendChild(opt);
      });

    // Restore previous cathode if it's still in the list; otherwise the first option is selected.
    if ([...cathodeSel.options].some(o => o.value === prevValue)) {
      cathodeSel.value = prevValue;
    }

    if (cathodeSel.value !== prevValue) {
      if (electroCell._depleted) electroCell.reset();
      rebuildAndDraw(electroCell);
      if (electroCell.running) { electroCell.stop(); electroCell.start(); }
    }
  }

  document.getElementById('electro-anode').addEventListener('change', filterElectroCathodeOptions);
  filterElectroCathodeOptions();

  // Current label for electrolytic
  const currentEl = document.getElementById('electro-current');
  const currentLbl = document.getElementById('electro-current-label');
  if (currentEl && currentLbl) {
    currentEl.addEventListener('input', () => {
      currentLbl.textContent = parseFloat(currentEl.value).toFixed(1) + ' A';
    });
  }

  // Concentration value labels
  ['galvanic-conc-anode', 'galvanic-conc-cathode', 'electro-conc-anode', 'electro-conc-cathode'].forEach(id => {
    const el = document.getElementById(id);
    const lbl = document.getElementById(id + '-label');
    if (el && lbl) {
      el.addEventListener('input', () => { lbl.textContent = parseFloat(el.value).toFixed(2) + ' M'; });
    }
  });
});
