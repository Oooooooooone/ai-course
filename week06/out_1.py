import re

def normalize_phone(s):
    if not s:
        return None
    
    # 숫자만 추출
    digits = re.sub(r'\D', '', s)
    
    # +82 처리 (입력값에 +82가 포함된 경우를 위해 원본에서 처리 시도)
    # 하지만 위에서 \D를 모두 제거했으므로, 원본 s를 기준으로 +82를 0으로 치환하는 로직 필요
    if s.strip().startswith('+82'):
        digits = '0' + re.sub(r'\D', '', s[3:])
    
    if not digits:
        return None

    # 010 시작 (11자리: 3-4-4)
    if digits.startswith('010') and len(digits) == 11:
        return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
    
    # 011, 016, 017, 018, 019 시작
    elif digits.startswith(('011', '016', '017', '018', '019')):
        if len(digits) == 10:
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        else:
            return None
            
    else:
        return None
