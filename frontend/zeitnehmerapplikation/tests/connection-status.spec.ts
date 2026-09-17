import { test, expect } from "@playwright/test"

test.describe("Connection Status", () => {

    test.beforeEach(async ({ page }) => {
        await page.goto("/")
    })

    test("shows inactive status initially", async ({ page }) => {
        await expect(page.getByText("Status: Inactive")).toBeVisible()
    })

    test("activates the connection", async ({ page }) => {
        await page.getByRole("button", {
            name: "Activate",
            exact: true,
        }).click()

        await expect(page.getByText("Status: Active")).toBeVisible()
    })

    test("deactivates the connection", async ({ page }) => {
        await page.getByRole("button", {
            name: "Activate",
            exact: true,
        }).click()

        await page.getByRole("button", {
            name: "Deactivate",
            exact: true,
        }).click()

        await expect(page.getByText("Status: Inactive")).toBeVisible()
    })
})