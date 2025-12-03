import React, { useState, useRef, useEffect } from "react";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { v4 as uuidv4 } from 'uuid';
import { streamChatResponse } from "@/lib/api"; // Import the streaming API client

// Define the structure of a chat message
interface ChatMessage {
  id: string; // Use string for UUIDs for better uniqueness
  text: string;
  sender: "user" | "bot";
  streaming?: boolean; // Indicate if this message is currently being streamed
}

const ChatWindow: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false); // New state for typing indicator
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  const handleSendMessage = async () => {
    if (inputValue.trim() === "") return;

    const userMessageId = uuidv4();
    const userMessage: ChatMessage = {
      id: userMessageId,
      text: inputValue,
      sender: "user",
    };

    const botMessageId = uuidv4();
    const initialBotMessage: ChatMessage = {
      id: botMessageId,
      text: "", // Initial empty text for streaming bot response
      sender: "bot",
      streaming: true, // Mark as streaming
    };

    setMessages((prevMessages) => [...prevMessages, userMessage, initialBotMessage]);
    setInputValue("");
    setIsTyping(true); // Show typing indicator

    try {
      await streamChatResponse(
        userMessage.text,
        (chunk) => {
          // Update the bot's message with new chunks
          setMessages((prevMessages) =>
            prevMessages.map((msg) =>
              msg.id === botMessageId ? { ...msg, text: chunk } : msg
            )
          );
        },
        () => {
          // On complete, set streaming to false
          setMessages((prevMessages) =>
            prevMessages.map((msg) =>
              msg.id === botMessageId ? { ...msg, streaming: false } : msg
            )
          );
          setIsTyping(false); // Hide typing indicator
        },
        (error) => {
          // On error, display error message and set streaming to false
          setMessages((prevMessages) =>
            prevMessages.map((msg) =>
              msg.id === botMessageId
                ? { ...msg, text: `Error: ${error.message}`, streaming: false }
                : msg
            )
          );
          setIsTyping(false); // Hide typing indicator
        }
      );
    } catch (error: any) {
      console.error("Failed to stream chat response:", error);
      // Fallback for streamChatResponse initial fetch error
      setMessages((prevMessages) =>
        prevMessages.map((msg) =>
          msg.id === botMessageId
            ? { ...msg, text: `Error: ${error.message}`, streaming: false }
            : msg
        )
      );
      setIsTyping(false); // Hide typing indicator
    }
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter" && !isTyping) { // Prevent sending new message while bot is typing
      handleSendMessage();
    }
  };

  return (
    <div
      className="flex flex-col flex-grow bg-background rounded-lg shadow-md overflow-hidden"
      aria-label="Chat Window"
      data-testid="chat-window"
    >
      {/* Message history area */}
      <ScrollArea className="flex-grow p-4" aria-label="Message History" data-testid="message-history">
        {/* Welcome message */}
        <div className="mb-4 text-center text-muted-foreground">
          Welcome to Himolde Study Friend! How can I help you today?
        </div>
        {/* Chat messages */}
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex mb-2 ${
              message.sender === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`rounded-lg px-3 py-2 ${
                message.sender === "user"
                  ? "bg-primary text-primary-foreground"
                  : "bg-muted"
              }`}
            >
              {message.text}
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="flex mb-2 justify-start">
            <div className="rounded-lg px-3 py-2 bg-muted italic text-muted-foreground">
              Himolde Study Friend is typing...
            </div>
          </div>
        )}
        <div ref={endOfMessagesRef} />
        <ScrollBar orientation="vertical" />
      </ScrollArea>

      {/* Input field and send button */}
      <div className="border-t p-4 flex items-center gap-2">
        {/* Input component */}
        <Input
          type="text"
          placeholder="Type your message..."
          className="flex-grow"
          aria-label="Message input"
          data-testid="message-input"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isTyping} // Disable input while bot is typing
        />
        {/* Send button */}
        <Button aria-label="Send message" data-testid="send-button" onClick={handleSendMessage} disabled={isTyping}>
          Send
        </Button>
      </div>
    </div>
  );
};

export default ChatWindow;

