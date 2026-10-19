const test = require("node:test");
const assert = require("node:assert/strict");
const TissuePhysicsEngine = require("../components/tissue_physics_engine.js");

function makeEngine(options = {}) {
  return new TissuePhysicsEngine(55, 39, options);
}

test("initial state is flat, finite, and resettable", () => {
  const engine = makeEngine();
  assert.equal(engine.snapshot().maxDisplacement, 0);
  assert.equal(engine.snapshot().finite, true);
  assert.ok(engine.displacement.every((x) => x === 0));
});

test("contact produces a local displacement", () => {
  const engine = makeEngine();
  engine.applyIndentation(27, 19, 0.12, 2.5);
  assert.ok(engine.lastMaxDisplacement > 0);
  assert.ok(engine.lastMaxDisplacement <= 0.18);
  assert.ok(engine.displacement[19 * 55 + 27] > engine.displacement[19 * 55 + 35]);
});

test("boundary rim remains fixed after contact and stepping", () => {
  const engine = makeEngine();
  engine.applyIndentation(2, 2, 0.18, 4);
  for (let i = 0; i < 120; i++) engine.step(1 / 60);
  for (let y = 0; y < engine.rows; y++) {
    for (let x = 0; x < engine.columns; x++) {
      if (engine._fixed(x, y)) {
        const i = y * engine.columns + x;
        assert.equal(engine.displacement[i], 0);
        assert.equal(engine.velocity[i], 0);
      }
    }
  }
});

test("displacement is bounded under repeated large contacts", () => {
  const engine = makeEngine();
  for (let i = 0; i < 30; i++) engine.applyIndentation(27, 19, 0.2, 5);
  for (let i = 0; i < 120; i++) engine.step(1 / 30);
  assert.ok(engine.displacement.every((x) => x >= 0 && x <= 0.18));
  assert.ok(engine.velocity.every(Number.isFinite));
});

test("large frame deltas are substepped and remain finite", () => {
  const engine = makeEngine();
  engine.applyIndentation(27, 19, 0.15, 3);
  const max = engine.step(0.1);
  assert.ok(Number.isFinite(max));
  assert.equal(engine.snapshot().finite, true);
  assert.ok(engine.stepCount >= 12);
});

test("damping reduces oscillation energy in a free recovery test", () => {
  const engine = makeEngine({ damping: 12 });
  engine.applyIndentation(27, 19, 0.15, 2.5);
  let peak = engine.step(1 / 60);
  for (let i = 0; i < 180; i++) engine.step(1 / 60);
  assert.ok(engine.lastMaxDisplacement < peak);
});

test("zero coupling keeps a contact local to its own grid nodes", () => {
  const engine = makeEngine({ coupling: 0 });
  engine.applyIndentation(27, 19, 0.12, 1);
  engine.step(1 / 120);
  assert.equal(engine.displacement[19 * 55 + 35], 0);
});

test("invalid dimensions, parameters, and time steps are rejected", () => {
  assert.throws(() => new TissuePhysicsEngine(2, 10), /dimensions/);
  const engine = makeEngine();
  assert.throws(() => engine.setParameters({ stiffness: NaN }), /outside allowed range/);
  assert.throws(() => engine.setParameters({ damping: 99 }), /outside allowed range/);
  assert.throws(() => engine.step(0), /positive finite/);
  assert.throws(() => engine.applyIndentation(2, 2, -1, 1), /Contact requires/);
});

test("reset clears displacement, velocity, and step count", () => {
  const engine = makeEngine();
  engine.applyIndentation(27, 19, 0.15, 3);
  engine.step(1 / 60);
  engine.reset();
  assert.equal(engine.snapshot().maxDisplacement, 0);
  assert.equal(engine.snapshot().stepCount, 0);
  assert.ok(engine.displacement.every((x) => x === 0));
  assert.ok(engine.velocity.every((x) => x === 0));
});

test("changing parameters is deterministic for identical inputs", () => {
  const a = makeEngine({ stiffness: 30, damping: 8, coupling: 4 });
  const b = makeEngine({ stiffness: 30, damping: 8, coupling: 4 });
  for (const engine of [a, b]) {
    engine.applyIndentation(26, 18, 0.1, 2);
    for (let i = 0; i < 30; i++) engine.step(1 / 60);
  }
  assert.deepEqual(Array.from(a.displacement), Array.from(b.displacement));
});
