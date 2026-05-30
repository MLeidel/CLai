from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("GPTKEY"))

models = client.models.list()
for model in models:
    print(model.id)
