from openai import OpenAI
from django.conf import settings
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_slide_json(topic, author, institute, language, slide_count):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a professional presentation creator."
            },
            {
                "role": "user",
                "content": f"""
Mavzu: {topic}
Muallif: {author}
Institut: {institute}
Til: {language}
Slide soni: {slide_count}

Quyidagi formatda JSON qaytar:

{{
  "title_slide": {{
     "title": "...",
     "subtitle": "..."
  }},

  "slides": [
    {{
      "type": "section",
      "title": "..."
    }},
    {{
      "type": "bullet",
      "title": "...",
      "points": ["...", "...", "..."]
    }},
    {{
      "type": "image",
      "title": "...",
      "points": ["...", "..."]
    }},
    {{
      "type": "two_column",
      "title": "...",
      "left": ["...", "..."],
      "right": ["...", "..."]
    }}
  ],

  "conclusion": {{
     "title": "Rahmat!"
  }}
}}

Qoidalar:
- Slides soni aniq {slide_count} bo‘lsin
- Faqat JSON qaytar
"""
            }
        ]
    )

    return json.loads(response.choices[0].message.content)

def _default_slide_json(meta: dict, error_message: str) -> dict:
    """
    AI xato qilganda minimal slide struktura
    """

    return {
        "title_slide": {
            "title": meta.get("title", "Taqdimot mavzusi"),
            "subtitle": meta.get("author", "Muallif")
        },
        "slides": [
            {
                "title": "Kirish",
                "bullets": [
                    "Taqdimot mavzusiga kirish",
                    "Mavzuning dolzarbligi",
                    "Taqdimot maqsadi"
                ]
            },
            {
                "title": "Asosiy qism",
                "bullets": [
                    "Asosiy tushunchalar",
                    "Muhim faktlar",
                    "Tahlil va izohlar"
                ]
            },
            {
                "title": "Xulosa",
                "bullets": [
                    "Umumiy xulosa",
                    "Natijalar",
                    f"Texnik izoh: {error_message}"
                ]
            }
        ]
    }