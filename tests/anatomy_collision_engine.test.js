const test = require("node:test");
const assert = require("node:assert/strict");
const collision = require("../components/anatomy_collision_engine.js");

test("surface contact reports penetration and corrected position", () => {
  const result = collision.pointPlaneContact({x:0,y:1.5,z:0}, 1.58, 0.035);
  assert.equal(result.contact, true);
  assert.ok(result.penetration > 0);
  assert.ok(result.correctedY >= 1.58);
});

test("points outside the surface contact threshold remain free", () => {
  const result = collision.pointPlaneContact({x:0,y:2,z:0}, 1.58, 0.035);
  assert.equal(result.contact, false);
  assert.equal(result.penetration, 0);
});

test("sphere proxy detects contact and computes finite normal", () => {
  const result = collision.pointSphereContact({x:0.72,y:1.55,z:0.22}, {
    id:"vessel-proxy", label:"Vessel proxy", x:0.72, y:1.39, z:0.22, radius:0.34
  });
  assert.equal(result.contact, true);
  assert.equal(result.label, "Vessel proxy");
  assert.ok(result.penetration > 0);
  assert.ok(Number.isFinite(result.normal.y));
});

test("deepest overlapping proxy is selected", () => {
  const result = collision.deepestProxyContact({x:0,y:0,z:0}, [
    {id:"shallow", label:"Shallow", x:0.4, y:0, z:0, radius:0.5},
    {id:"deep", label:"Deep", x:0.1, y:0, z:0, radius:0.6}
  ]);
  assert.equal(result.id, "deep");
});

test("no structure contact returns null", () => {
  assert.equal(collision.deepestProxyContact({x:10,y:10,z:10}, [
    {id:"far", x:0, y:0, z:0, radius:1}
  ]), null);
});

test("invalid points and radii are rejected", () => {
  assert.throws(() => collision.pointPlaneContact({x:0,y:NaN,z:0}, 0), /finite 3D point/);
  assert.throws(() => collision.pointSphereContact({x:0,y:0,z:0}, {x:0,y:0,z:0,radius:0}), /positive radius/);
  assert.throws(() => collision.deepestProxyContact({x:0,y:0,z:0}, null), /array/);
});
