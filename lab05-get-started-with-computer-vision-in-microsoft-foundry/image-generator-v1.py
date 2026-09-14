import base64
from openai import OpenAI

endpoint = "https://your-project-resource.openai.azure.com/openai/v1/"
deployment_name = "your-text-to-image-model-deployment"
api_key = "<your-api-key>"

client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)

img = client.images.generate(
    model=deployment_name,
    prompt="A cute baby polar bear",
    n=1,
    size="1024x1024",
)

image_bytes = base64.b64decode(img.data[0].b64_json)
with open("output.png", "wb") as f:
    f.write(image_bytes)
