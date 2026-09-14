import sys
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

endpoint = "https://project65061053-resource.services.ai.azure.com/api/projects/Project65061053"

# Initialize AI Project Client
project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

my_agent = "computing-historian"
my_version = "1"

openai_client = project_client.get_openai_client()

# Create a conversation session to maintain chat context across turns
conversation = openai_client.conversations.create()

print("--- Computing Historian Agent Initialized ---")
print("Type 'quit' or 'exit' to stop the chat.\n")

while True:
    user_input = input("You: ").strip()

    # Check if user wants to exit
    if user_input.lower() in ["quit", "exit"]:
        print("Goodbye!")
        break

    # Skip empty inputs
    if not user_input:
        continue

    try:
        # Add the user message to the conversation context
        openai_client.conversations.items.create(
            conversation_id=conversation.id,
            items=[{"type": "message", "role": "user", "content": user_input}]
        )

        # Get response from agent
        response = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent_reference": {"name": my_agent, "version": my_version, "type": "agent_reference"}}
        )

        print(f"Agent: {response.output_text}\n")

    except Exception as e:
        print(f"An error occurred: {e}\n")
