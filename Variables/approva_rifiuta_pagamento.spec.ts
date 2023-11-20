import { test, expect } from '@playwright/test';
 
test('approva_pagamento', async ({ page }) => {
  await page.goto("URL");
  await page.getByPlaceholder('Codice Identificativo').click();
  await page.getByPlaceholder('Codice Identificativo').fill('1234567');
  await page.getByPlaceholder('PIN/Password ').click();
  await page.getByPlaceholder('PIN/Password ').fill('1');
  await page.getByRole('button', { name: 'Accedi' }).click();
  await page.locator('#codiceOTP').fill('1');
  await page.getByRole('button', { name: 'Accedi' }).click();
  await page.getByText('IBAN:IT77O0848283352871412938123').click();
  await page.getByRole('button', { name: 'SELEZIONA' }).click();
});

test('rifiuta_pagamento', async ({ page }) => {
    await page.goto("url");
    await page.getByPlaceholder('Codice Identificativo').click();
    await page.getByPlaceholder('Codice Identificativo').fill('1234567');
    await page.getByPlaceholder('PIN/Password ').click();
    await page.getByPlaceholder('PIN/Password ').fill('1');
    await page.getByRole('button', { name: 'Accedi' }).click();
    await page.locator('#codiceOTP').fill('1');
    await page.getByRole('button', { name: 'Accedi' }).click();
    await page.getByText('IBAN:IT77O0848283352871412938123').click();
    await page.getByRole('button', { name: 'SELEZIONA' }).click();
  });
  