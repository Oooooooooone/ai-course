from server import ask_server

def ask(prompt):
    return ask_server(prompt).split("\n")[0]

tests = [("프랑스", "파리"), ("일본", "도쿄"), ("이집트", "카이로"), ("캐나다", "오타와"), ("호주", "캔버라")]
shots = {
    0: "",
    1: "한국 → 서울\n",
    3: "한국 → 서울\n독일 → 베를린\n브라질 → 브라질리아\n",
}

for k, examples in shots.items():
    correct = 0
    for country, capital in tests:
        answer = ask(examples + f"{country} →")
        correct += capital in answer
    print(f"gemma4(26B) 예시 {k}개  정답 {correct}/5")