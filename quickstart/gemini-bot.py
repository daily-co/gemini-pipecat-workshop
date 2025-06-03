#
# Copyright (c) 2024–2025, Daily
#
# SPDX-License-Identifier: BSD 2-Clause License
#

import asyncio
import os
from datetime import datetime

import aiohttp
from dotenv import load_dotenv
from loguru import logger
from pipecat.adapters.schemas.function_schema import FunctionSchema
from pipecat.adapters.schemas.tools_schema import AdapterType, ToolsSchema
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.audio.vad.vad_analyzer import VADParams
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext
from pipecat.services.gemini_multimodal_live.gemini import (
    GeminiMultimodalLiveLLMService,
)
from pipecat.services.llm_service import FunctionCallParams
from pipecat.transports.services.daily import DailyParams, DailyTransport

from daily_runner import configure

load_dotenv(override=True)


#
# Configure your function call handlers:
# These functions run when the corresponding tool is called
#


async def fetch_weather_from_api(params: FunctionCallParams):
    temperature = 75 if params.arguments["format"] == "fahrenheit" else 24
    await params.result_callback(
        {
            "conditions": "nice",
            "temperature": temperature,
            "format": params.arguments["format"],
            "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        }
    )


async def fetch_restaurant_recommendation(params: FunctionCallParams):
    await params.result_callback({"name": "The Golden Dragon"})


#
# Provide a system instruction for Gemini Live
#

system_instruction = """
You are a helpful assistant who can answer questions and use tools.

You have three tools available to you:
1. get_current_weather: Use this tool to get the current weather in a specific location.
2. get_restaurant_recommendation: Use this tool to get a restaurant recommendation in a specific location.
3. google_search: Use this tool to search the web for information.
"""

#
# Define your functions using Pipecat's FunctionSchema format
# Alternatively, you can define using the native LLM format
#

weather_function = FunctionSchema(
    name="get_current_weather",
    description="Get the current weather",
    properties={
        "location": {
            "type": "string",
            "description": "The city and state, e.g. San Francisco, CA",
        },
        "format": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"],
            "description": "The temperature unit to use. Infer this from the user's location.",
        },
    },
    required=["location", "format"],
)
restaurant_function = FunctionSchema(
    name="get_restaurant_recommendation",
    description="Get a restaurant recommendation",
    properties={
        "location": {
            "type": "string",
            "description": "The city and state, e.g. San Francisco, CA",
        },
    },
    required=["location"],
)
search_tool = {"google_search": {}}

#
# ToolsSchema translates the tools to the native format
# Only required if using the FunctionSchema
#
tools = ToolsSchema(
    standard_tools=[weather_function, restaurant_function],
    custom_tools={AdapterType.GEMINI: [search_tool]},
)

#
# Run the quickstart
#


async def main():
    logger.info(f"Starting bot")

    async with aiohttp.ClientSession() as session:
        (room_url, token) = await configure(session)

        # Run example function with DailyTransport transport arguments.
        transport = DailyTransport(
            room_url,
            token,
            "Pipecat",
            params=DailyParams(
                audio_in_enabled=True,
                audio_out_enabled=True,
                vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.5)),
            ),
        )

        # Configure the Gemini Live Pipecat service
        llm = GeminiMultimodalLiveLLMService(
            api_key=os.getenv("GOOGLE_API_KEY"),
            system_instruction=system_instruction,
            tools=tools,
        )

        # Register tools so that Gemini Live has access
        llm.register_function("get_current_weather", fetch_weather_from_api)
        llm.register_function("get_restaurant_recommendation", fetch_restaurant_recommendation)

        # Configure a context and corresponding aggregator to collect conversation history
        # Add an initial user message to the context
        context = OpenAILLMContext(
            [{"role": "user", "content": "Say hello."}],
        )
        context_aggregator = llm.create_context_aggregator(context)

        # Configure your Pipeline. This will run the specified services continually
        pipeline = Pipeline(
            [
                transport.input(),
                context_aggregator.user(),
                llm,
                transport.output(),
                context_aggregator.assistant(),
            ]
        )

        # Configure a PipelineTask which configures and runs your Pipeline
        task = PipelineTask(
            pipeline,
            params=PipelineParams(
                allow_interruptions=True,
                enable_metrics=True,
                enable_usage_metrics=True,
            ),
        )

        # Event handler: On client connect, queue a context frame to initialize the conversation
        @transport.event_handler("on_client_connected")
        async def on_client_connected(transport, client):
            logger.info(f"Client connected")
            # Kick off the conversation.
            await task.queue_frames([context_aggregator.user().get_context_frame()])

        # Event handler: On client disconnect, cancel the PipelineTask and end the pipeline
        @transport.event_handler("on_client_disconnected")
        async def on_client_disconnected(transport, client):
            logger.info(f"Client disconnected")
            await task.cancel()

        # A runner instance which will run the PipelineTask
        runner = PipelineRunner()

        # Run the PipelineTask, which starts the Pipeline
        await runner.run(task)


if __name__ == "__main__":
    asyncio.run(main())
