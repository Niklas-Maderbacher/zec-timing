import { test, expect } from "@playwright/test"

test.describe("Attempt Result", () => {

    test.beforeEach(async ({ page }) => {
        await page.goto("/")
    })

    test("displays the result", async ({ page }) => {
        await expect(
            page.getByText(/Result = /)
        ).toBeVisible()
    })

    test("displays the selected team", async ({ page }) => {
        await expect(
            page.getByText(/Team = /)
        ).toBeVisible()
    })

    test("displays the selected driver", async ({ page }) => {
        await expect(
            page.getByText(/Driver = /)
        ).toBeVisible()
    })

    test("displays the selected challenge", async ({ page }) => {
        await expect(
            page.getByText(/Challenge = /)
        ).toBeVisible()
    })
})