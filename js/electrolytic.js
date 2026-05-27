class ElectrolyticCell extends CellRenderer {
  constructor(canvas, controls) {
    super(canvas);
    this.controls = controls;
  }

  // In electrolytic mode the user selects what's being plated:
  // cathode = target metal (being deposited), anode = source metal (dissolving)
  getAnodeHR()     { return getById(this.controls.anodeSelect.value); }
  getCathodeHR()   { return getById(this.controls.cathodeSelect.value); }
  isElectrolytic() { return true; }

  canAdvance() {
    const req = this.getRequiredVoltage();
    return req <= 0 || this.getCurrent() >= req;
  }

  start() {
    if (!this.canAdvance()) {
      this.stop();
      this.draw();
      return;
    }
    super.start();
  }

  // Voltage required = -E°cell (must overcome spontaneous direction)
  getRequiredVoltage() {
    const a = this.getAnodeHR();
    const c = this.getCathodeHR();
    if (!a || !c) return 0;
    return -calcNernstPotential(c, a, this.getConcCathode(), this.getConcAnode(), this.getTempK());
  }

  getCurrent() {
    return this.controls && this.controls.current
      ? parseFloat(this.controls.current.value)
      : 2.0;
  }

  _calcMassDeposited() {
    const cathode = this.getCathodeHR();
    if (!cathode) return 0;
    // FIXED: use this.realTime (unscaled seconds) not this.elapsedTime (speed-scaled).
    // Faraday's law is m = (M·I·t) / (n·F) where t is real time in seconds.
    // elapsedTime accumulates dt*speed/60 per frame, so at 4× speed it is 4× too large,
    // producing physically incorrect mass values. realTime accumulates dt/60 per frame.
    return (cathode.molarMass * this.getCurrent() * this.realTime) / (cathode.charge * 96485);
  }

  drawCircuitExtras() {
    const ctx = this.ctx;
    const lb = LAYOUT.leftBeaker;
    const rb = LAYOUT.rightBeaker;
    const wireY = lb.y - 55;
    const midX  = (lb.x + lb.w / 2 + rb.x + rb.w / 2) / 2;
    const required = this.getRequiredVoltage();

    this._drawBattery(ctx, midX, wireY, required);

    // Electron flow arrow reversed (right to left on wire above battery)
    const arrowX = midX - 50;
    this._drawArrow(ctx, arrowX + 30, wireY - 3, arrowX - 10, wireY - 3, '#ffeb3b', '');

    this._drawThermodynamicsPanel();

    // Show a warning when the applied current is below the required voltage (used as a
    // proxy for insufficient power: higher required voltage demands more current).
    const current = this.getCurrent();
    if (required > 0 && current < required) {
      const { canvasW, canvasH } = LAYOUT;
      ctx.save();
      ctx.fillStyle = 'rgba(183, 28, 28, 0.88)';
      ctx.fillRect(0, canvasH - 54, canvasW, 54);
      ctx.fillStyle = '#fff';
      ctx.font = 'bold 15px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(
        `⚡ NOT ENOUGH CURRENT — need ≥ ${required.toFixed(2)} A to drive this reaction`,
        canvasW / 2, canvasH - 27
      );
      ctx.restore();
    }
  }

  _drawBattery(ctx, cx, cy, requiredV) {
    const w = 52, h = 28;
    const x = cx - w / 2;
    const y = cy - h / 2;

    ctx.fillStyle = '#37474f';
    ctx.strokeStyle = '#90a4ae';
    ctx.lineWidth = 2;
    ctx.beginPath();
    if (ctx.roundRect) {
      ctx.roundRect(x, y, w, h, 5);
    } else {
      ctx.rect(x, y, w, h);
    }
    ctx.fill();
    ctx.stroke();

    // battery symbol lines
    const bx = cx - 10;
    ctx.strokeStyle = '#ef5350';
    ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(bx, y + 6); ctx.lineTo(bx, y + h - 6); ctx.stroke(); // long +
    ctx.strokeStyle = '#90a4ae';
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(bx + 8, y + 10); ctx.lineTo(bx + 8, y + h - 10); ctx.stroke(); // short -

    // + and - labels
    ctx.fillStyle = '#ef5350';
    ctx.font = 'bold 12px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('+', bx - 7, cy);
    ctx.fillStyle = '#90a4ae';
    ctx.fillText('−', bx + 15, cy);

    // voltage label — green "SPONTANEOUS" if no external power needed
    ctx.font = '11px monospace';
    if (requiredV <= 0) {
      ctx.fillStyle = '#66bb6a';
      ctx.fillText('SPONTANEOUS', cx, cy + h / 2 + 14);
    } else {
      ctx.fillStyle = '#fff';
      ctx.fillText('≥' + requiredV.toFixed(2) + ' V', cx, cy + h / 2 + 14);
    }
    ctx.textBaseline = 'alphabetic';
  }

  _drawArrow(ctx, x1, y1, x2, y2, color) {
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
    const angle = Math.atan2(y2 - y1, x2 - x1);
    ctx.beginPath();
    ctx.moveTo(x2, y2);
    ctx.lineTo(x2 - 10 * Math.cos(angle - 0.4), y2 - 10 * Math.sin(angle - 0.4));
    ctx.lineTo(x2 - 10 * Math.cos(angle + 0.4), y2 - 10 * Math.sin(angle + 0.4));
    ctx.closePath();
    ctx.fill();
  }

  _drawLabels() {
    super._drawLabels();
    const ctx = this.ctx;
    const cathode = this.getCathodeHR();
    if (!cathode) return;
    const rb = LAYOUT.rightBeaker;
    const mass = this._calcMassDeposited();

    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';

    const isGas = cathode.type === 'gas';
    ctx.fillStyle = 'rgba(255,224,130,0.85)';
    ctx.fillText(
      isGas ? `Evolving: ${cathode.name} (${cathode.metal})` : `Plating: ${cathode.metal} (${cathode.name})`,
      rb.x + rb.w / 2, rb.y + rb.h + 72
    );

    ctx.fillStyle = 'rgba(160,220,160,0.9)';
    ctx.fillText(
      `${isGas ? 'Evolved' : 'Deposited'}: ${mass.toFixed(4)} g`,
      rb.x + rb.w / 2, rb.y + rb.h + 90
    );
  }
}
