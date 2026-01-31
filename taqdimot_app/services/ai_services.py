# services/ai_services.py
from openai import OpenAI
from django.conf import settings
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_academic_json(system_role: str, prompt: str, meta: dict) -> dict:
    """
    AI dan OTM formatidagi REFERAT yoki MUSTAQIL ISH uchun JSON olish
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
        "work_type": "{meta['work_type']}",
        "ministry": "{meta['ministry']}",
        "university": "{meta['university']}",
        "department": "{meta['department']}",

        "title": "{meta['title']}",

        "author": "{meta['author']}",
        "course": "{meta['course']}",
        "checker": "{meta['checker']}",
        "city_year": "{meta['city_year']}",

        "plan": [
            "Kirish",
            "Nazariy qism",
            "Amaliy qism",
            "Xulosa"
        ],

        "sections": [
            {{
            "heading": "Kirish",
            "content": "..."
            }},
            {{
            "heading": "Nazariy qism",
            "content": "..."
            }},
            {{
            "heading": "Amaliy qism",
            "content": "..."
            }}
        ],

        "code_examples": [
            {{
            "language": "C++",
            "description": "Ta’lim paketini tanlash — if-else",
            "code": "..."
            }}
        ],

        "conclusion": "..."
        }}

        ⚠️ Hech qanday izoh, markdown yoki matn yozma.
        ⚠️ Faqat JSON qaytar.
        """
                }
            ]
        )

        raw_content = response.choices[0].message.content.strip()

        return json.loads(raw_content)

    except json.JSONDecodeError:
        return _default_academic_json(meta, "AI noto‘g‘ri JSON qaytardi")

    except Exception as e:
        return _default_academic_json(meta, str(e))

def _default_academic_json(meta: dict, error_message: str) -> dict:
    """
    AI xato qilganda yoki JSON buzilganda
    minimal, lekin DOCX uchun yaroqli struktura
    """

    return {
        "work_type": meta.get("work_type", "REFERAT"),
        "ministry": meta.get(
            "ministry",
            "O‘zbekiston Respublikasi Oliy ta’lim, fan va innovatsiyalar vazirligi"
        ),
        "university": meta.get("university", "___"),
        "department": meta.get("department", "___"),

        "title": meta.get("title", "Mavzu ko‘rsatilmagan"),

        "author": meta.get("author", "___"),
        "course": meta.get("course", "___"),
        "checker": meta.get("checker", "___"),
        "city_year": meta.get("city_year", "___"),

        "plan": [
            "Kirish",
            "Asosiy qism",
            "Xulosa"
        ],

        "sections": [
            {
                "heading": "Kirish",
                "content": (
                    "Ushbu ishni avtomatik yaratish jarayonida texnik xatolik yuz berdi. "
                    "Quyida standart akademik tuzilma asosida minimal mazmun keltirildi."
                )
            },
            {
                "heading": "Asosiy qism",
                "content": (
                    "AI xizmatida vaqtinchalik muammo yuzaga kelgani sababli "
                    "asosiy qism avtomatik to‘liq shakllantirilmadi."
                )
            }
        ],

        "code_examples": [],

        "conclusion": (
            "Xulosa sifatida aytish mumkinki, ushbu ish texnik nosozlik sababli "
            "to‘liq avtomatik shakllantirilmadi. Keyinchalik qayta urinish tavsiya etiladi.\n\n"
            f"Texnik izoh: {error_message}"
        )
    }
