import os
import openai

def run_api(model, prompt, temperature: float = 0):
    openai.api_key = ""
    client = openai.OpenAI(api_key=openai.api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
    )
    resp = response.choices[0].message.content
    return resp


class Secretary:
    def __init__(self, model):
        self.model = model

    def get_response(self, prompt):
        return run_api(self.model, prompt)