import asyncio
import os
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero, google, deepgram
from api import AssistantFnc

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a voice assistant created by LiveKit. Your interface with users will be voice. "
            "You should use short and concise responses, and avoiding usage of unpronouncable punctuation."
        ),
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    fnc_ctx = AssistantFnc()

    assitant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=deepgram.STT(),
        llm=google.LLM(model="gemini-2.0-flash",api_key= GOOGLE_API_KEY),
        # tts=deepgram.TTS(model='aura-hera-en'), 
        tts=google.TTS(language="en-IN",gender="female",voice_name="en-IN-Chirp-HD-F"),       
        chat_ctx=initial_ctx,
        fnc_ctx=fnc_ctx,
    )
    assitant.start(ctx.room)

    await asyncio.sleep(1)
    await assitant.say("Hey, how can I help you today!", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))