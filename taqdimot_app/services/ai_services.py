# services/ai_services.py
from openai import OpenAI
from django.conf import settings
import json
import textwrap

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_referat_json(system_role: str, prompt: str, bet: int = 1) -> dict:
    """
    AI dan JSON formatida referat yaratish.
    'bet' parametri: foydalanuvchi nechta bet bergan bo'lsa ham, AI 1 bet qilib qisqartiradi.
    """
    try:
        # AI so‘rovi
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": prompt + f"""
            Natijani faqat to‘g‘ri JSON formatida qaytar. Hajmni 1 betga mosla:

            {{
            "title": "",
            "sections": [
            {{"heading": "Kirish", "content": ""}},
            {{"heading": "Asosiy qism", "content": ""}},
            {{"heading": "Xulosa", "content": ""}}
            ]
            }}
            """}
            ]
        )
        raw_content = response.choices[0].message.content

        try:
            data = json.loads(raw_content)
        except json.JSONDecodeError:
            # AI noto‘g‘ri JSON yuborsa default struktura
            data = {
                "title": "Sarlavha mavjud emas",
                "sections": [
                    {"heading": "Kirish", "content": "Kirish matni mavjud emas."},
                    {"heading": "Asosiy qism", "content": "Asosiy qism matni mavjud emas."},
                    {"heading": "Xulosa", "content": "Xulosa matni mavjud emas."}
                ]
            }

        return data

    except Exception as e:
        return {
            "title": "Xatolik yuz berdi",
            "sections": [
                {"heading": "Kirish", "content": f"AI so‘rovi bajarilmadi: {str(e)}"},
                {"heading": "Asosiy qism", "content": ""},
                {"heading": "Xulosa", "content": ""}
            ]
        }