import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

AI_API_KEY = os.getenv("AI_API_KEY")


# to be added
#with open("personality.json", "r", encoding="utf-8") as f:
#    prompt = json.load(f)["prompt"]
prompt = '''

'''


conversationHistory = []

def aiTextInTextOut(_userInput):
    # add user input to conversation history
    conversationHistory.append({
        'type': 'message',
        'role': 'user',
        'content': [
            {
                'type': 'input_text',
                'text': _userInput,
            },
        ],
    })

    # request body
    response = requests.post(
        'https://ai.hackclub.com/proxy/v1/responses',
        headers={
            'Authorization': f"Bearer {AI_API_KEY}",
            'Content-Type': 'application/json',
        },
        json={
            'model': 'google/gemini-2.5-flash',
            'input': conversationHistory,   
            'max_output_tokens': 9000,
        }
    ).json()

    # store reply
    conversationHistory.append({
        'type': 'message',
        'role': 'assistant',
        'id': response["output"][0]["id"],
        'status': 'completed',
        'content': response["output"][0]["content"]
    })

    # return response
    return response["output"][0]["content"][0]["text"]


def initAiPrompt():
    
    # this defines the first message as the prompt
    conversationHistory.append({
        'type': 'message',
        'role': 'user',
        'content': [
            {
                'type': 'input_text',
                'text': prompt,
            },
        ],
    })

    # the request body
    response = requests.post(
        'https://ai.hackclub.com/proxy/v1/responses',
        headers={
            'Authorization': f"Bearer {AI_API_KEY}",
            'Content-Type': 'application/json',
        },
        json={
            'model': 'google/gemini-2.5-flash',
            'input': conversationHistory,   # send full history
            'max_output_tokens': 9000,
        }
    ).json()

    # store reply
    conversationHistory.append({
        'type': 'message',
        'role': 'assistant',
        'id': response["output"][0]["id"],
        'status': 'completed',
        'content': response["output"][0]["content"]
    })


initAiPrompt()

userInput = input("Message: ")

result = aiTextInTextOut(userInput)

print(result)
