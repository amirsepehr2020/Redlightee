import random

respon = {
    "سلام":{"score":2,"answer":["سلام به روی ماهت","سلام جیگر من"]},
    "خوبی":{"score":1,"answer":["خوبم چطوری ","چطوری جیگر منم خوبم عزیزم"]},
    "چه کار مي کني":{"score":1,"answer":["من ردلايتم و در خدمت شمام عشقم","هيچي عشقم فقط جواب شمارو مي دم"]}
}

normalize = {
    "سلام": ["سلام", "درود", "سلاممم", "سلامم","سللم"],
    "خوبی": ["خوبی", "چطوری", "حالت چطوره", "خوبی؟"],
    "چه کار مي کني":["چي کار مي کني","مي کني چيکار","چه کاره اي","چه انجام مي دهي"]
}


def normalize_text(text):
    for main_word, variants in normalize.items():
        for v in variants:
            if v in text:
                text = text.replace(v, main_word)
    return text



def even(text):
    call=[]
    text= text.lower()
    text=normalize_text(text)
    for key,ssd in respon.items():
        if key in text:
            call.append((ssd["score"],random.choice(ssd["answer"])))
    
    if not call:
        return "چه سخنی مهمی گفتی و من نفهمیدم؟"
    
    call.sort(reverse=True)
    return " ".join([item[1] for item in call])

