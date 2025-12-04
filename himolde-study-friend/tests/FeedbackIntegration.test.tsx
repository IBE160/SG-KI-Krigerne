// himolde-study-friend/tests/FeedbackIntegration.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { vi } from 'vitest';
import FeedbackDisplay from '../src/components/FeedbackDisplay';
import { apiClient } from '../src/lib/api-client'; // Import the actual apiClient

// Mock the apiClient's sendFeedback method at the module level
vi.mock('../src/lib/api-client', () => ({
  apiClient: {
    sendFeedback: vi.fn(),
  },
}));

describe('Feedback Integration Test', () => {
  const mockQuery = 'Tell me about the course CS101.';
  const mockResponse = 'CS101 is an introduction to computer science.';

  beforeEach(() => {
    vi.clearAllMocks();
    // Ensure the mock is set to resolve successfully for default cases
    (apiClient.sendFeedback as ReturnType<typeof vi.fn>).mockResolvedValue({ message: 'Feedback received.' });
  });

  test('simulates full feedback submission flow from UI click to mocked backend call', async () => {
    // 1. Render the FeedbackDisplay component.
    render(
      <FeedbackDisplay
        query={mockQuery}
        response={mockResponse}
        onFeedbackSubmit={async (data) => apiClient.sendFeedback(data)}
      />
    );

    // Initial state: buttons should be visible and enabled
    const thumbsUpButton = screen.getByLabelText('Thumbs up for helpful response');
    const thumbsDownButton = screen.getByLabelText('Thumbs down for unhelpful response');
    expect(thumbsUpButton).toBeInTheDocument();
    expect(thumbsDownButton).toBeInTheDocument();
    expect(thumbsUpButton).toBeEnabled();
    expect(thumbsDownButton).toBeEnabled();

    // 2. Simulate a user click on a feedback icon (Thumbs Up).
    fireEvent.click(thumbsUpButton);

    // 3. Assert that apiClient.sendFeedback was called with the correct data.
    await waitFor(() => {
      expect(apiClient.sendFeedback).toHaveBeenCalledTimes(1);
      expect(apiClient.sendFeedback).toHaveBeenCalledWith({
        query: mockQuery,
        response: mockResponse,
        rating: 1,
      });
    });

    // 4. Assert that the UI updates correctly after the (mocked) submission.
    expect(screen.getByText('Thank you for your feedback!')).toBeInTheDocument();
    expect(screen.queryByLabelText('Thumbs up for helpful response')).not.toBeInTheDocument();
    expect(screen.queryByLabelText('Thumbs down for unhelpful response')).not.toBeInTheDocument();
  });

  test('simulates feedback submission error and verifies UI behavior', async () => {
    // Mock the API call to reject, simulating a backend error
    (apiClient.sendFeedback as ReturnType<typeof vi.fn>).mockRejectedValueOnce(new Error('Backend error'));

    render(
      <FeedbackDisplay
        query={mockQuery}
        response={mockResponse}
        onFeedbackSubmit={async (data) => apiClient.sendFeedback(data)}
      />
    );

    const thumbsDownButton = screen.getByLabelText('Thumbs down for unhelpful response');
    fireEvent.click(thumbsDownButton);

    // Assert that apiClient.sendFeedback was called
    await waitFor(() => {
      expect(apiClient.sendFeedback).toHaveBeenCalledTimes(1);
    });

    // Verify UI reverts to allowing re-submission
    expect(await screen.findByLabelText('Thumbs up for helpful response')).toBeEnabled();
    expect(await screen.findByLabelText('Thumbs down for unhelpful response')).toBeEnabled();
    expect(screen.queryByText('Thank you for your feedback!')).not.toBeInTheDocument();
  });
});
