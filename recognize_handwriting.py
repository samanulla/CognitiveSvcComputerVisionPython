from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

import os
import sys
import time

'''
Install the Computer Vision SDK:
    pip install --upgrade azure-cognitiveservices-vision-computervision
'''

remote_image_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/handwritten_text.jpg"

# Add your Computer Vision subscription key and endpoint to your environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
else:
    print("\nSet the COMPUTER_VISION_ENDPOINT environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

client_response = computervision_client.batch_read_file(remote_image_url, raw=True)

# The operation location is a URL with the last appendage as the ID
operation_location = client_response.headers["Operation-Location"]
operation_id = operation_location.split("/")[-1]

print("\nRecognizing text in a remote image with the batch Read API ... \n")

while True:
    result = computervision_client.get_read_operation_result(operation_id)
    if result.status not in ['NotStarted', 'Running']:
        break
    time.sleep(1)

if result.status == TextOperationStatusCodes.succeeded:
    for text_result in result.recognition_results:
        for line in text_result.lines:
            print(line.text)
            print(line.bounding_box)
            print()

local_image_path = "handwritten1.jpeg"
local_image = open(local_image_path, "rb")

client_response = computervision_client.batch_read_file_in_stream(local_image, raw=True)
operation_location = client_response.headers["Operation-Location"]
operation_id = operation_location.split("/")[-1]

print('---------------------------------------------------------------')
print("\nRecognizing text in a local image with the batch Read API ... \n")

while True:
    result = computervision_client.get_read_operation_result(operation_id)
    if result.status not in ['NotStarted', 'Running']:
        break
    time.sleep(1)

if result.status == TextOperationStatusCodes.succeeded:
    for text_result in result.recognition_results:
        for line in text_result.lines:
            print(line.text)
            print(line.bounding_box)
            print()
