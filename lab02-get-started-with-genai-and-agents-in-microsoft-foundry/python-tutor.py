# Before running the sample:
#    pip install azure-ai-projects>=2.1.0

import sys
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

endpoint = "your-project-endpoint"

# Initialize AI Project Client
project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

# Reference your newly created python-tutor agent
my_agent = "python-tutor"
my_version = "1"

openai_client = project_client.get_openai_client()

# Create a conversation context to remember previous messages in the session
conversation = openai_client.conversations.create()

print("--- Python & Data Science Tutor Initialized ---")
print("Ask any Python, Pandas, or NumPy questions below. Type 'quit' or 'exit' to stop.\n")

while True:
    user_input = input("You: ").strip()

    # Exit check
    if user_input.lower() in ["quit", "exit"]:
        print("\nHappy coding! Session ended.")
        break

    # Skip empty lines
    if not user_input:
        continue

    try:
        # Append user message to the conversation session
        openai_client.conversations.items.create(
            conversation_id=conversation.id,
            items=[{"type": "message", "role": "user", "content": user_input}]
        )

        # Send request to your python-tutor agent
        response = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent_reference": {"name": my_agent, "version": my_version, "type": "agent_reference"}}
        )

        print(f"\nPython Tutor: {response.output_text}\n")

    except Exception as e:
        print(f"\nAn error occurred: {e}\n")
