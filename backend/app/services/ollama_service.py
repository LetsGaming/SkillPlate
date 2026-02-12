import ollama
from ollama import ChatResponse

client = ollama.Client(host="http://ollama:11434")


def generate_course_content(theme: str, difficulty: str, duration: str, online: str, model: str = "gemma3:270m"):
    prompt = f"Erstelle einen Kurs mit Rezepten zu diesem Thema {theme} und dieser schwierigkeit {difficulty} und dieser länge {duration}"
    response: ChatResponse = client.chat(model=model, messages=[
        {
            "role": "system",
            "content": "Extract the parameters from the following text and return it as a "
                       "JSON object with keys 'theme', 'difficulty', 'duration', 'online'. Return ONLY the JSON."
        },
        {
            "role": "user",
            "content": prompt
        }])
    return response.message.content
