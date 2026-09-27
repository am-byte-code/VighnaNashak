# EcoSort

## AI-Powered Waste Segregation and Collection Dashboard

EcoSort is a smart waste-management prototype designed to assist garbage collection vehicles in identifying and segregating different types of waste.

The system combines a web-based dashboard with a local AI inference server.

---

## Waste Categories

EcoSort handles four waste categories:

- **Dry Waste**
  - Plastic
  - Paper
  - Cardboard
  - Glass
  - Metal

- **Organic Waste**
  - Food scraps
  - Fruit and vegetable waste
  - Other biodegradable waste

- **E-Waste**
  - Phones
  - Laptops
  - Chargers
  - Batteries
  - Electronic components

- **Medical Waste**
  - Syringes
  - Medicines
  - Medical gloves
  - Biohazard material
  - Other potentially hazardous medical waste

Medical waste is **flagged separately rather than being sent through the normal sorting process**. It can then be isolated and transported to an appropriate specialized facility.

---

## Main Features

### Driver Dashboard

The dashboard provides:

- Total collected waste
- Sorted waste statistics
- Category-wise waste breakdown
- Medical waste alerts
- Truck/ward information
- Assigned dustbin information
- Dustbin fill-level monitoring
- Interactive map of dustbin locations
- Image upload for waste classification
- Camera input for waste classification
- Connection status of the local AI server

### Dustbin Monitoring

Dustbins are represented using fill-level thresholds:

| Fill Level | Status |
|------------|--------|
| Up to 50% | Green |
| Around 75% | Yellow |
| 80% or above | Red |

This allows the driver/operator to identify bins that require attention.

---

## System Architecture

```text
                    ┌─────────────────────┐
                    │   EcoSort Dashboard │
                    │      (HTML/JS)      │
                    └──────────┬──────────┘
                               │
                               │ HTTP
                               ▼
                    ┌─────────────────────┐
                    │   Local AI Server   │
                    │      FastAPI        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   CLIP AI Model     │
                    │ openai/clip-vit-    │
                    │    base-patch32     │
                    └─────────────────────┘

The dashboard sends an image to the local server.

The server processes the image using the AI model and returns the predicted waste category and confidence score.

Technology Stack
Frontend
HTML
CSS
JavaScript
Leaflet.js
OpenStreetMap/ArcGIS map tiles
Backend
Python
FastAPI
Uvicorn
AI
Hugging Face Transformers
OpenAI CLIP (openai/clip-vit-base-patch32)
Zero-shot image classification
Image Processing
Pillow
Project Structure
EcoSort/
│
├── ai-server/
│   ├── .venv/
│   ├── server.py
│   └── requirements.txt
│
├── dashboard/
│   └── driver_dashboard.html
│
├── .gitignore
└── README.md

.venv/ is a local Python virtual environment and should not be uploaded to GitHub.

Installation
Requirements

You need:

Python 3.10+
Internet connection for the first model download
A modern web browser
Approximately 1 GB or more of free disk space for the AI model and dependencies

The AI inference runs locally on the computer.

No paid AI API key is required for the current prototype.

Running EcoSort
1. Open the project
cd EcoSort
2. Enter the AI server directory
cd ai-server
3. Create a virtual environment
Linux/macOS
python3 -m venv .venv

Activate it:

source .venv/bin/activate
Windows
py -m venv .venv

Activate it:

.venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
5. Start the AI server
python server.py

The server runs at:

http://127.0.0.1:8000

On the first run, the CLIP model will be downloaded and cached locally.

This may take some time depending on the internet connection.

Testing the AI Server

Once the server is running, open:

http://127.0.0.1:8000/health

A successful response should contain information similar to:

{
  "status": "ok",
  "model": "openai/clip-vit-base-patch32",
  "mode": "local-zero-shot",
  "model_loaded": true
}
Opening the Dashboard

After starting the AI server, open:

dashboard/driver_dashboard.html

in a web browser.

The dashboard communicates with:

http://127.0.0.1:8000/predict

for image classification.

How Image Classification Works

The dashboard sends the selected image to the FastAPI server.

The server:

Receives the image.
Converts it into a format suitable for the model.
Sends it to the CLIP zero-shot image classifier.
Compares the image against waste-category descriptions.
Selects the highest-scoring category.
Returns the category and confidence score to the dashboard.

Example response:

{
  "class": "ewaste",
  "confidence": 82.4,
  "scores": {
    "dry": 8.2,
    "organic": 3.1,
    "ewaste": 82.4,
    "medical": 6.3
  }
}
Important Note About the Current AI Model

The current implementation uses CLIP zero-shot image classification as a prototype AI model.

It is not a waste-specific model trained exclusively on a dedicated EcoSort waste dataset.

Therefore, the predictions should be treated as a prototype demonstration rather than production-grade waste-recognition results.

A future version can improve classification by training or fine-tuning a dedicated waste-segregation model using a properly labelled dataset.

Medical Waste Handling

Medical waste is treated differently from the normal waste categories.

When medical waste is detected, it should be:

Detected
   ↓
Flagged as Medical Waste
   ↓
Kept Separate
   ↓
Sent to Specialized Facility

It should not be mixed with the normal dry, organic, or e-waste streams.

GitHub

The project is designed to be portable.

The following should be committed:

server.py
requirements.txt
driver_dashboard.html
.gitignore
README.md

The following should not be committed:

.venv/
__pycache__/
model cache files
temporary files

The .gitignore file is included to prevent local environments and generated files from being uploaded.

Running on Another Computer

To run EcoSort on another computer:

git clone <repository-url>
cd EcoSort

Then:

cd ai-server

Create and activate the virtual environment and install the dependencies:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

On Windows:

py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

Then start:

python server.py

Finally, open:

dashboard/driver_dashboard.html

The AI model will be downloaded automatically the first time it is required.

Future Development

Possible improvements include:

Training a dedicated waste-classification model
Improving classification accuracy with a larger labelled dataset
Object detection for multiple waste items in one image
Automatic weight measurement integration
Real-time camera-based detection
Cloud/database integration
Historical waste collection analytics
Route optimization based on dustbin fill levels
Automated alerts for critical bins
Specialized medical-waste workflow
Deployment on edge hardware inside garbage trucks
Team Project

EcoSort is a prototype developed as a hackathon project demonstrating the integration of:

AI + Waste Segregation + IoT-style Monitoring + Interactive Dashboard
