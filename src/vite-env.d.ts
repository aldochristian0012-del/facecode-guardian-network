/// <reference types="vite/client" />

// Claude API type definition
interface Window {
  claude: {
    complete: (prompt: string) => Promise<string>;
  };
}
