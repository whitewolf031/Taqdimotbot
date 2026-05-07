import google.generativeai as genai
from django.conf import settings
import json

# Gemini sozlamalari
genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_academic_json(system_role: str, prompt: str, meta: dict) -> dict:
    """
    Gemini AI dan OTM formatidagi REFERAT yoki MUSTAQIL ISH uchun JSON olish
    """
    
    # Modelni sozlash (JSON rejimini yoqish bilan)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", # yoki "gemini-1.5-pro"
        system_instruction=system_role # System prompt shu yerga yoziladi
    )

    try:
        full_prompt = prompt + f"""
        Natijani FAQAT to‘g‘ri JSON formatida qaytar.
        Quyidagi struktura qat’iy saqlansin:

        {{
            "work_type": "{meta.get('work_type', '')}",
            "ministry": "{meta.get('ministry', '')}",
            "university": "{meta.get('university', '')}",
            "department": "{meta.get('department', '')}",
            "title": "{meta.get('title', '')}",
            "author": "{meta.get('author', '')}",
            "course": "{meta.get('course', '')}",
            "checker": "{meta.get('checker', '')}",
            "city_year": "{meta.get('city_year', '')}",
            "plan": ["Kirish", "Nazariy qism", "Amaliy qism", "Xulosa"],
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
                    "description": "...",
                    "code": "..."
                }}
            ],
            "conclusion": "..."
        }}
        """

        # Gemini so'rovi
        response = model.generate_content(
            full_prompt,
            generation_config={"response_mime_type": "application/json"}
        )

        # Gemini javobini JSON ga o'girish
        return json.loads(response.text)

    except json.JSONDecodeError:
        return _default_academic_json(meta, "Gemini noto‘g‘ri JSON qaytardi")

    except Exception as e:
        return _default_academic_json(meta, str(e))

def _default_academic_json(meta: dict, error_message: str) -> dict:
    """
    Xatolik yuz berganda qaytariladigan standart struktura
    """
    return {
        "work_type": meta.get("work_type", "REFERAT"),
        "ministry": meta.get("ministry", "O‘zbekiston Respublikasi Oliy ta’lim, fan va innovatsiyalar vazirligi"),
        "university": meta.get("university", "___"),
        "department": meta.get("department", "___"),
        "title": meta.get("title", "Mavzu ko‘rsatilmagan"),
        "author": meta.get("author", "___"),
        "course": meta.get("course", "___"),
        "checker": meta.get("checker", "___"),
        "city_year": meta.get("city_year", "___"),
        "plan": ["Kirish", "Asosiy qism", "Xulosa"],
        "sections": [
            {
                "heading": "Kirish",
                "content": "Texnik xatolik yuz berdi. Minimal mazmun keltirildi."
            },
            {
                "heading": "Asosiy qism",
                "content": "AI xizmatida vaqtinchalik muammo yuzaga keldi."
            }
        ],
        "code_examples": [],
        "conclusion": f"Xulosa: Texnik nosozlik yuz berdi. Xato: {error_message}"
    }