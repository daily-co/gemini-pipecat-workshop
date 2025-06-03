#
# Copyright (c) 2024–2025, Daily
#
# SPDX-License-Identifier: BSD 2-Clause License
#

import argparse
import os

import aiohttp
from pipecat.transports.services.helpers.daily_rest import (
    DailyRESTHelper,
    DailyRoomParams,
)


async def configure(aiohttp_session: aiohttp.ClientSession):
    parser = argparse.ArgumentParser(description="Daily AI SDK Bot Sample")
    parser.add_argument(
        "-k",
        "--apikey",
        type=str,
        required=False,
        help="Daily API Key (needed to create an owner token for the room)",
    )

    args, unknown = parser.parse_known_args()

    key = args.apikey or os.getenv("DAILY_API_KEY")

    if not key:
        raise Exception(
            "No Daily API key specified. use the -k/--apikey option from the command line, or set DAILY_API_KEY in your environment to specify a Daily API key."
        )

    daily_rest_helper = DailyRESTHelper(
        daily_api_key=key,
        daily_api_url=os.getenv("DAILY_API_URL", "https://api.daily.co/v1"),
        aiohttp_session=aiohttp_session,
    )

    room = await daily_rest_helper.create_room(DailyRoomParams())
    if not room.url:
        raise Exception("Failed to create Daily room")
    room_url = room.url

    token = await daily_rest_helper.get_token(room_url)
    if not token:
        raise Exception(f"Failed to create Daily room token: {room_url}")

    return (room_url, token)
