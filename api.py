import enum
from typing import Annotated
from livekit.agents import llm
import logging
import aiohttp


logger = logging.getLogger("weather")
logger.setLevel(logging.INFO)

# first define a class that inherits from llm.FunctionContext
class AssistantFnc(llm.FunctionContext):
    # the llm.ai_callable decorator marks this function as a tool available to the LLM
    # by default, it'll use the docstring as the function's description
    @llm.ai_callable(description="get the weather for a location")
    async def get_weather(
        self,
        # by using the Annotated type, arg description and type are available to the LLM
        location: Annotated[
            str, llm.TypeInfo(description="The location to get the weather for")
        ],
    ):
        """Called when the user asks about the weather. This function will return the weather for the given location."""
        logger.info(f"getting weather for {location}")
        url = f"https://wttr.in/{location}?format=%C+%t"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    weather_data = await response.text()
                    # response from the function call is returned to the LLM
                    # as a tool response. The LLM's response will include this data
                    return f"The weather in {location} is {weather_data}."
                else:
                    raise f"Failed to get weather data, status code: {response.status}"
    
    @llm.ai_callable(description="Get attendance status of a user by name")
    async def get_attendance_status(
        self,
        username: Annotated[str, llm.TypeInfo(description="The user's name")],
    ):
        """Called when the user asks for attendance status by name."""
        logger.info(f"Fetching attendance for {username}")

        url = f"http://127.0.0.1:5000/attendance/{username}"  # Localhost API
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return f"{data['username']} is {data['status']}."
                else:
                    return f"User {username} not found."