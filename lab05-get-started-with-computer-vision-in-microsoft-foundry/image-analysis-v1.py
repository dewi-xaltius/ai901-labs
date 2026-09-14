from openai import OpenAI

endpoint = "https://your-project-resource.openai.azure.com/openai/v1"
deployment_name = "your-deployed-model"
api_key = "your-api-key"

client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)

# Verified working image URL
sample_image_url = "https://microsoftlearning.github.io/mslearn-ai-fundamentals/data/joystick.png"

response = client.responses.create(
    model=deployment_name,
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "what's in this image?"},
            {"type": "input_image", "image_url": sample_image_url},
        ],
    }],
)

print(f"answer: {response.output_text}")
