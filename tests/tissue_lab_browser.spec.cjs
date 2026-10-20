const { test, expect } = require("@playwright/test");
const path = require("node:path");

const ROOT = process.cwd();
const LAB_URL = "/components/realistic_tissue_interaction_lab.html";

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
