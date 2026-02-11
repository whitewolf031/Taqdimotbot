from openai import OpenAI
from django.conf import settings
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_slide_json(system_role: str, prompt: str, meta: dict) -> dict:
    """
    AI dan POWERPOINT SLIDE uchun JSON olish
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_role},
                {
                    "role": "user",
                    "content": prompt + f"""

Natijani FAQAT to‘g‘ri JSON formatida qaytar.

Quyidagi struktura qat’iy saqlansin:

{{
  "title_slide": {{
    "title": "{meta['title']}",
    "subtitle": "{meta['author']}"
  }},

  "slides": [
    {{
      "title": "Kirish",
      "bullets": [
        "punkt 1",
        "punkt 2",
        "punkt 3"
      ]
    }},
    {{
      "title": "Asosiy tushunchalar",
      "bullets": [
        "punkt 1",
        "punkt 2",
        "punkt 3"
      ]
    }},
    {{
      "title": "Xulosa",
      "bullets": [
        "punkt 1",
        "punkt 2",
        "punkt 3"
      ]
    }}
  ]
}}

⚠️ Hech qanday izoh yozma
⚠️ Markdown yozma
⚠️ Faqat JSON qaytar
"""
                }
            ]
        )

        raw_content = response.choices[0].message.content.strip()
        return json.loads(raw_content)

    except json.JSONDecodeError:
        return _default_slide_json(meta, "AI noto‘g‘ri JSON qaytardi")

    except Exception as e:
        return _default_slide_json(meta, str(e))

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