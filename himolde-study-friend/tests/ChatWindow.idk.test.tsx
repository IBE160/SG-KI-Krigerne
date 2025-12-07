import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { expect } from 'vitest';
import ChatWindow from '../src/components/ChatWindow';
import * as api from '../src/lib/api'; // Import the api module to spy on it

describe('ChatWindow - "I don\'t know" scenario', () => {
  const mockStreamChatResponse = (message: string) => {
    // Split message into smaller chunks to simulate streaming
    const messageChunks = message.match(/.{1,10}/g) || [message]; // Split into 10-char chunks

    return vi.fn(async (
        query: string,
        onNewChunk: (chunk: string) => void,
        onComplete: () => void,
        onError: (error: Error) => void
    ) => {
      let accumulatedContent = "";
      for (const chunk of messageChunks) {
        accumulatedContent += chunk;
        onNewChunk(accumulatedContent);
        await new Promise(resolve => setTimeout(resolve, 50)); // Simulate network delay for each chunk
      }
      onComplete(); // Call onComplete after all chunks are sent
    });
  };

  it('should display the "I don\'t know" message correctly when no info is found', async () => {
    const idkMessage = "I'm sorry, I couldn't find the information for that course. You may want to check the official course page.";
    
    // Spy on streamChatResponse and mock its implementation
    const streamChatResponseSpy = vi.spyOn(api, 'streamChatResponse')
      .mockImplementation(mockStreamChatResponse(idkMessage));

    render(<ChatWindow />);

    // Simulate user typing a query
    const messageInput = screen.getByPlaceholderText('Type your message...');
    fireEvent.change(messageInput, { target: { value: 'Tell me about a non-existent course' } });

    // Simulate clicking the send button
    const sendButton = screen.getByRole('button', { name: /send message/i });
    fireEvent.click(sendButton);

    // Expect the "I don't know" message to be displayed
    const botMessage = await screen.findByText(idkMessage);
    expect(botMessage).toBeInTheDocument();

    // Verify styling: check for bg-muted class on the parent message bubble
    expect(botMessage.closest('.bg-muted')).toBeInTheDocument();

    // Ensure the mock was called
    expect(streamChatResponseSpy).toHaveBeenCalledTimes(1);
    expect(streamChatResponseSpy).toHaveBeenCalledWith(
        'Tell me about a non-existent course',
        expect.any(Function), // Corrected to expect.any(Function) for onNewChunk
        expect.any(Function), // Corrected to expect.any(Function) for onComplete
        expect.any(Function)  // Corrected to expect.any(Function) for onError
    );
  }, 10000); // Test timeout remains 10s for overall test execution.
});
