import re

def normalize_phone(s):
    if not s:
        return None
    
    # 특수문자 제거 및 +82 처리
    s = s.strip()
    if s.startswith("+82"):
        s = "0" + s[3:]
    
    # 숫자만 추출
    digits = re.sub(r'\D', '', s)
    
    if not digits:
        return None

    # 010으로 시작하는 경우 (11자리)
    if digits.startswith("010"):
        if len(digits) == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        else:
            return None
            
    # 011, 016, 017, 018, 019로 시작하는 경우
    elif digits.startswith(("011", "016", "017", "018", "019")):
        if len(digits) == 10:
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        else:
            return None
            
    # 그 외의 경우
    else:
        return None
