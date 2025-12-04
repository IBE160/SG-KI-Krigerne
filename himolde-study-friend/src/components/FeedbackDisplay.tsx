// frontend/src/components/FeedbackDisplay.tsx
import React, { useState } from 'react';
import { ThumbsUp, ThumbsDown } from 'lucide-react'; // Using lucide-react for icons

interface FeedbackDisplayProps {
  query: string;
  response: string;
  onFeedbackSubmit: (feedbackData: { query: string; response: string; rating: 1 | -1 }) => Promise<void>;
}

const FeedbackDisplay: React.FC<FeedbackDisplayProps> = ({ query, response, onFeedbackSubmit }) => {
  const [feedbackStatus, setFeedbackStatus] = useState<'idle' | 'submitted' | 'error'>('idle');
  const [submittedRating, setSubmittedRating] = useState<1 | -1 | null>(null);

  const handleFeedback = async (rating: 1 | -1) => {
    if (feedbackStatus !== 'idle') return; // Prevent multiple submissions

    setFeedbackStatus('submitted');
    setSubmittedRating(rating);

    try {
      await onFeedbackSubmit({ query, response, rating });
      // The component will naturally re-render with 'submitted' state
    } catch (error) {
      setFeedbackStatus('idle'); // Revert to idle to allow retry
      setSubmittedRating(null); // Clear rating on error
      console.error('Failed to submit feedback:', error);
      // TODO: Display a toast or other error message to the user
    }
  };

  if (feedbackStatus === 'submitted') {
    return (
      <div className="flex items-center text-sm text-gray-500 space-x-2">
        <span>Thank you for your feedback!</span>
        {submittedRating === 1 ? (
          <ThumbsUp className="h-4 w-4 text-green-500" fill="currentColor" />
        ) : (
          <ThumbsDown className="h-4 w-4 text-red-500" fill="currentColor" />
        )}
      </div>
    );
  }

  return (
    <div className="flex items-center space-x-2 text-gray-400">
      <button
        onClick={() => handleFeedback(1)}
        className="p-1 rounded-md hover:bg-gray-100 hover:text-green-500 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors duration-200"
        aria-label="Thumbs up for helpful response"
        disabled={feedbackStatus !== 'idle'} // Buttons are enabled only if idle
      >
        <ThumbsUp className="h-4 w-4" />
      </button>
      <button
        onClick={() => handleFeedback(-1)}
        className="p-1 rounded-md hover:bg-gray-100 hover:text-red-500 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors duration-200"
        aria-label="Thumbs down for unhelpful response"
        disabled={feedbackStatus !== 'idle'} // Buttons are enabled only if idle
      >
        <ThumbsDown className="h-4 w-4" />
      </button>
    </div>
  );
};

export default FeedbackDisplay;
