import { test, expect } from "@playwright/test"

test.describe("Number Input Card", () => {

    test.beforeEach(async ({ page }) => {
        await page.goto("/")
    })

    test("displays the titles", async ({ page }) => {
        await expect(
            page.getByText("Penalty Count")
        ).toBeVisible()

        await expect(
            page.getByText("Energy Consumption")
        ).toBeVisible()
    })

    test("displays the number inputs", async ({ page }) => {
        await expect(
            page.getByRole("spinbutton", {
                name: "Amount of Penalties",
            })
        ).toBeVisible()

        await expect(
            page.getByRole("spinbutton", {
                name: "Energy Consumption",
            })
        ).toBeVisible()
    })

    test("displays the placeholders", async ({ page }) => {
        await expect(
            page.getByRole("spinbutton", {
                name: "Amount of Penalties",
            })
        ).toHaveAttribute("placeholder", "Amount of Penalties")

        await expect(
            page.getByRole("spinbutton", {
                name: "Energy Consumption",
            })
        ).toHaveAttribute("placeholder", "Energy Consumption")
    })

    test("allows entering a number", async ({ page }) => {
        const input = page.getByRole("spinbutton", {
            name: "Amount of Penalties",
        })

        await input.fill("42")

        await expect(input).toHaveValue("42")
    })

    test("allows entering a decimal number", async ({ page }) => {
        const input = page.getByRole("spinbutton", {
            name: "Energy Consumption",
        })

        await input.fill("42.5")

        await expect(input).toHaveValue("42.5")
    })

    test("uses numeric input mode for penalty count", async ({ page }) => {
        const input = page.getByRole("spinbutton", {
            name: "Amount of Penalties",
        })

        await expect(input).toHaveAttribute("inputmode", "numeric")
    })

    test("uses decimal input mode for energy consumption", async ({ page }) => {
        const input = page.getByRole("spinbutton", {
            name: "Energy Consumption",
        })

        await expect(input).toHaveAttribute("inputmode", "decimal")
    })
})