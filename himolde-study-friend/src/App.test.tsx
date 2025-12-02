import { render, screen } from '@testing-library/react';
import { expect, test } from 'vitest';
import App from './App';

test('renders Vite + React heading', () => {
  render(<App />);
  expect(screen.getByText('Vite + React')).toBeInTheDocument();
});
