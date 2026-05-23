import { test, expect } from '@playwright/test';

test.describe('Visual Regression Tests', () => {
  test('Main Dashboard Page Visual Regression', async ({ page }) => {
    // Navigate to the demo app root page
    await page.goto('/');
    
    // Wait for Svelte hydration and charts lazy loading to stabilize
    await page.waitForTimeout(2000);
    
    // Check main page visual snapshot
    await expect(page).toHaveScreenshot('main-dashboard.png', {
      maxDiffPixelRatio: 0.05,
    });
  });

  test('Sidebar Navigation Responsive Visual Regression', async ({ page }) => {
    await page.goto('/');
    
    // Trigger viewport resize to test small screen auto-collapse behavior
    await page.setViewportSize({ width: 1024, height: 768 });
    await page.waitForTimeout(1000);

    await expect(page).toHaveScreenshot('collapsed-tablet-dashboard.png', {
      maxDiffPixelRatio: 0.05,
    });
  });
});
