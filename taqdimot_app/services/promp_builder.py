def build_prompt(data: dict):
    if data["type"] == "referat":
        system_role = "Sen OTM talabalari uchun akademik REFERAT yozuvchi yordamchisan."
        work_type = "REFERAT"
    else:
        system_role = "Sen OTM talabalari uchun MUSTAQIL ISH yozuvchi akademik yordamchisan."
        work_type = "MUSTAQIL ISH"

    prompt = f"""
    {work_type} yozib ber.

    Mavzu: {data['topic']}
    Universitet va kafedra: {data['institute']}
    Muallif: {data['author']}
    Til: {data['til']}
    Hajmi: {data['bet']} bet

    Qat’iy talablar:
    - Akademik uslub
    - OTM format
    - Kirish, Asosiy qism, Amaliy misol, Xulosa
    - Kod misoli bo‘lsin
    - Jadval va statistik izohlar qo‘shilsin
    """

    return system_role, prompt