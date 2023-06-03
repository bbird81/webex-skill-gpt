from webex_skills.api import SimpleAPI
from webex_skills.dialogue import responses
from webex_skills.models.mindmeld import DialogueState
import openai, os
import requests

openai.api_key = os.getenv("OPENAPI_KEY")

api = SimpleAPI()

@api.handle(default=True)
async def greet(current_state: DialogueState) -> DialogueState:
    #text = "Non ho capito, ma la skill funziona correttamente!"
    #Recupero la richiesta fatta a WBX-ASST e la inoltro a ChatGPT
    '''
    Formato di current_state:
    text='di parlare di leonardo da vinci usando al massimo 30 parole'
    context={'orgId': '84cdb17a-9c3b-4606-8012-cff9395757eb', 'userId': '65913665-ff3a-4b20-82fc-d2a5e4dfbfc5', 'userType': 'user', 'developerDeviceId': None, 'supportedDirectives': ['sleep', 'clear-web-view', 'speak', 'assistant-event', 'display-web-view', 'ui-hint', 'asr-hint', 'reply', 'listen']}
    params=Params(target_dialogue_state=None, time_zone='America/Los_Angeles', timestamp=1685800735, language='it', locale='it_IT', dynamic_resource={}, allowed_intents=None) 
    frame={} 
    history=[]
    directives=[]
    '''
    request = current_state.text
    print(f"Inoltrerò la seguente richiesta a Chat-GTP:\n{'-'*20}\n{request}\n{'-'*20}\n", flush=True)
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