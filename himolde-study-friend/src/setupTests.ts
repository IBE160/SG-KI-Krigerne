// himolde-study-friend/src/setupTests.ts
import '@testing-library/jest-dom'; // For extended DOM matchers
import { expect } from 'vitest'; // Import expect from vitest
import * as matchers from 'vitest-axe/matchers'; // Import all matchers

// Extend Vitest's expect with axe-core matchers
expect.extend(matchers);

// Mock scrollIntoView for JSDOM environment
window.HTMLElement.prototype.scrollIntoView = function() {};