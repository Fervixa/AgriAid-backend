# backend/main.py
from fastapi import FastAPI, Depends
from backend.firebase_admin_init import db
from backend.auth_deps import get_uid
from firebase_admin import firestore

app = FastAPI()

@app.post("/analyze")
async def analyze(payload: dict, uid: str = Depends(get_uid)):
    image_url = payload.get("imageUrl")
    symptom_text = payload.get("symptomText")

    # 1) create case doc
    case_ref = db.collection("cases").document()
    case_ref.set({
        "userId": uid,
        "imageUrl": image_url,
        "symptomText": symptom_text,
        "status": "processing",
        "createdAt": firestore.SERVER_TIMESTAMP
    })

    # 2) Call OpenAI Agent / ML model (omitted here) → get result_json
    # If quota or offline, return mock result:
    result_json = {
        "disease": "Mock blight",
        "remedy": "Apply fungicide X",
        "actions": ["Remove affected leaves", "Spray early morning"],
        "healthScore": 72
    }

    # 3) store result (include userId so client can read)
    result_ref = db.collection("results").document()
    result_ref.set({
        "userId": uid,
        **result_json,
        "createdAt": firestore.SERVER_TIMESTAMP
    })

    # 4) link case -> result
    case_ref.update({"status": "done", "resultId": result_ref.id})

    return {"caseId": case_ref.id, "resultId": result_ref.id, "result": result_json}
