import { test, expect } from "@playwright/test"

test.describe("Formula Card", () => {
    test.beforeEach(async ({ page }) => {
        await page.goto("/")
    })

    test("displays the formula card", async ({ page }) => {
        await expect(
            page.getByText("Formula", { exact: true })
        ).toBeVisible()
    })

    test("displays the formula description", async ({ page }) => {
        await expect(
            page.getByText(
                "Attempt time formula = end time - start time + (amount of penalties * time penalty)",
                { exact: true }
            )
        ).toBeVisible()
    })

    test("displays the timestamp formula", async ({ page }) => {
        await expect(
            page.getByText(
                /Attempt time formula = .* - .* \+ \(\d+ \* \d+\)/
            )
        ).toBeVisible()
    })

    test("displays the manual attempt time formula", async ({ page }) => {
        await expect(
            page.getByText(
                /Attempt time formula = .* \+ \(\d+ \* \d+\)/
            )
        ).toBeVisible()
    })
})