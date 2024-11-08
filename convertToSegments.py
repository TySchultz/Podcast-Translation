import requests
import os
import json
import time

AUDIO_FILE = "UnispanPodcast.wav"
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# API configuration
headers = {
    "Authorization": f"Bearer {REPLICATE_API_TOKEN}"
}

# First, upload the file to Replicate
def upload_to_replicate(file_path):
    print(f"Attempting to upload {file_path}...")
    
    # Verify API token
    if not REPLICATE_API_TOKEN:
        raise Exception("REPLICATE_API_TOKEN is not set in environment variables")
    
    # Upload file directly to Replicate
    with open(file_path, 'rb') as file:
        files = {
            'content': (os.path.basename(file_path), file, 'application/octet-stream')
        }
        response = requests.post(
            "https://api.replicate.com/v1/files",
            headers=headers,
            files=files
        )
    
    print(f"File upload status: {response.status_code}")
    
    if response.status_code != 201:
        print(f"Upload response: {response.text}")
        raise Exception(f"Failed to upload file: {response.text}")
    
    file_data = response.json()
    serving_url = file_data['urls']['get']
    print(f"File successfully uploaded. Serving URL: {serving_url}")
    return serving_url

# Upload file and get serving URL
file_url = upload_to_replicate(AUDIO_FILE)

# Prepare the request payload with the uploaded file URL
payload = {
    "version": "cbd15da9f839c5f932742f86ce7def3a03c22e2b4171d42823e83e314547003f",
    "input": {
        "file": file_url,
        "prompt": "",
        "file_url": "",
        "language": "en",
        "translate": False,
        "num_speakers": 2,
        "group_segments": True,
        "offset_seconds": 0,
        "transcript_output_format": "segments_only"
    }
}

# Make the transcription API request
headers["Content-Type"] = "application/json"

response = requests.post(
    "https://api.replicate.com/v1/predictions",
    headers=headers,
    json=payload
)

if response.status_code in [200, 201, 202]:
    prediction = response.json()
    prediction_id = prediction['id']
    
    # Poll until the prediction is complete
    while True:
        response = requests.get(
            f"https://api.replicate.com/v1/predictions/{prediction_id}",
            headers=headers
        )
        prediction = response.json()
        
        if prediction['status'] == 'succeeded':
            # Save the response to a JSON file
            with open('convertedSegments.json', 'w', encoding='utf-8') as f:
                json.dump(prediction, f, ensure_ascii=False, indent=2)
            print("Results saved to convertedSegments.json")
            
            # Print each segment
            if "output" in prediction and prediction["output"]:
                for segment in prediction["output"]["segments"]:
                    start_time = segment["start"]
                    end_time = segment["end"]
                    text = segment["text"]
                    print(f"[{start_time:.2f}s -> {end_time:.2f}s] {text}")
            break
        elif prediction['status'] == 'failed':
            print("Prediction failed:", prediction['error'])
            break
        else:
            print(f"Status: {prediction['status']}. Waiting...")
            time.sleep(10)  # Wait 10 seconds before checking again
else:
    print(f"Error: {response.status_code}")
    print(response.text)