// himolde-study-friend/tests/FeedbackDisplay.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { vi } from 'vitest';
import FeedbackDisplay from '../src/components/FeedbackDisplay';
import { apiClient } from '../src/lib/api-client'; // Import the actual apiClient
import { axe } from 'vitest-axe'; // Import axe


// Mock the apiClient's sendFeedback method
vi.mock('../src/lib/api-client', () => ({
  apiClient: {
    sendFeedback: vi.fn(),
  },
}));

describe('FeedbackDisplay', () => {
  const mockQuery = 'What is the exam format?';
  const mockResponse = 'The exam is a 3-hour written test.';
  const mockOnFeedbackSubmit = vi.fn();

  beforeEach(() => {
    // Reset mocks before each test
    vi.clearAllMocks();
    // Ensure the mock is set to resolve successfully for default cases
    (apiClient.sendFeedback as ReturnType<typeof vi.fn>).mockResolvedValue({ message: 'Feedback received.' });
  });

  // AC 3.1.1: Test rendering of feedback icons.
  test('renders thumbs up and thumbs down icons initially', () => {
    render(<FeedbackDisplay query={mockQuery} response={mockResponse} onFeedbackSubmit={mockOnFeedbackSubmit} />);

    const thumbsUpButton = screen.getByLabelText('Thumbs up for helpful response');
    const thumbsDownButton = screen.getByLabelText('Thumbs down for unhelpful response');

    expect(thumbsUpButton).toBeInTheDocument();
    expect(thumbsDownButton).toBeInTheDocument();
    expect(thumbsUpButton).toBeEnabled();
    expect(thumbsDownButton).toBeEnabled();
  });

  // AC 3.1.2 & AC 3.1.3: Test UI state changes after feedback (icons disabled/thank you message).
  // Mock ApiClient.sendFeedback to verify calls.
  test('sends feedback and updates UI on thumbs up click', async () => {
    render(<FeedbackDisplay query={mockQuery} response={mockResponse} onFeedbackSubmit={mockOnFeedbackSubmit} />);

    const thumbsUpButton = screen.getByLabelText('Thumbs up for helpful response');
    fireEvent.click(thumbsUpButton);

    // Expect the mock function to have been called with correct data
    await waitFor(() => {
      expect(mockOnFeedbackSubmit).toHaveBeenCalledTimes(1);
      expect(mockOnFeedbackSubmit).toHaveBeenCalledWith({
        query: mockQuery,
        response: mockResponse,
        rating: 1,
      });
    });

    // AC 3.1.3: Verify UI state change (Thank you message displayed, buttons are gone)
    expect(screen.getByText('Thank you for your feedback!')).toBeInTheDocument();
    expect(screen.queryByLabelText('Thumbs up for helpful response')).not.toBeInTheDocument();
    expect(screen.queryByLabelText('Thumbs down for unhelpful response')).not.toBeInTheDocument();
  });

  test('sends feedback and updates UI on thumbs down click', async () => {
    render(<FeedbackDisplay query={mockQuery} response={mockResponse} onFeedbackSubmit={mockOnFeedbackSubmit} />);

    const thumbsDownButton = screen.getByLabelText('Thumbs down for unhelpful response');
    fireEvent.click(thumbsDownButton);

    // Expect the mock function to have been called with correct data
    await waitFor(() => {
      expect(mockOnFeedbackSubmit).toHaveBeenCalledTimes(1);
      expect(mockOnFeedbackSubmit).toHaveBeenCalledWith({
        query: mockQuery,
        response: mockResponse,
        rating: -1,
      });
    });

    // AC 3.1.3: Verify UI state change (Thank you message displayed, buttons are gone)
    expect(screen.getByText('Thank you for your feedback!')).toBeInTheDocument();
    expect(screen.queryByLabelText('Thumbs up for helpful response')).not.toBeInTheDocument();
    expect(screen.queryByLabelText('Thumbs down for unhelpful response')).not.toBeInTheDocument();
  });

  test('handles feedback submission error gracefully', async () => {
    (mockOnFeedbackSubmit as ReturnType<typeof vi.fn>).mockRejectedValueOnce(new Error('Network Error'));

    render(<FeedbackDisplay query={mockQuery} response={mockResponse} onFeedbackSubmit={mockOnFeedbackSubmit} />);

    const thumbsUpButton = screen.getByLabelText('Thumbs up for helpful response');
    fireEvent.click(thumbsUpButton);

    // Expect the mock function to have been called
    await waitFor(() => {
      expect(mockOnFeedbackSubmit).toHaveBeenCalledTimes(1);
    });

    // Expect buttons to be re-enabled
    expect(await screen.findByLabelText('Thumbs up for helpful response')).toBeEnabled();
    expect(await screen.findByLabelText('Thumbs down for unhelpful response')).toBeEnabled();
    expect(screen.queryByText('Thank you for your feedback!')).not.toBeInTheDocument();
  });

  // AC 3.1.1, 3.1.3: Accessibility Testing for FeedbackDisplay
  test('should not have any accessibility violations', async () => {
    const { container } = render(<FeedbackDisplay query={mockQuery} response={mockResponse} onFeedbackSubmit={mockOnFeedbackSubmit} />);
    expect(await axe(container)).toHaveNoViolations();
  });
});

