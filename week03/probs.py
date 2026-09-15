import math
from openai import OpenAI

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")

questions = [
    "오늘 저녁 메뉴 하나만 추천해줘. 음식 이름 한 단어로만 답해.",
    "내 이름의 뜻은? 한 단어로만 답해.",
]
for q in questions:
    r = client.chat.completions.create(model="gemma4", messages=[{"role": "user", "content": q}],
                                        max_tokens=1, temperature=0, logprobs=True, top_logprobs=5)
    tops = r.choices[0].logprobs.content[0].top_logprobs
    print(q.split(".")[0])
    print("  ", ", ".join(f"'{t.token!r}' {math.exp(t.logprob) * 100:.1f}%" for t in tops))