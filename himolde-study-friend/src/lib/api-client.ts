// frontend/src/lib/api-client.ts
import { FeedbackData } from '../types/feedback';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'; // Default to localhost

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async sendFeedback(feedbackData: FeedbackData): Promise<{ message: string }> {
    const response = await fetch(`${this.baseUrl}/feedback`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(feedbackData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to send feedback');
    }

    const result = await response.json();
    return result.data;
  }

  // TODO: Add other API methods as needed
}

export const apiClient = new ApiClient();
