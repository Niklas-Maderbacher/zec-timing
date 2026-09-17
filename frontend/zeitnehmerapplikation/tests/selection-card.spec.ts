import { test, expect } from "@playwright/test"

test.describe("Selection Card", () => {

    test.beforeEach(async ({ page }) => {
        await page.route("**/challenges/", route =>
            route.fulfill({
                status: 200,
                contentType: "application/json",
                body: JSON.stringify([
                    {
                        id: 1,
                        name: "Challenge 1",
                        esp_mac_start1: "AA:AA:AA:AA:AA:01",
                        esp_mac_start2: "AA:AA:AA:AA:AA:02",
                        esp_mac_finish1: "AA:AA:AA:AA:AA:03",
                        esp_mac_finish2: "AA:AA:AA:AA:AA:04",
                    },
                ]),
            })
        )

        await page.goto("/")
    })

    test("displays the title", async ({ page }) => {
        await expect(
            page.getByText("Challenge", { exact: true })
        ).toBeVisible()
    })

    test("displays the selection button", async ({ page }) => {
        await expect(
            page.getByRole("button", { name: "Select Challenge" })
        ).toBeVisible()
    })

    test("opens the selection dropdown", async ({ page }) => {
        await page.getByRole("button", {
            name: "Select Challenge",
        }).click()

        await expect(
            page.getByRole("menu")
        ).toBeVisible()
    })

    test("displays the available items", async ({ page }) => {
        await page.getByRole("button", {
            name: "Select Challenge",
        }).click()

        await expect(
            page.getByRole("menuitemradio", {
                name: "Challenge 1",
            })
        ).toBeVisible()
    })

    test("allows selecting an item", async ({ page }) => {
        await page.getByRole("button", {
            name: "Select Challenge",
        }).click()

        await page.getByRole("menuitemradio", {
            name: "Challenge 1",
        }).click()

        await expect(
            page.getByRole("button", {
                name: "Challenge 1",
            })
        ).toBeVisible()

        await expect(
            page.getByText("Challenge = Challenge 1", { exact: true })
        ).toBeVisible()
    })
})