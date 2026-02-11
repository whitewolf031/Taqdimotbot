from rest_framework.views import APIView
from rest_framework.response import Response
from .services.slide_ai_services import generate_slide_json

class GenerateSlideAPIView(APIView):

    def post(self, request):
        data = request.data

        topic = data.get("topic")
        author = data.get("author")
        bet = data.get("bet")
        til = data.get("til")

        system_role = """
Sen professional taqdimot (PowerPoint) yozuvchi AI san.
Har bir slide qisqa, tushunarli va bullet-point formatda bo‘lsin.
"""

        prompt = f"""
Quyidagi mavzu uchun {bet} ta slide matni yoz:

Mavzu: {topic}
Til: {til}

Har bir slide:
- qisqa
- bullet points
- prezentatsiya uchun mos
"""

        meta = {
            "title": topic,
            "author": author
        }

        slide_json = generate_slide_json(system_role, prompt, meta)

        # keyingi bosqich → pptx yaratish
        # hozircha JSON qaytaramiz
        return Response(slide_json)