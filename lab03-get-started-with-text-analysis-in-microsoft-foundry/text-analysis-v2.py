import sys
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

key = "your-api-key"
endpoint = "https://your-project-resource.cognitiveservices.azure.com/"

# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Example method for detecting sensitive information (PII) from text 
def pii_recognition_example(client, user_text):
    documents = [user_text]
    response = client.recognize_pii_entities(documents, language="en")
    result = [doc for doc in response if not doc.is_error]
    
    for doc in result:
        print("\nRedacted Text: {}".format(doc.redacted_text))
        if not doc.entities:
            print("No PII entities detected.")
        for entity in doc.entities:
            print("Entity: {}".format(entity.text))
            print(" Category: {}".format(entity.category))
            print(" Confidence Score: {}".format(entity.confidence_score))
            print(" Offset: {}".format(entity.offset))
            print(" Length: {}".format(entity.length))

# Interactive Loop
print("--- Azure PII Recognition Tool ---")
print("Enter text to detect PII. Type 'quit' or 'exit' to stop.\n")

while True:
    user_input = input("Enter document text: ").strip()
    
    if user_input.lower() in ["quit", "exit"]:
        print("Exiting PII analyzer.")
        break
        
    if not user_input:
        continue

    try:
        pii_recognition_example(client, user_input)
        print("-" * 50 + "\n")
    except Exception as ex:
        print(f"An error occurred: {ex}\n")
