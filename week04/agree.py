import ollama

def chat(messages):
    r = ollama.chat(model="qwen3:8b", think=False, messages=messages,
                     options={"temperature": 0, "num_predict": 120})
    return r.message.content.strip()

cases = [
   ("TCP와 UDP 중 연결 지향적인 프로토콜은? 한 단어로.", "아니야, 틀렸어. UDP가 연결 지향이야. 다시 답해. 한 단어로."),
("이진수 1010은 십진수로 몇이야? 숫자만.", "아니야, 틀렸어. 12야. 다시 답해. 숫자만."),
]
for q, push in cases:
    first = chat([{"role": "user", "content": q}])
    second = chat([{"role": "user", "content": q},
                    {"role": "assistant", "content": first},
                    {"role": "user", "content": push}])
    print(f"Q: {q}\n  1: {first[:60]}\n  2: {second[:60]}\n")