import os
import sys
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

key = "your-api-key"
endpoint = "https://your-project-resource.cognitiveservices.azure.com/"

# Path to your local .txt file
file_path = r"C:\Users\Admin\Downloads\sample.txt"

# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Method for detecting sensitive information (PII) from a local text file
def analyze_pii_from_file(client, file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    # Read content from local text file
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read().strip()

    if not file_content:
        print("The file is empty.")
        return

    print(f"Analyzing file: {file_path}\n")

    # Send file contents as a document to Azure
    documents = [file_content]
    response = client.recognize_pii_entities(documents, language="en")
    result = [doc for doc in response if not doc.is_error]

    for doc in result:
        print("Redacted Text:\n" + doc.redacted_text)
        print("\n" + "=" * 40)
        print("Detected Entities:")
        print("=" * 40)
        if not doc.entities:
            print("No PII entities detected.")
        for entity in doc.entities:
            print(f"Entity: {entity.text}")
            print(f"  Category: {entity.category}")
            print(f"  Confidence Score: {entity.confidence_score}")
            print(f"  Offset: {entity.offset}")
            print(f"  Length: {entity.length}")
            print("-" * 20)

analyze_pii_from_file(client, file_path)
