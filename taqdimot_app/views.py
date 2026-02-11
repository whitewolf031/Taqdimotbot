from rest_framework.views import APIView
from rest_framework.response import Response
from .services.slide_ai_services import generate_slide_json

class GenerateSlideAPIView(APIView):

    def post(self, request):
        data = request.data

        topic = data.get("topic")
        author = data.get("author")
        bet = data.get("bet")  # slide soni
        til = data.get("til")  # til

        if not all([topic, author, bet, til]):
            return Response({"error": "topic, author, bet va til kerak"}, status=400)

        try:
            slide_count = int(bet)
        except ValueError:
            return Response({"error": "bet raqam bo‘lishi kerak"}, status=400)

        system_role = """
Sen professional taqdimot (PowerPoint) yozuvchi AI san.
Har bir slide qisqa, tushunarli va bullet-point formatda bo‘lsin.
"""

        prompt = f"""
Quyidagi mavzu uchun {slide_count} ta slide matni yoz:

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

        # Til va slide sonini AI funktsiyasiga uzatamiz
        slide_json = generate_slide_json(
            system_role=system_role,
            prompt=prompt,
            meta=meta,
            language=til,  # foydalanuvchi tanlagan til
            slide_count=int(bet)  # foydalanuvchi kiritgan slide beti
        )

        return Response(slide_json)