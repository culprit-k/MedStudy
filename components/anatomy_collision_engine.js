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


  // Swept point-vs-sphere contact catches a moving tool point that crosses a
  // proxy between frames. t is the closest point along the segment, in [0, 1].
  function sweptSphereContact(start, end, sphere) {
    finiteVector(start, "start");
    finiteVector(end, "end");
    if (!sphere || ![sphere.x, sphere.y, sphere.z, sphere.radius].every(Number.isFinite) || sphere.radius <= 0) {
      throw new Error("sphere must have finite coordinates and positive radius");
    }
    const vx = end.x - start.x, vy = end.y - start.y, vz = end.z - start.z;
    const lengthSq = vx * vx + vy * vy + vz * vz;
    const t = lengthSq > 1e-16
      ? Math.max(0, Math.min(1, ((sphere.x - start.x) * vx + (sphere.y - start.y) * vy + (sphere.z - start.z) * vz) / lengthSq))
      : 0;
    const closest = { x: start.x + t * vx, y: start.y + t * vy, z: start.z + t * vz };
    const result = pointSphereContact(closest, sphere);
    return { ...result, contact: result.distance <= sphere.radius, time: t, closestPoint: closest };
  }

  function deepestSweptProxyContact(start, end, proxies) {
    if (!Array.isArray(proxies)) throw new Error("proxies must be an array");
    let deepest = null;
    for (const proxy of proxies) {
      const result = sweptSphereContact(start, end, proxy);
      if (result.contact && (!deepest || result.penetration > deepest.penetration)) deepest = result;
    }
    return deepest;
  }

  const api = { pointPlaneContact, pointSphereContact, deepestProxyContact, sweptSphereContact, deepestSweptProxyContact };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.AnatomyCollisionEngine = api;
})(typeof globalThis !== "undefined" ? globalThis : this);
