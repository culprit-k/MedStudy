/* MedStudy educational tissue membrane physics.
 * Deterministic, bounded grid solver for a deformable teaching surface.
 * Values are dimensionless and are not calibrated to human tissue.
 */
(function (root) {
  "use strict";

  class TissuePhysicsEngine {
    constructor(columns, rows, options = {}) {
      if (!Number.isInteger(columns) || !Number.isInteger(rows) || columns < 5 || rows < 5) {
        throw new Error("Grid dimensions must be integers of at least 5.");
      }
      this.columns = columns;
      this.rows = rows;
      this.size = columns * rows;
      this.displacement = new Float32Array(this.size);
      this.velocity = new Float32Array(this.size);
      this.stiffness = options.stiffness ?? 34;
      this.damping = options.damping ?? 9;
      this.coupling = options.coupling ?? 5.5;
      this.maxDisplacement = options.maxDisplacement ?? 0.18;
      this.boundaryWidth = options.boundaryWidth ?? 2;
      this.lastMaxDisplacement = 0;
      this.stepCount = 0;
    }

    setParameters({ stiffness = this.stiffness, damping = this.damping, coupling = this.coupling } = {}) {
      this.stiffness = this._bounded(stiffness, 0, 100, "stiffness");
      this.damping = this._bounded(damping, 0, 40, "damping");
      this.coupling = this._bounded(coupling, 0, 20, "coupling");
    }

    _bounded(value, min, max, name) {
      const n = Number(value);
      if (!Number.isFinite(n) || n < min || n > max) throw new Error(name + " outside allowed range");
      return n;
    }

    _fixed(x, y) {
      return x < this.boundaryWidth || x >= this.columns - this.boundaryWidth ||
        y < this.boundaryWidth || y >= this.rows - this.boundaryWidth;
    }

    applyIndentation(cx, cy, amplitude = 0.1, radius = 3) {
      if (![cx, cy, amplitude, radius].every(Number.isFinite) || radius <= 0 || amplitude < 0) {
        throw new Error("Contact requires finite coordinates, non-negative amplitude, and positive radius.");
      }
      const minX = Math.max(this.boundaryWidth, Math.floor(cx - radius * 3));
      const maxX = Math.min(this.columns - this.boundaryWidth - 1, Math.ceil(cx + radius * 3));
      const minY = Math.max(this.boundaryWidth, Math.floor(cy - radius * 3));
      const maxY = Math.min(this.rows - this.boundaryWidth - 1, Math.ceil(cy + radius * 3));
      for (let y = minY; y <= maxY; y++) {
        for (let x = minX; x <= maxX; x++) {
          if (this._fixed(x, y)) continue;
          const dx = x - cx, dy = y - cy;
          const distance2 = dx * dx + dy * dy;
          const influence = Math.exp(-distance2 / (2 * radius * radius));
          const i = y * this.columns + x;
          this.displacement[i] = Math.min(this.maxDisplacement, this.displacement[i] + amplitude * influence);
        }
      }
      this._measure();
    }

    step(dt) {
      if (!Number.isFinite(dt) || dt <= 0) throw new Error("dt must be a positive finite number");
      // Substep large frame times to keep the explicit damped solver stable.
      const steps = Math.max(1, Math.ceil(dt / (1 / 120)));
      const h = Math.min(dt, 0.1) / steps;
      for (let s = 0; s < steps; s++) {
        for (let y = 0; y < this.rows; y++) {
          for (let x = 0; x < this.columns; x++) {
            const i = y * this.columns + x;
            if (this._fixed(x, y)) {
              this.displacement[i] = 0;
              this.velocity[i] = 0;
              continue;
            }
            let sum = 0, count = 0;
            if (x > 0) { sum += this.displacement[i - 1]; count++; }
            if (x + 1 < this.columns) { sum += this.displacement[i + 1]; count++; }
            if (y > 0) { sum += this.displacement[i - this.columns]; count++; }
            if (y + 1 < this.rows) { sum += this.displacement[i + this.columns]; count++; }
            const average = sum / count;
            const acceleration = -this.stiffness * this.displacement[i] -
              this.damping * this.velocity[i] + this.coupling * (average - this.displacement[i]);
            this.velocity[i] += acceleration * h;
            this.displacement[i] += this.velocity[i] * h;
            if (this.displacement[i] < 0) {
              this.displacement[i] = 0;
              if (this.velocity[i] < 0) this.velocity[i] = 0;
            }
            if (this.displacement[i] > this.maxDisplacement) {
              this.displacement[i] = this.maxDisplacement;
              if (this.velocity[i] > 0) this.velocity[i] = 0;
            }
            if (!Number.isFinite(this.displacement[i]) || !Number.isFinite(this.velocity[i])) {
              throw new Error("Physics solver became non-finite at node " + i);
            }
          }
        }
        this.stepCount++;
      }
      return this._measure();
    }

    _measure() {
      let max = 0;
      for (let i = 0; i < this.size; i++) {
        if (!Number.isFinite(this.displacement[i]) || !Number.isFinite(this.velocity[i])) {
          throw new Error("Non-finite state detected at node " + i);
        }
        if (this.displacement[i] > max) max = this.displacement[i];
      }
      this.lastMaxDisplacement = max;
      return max;
    }

    reset() {
      this.displacement.fill(0);
      this.velocity.fill(0);
      this.lastMaxDisplacement = 0;
      this.stepCount = 0;
    }

    snapshot() {
      return {
        columns: this.columns,
        rows: this.rows,
        maxDisplacement: this.lastMaxDisplacement,
        stepCount: this.stepCount,
        finite: this.displacement.every(Number.isFinite) && this.velocity.every(Number.isFinite)
      };
    }
  }

  if (typeof module !== "undefined" && module.exports) module.exports = TissuePhysicsEngine;
  root.TissuePhysicsEngine = TissuePhysicsEngine;
})(typeof globalThis !== "undefined" ? globalThis : this);
