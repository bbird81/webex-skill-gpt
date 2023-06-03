from webex_skills.api import SimpleAPI
from webex_skills.dialogue import responses
from webex_skills.models.mindmeld import DialogueState
from . import tokens
import openai
import requests

openai.api_key = tokens.OPENAPI_KEY

api = SimpleAPI()

@api.handle(default=True)
async def greet(current_state: DialogueState) -> DialogueState:
    #text = "Non ho capito, ma la skill funziona correttamente!"
    #Recupero la richiesta fatta a WBX-ASST e la inoltro a ChatGPT
    request = DialogueState.history[0]['text']
    print(f"Inoltrerò la seguente richiesta a Chat-GTP:\n{'-'*20}\n{request}\n{'-'*20}\n")
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "Sei un chatbot"},
            {"role": "user", "content": request}
        ]
    )
    #estraggo la risposta
    result = ''
    for choice in response.choices:
        result += choice.message.content

    text=result
    new_state = current_state.copy()
    new_state.directives = [responses.Reply(text), responses.Speak(text), responses.Sleep(10), ]
    return new_state

@api.handle(pattern=r'.*\s(saluta|salutare)\s?.*')
async def salutare(current_state: DialogueState) -> DialogueState:
    
    text = 'Grazie a tutti per essere intervenuti oggi, spero Thomas vi abbia raccontato cose interessanti!'
    new_state = current_state.copy()
    #assistant_event_payload = {'name': 'wifiguest', 'payload': {'id': 'hackathon'}}
    #new_state.directives = [responses.Reply(text), responses.Speak(text), responses.AssistantEvent(payload=assistant_event_payload), responses.Sleep(10), ]
    new_state.directives = [responses.Reply(text), responses.Speak(text), responses.Sleep(10), ]

    return new_state