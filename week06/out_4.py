import re

def normalize_phone(s):
    if not s:
        return None
    
    # 숫자만 추출
    digits = re.sub(r'\D', '', s)
    
    # +82 처리 (원본 문자열에 +82가 포함되어 있는 경우 대응)
    if s.strip().startswith('+82'):
        digits = '0' + digits[2:] if len(digits) > 2 else digits

    # 010 시작 (11자리: 3-4-4)
    if digits.startswith('010') and len(digits) == 11:
        return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
    
    # 011, 016, 017, 018, 019 시작
    elif digits[:3] in ['011', '016', '017', '018', '019']:
        if len(digits) == 10:
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
            
    return None
