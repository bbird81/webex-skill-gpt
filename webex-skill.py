from webex_skills.api import SimpleAPI
from webex_skills.dialogue import responses
from webex_skills.models.mindmeld import DialogueState
import openai, os

openai.api_key = os.getenv("OPENAI_KEY")
api = SimpleAPI()

@api.handle(default=True)
async def greet(current_state: DialogueState) -> DialogueState:
    request = current_state.text
    print(f"Text sent to ChatGPT:\n{'-'*20}\n{request}\n{'-'*20}\n", flush=True)
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user", "content": request}
        ]
    )
    result = ''
    for choice in response.choices:
        result += choice.message.content

    text=result
    new_state = current_state.copy()
    new_state.directives = [responses.Reply(text), responses.Speak(text), responses.Sleep(10), ]
    return new_state