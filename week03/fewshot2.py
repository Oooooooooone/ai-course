import ollama

def ask(model, prompt):
    r = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}],
                     think=False, options={"temperature": 0, "num_predict": 60})
    return r.message.content.strip().split("\n")[0]


tests_a = [("사과", "과일"), ("당근", "채소"), ("연어", "생선"), ("장미", "꽃"), ("사자", "동물")]
shots_a = {
    0: "",
    1: "당근 → 채소\n",
    3: "당근 → 채소\n사과 → 과일\n장미 → 꽃\n",
}


tests_b = [("big", "bigger"), ("small", "smaller"), ("fast", "faster"), ("happy", "happier"), ("hot", "hotter")]
shots_b = {
    0: "",
    1: "small → smaller\n",
    3: "small → smaller\nfast → faster\nhappy → happier\n",
}

for name, tests, shots in [("분류", tests_a, shots_a), ("비교급", tests_b, shots_b)]:
    print(f"--- {name} ---")
    for model in ["qwen3:1.7b", "qwen3:8b"]:
        for k, examples in shots.items():
            correct = 0
            for a, b in tests:
                answer = ask(model, examples + f"{a} →")
                correct += b in answer
            print(f"{model:11s} 예시 {k}개  정답 {correct}/5")