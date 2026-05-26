class GalvanicCell extends CellRenderer {
  constructor(canvas, controls) {
    super(canvas);
    this.controls = controls; // { anodeSelect, cathodeSelect, concAnode, concCathode }
  }

  getAnodeHR()     { return getById(this.controls.anodeSelect.value); }
  getCathodeHR()   { return getById(this.controls.cathodeSelect.value); }
  isElectrolytic() { return false; }

  getVoltage() {
    if (this._depleted) return 0;
    const a = this.getAnodeHR();
    const c = this.getCathodeHR();
    if (!a || !c) return 0;
    return calcNernstPotential(c, a, this.getConcCathode(), this.getConcAnode());
  }

  drawCircuitExtras() {
    const ctx = this.ctx;
    const lb = LAYOUT.leftBeaker;
    const rb = LAYOUT.rightBeaker;
    const wireY = lb.y - 55;
    const midX  = (lb.x + lb.w / 2 + rb.x + rb.w / 2) / 2;
    const voltage = this.getVoltage();

    const a = this.getAnodeHR();
    const c = this.getCathodeHR();
    const E0   = (a && c) ? calcStandardCellPotential(c, a) : 1;
    const warn = !this._depleted && E0 > 0 && voltage >= 0 && (voltage / E0) < 0.15;

    this.drawVoltmeter(midX, wireY, voltage, 'Voltmeter', warn);

    // Electron flow arrow on wire
    const arrowX = midX + 60;
    this._drawArrow(ctx, arrowX, wireY - 3, arrowX + 40, wireY - 3, '#ffeb3b', '  e⁻');

    this._drawThermodynamicsPanel();
  }

  _drawArrow(ctx, x1, y1, x2, y2, color, label) {
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
    // arrowhead
    const angle = Math.atan2(y2 - y1, x2 - x1);
    ctx.beginPath();
    ctx.moveTo(x2, y2);
    ctx.lineTo(x2 - 10 * Math.cos(angle - 0.4), y2 - 10 * Math.sin(angle - 0.4));
    ctx.lineTo(x2 - 10 * Math.cos(angle + 0.4), y2 - 10 * Math.sin(angle + 0.4));
    ctx.closePath();
    ctx.fill();
    if (label) {
      ctx.font = '11px sans-serif';
      ctx.textAlign = 'left';
      ctx.fillStyle = color;
      ctx.fillText(label, x2 + 4, y2 + 4);
    }
  }
}
