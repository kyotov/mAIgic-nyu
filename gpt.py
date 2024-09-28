from openai import OpenAI
import os

client = OpenAI()

# Set your API key

# Make a request to the OpenAI API
response = client.chat.completions.create(
    model="gpt-4",  # Specify the model, e.g., gpt-3.5-turbo, gpt-4
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of Bulgaria?"},
    ],
)

# Extract and print the response
print(response.choices[0].message.content)
