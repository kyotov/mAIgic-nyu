import openai
import os

# Set your API key
openai.api_key = os.getenv("OPENAI_KEY")

# Make a request to the OpenAI API
response = openai.ChatCompletion.create(
  model="gpt-4",  # Specify the model, e.g., gpt-3.5-turbo, gpt-4
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
)

# Extract and print the response
print(response['choices'][0]['message']['content'])
