import React from "react";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

const ChatWindow: React.FC = () => {
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
        {/* Chat messages will go here */}
        <ScrollBar orientation="vertical" />
      </ScrollArea>

      {/* Input field and send button */}
      <div className="border-t p-4 flex items-center gap-2">
        {/* Input component */}
        <Input
          type="text"
          placeholder="Type your message..."
          className="flex-grow" // shadcn/ui Input has its own styling
          aria-label="Message input"
        />
        {/* Send button */}
        <Button aria-label="Send message">Send</Button>
      </div>
    </div>
  );
};

export default ChatWindow;
