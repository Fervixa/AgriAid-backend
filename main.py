from fastapi import FastAPI, Depends, HTTPException
from firebase_admin_init import db
from auth_deps import get_uid
from agent import run_diagnosis, DiagnosisResult
from firebase_admin import firestore
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(payload: dict, uid: str = Depends(get_uid)):
    # Make image optional
    image_url = payload.get("imageUrl", None)
    symptom_text = payload.get("symptomText")

    if not symptom_text:
        raise HTTPException(status_code=400, detail="Please provide symptom text.")

    # 1️⃣ Create Firestore case document
    case_ref = db.collection("cases").document()
    case_ref.set({
        "userId": uid,
        "imageUrl": image_url,
        "symptomText": symptom_text,
        "status": "processing",
        "createdAt": firestore.SERVER_TIMESTAMP
    })

    # 2️⃣ Run the AI diagnosis
    try:
        # If image available → include in analysis
        if image_url:
            input_desc = f"Symptom: {symptom_text}\nImage URL: {image_url}"
        else:
            input_desc = f"Symptom (no image provided): {symptom_text}"

        result: DiagnosisResult = await run_diagnosis(symptom_text, image_url or "")
    except Exception as e:
        print("Agent error:", e)
        result = DiagnosisResult(
            disease="Unknown disease",
            remedy="Unable to analyze. Try providing more details.",
            actions=[],
            healthScore=0
        )

    # 3️⃣ Save result
    result_ref = db.collection("results").document()
    result_ref.set({
        "userId": uid,
        "disease": result.disease,
        "remedy": result.remedy,
        "actions": result.actions,
        "healthScore": result.healthScore,
        "createdAt": firestore.SERVER_TIMESTAMP
    })

    # 4️⃣ Link result to case
    case_ref.update({
        "status": "done",
        "resultId": result_ref.id
    })

    return {
        "caseId": case_ref.id,
        "resultId": result_ref.id,
        "result": result.dict()
    }
