import { test, expect } from '@playwright/test';

const BASE = 'http://localhost:3000';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

async function loginAs(page: any, username: string, password: string) {
  await page.goto(BASE);
  await page.getByRole('button', { name: 'Account' }).click();
  await page.getByRole('textbox', { name: 'Username' }).fill(username);
  await page.getByRole('textbox', { name: 'Password' }).fill(password);
  await page.getByRole('button', { name: 'Login' }).click();
  // Wait until the login button is gone, confirming auth state has settled
  await expect(page.getByRole('button', { name: 'Login' })).not.toBeVisible();
}

async function logout(page: any) {
  await page.getByRole('button', { name: 'Account' }).click();
  await page.getByRole('button', { name: 'Logout' }).click();
}

// ---------------------------------------------------------------------------
// Admin — navigation
// ---------------------------------------------------------------------------

test.describe('Admin navigation', () => {
  test.describe.configure({ mode: 'serial' });

  test('admin can log in and see all tabs', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await expect(page.getByRole('button', { name: 'Leaderboard' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Attempts' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Teams' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Challenges' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Users' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Export' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Account' })).toBeVisible();
  });

  test('admin can visit Leaderboard tab', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await page.getByRole('button', { name: 'Leaderboard' }).click();
    await expect(page.getByRole('heading', { name: 'Leaderboard' })).toBeVisible();
    await expect(page.getByText('Close to Series')).toBeVisible();
    await expect(page.getByText('Advanced Class')).toBeVisible();
    await expect(page.getByText('Professional Class')).toBeVisible();
  });

  test('admin can visit Attempts tab', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await page.getByRole('button', { name: 'Attempts' }).click();
    await expect(page.getByRole('heading', { name: 'Attempts Management' })).toBeVisible();
    await expect(page.getByRole('columnheader', { name: 'Team' })).toBeVisible();
    await expect(page.getByRole('columnheader', { name: 'Driver' })).toBeVisible();
    await expect(page.getByRole('columnheader', { name: 'Duration' })).toBeVisible();
    await expect(page.getByRole('columnheader', { name: 'Energy Used' })).toBeVisible();
    await expect(page.getByRole('columnheader', { name: 'Valid' })).toBeVisible();
  });

  test('admin can visit Teams tab', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await page.getByRole('button', { name: 'Teams' }).click();
    await expect(page.getByRole('heading', { name: /teams/i })).toBeVisible();
  });

  test('admin can visit Challenges tab', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await page.getByRole('button', { name: 'Challenges' }).click();
    await expect(page.getByRole('heading', { name: 'Challenge Management' })).toBeVisible();
    await expect(page.getByRole('columnheader', { name: 'Name' })).toBeVisible();
    await expect(page.getByRole('columnheader', { name: 'Max Attempts' })).toBeVisible();
  });

  test('admin can visit Users tab', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await page.getByRole('button', { name: 'Users' }).click();
    await expect(page.getByRole('heading', { name: 'User Management' })).toBeVisible();
  });

  test('admin can visit Export tab', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await page.getByRole('button', { name: 'Export' }).click();
    await expect(page.getByRole('heading', { name: 'Data Export' })).toBeVisible();
    await expect(page.getByText('Leaderboard Export')).toBeVisible();
    await expect(page.getByText('Attempts Export')).toBeVisible();
  });

  test('admin Account tab shows username and role', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await page.getByRole('button', { name: 'Leaderboard' }).click();
    await page.getByRole('button', { name: 'Account' }).click();
    await expect(page.getByText('Username')).toBeVisible();
    await expect(page.getByText('admin').first()).toBeVisible();
    await expect(page.getByText('Role')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Logout' })).toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// Admin — Attempts management
// ---------------------------------------------------------------------------

test.describe('Admin — Attempts', () => {
  test.describe.configure({ mode: 'serial' });

  test('attempts load for selected challenge', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await page.getByRole('button', { name: 'Attempts' }).click();
    // Challenge selector should be pre-populated with the first challenge
    await expect(page.locator('[role="combobox"]').first()).not.toBeEmpty();
    // Table body should have at least one row or show empty state
    const rows = page.getByRole('row');
    await expect(rows.first()).toBeVisible();
  });

  test('can switch challenge in Attempts tab', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await page.getByRole('button', { name: 'Attempts' }).click();
    await page.locator('[role="combobox"]').first().click();
    const options = page.getByRole('option');
    const count = await options.count();
    if (count > 1) {
      await options.nth(1).click();
      await expect(page.getByRole('heading', { name: 'All Attempts' })).toBeVisible();
    }
  });

  test('can open and close edit dialog for an attempt', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await page.getByRole('button', { name: 'Attempts' }).click();
    const editButtons = page.getByRole('row').nth(1).getByRole('button');
    const count = await editButtons.count();
    if (count > 0) {
      await editButtons.first().click();
      await expect(page.getByRole('dialog')).toBeVisible();
      await expect(page.getByText('Edit Attempt')).toBeVisible();
      await expect(page.getByLabel('Energy Used (Wh)')).toBeVisible();
      await page.getByRole('button', { name: 'Cancel' }).click();
      await expect(page.getByRole('dialog')).not.toBeVisible();
    }
  });

  test('edit attempt dialog updates validity status', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await page.getByRole('button', { name: 'Attempts' }).click();
    const editButtons = page.getByRole('row').nth(1).getByRole('button');
    if (await editButtons.count() > 0) {
      await editButtons.first().click();
      await expect(page.getByRole('dialog')).toBeVisible();
      await page.getByLabel('Validity Status').click();
      await expect(page.getByRole('option', { name: '✓ Valid' })).toBeVisible();
      await expect(page.getByRole('option', { name: '✗ Invalid' })).toBeVisible();
      // Close without saving
      await page.keyboard.press('Escape');
    }
  });
});

// ---------------------------------------------------------------------------
// Admin — Challenges management
// ---------------------------------------------------------------------------

test.describe('Admin — Challenges', () => {
  test.describe.configure({ mode: 'serial' });

  test('challenges table lists existing challenges', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await page.getByRole('button', { name: 'Challenges' }).click();
    // At least the header row should be visible
    await expect(page.getByRole('columnheader', { name: 'Name' })).toBeVisible();
    await expect(page.getByRole('columnheader', { name: 'Max Attempts' })).toBeVisible();
    await expect(page.getByRole('columnheader', { name: 'Start MACs' })).toBeVisible();
    await expect(page.getByRole('columnheader', { name: 'Finish MACs' })).toBeVisible();
  });

  test('can open and cancel challenge edit dialog', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await page.getByRole('button', { name: 'Challenges' }).click();
    const editBtn = page.getByRole('row').nth(1).getByRole('button');
    if (await editBtn.count() > 0) {
      await editBtn.first().click();
      await expect(page.getByRole('dialog')).toBeVisible();
      await expect(page.getByText('Edit Challenge')).toBeVisible();
      await expect(page.getByLabel('Challenge Name')).toBeVisible();
      await expect(page.getByLabel('Max Attempts')).toBeVisible();
      await page.getByRole('button', { name: 'Cancel' }).click();
      await expect(page.getByRole('dialog')).not.toBeVisible();
    }
  });

  test('challenge edit dialog pre-fills existing values', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await page.getByRole('button', { name: 'Challenges' }).click();
    const editBtn = page.getByRole('row').nth(1).getByRole('button');
    if (await editBtn.count() > 0) {
      const challengeName = await page.getByRole('row').nth(1).getByRole('cell').nth(0).innerText();
      await editBtn.first().click();
      await expect(page.getByLabel('Challenge Name')).toHaveValue(challengeName);
      await page.getByRole('button', { name: 'Cancel' }).click();
    }
  });
});

// ---------------------------------------------------------------------------
// Admin — Export
// ---------------------------------------------------------------------------

test.describe('Admin — Export', () => {
  test.describe.configure({ mode: 'serial' });

  test('leaderboard export controls are all present', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await page.getByRole('button', { name: 'Export' }).click();
    await expect(page.getByText('Leaderboard Export')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Export Leaderboard' })).toBeEnabled();
  });

  test('attempts export controls are all present', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await page.getByRole('button', { name: 'Export' }).click();
    await expect(page.getByText('Attempts Export')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Export Attempts' })).toBeEnabled();
  });

  test('can change leaderboard export format to Excel', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await page.getByRole('button', { name: 'Export' }).click();
    await page.getByRole('combobox').nth(2).click();
    await page.getByRole('option', { name: 'Excel' }).click();
    await expect(page.getByRole('combobox').filter({ hasText: 'Excel' })).toBeVisible();
  });

  test('can change leaderboard category', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await page.getByRole('button', { name: 'Export' }).click();
    const categorySelect = page.locator('[role="combobox"]').filter({ hasText: /class|series/i }).first();
    await categorySelect.click();
    await page.getByRole('option', { name: 'Professional Class' }).click();
    await expect(categorySelect).toHaveText('Professional Class');
  });
});

// ---------------------------------------------------------------------------
// Admin — Leaderboard
// ---------------------------------------------------------------------------

test.describe('Admin — Leaderboard', () => {
  test.describe.configure({ mode: 'serial' });

  test('leaderboard shows three category columns', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await page.getByRole('button', { name: 'Leaderboard' }).click();
    await expect(page.getByText('Close to Series')).toBeVisible();
    await expect(page.getByText('Advanced Class')).toBeVisible();
    await expect(page.getByText('Professional Class')).toBeVisible();
  });

  test('can switch challenge on leaderboard', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await page.getByRole('button', { name: 'Leaderboard' }).click();
    await page.locator('[role="combobox"]').first().click();
    const options = page.getByRole('option');
    if (await options.count() > 1) {
      await options.nth(1).click();
    }
    await expect(page.getByText('Advanced Class')).toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// Login — edge cases
// ---------------------------------------------------------------------------

test.describe('Login', () => {
  test.describe.configure({ mode: 'serial' });

  test('wrong credentials show an error', async ({ page }) => {
    await page.goto(BASE);
    await page.getByRole('button', { name: 'Account' }).click();
    await page.getByRole('textbox', { name: 'Username' }).fill('notauser');
    await page.getByRole('textbox', { name: 'Password' }).fill('wrongpassword');
    await page.getByRole('button', { name: 'Login' }).click();
    await expect(page.getByRole('alert')).toBeVisible();
  });

  test('login form clears after successful login', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    // After login the form is replaced by account info — no inputs visible
    await page.getByRole('button', { name: 'Account' }).click();
    await expect(page.getByRole('textbox', { name: 'Username' })).not.toBeVisible();
  });

  test('logging out returns to login form', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await logout(page);
    await expect(page.getByRole('heading', { name: 'Login' })).toBeVisible();
    await expect(page.getByRole('textbox', { name: 'Username' })).toBeVisible();
  });

  test('logging out hides admin-only tabs', async ({ page }) => {
    await loginAs(page, 'admin', 'changeme');
    await expect(page.getByRole('button', { name: 'Attempts' })).toBeVisible();
    await logout(page);
    await expect(page.getByRole('button', { name: 'Attempts' })).not.toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// Teamlead role
// ---------------------------------------------------------------------------

test.describe('Teamlead navigation', () => {
  test.describe.configure({ mode: 'serial' });

  test('teamlead only sees allowed tabs', async ({ page }) => {
    await loginAs(page, 'teamlead', 'changeme');
    await expect(page.getByRole('button', { name: 'Leaderboard' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Teams' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Account' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Attempts' })).not.toBeVisible();
    await expect(page.getByRole('button', { name: 'Users' })).not.toBeVisible();
    await expect(page.getByRole('button', { name: 'Export' })).not.toBeVisible();
    await expect(page.getByRole('button', { name: 'Challenges' })).not.toBeVisible();
  });

  test('teamlead Teams tab shows their own team view', async ({ page }) => {
    await loginAs(page, 'teamlead', 'changeme');
    await page.getByRole('button', { name: 'Teams' }).click();
    await expect(page.getByRole('heading', { name: /team/i })).toBeVisible();
    // TeamLeadView has driver management; confirm admin TeamsTab heading is NOT shown
    await expect(page.getByRole('heading', { name: 'Teams Management' })).not.toBeVisible();
  });

  test('teamlead can view leaderboard', async ({ page }) => {
    await loginAs(page, 'teamlead', 'changeme');
    await page.getByRole('button', { name: 'Leaderboard' }).click();
    await expect(page.getByText('Advanced Class')).toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// Viewer role
// ---------------------------------------------------------------------------

test.describe('Viewer navigation', () => {
  test.describe.configure({ mode: 'serial' });

  test('viewer only sees Leaderboard and Account', async ({ page }) => {
    await loginAs(page, 'viewer', 'changeme');
    await expect(page.getByRole('button', { name: 'Leaderboard' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Account' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Attempts' })).not.toBeVisible();
    await expect(page.getByRole('button', { name: 'Teams' })).not.toBeVisible();
    await expect(page.getByRole('button', { name: 'Export' })).not.toBeVisible();
  });

  test('viewer can view leaderboard', async ({ page }) => {
    await loginAs(page, 'viewer', 'changeme');
    await expect(page.getByText('Advanced Class')).toBeVisible();
  });
});