# saarathi-ai-assistive-shopping
An AI-based voice-guided shopping assistant for visually impaired users, integrating YOLOv8 object detection, EasyOCR, brand matching, speech interaction, shopping-list management, and relative depth estimation.


# SAARATHI AI – AI-Based Goal-Oriented Shopping Assistant for Visually Impaired Users

## Overview

SAARATHI AI is an AI-based assistive shopping system designed to help visually impaired users manage their shopping activities through voice interaction and computer vision.

The system allows users to create shopping lists using voice commands, detect products through a camera, extract visible product information using Optical Character Recognition (OCR), and match recognised brands with the requested shopping items.

It also provides voice-based shopping progress management, allowing users to update collected quantities, check remaining products, and interact with their shopping list without manually typing.

The current implementation is a laptop-based prototype, with the long-term goal of integrating the system into smart glasses.

## Objectives

- Enable hands-free shopping-list creation through voice commands.
- Detect products using computer vision.
- Extract visible text from product packaging using OCR.
- Match recognised brand information with requested products.
- Provide spoken feedback to users.
- Track collected and remaining shopping quantities.
- Explore relative depth estimation for additional visual information.

## System Architecture

The system consists of the following modules:

1. **Voice Input and Speech Recognition:** Converts spoken user commands into text.
2. **Intent Understanding:** Extracts product names, brands, quantities, and user commands.
3. **Shopping List Management:** Stores and updates shopping information using JSON.
4. **Object Detection:** Uses YOLOv8 to detect objects in camera frames.
5. **OCR Processing:** Uses EasyOCR to extract visible text from detected product regions.
6. **Brand Matching:** Compares extracted text with requested product and brand information.
7. **Relative Depth Estimation:** Uses Depth Anything V2 to generate relative depth maps.
8. **Text-to-Speech:** Provides spoken responses and confirmations.
9. **Shopping Conversation:** Allows users to manage collected and remaining products through voice commands.

## Algorithms and Technologies

| Algorithm / Technology | Purpose |
|---|---|
| YOLOv8s | Live object detection |
| YOLOv8n | Separate SKU-110K training and evaluation experiment |
| EasyOCR | Text detection and recognition |
| Rule-Based String Matching | Brand and product matching |
| Speech Recognition | Voice-to-text conversion |
| Text-to-Speech (TTS) | Spoken feedback |
| Depth Anything V2 | Relative depth estimation |
| Non-Maximum Suppression (NMS) | Removing overlapping detection boxes |
| Rule-Based Intent Recognition | Understanding predefined voice commands |

## Implementation Details

### 1. Voice-Based Shopping List Creation

Users can specify products and quantities through voice commands.

Example:
- Add two Coca-Cola.
- Add five Britannia biscuits.

The system extracts the requested information and stores it in a JSON-based shopping list.

### 2. Product Detection and Brand Matching

The live detection pipeline uses YOLOv8s to identify product regions.

Detected regions are cropped and passed to EasyOCR to extract visible text. The extracted text is compared against the requested product and brand information using rule-based matching.

### 3. Shopping Conversation

The conversational module supports commands for:

- Collecting products.
- Checking remaining quantities.
- Displaying the shopping list.
- Reducing requested quantities.
- Repeating the previous response.
- Ending the shopping session.

### 4. Relative Depth Estimation

Depth Anything V2 is used to generate relative depth maps from camera images. The output represents relative depth information and does not directly provide calibrated physical distances.

### 5. SKU-110K Experiment

A separate experiment uses YOLOv8n for product-object detection on the SKU-110K dataset. This experiment is distinct from the YOLOv8s live OCR and brand-matching pipeline.

## Technology Stack

- Python
- PyTorch
- YOLOv8
- OpenCV
- EasyOCR
- SpeechRecognition
- Depth Anything V2
- JSON
- macOS Text-to-Speech (`say`)
- Apple Silicon MPS acceleration

## Project Structure

The repository contains the following main modules (the exact folder contents may vary as development progresses):

```text
saarathi-ai/
│
├── shopping_assistant.py
├── shopping_conversation.py
├── shopping_list.py
├── intent_understanding.py
├── voice_assistant.py
│
├── pipeline.py
├── product_matching.py
├── brand_matching.py
│
├── live_detection.py
├── yolo_ocr_test.py
├── yolo_easyocr_integration.py
├── ocr_test.py
│
├── predict_baseline.py
├── evaluate_baseline.py
├── baseline_metrics.csv
│
├── shopping_data.json
│
├── Depth-Anything-V2/
│   ├── checkpoints/
│   ├── depth_estimation_test.py
│   └── app.py
│
├── assets/
├── tests/
├── runs/
│
└── README.md
```

## Installation and Setup

### Requirements

- Python 3.9 or compatible version.
- macOS or another supported Python environment.
- Camera access for live detection.
- Required Python packages and model checkpoints.

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/saarathi-ai.git
```

```bash
cd saarathi-ai
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

Install the required packages according to the project's dependency configuration.

If a `requirements.txt` file is provided:

```bash
pip install -r requirements.txt
```

### 4. Configure model checkpoints

Ensure that the required YOLO and Depth Anything V2 model weights are available in their expected locations.

The Depth Anything V2 checkpoint should be placed in:

```text
Depth-Anything-V2/checkpoints/
```

Do not commit large model weights or datasets unless their licences and GitHub storage requirements permit it. Provide download instructions where necessary.

## Running the Project

Run the commands from the repository root after activating the virtual environment.

### Shopping Assistant

```bash
python shopping_assistant.py
```

This module allows users to add products to their shopping list through voice input.

### Shopping Conversation

```bash
python shopping_conversation.py
```

This module manages shopping progress through voice commands.

### Live YOLO and OCR Integration

```bash
python yolo_easyocr_integration.py
```

This module demonstrates live object detection, OCR, and brand matching.

### SKU-110K Baseline Prediction

```bash
python predict_baseline.py
```

### SKU-110K Evaluation

```bash
python evaluate_baseline.py
```

### Depth Estimation

```bash
python Depth-Anything-V2/depth_estimation_test.py
```

Make sure the required model checkpoints and input images are available before running these scripts.

## Example Shopping Interaction

A sample shopping-list interaction:

| Product | Requested Quantity |
|---|---:|
| Coca-Cola | 2 |
| Britannia biscuits | 5 |

Example voice commands:

- "I collected one Coca-Cola."
- "I picked up three biscuits."
- "How many products are remaining?"
- "Show my shopping list."
- "Repeat."
- "Stop shopping."

The system updates the shopping progress and maintains the information in the JSON file.

## Novelty and Contribution

The proposed system focuses on integrating goal-oriented shopping assistance with voice-based interaction for visually impaired users.

Its main contribution is the integration of:

- Voice-based shopping-list creation.
- Visual product detection.
- OCR-based product text
