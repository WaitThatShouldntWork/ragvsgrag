import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatCompletionResponse, ChatMessage
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client_mistral = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
client = OpenAI()
OpenAI.api_key= os.getenv("OPENAI_API_KEY")

def call_model(system_prompt, user_prompt):
    response = __get_response(system_prompt, user_prompt)
    return response.choices[0].message.content

def __get_response(system_prompt, user_prompt):
    response = client_mistral.chat(
        model="mistral-large-latest",
        response_format={"type": "json_object"},
        messages=[
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_prompt),
        ],
    )
    return response

def call_openai(system_prompt, user_prompt):
            response = client.chat.completions.create( 
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
            )
            return response.choices[0].message.content

# system_prompt = "You are a helpful assistant."
# user_prompt = "What is the capital of France?"
# print(call_model(system_prompt, user_prompt))