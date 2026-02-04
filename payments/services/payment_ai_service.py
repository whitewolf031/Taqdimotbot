import json
from openai import OpenAI
from django.conf import settings
from botconfig import BotConfig
from payments.services.telegram_image_service import download_telegram_photo_as_base64

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def check_with_ai(file_id: str) -> dict:
    image_base64 = download_telegram_photo_as_base64(file_id)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a payment receipt verification AI.\n"
                    "Analyze the image and determine whether it is a REAL payment receipt.\n\n"
                    "Respond ONLY in JSON:\n"
                    "{"
                    '"is_payment_receipt": true/false,'
                    '"confidence": number,'
                    '"detected_amount": number or null,'
                    '"provider": "click/payme/bank/unknown"'
                    "}"
                )
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )

    return json.loads(response.choices[0].message.content)