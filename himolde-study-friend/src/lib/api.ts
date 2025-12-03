// himolde-study-friend/src/lib/api.ts

interface ChatResponseChunk {
  type: "chunk" | "done";
  content?: string;
}

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function streamChatResponse(
  query: string,
  onNewChunk: (chunk: string) => void,
  onComplete: () => void,
  onError: (error: Error) => void
) {
  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to get chat response");
    }

    const reader = response.body
      ?.pipeThrough(new TextDecoderStream())
      .getReader();

    if (!reader) {
      throw new Error("Failed to get readable stream from response.");
    }

    let accumulatedContent = "";
    while (true) {
      const { value, done } = await reader.read();
      if (done) {
        break;
      }

      // Process each line for SSE format "data: {json}\n\n"
      const lines = value.split("\n\n").filter(Boolean); // Split by double newline and remove empty strings
      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const jsonString = line.substring(6);
          try {
            const parsedChunk: ChatResponseChunk = JSON.parse(jsonString);
            if (parsedChunk.type === "chunk" && parsedChunk.content) {
              accumulatedContent += parsedChunk.content;
              onNewChunk(accumulatedContent); // Send accumulated content for real-time display
            } else if (parsedChunk.type === "done") {
              onComplete();
              return;
            }
          } catch (jsonError) {
            console.error("Failed to parse JSON chunk:", jsonString, jsonError);
            onError(new Error("Failed to parse chat response chunk."));
            return;
          }
        }
      }
    }
  } catch (error: any) {
    console.error("Streaming chat response error:", error);
    onError(error);
  }
}
