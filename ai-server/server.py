from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from transformers import pipeline
import io


# ============================================================
# EcoSort Local AI Server
# ============================================================

app = FastAPI(title="EcoSort Local AI")


# Allow the dashboard to communicate with this server.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MODEL_NAME = "openai/clip-vit-base-patch32"


# Human-readable descriptions are more useful than just
# "dry", "organic", etc. for a zero-shot vision model.
CANDIDATE_LABELS = [
    "a banana peel or fruit peel",
    "food scraps, fruits or vegetables",
    "a plastic bottle or plastic container",
    "paper, cardboard or newspaper",
    "a glass bottle or metal can",
    "a phone, smartphone or tablet",
    "a laptop, computer or electronic device",
    "a charger, cable or circuit board",
    "a battery or electronic battery",
    "a syringe or needle",
    "medicine, pills or a medicine packet",
    "medical gloves, bandages or medical waste"
]

LABEL_TO_CATEGORY = {
    "a banana peel or fruit peel": "organic",
    "food scraps, fruits or vegetables": "organic",

    "a plastic bottle or plastic container": "dry",
    "paper, cardboard or newspaper": "dry",
    "a glass bottle or metal can": "dry",

    "a phone, smartphone or tablet": "ewaste",
    "a laptop, computer or electronic device": "ewaste",
    "a charger, cable or circuit board": "ewaste",
    "a battery or electronic battery": "ewaste",

    "a syringe or needle": "medical",
    "medicine, pills or a medicine packet": "medical",
    "medical gloves, bandages or medical waste": "medical"
}

print("Loading EcoSort AI model...")
print(f"Model: {MODEL_NAME}")

classifier = pipeline(
    "zero-shot-image-classification",
    model=MODEL_NAME
)

print("EcoSort AI model loaded successfully.")


# ============================================================
# Health check
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": MODEL_NAME,
        "mode": "local-zero-shot",
	"model_loaded": True
    }


# ============================================================
# Image prediction
# ============================================================

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image file."
        )

    try:
        image_bytes = await file.read()

        image = Image.open(
            io.BytesIO(image_bytes)
        ).convert("RGB")

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not read the uploaded image."
        )

    # Run zero-shot classification
    results = classifier(
        image,
        candidate_labels=CANDIDATE_LABELS
    )

    # Results are already sorted highest -> lowest
    best = results[0]

    category = LABEL_TO_CATEGORY[best["label"]]
    confidence = float(best["score"])

    # Return all category scores as well.
    scores = {}

    for result in results:
        scores[
            LABEL_TO_CATEGORY[result["label"]]
        ] = round(float(result["score"]) * 100, 2)

    return {
        "class": category,
        "confidence": round(confidence * 100, 2),
        "scores": scores,
        "model": MODEL_NAME
    }


# ============================================================
# Run server
# ============================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
