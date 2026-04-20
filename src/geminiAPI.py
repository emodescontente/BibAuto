from google import genai
from google.genai import types

async def InnitGeminiChat(APIkey: str, instructions: str = ""):
    client = genai.Client(api_key=APIkey)

    config = types.GenerateContentConfig(
        system_instruction=instructions,
        temperature=0.0 
    )

    chat = client.aio.chats.create(
        model="gemini-3.1-flash-lite-preview", 
        config=config
    )
    
    return chat, client

async def SendImageChat(src: str, message: str, chat, client):
    with open(src, 'rb') as f:
        image_bytes = f.read()     

    response = await chat.send_message([
        types.Part.from_bytes(
            data=image_bytes,
            mime_type='image/jpeg'
        ),
        message
    ])

    return response.text