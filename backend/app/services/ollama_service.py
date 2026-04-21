import ollama
from ollama import ChatResponse
from pydantic import BaseModel


class Ingredients(BaseModel):
    ingredient_name: str
    ingredient_type: str
    amount: float
    unit: str


class Recipe(BaseModel):
    recipe_name: str
    recipe_instructions: str
    ingredients: list[Ingredients]


class Course(BaseModel):
    theme: str
    difficulty: str
    duration: int
    online: bool
    recipes: list[Recipe]


client = ollama.Client(host="http://ollama:11434")


def generate_course_content(theme: str, difficulty: str, duration: str, online: str, model: str = "gemma4:e2b"):
    prompt = f"Erstelle einen Kurs mit Rezepten zu diesem Thema {theme} und dieser schwierigkeit {difficulty} und dieser länge {duration} und dem Online Status mit {online}"
    response: ChatResponse = client.chat(
        model=model,
        format=Course.model_json_schema(),
        options={'temperature': 0},
        messages=[
            {
                "role": "system",
                "content": "You are a profi cook that gives direct and only specific instructions"
            },
            {
                "role": "user",
                "content": prompt
            }])
    return Course.model_validate_json(response.message.content)
