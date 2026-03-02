import { test, expect } from './fixtures';

test('admin can see all tabs', async ({ page }) => {
  await page.goto('http://localhost:3000/');
  await page.getByRole('button', { name: 'Account' }).click();
  await page.getByRole('textbox', { name: 'Username' }).click();
  await page.getByRole('textbox', { name: 'Username' }).fill('admin');
  await page.getByRole('textbox', { name: 'Password' }).click();
  await page.getByRole('textbox', { name: 'Password' }).fill('changeme');
  await page.getByRole('button', { name: 'Login' }).click();
  await page.getByRole('button', { name: 'Leaderboard' }).click();
  await page.getByRole('button', { name: 'Attempts' }).click();
  await page.getByRole('button', { name: 'Teams' }).click();
  await page.getByRole('button', { name: 'Challenges' }).click();
  await page.getByRole('button', { name: 'Users' }).click();
  await page.getByRole('button', { name: 'Export' }).click();
  await page.getByRole('button', { name: 'Account' }).click();
});

test('teamlead sees correct tabs', async ({ page, teamleadUser }) => {
  test.describe.configure({ mode: 'serial' });
  await page.goto('http://localhost:3000/');
  await page.getByRole('button', { name: 'Account' }).click();
  await page.getByRole('textbox', { name: 'Username' }).fill(teamleadUser.username);
  await page.getByRole('textbox', { name: 'Password' }).fill(teamleadUser.password);
  await page.getByRole('button', { name: 'Login' }).click();
  await expect(page.getByRole('button', { name: 'Leaderboard' })).toBeVisible();
});
