// himolde-study-friend/tests/ChatWindow.test.tsx
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import ChatWindow from "@/components/ChatWindow";
import { vi } from "vitest";
import * as api from "@/lib/api"; // Import the actual module

// Spy on the streamChatResponse function
const mockStreamChatResponse = vi.spyOn(api, "streamChatResponse");

describe("ChatWindow", () => {
  beforeEach(() => {
    // Reset the mock before each test
    mockStreamChatResponse.mockReset();
    // Default mock implementation for successful streaming
    mockStreamChatResponse.mockImplementation(
      async (query, onNewChunk, onComplete, onError) => {
        const fullResponse = `Bot response to: ${query}`;
        // Simulate streaming in chunks
        let currentContent = "";
        for (let i = 0; i < fullResponse.length; i++) {
          currentContent += fullResponse[i];
          onNewChunk(currentContent);
          await new Promise((resolve) => setTimeout(resolve, 10)); // Small delay to simulate async
        }
        onComplete();
      }
    );
  });

  test("renders welcome message and input field", () => {
    render(<ChatWindow />);

    expect(
      screen.getByText(/Welcome to Himolde Study Friend!/i)
    ).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Type your message.../i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Send/i })).toBeInTheDocument();
  });

  test("sends a user message and displays it", async () => {
    render(<ChatWindow />);
    const input = screen.getByPlaceholderText(/Type your message.../i);
    const sendButton = screen.getByRole("button", { name: /Send/i });

    fireEvent.change(input, { target: { value: "Hello bot" } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText("Hello bot")).toBeInTheDocument();
    });
    expect(input).toHaveValue(""); // Input should be cleared
  });

  test("displays typing indicator and streams bot response", async () => {
    render(<ChatWindow />);
    const input = screen.getByPlaceholderText(/Type your message.../i);
    const sendButton = screen.getByRole("button", { name: /Send/i });

    fireEvent.change(input, { target: { value: "Test streaming" } });
    fireEvent.click(sendButton);

    // Expect typing indicator to appear
    await waitFor(() => {
      expect(screen.getByText(/Himolde Study Friend is typing.../i)).toBeInTheDocument();
    });

    // Check if the bot's message is being streamed and updated
    await waitFor(
      () => {
        expect(screen.getByText(/Bot response to: Test streaming/i)).toBeInTheDocument();
      },
      { timeout: 2000 } // Give it some time to stream
    );

    // Expect typing indicator to disappear after streaming completes
    await waitFor(() => {
      expect(screen.queryByText(/Himolde Study Friend is typing.../i)).not.toBeInTheDocument();
    });

    expect(mockStreamChatResponse).toHaveBeenCalledWith(
      "Test streaming",
      expect.any(Function),
      expect.any(Function),
      expect.any(Function)
    );
  });

  test("disables input and send button while bot is typing", async () => {
    render(<ChatWindow />);
    const input = screen.getByPlaceholderText(/Type your message.../i);
    const sendButton = screen.getByRole("button", { name: /Send/i });

    fireEvent.change(input, { target: { value: "Disable test" } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(input).toBeDisabled();
      expect(sendButton).toBeDisabled();
    });

    // Wait for streaming to complete
    await waitFor(
      () => {
        expect(input).not.toBeDisabled();
        expect(sendButton).not.toBeDisabled();
      },
      { timeout: 2000 }
    );
  });

  test("handles streaming error gracefully", async () => {
    const errorMessage = "Network error during streaming";
    mockStreamChatResponse.mockImplementationOnce(
      async (query, onNewChunk, onComplete, onError) => {
        onError(new Error(errorMessage));
      }
    );

    render(<ChatWindow />);
    const input = screen.getByPlaceholderText(/Type your message.../i);
    const sendButton = screen.getByRole("button", { name: /Send/i });

    fireEvent.change(input, { target: { value: "Error test" } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument();
    });

    // Typing indicator should disappear
    expect(screen.queryByText(/Himolde Study Friend is typing.../i)).not.toBeInTheDocument();
    // Input and button should be re-enabled
    expect(input).not.toBeDisabled();
    expect(sendButton).not.toBeDisabled();
  });
});
