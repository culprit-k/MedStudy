const { test, expect } = require("@playwright/test");
const path = require("node:path");
const fs = require("node:fs");

const ROOT = process.cwd();
const LAB_URL = "/components/realistic_tissue_interaction_lab.html";
const KIDNEY_URL = "/components/kidney_anatomy_lab.html";


function makeMockGlb() {
  const positions = Buffer.alloc(36);
  const vertices = [
    [-0.45, -0.8, 0],
    [0.45, -0.8, 0],
    [0.1, 0.8, 0],
  ];
  vertices.flat().forEach((value, index) => positions.writeFloatLE(value, index * 4));
  const indices = Buffer.alloc(6);
  [0, 1, 2].forEach((value, index) => indices.writeUInt16LE(value, index * 2));
  const binary = Buffer.concat([positions, indices, Buffer.alloc(2)]);
  const document = {
    asset: { version: "2.0", generator: "MedStudy deterministic browser fixture" },
    scene: 0,
    scenes: [{ nodes: [0] }],
    nodes: [{ mesh: 0, name: "Fixture kidney surface" }],
    meshes: [{ primitives: [{ attributes: { POSITION: 0 }, indices: 1, material: 0 }] }],
    materials: [{ pbrMetallicRoughness: { baseColorFactor: [0.62, 0.22, 0.25, 1], roughnessFactor: 0.8 } }],
    buffers: [{ byteLength: 42 }],
    bufferViews: [
      { buffer: 0, byteOffset: 0, byteLength: 36, target: 34962 },
      { buffer: 0, byteOffset: 36, byteLength: 6, target: 34963 },
    ],
    accessors: [
      { bufferView: 0, componentType: 5126, count: 3, type: "VEC3", min: [-0.45, -0.8, 0], max: [0.45, 0.8, 0] },
      { bufferView: 1, componentType: 5123, count: 3, type: "SCALAR", min: [0], max: [2] },
    ],
  };
  const json = Buffer.from(JSON.stringify(document));
  const jsonPadding = (4 - (json.length % 4)) % 4;
  const paddedJson = Buffer.concat([json, Buffer.alloc(jsonPadding, 0x20)]);
  const header = Buffer.alloc(12);
  header.writeUInt32LE(0x46546c67, 0);
  header.writeUInt32LE(2, 4);
  header.writeUInt32LE(12 + 8 + paddedJson.length + 8 + binary.length, 8);
  const jsonHeader = Buffer.alloc(8);
  jsonHeader.writeUInt32LE(paddedJson.length, 0);
  jsonHeader.writeUInt32LE(0x4e4f534a, 4);
  const binHeader = Buffer.alloc(8);
  binHeader.writeUInt32LE(binary.length, 0);
  binHeader.writeUInt32LE(0x004e4942, 4);
  return Buffer.concat([header, jsonHeader, paddedJson, binHeader, binary]);
}

async function installKidneyRuntimeRoutes(page) {
  await page.route("https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js", route => route.fulfill({
    path: path.join(ROOT, "node_modules/three/build/three.min.js"),
    contentType: "application/javascript",
  }));
  const kidneyHtml = fs.readFileSync(path.join(ROOT, "components/kidney_anatomy_lab.html"), "utf8")
    .replace("__STATION__", JSON.stringify("Instrument targeting and hand-eye coordination"));
  await page.route("**/components/kidney_anatomy_lab.html", route => route.fulfill({
    status: 200,
    contentType: "text/html",
    body: kidneyHtml,
  }));
}

async function installLocalRuntimeRoutes(page) {
  const routes = [
    ["https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js", "node_modules/three/build/three.min.js"],
    ["https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js", "node_modules/three/examples/js/loaders/GLTFLoader.js"],
    ["https://raw.githubusercontent.com/culprit-k/MedStudy/main/components/tissue_physics_engine.js", "components/tissue_physics_engine.js"],
    ["https://raw.githubusercontent.com/culprit-k/MedStudy/main/components/anatomy_collision_engine.js", "components/anatomy_collision_engine.js"],
  ];
  for (const [url, file] of routes) {
    await page.route(url, route => route.fulfill({
      path: path.join(ROOT, file),
      contentType: "application/javascript",
    }));
  }
}

test("3D tissue lab loads, supports an incision drag, and resets", async ({ page }) => {
  const pageErrors = [];
  page.on("pageerror", error => pageErrors.push(error.message));
  await installLocalRuntimeRoutes(page);

  await page.goto(LAB_URL);
  await expect(page.locator("#scene")).toBeVisible();
  await page.waitForFunction(
    () => Boolean(window.THREE && window.TissuePhysicsEngine && window.AnatomyCollisionEngine),
    null,
    { timeout: 30000 }
  );
  await expect(page.locator("#status")).toContainText("Explore mode");

  await page.getByRole("button", { name: "Incision", exact: true }).click();
  await expect(page.locator("#status")).toContainText("Incision practice");

  const canvas = await page.locator("#scene").boundingBox();
  expect(canvas).not.toBeNull();
  const startX = canvas.x + canvas.width * 0.38;
  const startY = canvas.y + canvas.height * 0.53;
  await page.mouse.move(startX, startY);
  await page.mouse.down();
  await page.mouse.move(startX + Math.min(120, canvas.width * 0.2), startY + 18, { steps: 4 });
  await page.mouse.up();

  await expect(page.locator("#incisionCount")).not.toHaveText("0");
  await page.getByRole("button", { name: "Reset training field", exact: true }).click();
  await expect(page.locator("#incisionCount")).toHaveText("0");
  await expect(page.locator("#stitchCount")).toHaveText("0");
  await expect(page.locator("#integrity")).toHaveText("100%");
  await expect(page.locator("#contactState")).toHaveText("No contact");
  expect(pageErrors).toEqual([]);
});

test("layout remains usable at a phone-width viewport", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await installLocalRuntimeRoutes(page);
  await page.goto(LAB_URL);
  await page.waitForFunction(
    () => Boolean(window.THREE && window.TissuePhysicsEngine && window.AnatomyCollisionEngine),
    null,
    { timeout: 30000 }
  );
  await expect(page.locator("#scene")).toBeVisible();
  await expect(page.getByRole("button", { name: "Reset training field", exact: true })).toBeVisible();

  const layout = await page.locator("body").evaluate(element => ({
    width: element.clientWidth,
    scrollWidth: element.scrollWidth,
    columns: getComputedStyle(document.querySelector(".shell")).gridTemplateColumns,
  }));
  expect(layout.scrollWidth).toBeLessThanOrEqual(layout.width + 1);
  expect(layout.columns.trim().split(/\s+/)).toHaveLength(1);
});


test("kidney anatomy lab renders a single-organ model and its anatomy controls work", async ({ page }) => {
  const pageErrors = [];
  page.on("pageerror", error => pageErrors.push(error.message));
  await installKidneyRuntimeRoutes(page);
  await page.goto(KIDNEY_URL);

  await page.waitForFunction(() => Boolean(window.THREE), null, { timeout: 10000 });
  await expect(page.locator("#scene")).toBeVisible();
  await expect(page.locator("#anatomyLegend")).toContainText(/renal pelvis/i);
  await expect(page.locator("#assetStatus")).toContainText("Original single-kidney geometry loaded", { timeout: 10000 });

  await page.getByRole("button", { name: "Cutaway", exact: true }).click();
  await expect(page.locator("#result")).toContainText("Cutaway view");
  await page.getByRole("button", { name: "Cortex", exact: true }).click();
  await expect(page.locator("#cortexLayer")).not.toHaveClass(/active/);
  await page.getByRole("button", { name: "Outer surface", exact: true }).click();
  await expect(page.locator("#result")).toContainText("Outer renal surface hidden");

  await page.getByRole("button", { name: "Camera orbit", exact: true }).click();
  await expect(page.locator("#result")).toContainText("Camera orbit active");
  await page.getByRole("button", { name: "Instrument", exact: true }).click();
  await expect(page.locator("#result")).toContainText("Instrument mode active");
  await page.getByRole("button", { name: "Start target drill", exact: true }).click();
  await expect(page.locator("#result")).toContainText("Target drill started");
  await page.getByRole("button", { name: "Reset view", exact: true }).click();
  await expect(page.locator("#result")).toContainText("View reset");
  await expect(page.locator("#surfaceToggle")).toHaveClass(/active/);
  expect(pageErrors).toEqual([]);
});

test("kidney anatomy controls fit a phone-width viewport", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await installKidneyRuntimeRoutes(page);
  await page.goto(KIDNEY_URL);
  await page.waitForFunction(() => Boolean(window.THREE), null, { timeout: 10000 });
  await expect(page.locator("#scene")).toBeVisible();
  await expect(page.getByRole("button", { name: "Start target drill", exact: true })).toBeVisible();
  await expect(page.getByRole("button", { name: "Calyces / pelvis / ureter", exact: true })).toBeVisible();

  const layout = await page.locator("#bottom").evaluate(element => ({
    width: element.clientWidth,
    scrollWidth: element.scrollWidth,
    sceneWidth: document.querySelector("#scene").clientWidth,
  }));
  expect(layout.scrollWidth).toBeLessThanOrEqual(layout.width + 1);
  expect(layout.sceneWidth).toBeGreaterThan(250);
});
