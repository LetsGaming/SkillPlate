import os
import re

from openai import OpenAI
from pydantic import BaseModel, ValidationError


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


# client = ollama.Client(host="http://ollama:11434")
client = OpenAI(
    base_url="https://ollama.com/v1",
    api_key=os.environ.get("OLLAMA_API_KEY")
)


def generate_course_content(theme: str, difficulty: str, duration: int, online: bool):
    model: str = "gemma4:31b"

    prompt = (
        f"Erstelle einen Kurs mit Rezepten zum Thema '{theme}'. "
        f"Schwierigkeit: {difficulty}, Dauer: {duration} Stunden, "
        f"Online-Kurs: {'Ja' if online else 'Nein'}."
    )

    try:
        response = client.chat.completions.parse(
            model=model,
            temperature=0.0,  # Wichtig für strikte Fakten/Strukturen
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional chef. You must output valid JSON matching the schema. "
                        "CRITICAL: Do NOT wrap the response in ```json ... ``` code blocks. "
                        "Output ONLY the raw JSON string starting with { and ending with }."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            # Das hier sorgt dafür, dass die Cloud das Schema strikt erzwingt
            response_format=Course
        )

        # Das Ergebnis kommt bereits fertig als "Course"-Objekt zurück!
        course_object = response.choices[0].message.content.strip()

        if course_object.startswith("```"):
            re.sub(r'\s*```$', '', course_object)
        print(course_object)
        return course_object
    except ValidationError as e:
        print(f"Falsches Objekt wurde zurückgegben: {e}")
        return None
    except Exception as e:
        print(f"API Fehler: {e}")
        return None
