import React, { useState, useRef, useEffect } from "react";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

// Define the structure of a chat message
interface ChatMessage {
  id: number;
  text: string;
  sender: "user" | "bot";
}

const ChatWindow: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState("");
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = () => {
    if (inputValue.trim() === "") return;

    const userMessage: ChatMessage = {
      id: messages.length + 1,
      text: inputValue,
      sender: "user",
    };

    const currentInputValue = inputValue;
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInputValue("");

    // Simulate bot echo response
    setTimeout(() => {
      setMessages((prevMessages) => {
        const botMessage: ChatMessage = {
          id: prevMessages.length + 1,
          text: currentInputValue, // Echo the same message back
          sender: "bot",
        };
        return [...prevMessages, botMessage];
      });
    }, 500);
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      handleSendMessage();
    }
  };

  return (
    <div
      className="flex flex-col flex-grow bg-background rounded-lg shadow-md overflow-hidden"
      aria-label="Chat Window"
    >
      {/* Message history area */}
      <ScrollArea className="flex-grow p-4" aria-label="Message History">
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
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        {/* Send button */}
        <Button aria-label="Send message" onClick={handleSendMessage}>
          Send
        </Button>
      </div>
    </div>
  );
};

export default ChatWindow;
