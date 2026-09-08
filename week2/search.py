import ollama
import numpy as np

def emb(text):
    return np.array(ollama.embed(model="bge-m3", input=text).embeddings[0])

docs = [
    "넷플릭스는 매달 정해진 날짜에 요금이 자동으로 결제된다",
    "티빙은 KBS, MBC, SBS 방송사의 콘텐츠를 제공한다",
    "쿠팡 와우 회원은 추가 비용 없이 프라임 비디오를 이용할 수 있다",
    "디즈니플러스는 마블과 픽사 애니메이션을 독점 제공한다",
    "웨이브는 지상파 방송 다시보기에 강점이 있다",
    "왓챠는 한국 영화와 독립 영화 큐레이션으로 유명하다",
    "애플TV플러스는 자체 제작 오리지널 시리즈 위주로 운영한다",
    "OTT 계정을 여러 명이 나눠쓰면 월 부담금이 줄어든다",
    "4K 화질로 시청하려면 인터넷 속도가 최소 25Mbps 이상이어야 한다",
    "해외에서 국내 OTT를 이용하려면 VPN 우회가 필요한 경우가 있다"
]

D = np.stack([emb(d) for d in docs])

def search(question, k=3):
    q = emb(question)
    sims = D @ q / (np.linalg.norm(D, axis=1) * np.linalg.norm(q))
    for i in np.argsort(-sims)[:k]:
        print(f"  {sims[i]:.3f}  {docs[i]}")

for question in ["돈 안 내고 아마존 드라마 볼 수 있는 방법 있어?",
                  "친구랑 같이 써서 값 줄일 수 있어?",
                  "외국에서도 한국 서비스 볼 수 있어?"]:
    print("Q:", question)
    search(question)