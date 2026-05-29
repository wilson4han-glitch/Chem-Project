// Shared layout constants
const LAYOUT = {
  canvasW: 860,
  canvasH: 480,
  leftBeaker:  { x: 90,  y: 120, w: 180, h: 220 },
  rightBeaker: { x: 590, y: 120, w: 180, h: 220 },
  saltBridge: { y: 150, h: 40 },   // y-top of bridge tube
  electrodeW: 18,
  electrodeH: 160,
};

class CellRenderer {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.particles = new ParticleSystem();
    this.running = false;
    this.rafId = null;
    this.speed = 1.0;
    this.elapsedTime = 0;
    this.realTime = 0;          // FIXED: unscaled seconds, for Faraday mass calculation
    this._concSnapshot = null;
    this._concAccAnode = null;
    this._concAccCathode = null;
    this.anodeElectrodeH = LAYOUT.electrodeH;
    this.cathodeElectrodeH = LAYOUT.electrodeH;
    this.lastTs = null;
    this._depleted = false;
    this._exhausted = false;
  }

  // Subclasses override
  getAnodeHR()   { return null; }
  getCathodeHR() { return null; }
  getConcAnode() {
    if (this._concAccAnode !== null) return this._concAccAnode;
    return this.controls ? parseFloat(this.controls.concAnode.value) : 1.0;
  }
  getConcCathode() {
    if (this._concAccCathode !== null) return this._concAccCathode;
    return this.controls ? parseFloat(this.controls.concCathode.value) : 1.0;
  }
  isElectrolytic() { return false; }
  getCurrent()     { return 2.0; }
  // Subclasses override to block the animation loop under specific conditions.
  canAdvance()     { return true; }

  getTempK() {
    if (this.controls && this.controls.tempSlider) {
      return parseFloat(this.controls.tempSlider.value) + 273.15;
    }
    return 298.15;
  }

  reset() {
    this.elapsedTime = 0;
    this.realTime = 0;          // FIXED: unscaled wall-clock seconds, used by Faraday calculation
    this.anodeElectrodeH = LAYOUT.electrodeH;
    this.cathodeElectrodeH = LAYOUT.electrodeH;
    this._concAccAnode = null;
    this._concAccCathode = null;
    this._depleted = false;
    this._exhausted = false;
    this._restoreConcentrations();
    this.rebuildParticles();
  }

  _initAccumulators() {
    if (!this.controls) return;
    this._concAccAnode   = parseFloat(this.controls.concAnode.value);
    this._concAccCathode = parseFloat(this.controls.concCathode.value);
  }

  rebuildParticles() {
    const anode = this.getAnodeHR();
    const cathode = this.getCathodeHR();
    if (!anode || !cathode) return;

    const lb = LAYOUT.leftBeaker;
    const rb = LAYOUT.rightBeaker;

    // Electron path: anode electrode top -> left wire -> top wire -> right wire -> cathode electrode top
    // Galvanic: left=anode, right=cathode  |  Electrolytic: reversed
    const anodeTopX = lb.x + lb.w / 2;
    const cathodeTopX = rb.x + rb.w / 2;
    const wireY = lb.y - 55;

    let electronPath;
    if (!this.isElectrolytic()) {
      electronPath = [
        { x: anodeTopX, y: lb.y + 30 },
        { x: anodeTopX, y: wireY },
        { x: cathodeTopX, y: wireY },
        { x: cathodeTopX, y: rb.y + 30 },
      ];
    } else {
      // reversed direction for electrolytic
      electronPath = [
        { x: cathodeTopX, y: rb.y + 30 },
        { x: cathodeTopX, y: wireY },
        { x: anodeTopX, y: wireY },
        { x: anodeTopX, y: lb.y + 30 },
      ];
    }

    // Salt bridge: cations move toward cathode (right), anions toward anode (left)
    const bridgeY = LAYOUT.saltBridge.y + LAYOUT.saltBridge.h / 2;
    const bridgeLeftX  = lb.x + lb.w;
    const bridgeRightX = rb.x;
    const cationPath = [
      { x: bridgeLeftX + 10,  y: bridgeY - 6 },
      { x: (bridgeLeftX + bridgeRightX) / 2, y: bridgeY - 10 },
      { x: bridgeRightX - 10, y: bridgeY - 6 },
    ];
    const anionPath = [
      { x: bridgeRightX - 10, y: bridgeY + 6 },
      { x: (bridgeLeftX + bridgeRightX) / 2, y: bridgeY + 10 },
      { x: bridgeLeftX + 10,  y: bridgeY + 6 },
    ];

    this.electronPath = electronPath;
    this.particles.initParticles(electronPath, cationPath, anionPath, anode, cathode, 8, this.speed);
  }

  start() {
    if (this._depleted || this._exhausted) return;
    if (this.elapsedTime === 0) this._snapshotConcentrations();
    // FIXED: only initialise accumulators when null (fresh start or after reset/conc change).
    // Calling _initAccumulators() unconditionally would overwrite mid-run accumulated
    // concentrations every time start() is called (e.g. stop → play, or electrode change
    // while running), discarding all progress.
    if (this._concAccAnode === null) this._initAccumulators();
    if (this.rafId) cancelAnimationFrame(this.rafId);
    this.running = true;
    this.lastTs = performance.now();
    this.rafId = requestAnimationFrame(t => this._loop(t));
  }

  stop() {
    this.running = false;
    if (this.rafId) {
      cancelAnimationFrame(this.rafId);
      this.rafId = null;
    }
  }

  _loop(ts) {
    if (!this.running) return;
    if (!this.canAdvance()) {
      this.running = false;
      this.rafId = null;
      this.draw();
      return;
    }
    const dt = Math.min((ts - this.lastTs) / 16.67, 3);
    this.lastTs = ts;
    this.elapsedTime += (dt * this.speed) / 60;
    this.realTime += dt / 60;
    this.particles.update(dt * this.speed);
    this._updateElectrodes(dt);
    this._tickConcentrations(dt);
    this.draw();
    this.rafId = requestAnimationFrame(t => this._loop(t));
  }

  _updateElectrodes(dt) {
    const delta = 0.004 * dt * this.speed;
    const anode   = this.getAnodeHR();
    const cathode = this.getCathodeHR();
    if (!anode   || anode.type   !== 'gas') this.anodeElectrodeH   = Math.max(20, this.anodeElectrodeH - delta);
    if (!cathode || cathode.type !== 'gas') this.cathodeElectrodeH = Math.min(LAYOUT.electrodeH * 1.6, this.cathodeElectrodeH + delta);
  }

  draw() {
    const ctx = this.ctx;
    const { canvasW, canvasH } = LAYOUT;
    ctx.clearRect(0, 0, canvasW, canvasH);

    this._drawBackground();
    this._drawSaltBridge();
    this._drawWires();
    this._drawBeakers();
    this._drawElectrodes();
    this.drawCircuitExtras(); // voltmeter or battery — subclass
    this.particles.draw(ctx);
    this._drawLabels();
    this._drawTimer();
    if (this._depleted)  this._drawDepletedOverlay();
    if (this._exhausted) this._drawExhaustedOverlay();
  }

  _drawDepletedOverlay() {
    const ctx = this.ctx;
    const { canvasW, canvasH } = LAYOUT;
    const cx = canvasW / 2;

    ctx.fillStyle = 'rgba(0,0,0,0.72)';
    ctx.fillRect(0, 0, canvasW, canvasH);

    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    // Heading
    ctx.fillStyle = '#66bb6a';
    ctx.font = 'bold 34px sans-serif';
    ctx.fillText('EQUILIBRIUM REACHED', cx, canvasH / 2 - 80);

    // Subheading
    ctx.fillStyle = 'rgba(180,210,255,0.9)';
    ctx.font = '15px monospace';
    ctx.fillText('E = 0.000 V  ·  ΔG = 0  ·  No net reaction', cx, canvasH / 2 - 46);

    // Divider
    ctx.strokeStyle = 'rgba(102,187,106,0.4)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(cx - 200, canvasH / 2 - 26);
    ctx.lineTo(cx + 200, canvasH / 2 - 26);
    ctx.stroke();

    const a = this.getAnodeHR();
    const c = this.getCathodeHR();
    if (a && c) {
      // K value
      const n    = lcm(a.charge, c.charge);
      const E0   = calcStandardCellPotential(c, a);
      const Kexp = (n * E0) / calcNernstFactor(this.getTempK());
      let Kstr;
      if      (Kexp >  300) Kstr = '≫ 1';
      else if (Kexp < -300) Kstr = '≪ 1';
      else {
        let expFloor = Math.floor(Kexp);
        let mantissa = Math.pow(10, Kexp - expFloor);
        if (parseFloat(mantissa.toFixed(2)) >= 10) { mantissa /= 10; expFloor += 1; }
        Kstr = `${mantissa.toFixed(2)} × 10^${expFloor}`;
      }

      ctx.fillStyle = 'rgba(255,236,130,0.95)';
      ctx.font = 'bold 15px monospace';
      ctx.fillText(`Q = K = ${Kstr}`, cx, canvasH / 2 - 4);

      // Final equilibrium concentrations
      const concA = Math.max(this.getConcAnode(),   1e-15);
      const concC = Math.max(this.getConcCathode(), 1e-15);
      const concAstr = concA < 0.001 ? concA.toExponential(2) : concA.toFixed(4);
      const concCstr = concC < 0.001 ? concC.toExponential(2) : concC.toFixed(4);

      ctx.fillStyle = 'rgba(180,210,255,0.85)';
      ctx.font = '13px monospace';
      ctx.fillText(`[${a.ion}]eq = ${concAstr} M   [${c.ion}]eq = ${concCstr} M`, cx, canvasH / 2 + 24);
    }

    // Footer
    ctx.fillStyle = 'rgba(170,170,170,0.7)';
    ctx.font = '13px sans-serif';
    ctx.fillText('The driving force is exhausted — press Reset to restart', cx, canvasH / 2 + 58);
    ctx.textBaseline = 'alphabetic';
  }

  _drawExhaustedOverlay() {
    const ctx = this.ctx;
    const { canvasW, canvasH } = LAYOUT;
    const cx = canvasW / 2;

    ctx.fillStyle = 'rgba(0,0,0,0.72)';
    ctx.fillRect(0, 0, canvasW, canvasH);

    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    ctx.fillStyle = '#ffa726';
    ctx.font = 'bold 34px sans-serif';
    ctx.fillText('SOLUTION EXHAUSTED', cx, canvasH / 2 - 80);

    ctx.fillStyle = 'rgba(180,210,255,0.9)';
    ctx.font = '15px monospace';
    ctx.fillText('Cathode ions fully depleted — plating stops', cx, canvasH / 2 - 46);

    ctx.strokeStyle = 'rgba(255,167,38,0.4)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(cx - 200, canvasH / 2 - 26);
    ctx.lineTo(cx + 200, canvasH / 2 - 26);
    ctx.stroke();

    const a = this.getAnodeHR();
    const c = this.getCathodeHR();
    if (a && c) {
      const concA = this.getConcAnode();
      const concC = this.getConcCathode();
      ctx.fillStyle = 'rgba(180,210,255,0.85)';
      ctx.font = '13px monospace';
      ctx.fillText(
        `[${a.ion}] = ${concA.toFixed(4)} M   [${c.ion}] ≈ 0 M`,
        cx, canvasH / 2 - 4
      );

      if (this.realTime !== undefined) {
        const cathode = c;
        const mass = (cathode.molarMass * this.getCurrent() * this.realTime) / (cathode.charge * 96485);
        ctx.fillStyle = 'rgba(255,224,130,0.95)';
        ctx.font = 'bold 15px monospace';
        ctx.fillText(`Total deposited: ${mass.toFixed(4)} g of ${cathode.metal}`, cx, canvasH / 2 + 24);
      }
    }

    ctx.fillStyle = 'rgba(170,170,170,0.7)';
    ctx.font = '13px sans-serif';
    ctx.fillText('No ions remain to reduce — press Reset to restart', cx, canvasH / 2 + 58);
    ctx.textBaseline = 'alphabetic';
  }

  _drawBackground() {
    const ctx = this.ctx;
    ctx.fillStyle = '#1a1a2e';
    ctx.fillRect(0, 0, LAYOUT.canvasW, LAYOUT.canvasH);
  }

  _drawBeakers() {
    const ctx = this.ctx;
    const anode = this.getAnodeHR();
    const cathode = this.getCathodeHR();
    [
      { b: LAYOUT.leftBeaker,  hr: anode,   label: 'Anode' },
      { b: LAYOUT.rightBeaker, hr: cathode, label: 'Cathode' },
    ].forEach(({ b, hr, label }) => {
      // solution fill
      ctx.fillStyle = hr ? hr.solutionColor : 'rgba(100,150,200,0.3)';
      ctx.fillRect(b.x + 3, b.y + 3, b.w - 6, b.h - 6);

      // beaker outline
      ctx.strokeStyle = 'rgba(200,230,255,0.7)';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(b.x, b.y);
      ctx.lineTo(b.x, b.y + b.h);
      ctx.lineTo(b.x + b.w, b.y + b.h);
      ctx.lineTo(b.x + b.w, b.y);
      ctx.stroke();

      // label
      ctx.fillStyle = 'rgba(200,230,255,0.7)';
      ctx.font = '13px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(label, b.x + b.w / 2, b.y + b.h + 20);

      // ion concentration
      if (hr) {
        ctx.fillStyle = 'rgba(180,210,255,0.6)';
        ctx.font = '11px sans-serif';
        const conc = label === 'Anode' ? this.getConcAnode() : this.getConcCathode();
        ctx.fillText(`[${hr.ion}] = ${conc.toFixed(2)} M`, b.x + b.w / 2, b.y + b.h + 36);
      }
    });
  }

  _drawElectrodes() {
    const ctx = this.ctx;
    const anode = this.getAnodeHR();
    const cathode = this.getCathodeHR();
    const lb = LAYOUT.leftBeaker;
    const rb = LAYOUT.rightBeaker;
    const ew = LAYOUT.electrodeW;

    // Anode (left) — shrinks
    const ax = lb.x + lb.w / 2 - ew / 2;
    const aH = this.anodeElectrodeH;
    const aY = lb.y + 10;
    ctx.fillStyle = anode ? anode.color : '#aaa';
    ctx.fillRect(ax, aY, ew, aH);
    ctx.strokeStyle = 'rgba(255,255,255,0.25)';
    ctx.lineWidth = 1;
    ctx.strokeRect(ax, aY, ew, aH);
    if (anode) {
      ctx.fillStyle = 'rgba(255,255,255,0.85)';
      ctx.font = 'bold 12px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(anode.metal, lb.x + lb.w / 2, aY - 8);
    }

    // Cathode (right) — grows, clamped so it never extends below the beaker wall
    const cY = rb.y + 10;
    const cH = Math.min(this.cathodeElectrodeH, rb.y + rb.h - cY - 2);
    const cx = rb.x + rb.w / 2 - ew / 2;
    ctx.fillStyle = cathode ? cathode.color : '#aaa';
    ctx.fillRect(cx, cY, ew, cH);
    ctx.strokeStyle = 'rgba(255,255,255,0.25)';
    ctx.lineWidth = 1;
    ctx.strokeRect(cx, cY, ew, cH);
    if (cathode) {
      ctx.fillStyle = 'rgba(255,255,255,0.85)';
      ctx.font = 'bold 12px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(cathode.metal, rb.x + rb.w / 2, cY - 8);
    }
  }

  _drawSaltBridge() {
    const ctx = this.ctx;
    const lb = LAYOUT.leftBeaker;
    const rb = LAYOUT.rightBeaker;
    const by = LAYOUT.saltBridge.y;
    const bh = LAYOUT.saltBridge.h;
    const x1 = lb.x + lb.w;
    const x2 = rb.x;

    // tube background
    ctx.fillStyle = 'rgba(230,200,120,0.25)';
    ctx.fillRect(x1, by, x2 - x1, bh);

    // tube outline
    ctx.strokeStyle = 'rgba(230,200,120,0.7)';
    ctx.lineWidth = 2;
    ctx.strokeRect(x1, by, x2 - x1, bh);

    // label
    ctx.fillStyle = 'rgba(230,200,120,0.8)';
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Salt Bridge', (x1 + x2) / 2, by - 8);
  }

  _drawWires() {
    const ctx = this.ctx;
    const lb = LAYOUT.leftBeaker;
    const rb = LAYOUT.rightBeaker;
    const wireY = lb.y - 55;
    const lx = lb.x + lb.w / 2;
    const rx = rb.x + rb.w / 2;

    ctx.strokeStyle = '#ccc';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(lx, lb.y + 10);
    ctx.lineTo(lx, wireY);
    ctx.lineTo(rx, wireY);
    ctx.lineTo(rx, rb.y + 10);
    ctx.stroke();
  }

  // Subclass draws voltmeter or battery here
  drawCircuitExtras() {}

  _drawLabels() {
    const ctx = this.ctx;
    const anode = this.getAnodeHR();
    const cathode = this.getCathodeHR();
    if (!anode || !cathode) return;

    // Half-reaction strings at bottom
    ctx.fillStyle = 'rgba(180,210,255,0.8)';
    ctx.font = '12px monospace';
    ctx.textAlign = 'center';

    const lb = LAYOUT.leftBeaker;
    const rb = LAYOUT.rightBeaker;
    ctx.fillText(getHalfReactionString(anode, true),  lb.x + lb.w / 2, lb.y + lb.h + 55);
    ctx.fillText(getHalfReactionString(cathode, false), rb.x + rb.w / 2, rb.y + rb.h + 55);

    // Oxidation / Reduction arrows
    ctx.fillStyle = '#ef5350';
    ctx.font = 'bold 11px sans-serif';
    ctx.fillText('OXIDATION', lb.x + lb.w / 2, lb.y - 25);
    ctx.fillStyle = '#42a5f5';
    ctx.fillText('REDUCTION', rb.x + rb.w / 2, rb.y - 25);
  }

  _tickConcentrations(dt) {
    if (!this.controls) return;
    const { concAnode, concCathode } = this.controls;
    if (!concAnode || !concCathode) return;
    if (this._concAccAnode === null) this._initAccumulators();

    const anode   = this.getAnodeHR();
    const cathode = this.getCathodeHR();
    if (!anode || !cathode) return;

    const rate = 0.004 * dt * this.speed;

    if (this.isElectrolytic()) {
      const anodeMax    = parseFloat(concAnode.max)   || 2.0;
      const cathodeMin  = parseFloat(concCathode.min) || 0.01;
      const currentScale = this.getCurrent() / 2.0;
      const newAnode   = this._concAccAnode   + rate * currentScale;
      const newCathode = this._concAccCathode - rate * currentScale;
      if (newCathode < cathodeMin) {
        this._concAccCathode = cathodeMin;
        this._exhausted = true;
        this.stop();
        return;
      }
      if (newAnode > anodeMax) return;
      this._concAccAnode   = newAnode;
      this._concAccCathode = newCathode;
    } else {
      const E = calcNernstPotential(cathode, anode, this._concAccCathode, this._concAccAnode, this.getTempK());
      // Deplete when voltage reaches zero (low-K cells) OR when the cathode
      // reactant is fully consumed (high-K cells like Zn/Cu whose internal
      // concentration floor keeps E >> 0.002 V even after the reactant is gone).
      if (E <= 0.002 || this._concAccCathode <= 0) {
        this._depleted = true;
        this.stop();
      } else {
        const anodeMax = parseFloat(concAnode.max) || 2.0;
        this._concAccAnode   = Math.min(this._concAccAnode + rate * E, anodeMax);
        this._concAccCathode = Math.max(this._concAccCathode - rate * E, 0);
      }
    }

    concAnode.value   = this._concAccAnode.toFixed(3);
    concCathode.value = this._concAccCathode.toFixed(3);
    this._updateConcLabels();
  }

  _updateConcLabels() {
    if (!this.controls) return;
    const { concAnode, concCathode } = this.controls;
    const aLbl = document.getElementById(concAnode.id   + '-label');
    const cLbl = document.getElementById(concCathode.id + '-label');
    if (aLbl) aLbl.textContent = parseFloat(concAnode.value).toFixed(2)   + ' M';
    if (cLbl) cLbl.textContent = parseFloat(concCathode.value).toFixed(2) + ' M';
  }

  _snapshotConcentrations() {
    if (!this.controls) return;
    this._concSnapshot = {
      anode:   parseFloat(this.controls.concAnode.value),
      cathode: parseFloat(this.controls.concCathode.value),
    };
  }

  _restoreConcentrations() {
    if (!this.controls || !this._concSnapshot) return;
    this.controls.concAnode.value   = this._concSnapshot.anode;
    this.controls.concCathode.value = this._concSnapshot.cathode;
    this._updateConcLabels();
  }

  _drawTimer() {
    const t = this.elapsedTime;
    const mins   = Math.floor(t / 60);
    const secs   = Math.floor(t % 60);
    const tenths = Math.floor((t % 1) * 10);
    const str = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}.${tenths}`;

    const ctx = this.ctx;
    ctx.font = '13px monospace';
    ctx.textAlign = 'right';
    ctx.textBaseline = 'middle';

    const x = LAYOUT.canvasW - 10;
    const y = LAYOUT.canvasH - 14;
    const tw = ctx.measureText(str).width;

    ctx.fillStyle = 'rgba(0,0,0,0.5)';
    ctx.fillRect(x - tw - 10, y - 11, tw + 18, 22);
    ctx.fillStyle = 'rgba(160,220,255,0.9)';
    ctx.fillText(str, x, y);
    ctx.textBaseline = 'alphabetic';
  }

  _drawThermodynamicsPanel() {
    const a = this.getAnodeHR();
    const c = this.getCathodeHR();
    if (!a || !c) return;

    const n      = lcm(a.charge, c.charge);
    const E      = calcNernstPotential(c, a, this.getConcCathode(), this.getConcAnode(), this.getTempK());
    const E0     = calcStandardCellPotential(c, a);
    const deltaG = -(n * 96485 * E) / 1000; // kJ/mol

    // K = 10^(nE° / nernstFactor); avoid Infinity in display
    const Kexp     = (n * E0) / calcNernstFactor(this.getTempK());
    let Kstr;
    if      (Kexp >  300) Kstr = '≫ 1';
    else if (Kexp < -300) Kstr = '≪ 1';
    else {
      let expFloor = Math.floor(Kexp);
      let mantissa = Math.pow(10, Kexp - expFloor);
      if (parseFloat(mantissa.toFixed(2)) >= 10) { // FIXED: toFixed rounding can produce "10.00"; renormalize
        mantissa /= 10;
        expFloor += 1;
      }
      Kstr = `${mantissa.toFixed(2)} × 10^${expFloor}`;
    }

    const lb   = LAYOUT.leftBeaker;
    const rb   = LAYOUT.rightBeaker;
    const midX = (lb.x + lb.w / 2 + rb.x + rb.w / 2) / 2;
    const panelY = lb.y + lb.h * 0.65; // 263 — below salt bridge (190), above beaker labels (360)
    const boxW = 210, boxH = 54;
    const ctx  = this.ctx;

    ctx.fillStyle = 'rgba(0,0,0,0.5)';
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(midX - boxW / 2, panelY - boxH / 2, boxW, boxH, 6);
    else ctx.rect(midX - boxW / 2, panelY - boxH / 2, boxW, boxH);
    ctx.fill();

    ctx.font = '12px monospace';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    ctx.fillStyle = deltaG <= 0 ? '#66bb6a' : '#ef5350';
    ctx.fillText(`ΔG = ${deltaG.toFixed(1)} kJ/mol`, midX, panelY - 14);

    ctx.fillStyle = 'rgba(180,210,255,0.85)';
    ctx.fillText(`K = ${Kstr}`, midX, panelY + 14);

    ctx.textBaseline = 'alphabetic';
  }

  // Shared helper: draw a voltmeter circle
  drawVoltmeter(x, y, voltage, label, warn = false) {
    const ctx = this.ctx;
    const r = 32;

    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = '#263238';
    ctx.fill();

    let ringColor;
    if (warn) {
      const pulse = 0.55 + 0.45 * Math.abs(Math.sin(this.elapsedTime * 3));
      ringColor = `rgba(255,152,0,${pulse.toFixed(2)})`;
    } else {
      ringColor = voltage >= 0 ? '#66bb6a' : '#ef5350';
    }
    ctx.strokeStyle = ringColor;
    ctx.lineWidth = 3;
    ctx.stroke();

    ctx.fillStyle = '#fff';
    ctx.font = 'bold 11px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(label || 'V', x, y - 10);
    ctx.font = 'bold 13px monospace';
    ctx.fillStyle = warn ? '#ff9800' : (voltage >= 0 ? '#66bb6a' : '#ef5350');
    ctx.fillText((voltage >= 0 ? '+' : '') + voltage.toFixed(3) + ' V', x, y + 8);
    ctx.textBaseline = 'alphabetic';
  }
}
