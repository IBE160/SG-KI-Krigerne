import { test, expect, Page } from '@playwright/test';

// Define the base URL of your application
const BASE_URL = 'http://localhost:5173';

test.describe('Chat Interface Responsiveness and Accessibility', () => {
  // Before each test, navigate to the base URL
  test.beforeEach(async ({ page }) => {
    await page.goto(BASE_URL);
  });

  test('should display chat interface responsively on desktop viewports', async ({ page }) => {
    // Desktop viewport sizes to test
    const desktopViewports = [
      { width: 1024, height: 768 },
      { width: 1280, height: 800 },
      { width: 1920, height: 1080 },
    ];

    for (const viewport of desktopViewports) {
      await page.setViewportSize(viewport);
      await expect(page.locator('.chat-container')).toBeVisible(); // Assuming a class 'chat-container' for the main chat area

      // Check if input field and send button are visible
      await expect(page.getByRole('textbox', { name: 'Chat input' })).toBeVisible(); // Assuming aria-label 'Chat input'
      await expect(page.getByRole('button', { name: 'Send' })).toBeVisible(); // Assuming aria-label 'Send' or text 'Send'

      // Optional: Add more specific assertions for layout, e.g., element positions or widths
      // await expect(page.locator('.chat-container')).toHaveCSS('width', `${viewport.width * 0.7}px`); // Example: if it takes 70% width
      // await expect(page.locator('.chat-container')).toHaveCSS('margin-left', 'auto');
      // await expect(page.locator('.chat-container')).toHaveCSS('margin-right', 'auto');

      // Take a screenshot for visual regression testing (optional but recommended)
      // await page.screenshot({ path: `playwright-screenshots/desktop-${viewport.width}.png` });
    }
  });

  test('should have keyboard navigation accessibility', async ({ page }) => {
    // Ensure the chat input is initially focused
    await expect(page.getByRole('textbox', { name: 'Chat input' })).toBeFocused();

    // Tab to the send button
    await page.keyboard.press('Tab');
    await expect(page.getByRole('button', { name: 'Send' })).toBeFocused();

    // If there are other interactive elements (e.g., feedback icons), tab through them
    // await page.keyboard.press('Tab');
    // await expect(page.getByRole('button', { name: 'Thumbs up' })).toBeFocused(); // Example feedback icon

    // Simulate typing and sending a message
    await page.getByRole('textbox', { name: 'Chat input' }).type('Hello, what are the mandatory assignments for TDT4140?');
    await page.keyboard.press('Enter');

    // Wait for the bot's response and check if it's rendered.
    // Assuming the bot's response appears in a div with a specific class or role
    await expect(page.locator('.bot-message-bubble')).toBeVisible(); // Assuming a class for bot messages

    // Focus should remain on the input field after sending a message
    await expect(page.getByRole('textbox', { name: 'Chat input' })).toBeFocused();
  });

  test('should have correct aria-labels for key interactive elements', async ({ page }) => {
    // Check aria-label for the chat input field
    const chatInput = page.getByRole('textbox', { name: 'Chat input' });
    await expect(chatInput).toHaveAttribute('aria-label', 'Chat input');

    // Check aria-label for the send button
    const sendButton = page.getByRole('button', { name: 'Send' });
    await expect(sendButton).toHaveAttribute('aria-label', 'Send message'); // Assuming a more descriptive aria-label

    // Example for a message bubble (if it has interactive elements or specific roles)
    // const firstBotMessage = page.locator('.bot-message-bubble').first();
    // await expect(firstBotMessage).toHaveAttribute('role', 'status'); // Or other appropriate role
    // await expect(firstBotMessage).toHaveAttribute('aria-live', 'polite');

    // If feedback icons exist
    // await expect(page.getByRole('button', { name: 'Thumbs up' })).toHaveAttribute('aria-label', 'Rate response as helpful');
    // await expect(page.getByRole('button', { name: 'Thumbs down' })).toHaveAttribute('aria-label', 'Rate response as unhelpful');
  });
});
