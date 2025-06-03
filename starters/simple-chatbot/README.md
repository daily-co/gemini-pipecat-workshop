# Simple Chatbot

<img src="image.png" width="420px">

This repository demonstrates a simple AI chatbot with real-time audio/video interaction, implemented using different client and server options. The bot server supports multiple AI backends, and you can connect to it using five different client approaches.

## Gemini Bot

A Gemini bot to power your voice AI client:

- Uses Google's Gemini Multimodal Live model
- Requires Gemini API key

## Five Client Options

1. **Daily Prebuilt** (Simplest)

   - Direct connection through a Daily Prebuilt room
   - For demo purposes only; handy for quick testing

2. **JavaScript**

   - Basic implementation using [Pipecat JavaScript SDK](https://docs.pipecat.ai/client/js/introduction)
   - No framework dependencies
   - Good for learning the fundamentals

3. **React**

   - Basic impelmentation using [Pipecat React SDK](https://docs.pipecat.ai/client/react/introduction)
   - Demonstrates the basic client principles with Pipecat React

4. **Android**

   - Basic implementation using [Pipecat Android SDK](https://docs.pipecat.ai/client/android/introduction)
   - Demonstrates the basic client principles with Pipecat Android

5. **iOS**
   - Basic implementation using [Pipecat iOS SDK](https://docs.pipecat.ai/client/ios/introduction)
   - Demonstrates the basic client principles with Pipecat iOS

## Quick Start

### First, start the bot server:

1. Navigate to the server directory:
   ```bash
   cd server
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy env.example to .env and configure:

   - Add your API keys

5. Start the server:
   ```bash
   python server.py
   ```

### Next, connect using your preferred client app:

- [Android Guide](client/android/README.md)
- [iOS Guide](client/ios/README.md)
- [Daily Prebuilt](client/prebuilt/README.md)
- [JavaScript Guide](client/javascript/README.md)
- [React Guide](client/react/README.md)

## Important Note

The bot server must be running for any of the client implementations to work. Start the server first before trying any of the client apps.

## Requirements

- Python 3.10+
- Node.js 16+ (for JavaScript and React implementations)
- Daily API key
- Gemini API key (for Gemini bot)
- Modern web browser with WebRTC support

## Project Structure

```
simple-chatbot/
├── server/              # Bot server implementation
│   ├── bot.py           # Gemini bot implementation
│   ├── runner.py        # Server runner utilities
│   ├── server.py        # FastAPI server
│   └── requirements.txt
└── client/              # Client implementations
    ├── android/         # Daily Android connection
    ├── ios/             # Daily iOS connection
    ├── javascript/      # Daily JavaScript connection
    ├── prebuilt/        # Pipecat Prebuilt client
    ├── react/           # Pipecat React client
    └── react-native/    # Pipecat React Native client
```
