import os

from openai import OpenAI

# Get API key from environment variable
api_key = "putapikeyhere"
client = OpenAI(api_key=api_key)


def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
    return transcript["text"]

def generate_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content


def text_to_speech(text, output_path):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    with open(output_path, "wb") as audio_file:
        audio_file.write(response["data"])
