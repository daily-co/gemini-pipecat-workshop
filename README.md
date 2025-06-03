# AI Eng World's Fair: Pipecat + Gemini Workshop

Welcome to the Pipecat + Gemini workshop! This repo will help you get set up to start building with Pipecat and Gemini. First up, let's get your dev environment configured and run a quickstart project.

## Prerequisites

- Python 3.10+
- Linux, MacOS, or Windows Subsystem for Linux (WSL)

## Quickstart

1. Download this repo to get started:

```bash
git clone git@github.com:daily-co/gemini-pipecat-workshop.git
cd gemini-pipecat-workshop
```

2. Set up a virtual environment:

```bash
python3 -m venv env
source env/bin/activate
```

3. Navigate to the quickstart directory:

```bash
cd quickstart
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create a `.env` file with your Google API key:

```bash
cp env.example .env
```

You can obtain a Google Gemini API key: https://aistudio.google.com/app/apikey.

> A free Daily API key is provided for you for the duration of this workshop.
> Sign up for your own Daily API key at: https://dashboard.daily.co.

6. Run the example:

```bash
python gemini-bot.py
```

You'll see a URL (http://localhost:7860) in the console output. Open this URL in your browser to join the session.

## Starters

Once your Pipecat environment is configured and you've run the quickstart, there are two example projects to reference as you build out your Gemini bot:

### simple-chatbot

For client/server apps, this is your starting point.

This starter contains client and server examples:

- Client: 6 different options to run your client, including
- Server: your Gemini bot, which will look very similar to the quickstart

Refer to the [simple-chatbot README](/starters/simple-chatbot/README.md) for more details.

### twilio-chatbot

For phone applications, this is your starting point.

This project includes a Gemini server bot that you can call via a Twilio websocket connection.

Refer to the [twilio-chatbot README](/starters/twilio-chatbot/README.md) for more details.

## Docs

- [Pipecat docs](https://docs.pipecat.ai): Contains guides, server docs, and client docs for the client SDKs
- [Gemini docs](https://ai.google.dev/gemini-api/docs/live)

## Other Gemini projects for reference:

- [Word Wrangler](https://github.com/pipecat-ai/pipecat/tree/main/examples/word-wrangler-gemini-live)

  - Web: A web-based game using Gemini Live, where the AI player tries to guess words your describe
  - Phone: A phone-based version of the same game, where two AI players join you in a word guessing game

- [AI Engineering World's Fair Voice helper](https://github.com/daily-co/ai-worlds-fair-bot)
  - This bot is featured on the AI Engineer World's Fair home page. See the client and server code that powers it.
