import re

def normalize_phone(s):
    if not s:
        return None
    
    # 숫자만 추출
    digits = re.sub(r'\D', '', s)
    
    # +82 처리 (입력 문자열에서 +82가 있으면 0으로 치환 후 숫자 추출)
    if s.strip().startswith('+82'):
        digits = '0' + re.sub(r'\D', '', s[3:])
    
    # 자릿수 및 시작 번호에 따른 포맷팅
    if digits.startswith('010'):
        if len(digits) == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        else:
            return None
            
    elif digits.startswith(('011', '016', '017', '018', '019')):
        if len(digits) == 10:
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        else:
            return None
    else:
        return None
