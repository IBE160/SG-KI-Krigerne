// frontend/src/types/feedback.ts
export interface FeedbackData {
  query: string;
  response: string;
  rating: 1 | -1; // 1 for thumbs up, -1 for thumbs down
  sessionId?: string; // Optional session ID
}