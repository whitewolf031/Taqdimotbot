# taqdimot_app/api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from taqdimot_app.services.promp_builder import build_prompt
from taqdimot_app.services.ai_services import generate_academic_json
from taqdimot_app.services.word_services import build_docx_academic
import uuid

@api_view(["POST"])
def generate_work(request):
    data = request.data

    system_role, prompt = build_prompt(data)

    meta = {
        "work_type": "REFERAT" if data["type"] == "referat" else "MUSTAQIL ISH",
        "ministry": "O‘zbekiston Respublikasi Oliy ta’lim, fan va innovatsiyalar vazirligi",
        "university": data["institute"],
        "department": data.get("department", "___"),

        "title": data["topic"],

        "author": data["author"],
        "course": data.get("course", "___"),
        "checker": data.get("checker", "___"),
        "city_year": data.get("city_year", "Toshkent – 2026"),
    }

    json_data = generate_academic_json(system_role, prompt, meta)

    filename = f"{data['type']}_{uuid.uuid4().hex}"
    file_path = build_docx_academic(json_data, filename)

    return Response({
        "file": request.build_absolute_uri(file_path)
    })