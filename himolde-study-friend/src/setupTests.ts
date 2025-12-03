// himolde-study-friend/src/setupTests.ts
import '@testing-library/jest-dom';

// Mock scrollIntoView as it's not implemented in JSDOM
window.HTMLElement.prototype.scrollIntoView = vi.fn();