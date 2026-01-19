# taqdimot_app/api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from taqdimot_app.services.promp_builder import build_prompt
from taqdimot_app.services.ai_services import generate_referat_json
from taqdimot_app.services.word_services import build_docx
import uuid

@api_view(["POST"])
def generate_work(request):
    data = request.data

    system_role, prompt = build_prompt(data)
    json_data = generate_referat_json(system_role, prompt)

    filename = f"{data['type']}_{uuid.uuid4().hex}"
    file_path = build_docx(json_data, filename)

    return Response({
        "file": request.build_absolute_uri(file_path)
    })
