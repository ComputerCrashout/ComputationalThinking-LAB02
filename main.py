import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI-Translation")

app = FastAPI(
    title="English-to-Vietnamese Machine Translation API",
    description="A Web API for English-to-Vietnamese translation using Hugging Face's Helsinki-NLP/opus-mt-en-vi model.",
    version="1.0.0",
)

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_NAME = "Helsinki-NLP/opus-mt-en-vi"

tokenizer = None
model = None

# Initialize and load model & tokenizer locally
try:
    logger.info(f"Loading Hugging Face model: {MODEL_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    logger.info("Model loaded successfully!")
except Exception as e:
    logger.error(f"Failed to load model: {e}")


# Request Pydantic Schema
class TranslationRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        description="The English text to be translated (cannot be empty)",
    )


# Response Pydantic Schema
class TranslationResponse(BaseModel):
    input: str
    output: str
    status: str


# 1. GET / - Root Endpoint (System Description)
@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {
        "system": "English-to-Vietnamese Machine Translation API",
        "model_name": MODEL_NAME,
        "model_url": f"https://huggingface.co/{MODEL_NAME}",
        "endpoints": {
            "GET /": "API Information",
            "GET /health": "Check system operational status",
            "POST /predict": "Submit English text for translation to Vietnamese",
        },
    }


# 2. GET /health - Health Check Endpoint
@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    if model is None or tokenizer is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded or unavailable",
        )
    return {"status": "healthy", "model_loaded": True}


# 3. POST /predict - Translation Prediction Endpoint
@app.post(
    "/predict",
    response_model=TranslationResponse,
    status_code=status.HTTP_200_OK,
)
@app.post("/api/chat")
async def predict(request: TranslationRequest):
    text_to_translate = request.message.strip()
    if not text_to_translate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Input 'message' cannot be empty or contain only whitespace.",
        )

    if model is None or tokenizer is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Translation model is currently unavailable.",
        )

    try:
        # Tokenize input text
        inputs = tokenizer(
            text_to_translate, return_tensors="pt", padding=True, truncation=True
        )

        # Generate translation tokens
        translated_tokens = model.generate(**inputs)

        # Decode tokens to text
        translated_text = tokenizer.decode(
            translated_tokens[0], skip_special_tokens=True
        )

        return TranslationResponse(
            input=text_to_translate,
            output=translated_text,
            status="success",
        )
    except Exception as e:
        logger.error(f"Inference error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during model inference: {str(e)}",
        )