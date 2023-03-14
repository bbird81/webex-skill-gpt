from webex_skills.api import SimpleAPI
from webex_skills.dialogue import responses
from webex_skills.models.mindmeld import DialogueState
import requests

api = SimpleAPI()

@api.handle(default=True)
async def greet(current_state: DialogueState) -> DialogueState:
    text = "Non ho capito, ma la skill funziona correttamente!"
    new_state = current_state.copy()
    new_state.directives = [responses.Reply(text), responses.Speak(text), responses.Sleep(10), ]
    return new_state

@api.handle(pattern=r'.*\sabracadabra\s?.*')
async def spawnguestwifi(current_state: DialogueState) -> DialogueState:

    text = 'Wifi Guest user created, now showing on device'
    new_state = current_state.copy()
    assistant_event_payload = {'name': 'wifiguest', 'payload': {'id': 'hackathon'}}
    new_state.directives = [responses.Reply(text), responses.Speak(text), responses.AssistantEvent(payload=assistant_event_payload), responses.Sleep(10), ]

    return new_state