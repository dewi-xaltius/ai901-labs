key = "your-api-key"
endpoint = "https://your-project-resource.cognitiveservices.azure.com/"

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Example method for detecting sensitive information (PII) from text 
def pii_recognition_example(client):
    documents = [
        "My phone number is 555-123-4567 and my email is john@example.com."
    ]
    response = client.recognize_pii_entities(documents, language="en")
    result = [doc for doc in response if not doc.is_error]
    for doc in result:
        print("Redacted Text: {}".format(doc.redacted_text))
        for entity in doc.entities:
            print("Entity: {}".format(entity.text))
            print(" Category: {}".format(entity.category))
            print(" Confidence Score: {}".format(entity.confidence_score))
            print(" Offset: {}".format(entity.offset))
            print(" Length: {}".format(entity.length))

pii_recognition_example(client)
