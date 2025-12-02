import ChatWindow from "./components/ChatWindow";

function App() {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="bg-primary text-primary-foreground p-4">
        <h1 className="text-xl font-bold">Himolde Study Friend</h1>
      </header>
      <main className="flex-grow container mx-auto p-4 flex justify-center items-center">
        {/* Chat interface will be rendered here */}
        <div className="w-full max-w-lg h-full max-h-[calc(100vh-120px)]">
          {" "}
          {/* Adjust max-h as needed */}
          <ChatWindow />
        </div>
      </main>
      <footer className="bg-muted text-muted-foreground p-4 text-center">
        <p>&copy; {new Date().getFullYear()} Himolde Study Friend</p>
      </footer>
    </div>
  );
}

export default App;
