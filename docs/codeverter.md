# CodeVerter

## Overview

CodeVerter is an AI-powered code conversion tool that allows developers to convert code between 25+ programming languages using Claude AI. This tool is part of the FaceCode Guardian Network ecosystem, providing transparency and accessibility for code transformation needs.

## Features

- **25+ Programming Languages**: Support for Python, JavaScript, TypeScript, Java, C++, C#, Go, Rust, and many more
- **Intuitive Interface**: Clean, dark-mode UI with side-by-side code comparison
- **Smart Language Selection**: Searchable dropdown menus for quick language selection
- **Real-time Conversion**: Instant code conversion powered by Claude AI
- **Error Handling**: Clear error messages and validation

## Supported Languages

Python, JavaScript, TypeScript, Java, C++, C#, C, Go, Rust, Swift, Kotlin, PHP, Ruby, Scala, R, MATLAB, Perl, Haskell, Lua, Dart, Elixir, F#, Clojure, Objective-C, Visual Basic

## Getting Started

### Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Claude AI API access (via window.claude.complete)

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### Usage

1. Select your source programming language from the dropdown
2. Select your target programming language
3. Enter or paste your code in the left panel
4. Click "Convert Code" to transform your code
5. Review the converted code in the right panel

## Technical Stack

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **AI Engine**: Claude AI

## Component Structure

```
src/
├── components/
│   └── CodeVerter.tsx    # Main component with language converter
├── App.tsx               # Root application component
├── main.tsx             # Application entry point
├── index.css            # Global styles with Tailwind
└── vite-env.d.ts        # TypeScript declarations
```

## API Integration

CodeVerter uses the Claude AI API through the `window.claude.complete()` interface. Ensure your environment has this API available:

```typescript
interface Window {
  claude: {
    complete: (prompt: string) => Promise<string>;
  };
}
```

## Ethical Considerations

As part of the FaceCode Guardian Network, CodeVerter adheres to ethical AI principles:

- **Transparency**: Clear indication of AI-powered conversion
- **User Control**: Manual review and adjustment capabilities
- **Accessibility**: Intuitive interface compliant with accessibility standards
- **Privacy**: Code processing respects user data privacy

## Future Enhancements

- Code syntax highlighting
- Multi-file conversion support
- Conversion history
- Export/download converted code
- Diff view for before/after comparison
- Support for code snippets library

## License

This project is part of the FaceCode Guardian Network and is distributed under the Ethical FaceCode License v1.0.

## Contributing

Contributions are welcome! Please ensure all code follows the ethical principles outlined in the FaceCode Guardian Network documentation.

---

**Part of the FaceCode Guardian Network**
*Protecting digital dignity through ethical AI*
