from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("Qwen/Qwen3-8B")

pairs = [
    ("나는 어제 친구와 함께 영화를 봤다", "I watched a movie with a friend yesterday"),
    ("인공지능은 데이터에서 규칙을 스스로 배운다", "Artificial intelligence learns rules from data by itself"),
    ("대한민국의 수도는 서울이다", "The capital of Korea is Seoul"),
    ("트랜스포머 모델은 어텐션 메커니즘을 사용한다", "Transformer models use attention mechanisms"),
    ("이 카페 분위기 너무 힙하고 갓생 사는 느낌이야", "This cafe has such a cool vibe, it feels like living your best life"),
    ("아이스 아메리카노 한 잔 주세요", "One iced americano please"),
]
for ko, en in pairs:
    ki, ei = tok.encode(ko), tok.encode(en)
    print(f"한국어 {len(ki):2d} 토큰: {[tok.decode([i]) for i in ki]}")
    print(f"영어   {len(ei):2d} 토큰: {[tok.decode([i]) for i in ei]}")
    print(f"비율 {len(ki)/len(ei):.2f}\n")
print("어휘 크기:", tok.vocab_size)