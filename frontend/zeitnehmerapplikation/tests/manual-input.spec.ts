import { test, expect } from "@playwright/test"

test.describe("Manual Attempt Time Input", () => {

    test.beforeEach(async ({ page }) => {
        await page.goto("/")
    })

    function getTimeInputs(page: any) {
        return page
            .getByTestId("manual-attempt-time")
            .locator('input[inputmode="numeric"]')
    }

    test("displays the manual attempt time label", async ({ page }) => {
        await expect(
            page.getByText("Manual Attempt Time:")
        ).toBeVisible()
    })

    test("displays the time inputs", async ({ page }) => {
        const inputs = getTimeInputs(page)

        await expect(inputs.nth(0)).toBeVisible()
        await expect(inputs.nth(1)).toBeVisible()
        await expect(inputs.nth(2)).toBeVisible()
    })

    test("displays the Set button", async ({ page }) => {
        await expect(
            page.getByRole("button", { name: "Set" })
        ).toBeVisible()
    })

    test("allows entering hours, minutes and seconds", async ({ page }) => {
        const inputs = getTimeInputs(page)

        await inputs.nth(0).fill("01")
        await inputs.nth(1).fill("23")
        await inputs.nth(2).fill("45")

        await expect(inputs.nth(0)).toHaveValue("01")
        await expect(inputs.nth(1)).toHaveValue("23")
        await expect(inputs.nth(2)).toHaveValue("45")
    })

    test("sets the manual attempt time", async ({ page }) => {
        const inputs = getTimeInputs(page)

        await inputs.nth(0).fill("01")
        await inputs.nth(1).fill("23")
        await inputs.nth(2).fill("45")

        await page.getByRole("button", { name: "Set" }).click()

        await expect(inputs.nth(0)).toHaveValue("01")
        await expect(inputs.nth(1)).toHaveValue("23")
        await expect(inputs.nth(2)).toHaveValue("45")
    })
})