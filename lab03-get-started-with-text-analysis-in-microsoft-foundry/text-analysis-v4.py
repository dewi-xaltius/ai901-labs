import os
import sys
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

key = "your-api-key"
endpoint = "https://your-project-resource.cognitiveservices.azure.com/"

file_path = r"C:\Users\Admin\Downloads\sample.txt"

# Target categories to redact
TARGET_CATEGORIES = ["PhoneNumber", "Email", "USSocialSecurityNumber"]

def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    return TextAnalyticsClient(endpoint=endpoint, credential=ta_credential)

client = authenticate_client()

def analyze_filtered_pii(client, file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read().strip()

    if not file_content:
        print("The file is empty.")
        return

    print(f"Analyzing file: {file_path}")
    print(f"Filtering Azure redaction for: {', '.join(TARGET_CATEGORIES)}\n")

    documents = [file_content]
    
    # Pass categories_filter to Azure so it ONLY redacts the requested categories
    response = client.recognize_pii_entities(
        documents, 
        language="en", 
        categories_filter=TARGET_CATEGORIES
    )
    result = [doc for doc in response if not doc.is_error]

    for doc in result:
        print("=" * 40)
        print("REDACTED TEXT (Target Categories Only):")
        print("=" * 40)
        print(doc.redacted_text)
        print("\n")

        print("=" * 40)
        print("DETECTED ENTITIES:")
        print("=" * 40)

        if not doc.entities:
            print("No matching entities found for the specified categories.")
            return

        for entity in doc.entities:
            print(f"Entity Text: {entity.text}")
            print(f"  Category: {entity.category}")
            print(f"  Confidence: {entity.confidence_score:.2f}")
            print(f"  Offset: {entity.offset}")
            print(f"  Length: {entity.length}")
            print("-" * 20)

analyze_filtered_pii(client, file_path)
