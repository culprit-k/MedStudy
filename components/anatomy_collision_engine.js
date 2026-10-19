/* Educational collision helpers for MedStudy's synthetic training scene.
 * Geometry and units are scene-space approximations, not clinical measurements.
 */
(function (root) {
  "use strict";

  function finiteVector(v, name) {
    if (!v || ![v.x, v.y, v.z].every(Number.isFinite)) {
      throw new Error(name + " must be a finite 3D point");
    }
  }

  function pointPlaneContact(point, planeY, radius = 0) {
    finiteVector(point, "point");
    if (![planeY, radius].every(Number.isFinite) || radius < 0) {
      throw new Error("planeY must be finite and radius non-negative");
    }
    const signedDistance = point.y - planeY;
    const penetration = Math.max(0, radius - signedDistance);
    return {
      contact: penetration > 0,
      penetration,
      signedDistance,
      correctedY: penetration > 0 ? planeY + radius : point.y
    };
  }

  function pointSphereContact(point, sphere) {
    finiteVector(point, "point");
    if (!sphere || ![sphere.x, sphere.y, sphere.z, sphere.radius].every(Number.isFinite) || sphere.radius <= 0) {
      throw new Error("sphere must have finite coordinates and positive radius");
    }
    const dx = point.x - sphere.x, dy = point.y - sphere.y, dz = point.z - sphere.z;
    const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);
    const penetration = Math.max(0, sphere.radius - distance);
    const normal = distance > 1e-8
      ? { x: dx / distance, y: dy / distance, z: dz / distance }
      : { x: 0, y: 1, z: 0 };
    return {
      id: sphere.id || "unnamed",
      label: sphere.label || "Unlabelled proxy",
      contact: penetration > 0,
      penetration,
      distance,
      normal
    };
  }

  function deepestProxyContact(point, proxies) {
    if (!Array.isArray(proxies)) throw new Error("proxies must be an array");
    let deepest = null;
    for (const proxy of proxies) {
      const result = pointSphereContact(point, proxy);
      if (result.contact && (!deepest || result.penetration > deepest.penetration)) deepest = result;
    }
    return deepest;
  }

  const api = { pointPlaneContact, pointSphereContact, deepestProxyContact };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.AnatomyCollisionEngine = api;
})(typeof globalThis !== "undefined" ? globalThis : this);
