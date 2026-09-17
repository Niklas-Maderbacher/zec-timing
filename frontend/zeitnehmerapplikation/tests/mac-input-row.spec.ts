import { test, expect } from "@playwright/test"

test.describe("MAC Input Row", () => {

    test.beforeEach(async ({ page }) => {
        await page.goto("/")
    })

    test("displays the input", async ({ page }) => {
        await expect(
            page.getByRole("textbox", {
                name: "Update Start 1 ESP32 MAC"
            })
        ).toBeVisible()
    })

    test("displays the placeholder", async ({ page }) => {
        await expect(
            page.getByRole("textbox", {
                name: "Update Start 1 ESP32 MAC"
            })
        ).toHaveAttribute("placeholder", "ESP32 MAC")
    })

    test("displays the update button", async ({ page }) => {
        await expect(
            page.getByRole("button", { name: "Update Start 1" })
        ).toBeVisible()
    })

    test("allows entering a MAC address", async ({ page }) => {
        const input = page.getByRole("textbox", {
            name: "Update Start 1 ESP32 MAC"
        })

        await input.fill("AA:BB:CC:DD:EE:FF")

        await expect(input).toHaveValue("AA:BB:CC:DD:EE:FF")
    })

    test("allows updating the MAC address", async ({ page }) => {
        const input = page.getByRole("textbox", {
            name: "Update Start 1 ESP32 MAC"
        })

        await input.fill("AA:BB:CC:DD:EE:FF")

        await page.getByRole("button", {
            name: "Update Start 1"
        }).click()
    })
})