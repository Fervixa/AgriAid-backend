from agents import Agent, Runner
from pydantic import BaseModel
from typing import List

# Define the output schema (for structured JSON)
class DiagnosisResult(BaseModel):
    disease: str
    remedy: str
    actions: List[str]
    healthScore: int

# Create an agent instance with instructions:
diagnosis_agent = Agent(
    name="CropDoctorAgent",
    instructions=(
        "You are an AI expert in plant diseases. "
        "Given a symptom description and image URL, diagnose the disease, recommend remedy and steps, "
        "and give a health score (0–100). "
        "Return a JSON matching the schema DiagnosisResult."
    ),
    output_type=DiagnosisResult  # ensures agent returns that structured type
)

async def run_diagnosis(symptom: str, image_url: str) -> DiagnosisResult:
    input_text = f"Symptom: {symptom}\nImage: {image_url}"
    result = await Runner.run(diagnosis_agent, input_text)
    # result.final_output is a DiagnosisResult instance
    return result.final_output
