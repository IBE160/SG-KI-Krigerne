import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect } from "vitest";
import ChatWindow from "./ChatWindow";

// Extend Vitest with DOM-specific assertions from @testing-library/jest-dom
import "@testing-library/jest-dom";

describe("ChatWindow @p0", () => {
  it("renders correctly with message history area, input field, and send button @p0 @smoke", () => {
    render(<ChatWindow />);

    // Check if the chat window is displayed (AC 3)
    const chatWindow = screen.getByLabelText(/chat window/i); // Using getByLabelText as div with aria-label does not automatically get 'complementary' role
    expect(chatWindow).toBeInTheDocument();

    // Check for the message history area (AC 4)
    const messageHistoryArea = screen.getByLabelText(/message history/i); // Using getByLabelText as ScrollArea with aria-label does not automatically get 'region' role
    expect(messageHistoryArea).toBeInTheDocument();

    // Check for the welcome message (AC 4)
    expect(
      screen.getByText(/welcome to himolde study friend/i),
    ).toBeInTheDocument();

    // Check for the text input field (AC 5)
    expect(
      screen.getByPlaceholderText(/type your message/i),
    ).toBeInTheDocument();

    // Check for the "Send" button (AC 6)
    expect(screen.getByRole("button", { name: /send/i })).toBeInTheDocument();
  });

  it("allows user to type into the input field", async () => {
    const user = userEvent.setup();
    render(<ChatWindow />);

    const inputField = screen.getByPlaceholderText(/type your message/i);
    await user.type(inputField, "Hello world");

    expect(inputField).toHaveValue("Hello world");
  });

  // Placeholder test for responsiveness (AC 7, 8)
  // Note: Full responsiveness testing requires browser environment (e.g., Playwright)
  // This test checks for basic structural elements relevant to responsiveness.
  it("has responsive container elements", () => {
    render(<ChatWindow />);
    const chatWindow = screen.getByLabelText(/chat window/i);
    // Expect some class that indicates responsiveness, e.g., flex-col
    expect(chatWindow).toHaveClass("flex-col"); // Assumes flex-col is part of responsive layout
  });

  // Placeholder test for keyboard navigation (AC 9)
  // Note: Full keyboard navigation testing involves simulating focus shifts,
  // which is better done with actual browser interaction or dedicated testing utilities.
  it("input field and button are keyboard accessible", async () => {
    const user = userEvent.setup();
    render(<ChatWindow />);
    const inputField = screen.getByPlaceholderText(/type your message/i);
    const sendButton = screen.getByRole("button", { name: /send/i });

    await user.tab();
    expect(inputField).toHaveFocus();
    await user.tab();
    expect(sendButton).toHaveFocus();
  });

  // Placeholder test for color contrast and aria-labels (AC 10, 11)
  // Note: Color contrast is difficult to test purely in JSDOM environment without visual tools.
  // aria-labels are already checked implicitly by getByRole(..., { name: ... })
  it("ensures core accessibility attributes are present", () => {
    render(<ChatWindow />);
    expect(screen.getByLabelText(/chat window/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/message history/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/type your message/i)).toHaveAttribute(
      "aria-label",
      expect.any(String),
    ); // Assuming Input component provides aria-label
    expect(screen.getByRole("button", { name: /send/i })).toHaveAttribute(
      "aria-label",
      expect.any(String),
    ); // Assuming Button component provides aria-label
  });

  describe("Message Submission and Echo @p1", () => {
    it("adds the message to history and clears input on send button click", async () => {
      const user = userEvent.setup();
      render(<ChatWindow />);
      const inputField = screen.getByPlaceholderText(/type your message/i);
      const sendButton = screen.getByRole("button", { name: /send/i });

      await user.type(inputField, "A new message");
      await user.click(sendButton);

      expect(screen.getByText("A new message")).toBeInTheDocument();
      expect(inputField).toHaveValue("");
    });

    it("adds the message to history and clears input on Enter key press", async () => {
      const user = userEvent.setup();
      render(<ChatWindow />);
      const inputField = screen.getByPlaceholderText(/type your message/i);

      await user.type(inputField, "Another message{enter}");

      expect(screen.getByText("Another message")).toBeInTheDocument();
      expect(inputField).toHaveValue("");
    });

    it("simulates a bot echo response after a short delay", async () => {
      const user = userEvent.setup();
      render(<ChatWindow />);
      const inputField = screen.getByPlaceholderText(/type your message/i);

      await user.type(inputField, "Echo this!{enter}");

      // The user's message appears instantly
      expect(screen.getByText("Echo this!")).toBeInTheDocument();

      // The bot's echo appears after a delay. findBy... queries wait for appearance.
      const botEcho = await screen.findByText("Echo this!", {
        selector: ".bg-muted", // Differentiate from user's message
      });
      expect(botEcho).toBeInTheDocument();
    });
  });
});
