import { test, expect } from "@playwright/test"

test.describe("Timestamp Selector", () => {
    test.beforeEach(async ({ page }) => {
        await page.goto("/test-timestamp-selector")
    })

    test("displays the timestamp selector", async ({ page }) => {
        await expect(
            page.getByText("Start timestamp:", { exact: true })
        ).toBeVisible()

        await expect(
            page.getByRole("button", {
                name: "Select Start timestamp",
            })
        ).toBeVisible()
    })

    test("opens the timestamp dropdown", async ({ page }) => {
        await page.getByRole("button", {
            name: "Select Start timestamp",
        }).click()

        await expect(page.getByRole("menu")).toBeVisible()
    })

    test("displays the available timestamps", async ({ page }) => {
        await page.getByRole("button", {
            name: "Select Start timestamp",
        }).click()

        await expect(
            page.getByRole("menuitemcheckbox")
        ).toHaveText([
            "2026-01-01T00:00:01.000Z",
            "2026-01-01T00:00:02.000Z",
            "2026-01-01T00:00:03.000Z",
        ])
    })

    test("allows selecting a timestamp", async ({ page }) => {
        await page.getByRole("button", {
            name: "Select Start timestamp",
        }).click()

        const timestamp = page.getByRole("menuitemcheckbox").first()

        await timestamp.click()

        await expect(timestamp).toHaveAttribute(
            "data-state",
            "checked"
        )
    })

    test("allows selecting multiple timestamps", async ({ page }) => {
        await page.getByRole("button", {
            name: "Select Start timestamp",
        }).click()

        const timestamps = page.getByRole("menuitemcheckbox")

        await timestamps.nth(0).click()
        await timestamps.nth(1).click()

        await expect(timestamps.nth(0))
            .toHaveAttribute("data-state", "checked")

        await expect(timestamps.nth(1))
            .toHaveAttribute("data-state", "checked")
    })

    test("allows deselecting a timestamp", async ({ page }) => {
        await page.getByRole("button", {
            name: "Select Start timestamp",
        }).click()

        const timestamp = page.getByRole("menuitemcheckbox").first()

        await timestamp.click()
        await expect(timestamp)
            .toHaveAttribute("data-state", "checked")

        await timestamp.click()
        await expect(timestamp)
            .toHaveAttribute("data-state", "unchecked")
    })
})