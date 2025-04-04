from fastapi import APIRouter
import csv

router = APIRouter()

@router.get("/api/questions")
async def get_questions():
    with open("app/seed/questions.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        questions = list(reader)
    return questions
