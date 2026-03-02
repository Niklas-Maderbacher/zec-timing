import { test as base, expect } from '@playwright/test';

type MyFixtures = {
  teamleadUser: { username: string; password: string };
};

export const test = base.extend<MyFixtures>({
    teamleadUser: async ({ page }, use) => {
        const username = 'test_team_lead';
        await page.goto('http://localhost:3000/');
        await page.getByRole('button', { name: 'Account' }).click();
        await page.getByRole('textbox', { name: 'Username' }).fill('admin');
        await page.getByRole('textbox', { name: 'Password' }).fill('changeme');
        await page.getByRole('button', { name: 'Login' }).click();
        await page.getByRole('button', { name: 'Users' }).click();
        await page.getByRole('button', { name: 'Add User' }).click();
        await page.getByRole('textbox', { name: 'Username' }).fill(username);
        await page.getByRole('textbox', { name: 'Password' }).fill('123');
        await page.getByRole('button', { name: 'Create User' }).click();
        await expect(page.locator('[data-slot="dialog-overlay"]')).not.toBeVisible({ timeout: 10000 });

        // assign TEAM_LEAD role
        await page.getByRole('row', { name: username }).getByRole('button', { name: 'Edit' }).click();
        await page.getByRole('checkbox', { name: 'TEAM_LEAD' }).check();
        await page.getByRole('button', { name: 'Update Roles' }).click();
        await expect(page.locator('[data-slot="dialog-overlay"]')).not.toBeVisible({ timeout: 10000 });

        await page.getByRole('button', { name: 'Account' }).click();
        await page.getByRole('button', { name: 'Logout' }).click();

        await use({ username:'test_team_lead', password: '123' });

        // teardown
        await page.goto('http://localhost:3000/');
        await page.getByRole('button', { name: 'Account' }).click();
        await page.getByRole('textbox', { name: 'Username' }).fill('admin');
        await page.getByRole('textbox', { name: 'Password' }).fill('changeme');
        await page.getByRole('button', { name: 'Login' }).click();
        await page.getByRole('button', { name: 'Users' }).click();
        await page.getByRole('row', { name: username }).getByRole('button').nth(2).click();
        await page.getByRole('button', { name: 'Delete' }).click();
        await expect(page.locator('[data-slot="dialog-overlay"]')).not.toBeVisible({ timeout: 10000 });
        },
});

export { expect };