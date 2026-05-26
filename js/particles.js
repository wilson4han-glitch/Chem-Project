class ParticleSystem {
  constructor() {
    this.electrons = [];
    this.ions = [];
  }

  reset() {
    this.electrons = [];
    this.ions = [];
  }

  // path: array of {x,y} waypoints; particle follows them sequentially
  spawnElectron(path, speed) {
    this.electrons.push({
      path,
      pathIndex: 0,
      t: Math.random(), // stagger start positions along path
      speed: speed || 1.2,
      radius: 5,
      color: '#ffeb3b',
    });
  }

  spawnIon(path, speed, color, label, charge) {
    this.ions.push({
      path,
      pathIndex: 0,
      t: Math.random(),
      speed: speed || 0.5,
      radius: 6,
      color,
      label,
      charge,
    });
  }

  // Initialize a full set of particles for a cell
  initParticles(electronPath, cationPath, anionPath, anodeHR, cathodeHR, count, speed) {
    this.reset();
    for (let i = 0; i < count; i++) {
      this.spawnElectron(electronPath, speed * 1.4);
    }
    for (let i = 0; i < Math.floor(count * 0.6); i++) {
      this.spawnIon(cationPath, speed * 0.6, cathodeHR.color, cathodeHR.ion, '+');
    }
    for (let i = 0; i < Math.floor(count * 0.6); i++) {
      this.spawnIon(anionPath, speed * 0.6, '#ff7043', 'NO₃⁻', '-');
    }
  }

  update(dt) {
    const step = dt * 0.016;
    for (let i = 0; i < this.electrons.length; i++) {
      const p = this.electrons[i];
      p.t += p.speed * step;
      if (p.t >= 1) p.t -= 1;
    }
    for (let i = 0; i < this.ions.length; i++) {
      const p = this.ions[i];
      p.t += p.speed * step;
      if (p.t >= 1) p.t -= 1;
    }
  }

  // Get current x,y of a particle along its multi-segment path
  _getPosition(p) {
    const path = p.path;
    if (path.length < 2) return path[0];
    // distribute t evenly across segments
    const segments = path.length - 1;
    const total = p.t * segments;
    const seg = Math.min(Math.floor(total), segments - 1);
    const segT = total - seg;
    const a = path[seg];
    const b = path[seg + 1];
    return {
      x: a.x + (b.x - a.x) * segT,
      y: a.y + (b.y - a.y) * segT,
    };
  }

  draw(ctx) {
    this.electrons.forEach(p => {
      const pos = this._getPosition(p);
      ctx.beginPath();
      ctx.arc(pos.x, pos.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.shadowColor = p.color;
      ctx.shadowBlur = 8;
      ctx.fill();
      ctx.shadowBlur = 0;
      // minus sign
      ctx.fillStyle = '#333';
      ctx.font = 'bold 8px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('−', pos.x, pos.y);
    });

    this.ions.forEach(p => {
      const pos = this._getPosition(p);
      ctx.beginPath();
      ctx.arc(pos.x, pos.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.globalAlpha = 0.85;
      ctx.fill();
      ctx.globalAlpha = 1;
      ctx.strokeStyle = 'rgba(255,255,255,0.5)';
      ctx.lineWidth = 1;
      ctx.stroke();
      ctx.fillStyle = '#fff';
      ctx.font = 'bold 7px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(p.charge, pos.x, pos.y);
    });
  }
}
