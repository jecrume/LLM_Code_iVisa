from flask import Flask, request
import os
import requests
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConverstationAnalylsisClient

load_dotenv()
app = Flask(__name__)

@app.route('getIntentEntities', methods=['POST'])
def getIntentEntities():
    text = "None"
    request_data = request.get_json()

    if request_data:
        if 'text' in request_data:
            text = request_data['text']
        else:
            return "No text found in request"

    clu_endpoint = os.environ['ENDPOINT']
    clu_key = os.environ['KEY']
    project_name = os.environ['PROJECT_NAME']
    deployment_name = os.environ['DEPLOYMENT_NAME']
    client = ConverstationAnalylsisClient(clu_endpoint,AzureKeyCredential(clu_key))

    with client:
        result = client.analyze_conversation(
            headers = {"Ocp-Apim-Subscription-Key": clu_key, "Apim-Request-Id": "Insert Request Id", 
            "Content-Type": "application/json"},
            task = {
                "kind": "Conversation",
                "analysisInput": {
                    "conversationItem": {
                        "participantId": "1",
                        "Id": "1",
                        "modality": "text",
                        "language": "en",
                        "text": "text"
                    }
                },
                "parameters": {
                    "projectName": project_name,
                    "verbose": True,
                    "deploymentName": deployment_name,
                    "stringIndexType": "TextElement_V8"
                }
            }

        )
    res = result.json()
    response = {
    "intent": res["result"]["prediction"]["topIntent"],
    "entities": res["result"]["prediction"]["entities"]
    }

    return response