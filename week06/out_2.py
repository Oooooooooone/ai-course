import re

def normalize_phone(s):
    if not s:
        return None
    
    # 숫자만 추출
    digits = re.sub(r'\D', '', s)
    
    # +82 처리 (입력 문자열에서 직접 처리하기 위해 원본 패턴 확인 필요하나, 
    # 규칙상 숫자로 변환된 후의 처리가 명확하므로 정규식 전 단계에서 처리)
    if s.strip().startswith('+82'):
        digits = '0' + digits[3:] if len(digits) > 3 else digits # 사실상 +82를 0으로 치환하는 로직
        # 위 방식보다 정확하게:
        temp_s = s.strip()
        if temp_s.startswith('+82'):
            digits = '0' + re.sub(r'\D', '', temp_s[3:])

    # 재정의된 digits 추출 (위 로직 통합)
    digits = re.sub(r'\D', '', s)
    if s.strip().startswith('+82'):
        digits = '0' + re.sub(r'\D', '', s.strip()[3:])

    if not digits:
        return None

    # 010 시작 (11자리: 3-4-4)
    if digits.startswith('010'):
        if len(digits) == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        else:
            return None

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
