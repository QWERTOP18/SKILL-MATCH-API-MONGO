from fastapi import APIRouter
import csv

router = APIRouter()

@router.get("/questions")
async def get_questions():
    with open("seed/questions.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        questions = list(reader)
    return questions
