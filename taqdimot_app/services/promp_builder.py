# services/prompt_builder.py
def build_prompt(data: dict):
    if data["type"] == "referat":
        system_role = "Sen akademik referat yozuvchi yordamchisan."
        work_type = "REFERAT"
    else:
        system_role = "Sen mustaqil ish yozuvchi akademik yordamchisan."
        work_type = "MUSTAQIL ISH"

    prompt = f"""
    {work_type} yozib ber.

    Mavzu: {data['topic']}
    Institut va kafedra: {data['institute']}
    Muallif: {data['author']}
    Til: {data['til']}
    Hajmi: {data['bet']} bet

    Tuzilishi:
    - Kirish
    - Asosiy qism
    - Xulosa
    """

    return system_role, prompt