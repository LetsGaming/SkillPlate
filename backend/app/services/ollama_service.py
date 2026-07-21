from google import genai
from google.genai import types
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
client = genai.Client()


def generate_course_content(theme: str, difficulty: str, duration: int, online: bool):
    model: str = "gemini-3.1-flash-lite"

    prompt = (
        f"Erstelle einen Kurs mit Rezepten zum Thema '{theme}'. "
        f"Schwierigkeit: {difficulty}, Dauer: {duration} Stunden, "
        f"Online-Kurs: {'Ja' if online else 'Nein'}."
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are a professional chef.",
                temperature=0.0,  # Wichtig für strikte Strukturen
                # Hier zwingen wir Gemini, exakt dein Pydantic-Schema zu nutzen
                response_mime_type="application/json",
                response_schema=Course,
            ),
        )

        # 4. Validierung und Umwandlung in das Pydantic-Objekt
        # Gemini liefert bei 'response_schema' validiertes JSON als Text im .text-Attribut
        course_object = Course.model_validate_json(response.text)

        print("Erfolgreich generiert:")
        print(course_object.model_dump_json(indent=2))

        return course_object
    except ValidationError as e:
        print(f"Falsches Objekt wurde zurückgegben: {e}")
        return None
    except Exception as e:
        print(f"API Fehler: {e}")
        return None
