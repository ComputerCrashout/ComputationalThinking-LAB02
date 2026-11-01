# Machine Translation Web API - FastAPI & Hugging Face

## Student Information
- **Student Name:** Vũ Thanh Hải
- **Student ID:** 25127323
- **Class:** 25C09
- **Course:** Computational Thinking - Lab02 (Web API)

---

## Hugging Face Model Information
- **Model Name:** `Helsinki-NLP/opus-mt-en-vi`
- **Hugging Face Link:** [https://huggingface.co/Helsinki-NLP/opus-mt-en-vi](https://huggingface.co/Helsinki-NLP/opus-mt-en-vi)
- **Task:** Machine Translation (English to Vietnamese)

---

## System Description
This project is a functional Web API built using **FastAPI** that deploys a pre-trained sequence-to-sequence translation model from Hugging Face. The application runs local model inference using the `transformers` library, accepting English text as input and returning structured JSON responses containing the translated Vietnamese output.

### API Endpoints
- `GET /`: Returns API information and system overview.
- `GET /health`: Checks the operational status of the server and model.
- `POST /predict`: Receives an English string and returns the Vietnamese translation.

---

## Installation Guide

1. **Clone the repository:**
```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd huggingface-fastapi-lab
```

2. **Create and activate a virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Linux/macOS
# .venv\Scripts\activate   # On Windows
```


3. **Install required dependencies:**
```bash
pip install -r requirements.txt
```

---

## Running the Application

Launch the FastAPI server using `uvicorn`:

```bash
uvicorn main:app --reload

```

* **Base URL:** `http://127.0.0.1:8000`
* **Interactive Swagger Documentation:** `http://127.0.0.1:8000/docs`

---

## API Usage & Examples

### 1. Health Check Endpoint (`GET /health`)

```bash
curl -X GET "[http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)"

```

**JSON Response:**

```json
{
  "status": "healthy",
  "model_loaded": true
}

```

### 2. Prediction Endpoint (`POST /predict`)

```bash
curl -X POST "[http://127.0.0.1:8000/predict](http://127.0.0.1:8000/predict)" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello world"}'

```

**JSON Response:**

```json
{
  "input": "Hello world",
  "output": "Xin chào thế giới",
  "status": "success"
}

```

---

## Running Automated Tests

Run the test suite using Python's `requests` library:

```bash
python3 test_api.py

```

---

## Demonstration Video

* **Demonstration Video Link:** 