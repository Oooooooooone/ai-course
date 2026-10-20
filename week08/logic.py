from datetime import datetime

def validate_time(time_str: str) -> tuple[bool, str | None]:
    stripped_time = time_str.strip()
    
    if not stripped_time:
        return False, "시각은 09:30처럼 입력하세요"
    
    if len(stripped_time) != 5 or stripped_time[2] != ':':
        return False, "시각은 09:30처럼 입력하세요"
        
    try:
        h_str, m_str = stripped_time.split(':')
        if len(h_str) != 2 or len(m_str) != 2:
             return False, "시각은 09:30처럼 입력하세요"

        h, m = int(h_str), int(m_str)
        
        if not (0 <= h <= 23 and 0 <= m <= 59):
            return False, "없는 시각입니다"
            
        return True, None
    except ValueError:
        return False, "시각은 09:30처럼 입력하세요"

def calculate_fee(minutes: int) -> int:
    if minutes <= 30:
        return 0
    
    fee = ((minutes - 31) // 10 + 1) * 500
    return min(fee, 20000)

def format_currency(amount: int) -> str:
    return f"{amount:,}"

def calculate_total(fee_list: list[int]) -> int:
    return sum(fee_list)

def process_calculation(start_input: str, end_input: str) -> tuple[dict | None, str | None]:
    start_str = start_input.strip()
    end_str = end_input.strip()
    
    if not start_str:
        return None, "입차 시각을 입력하세요"
    if not end_str:
        return None, "출차 시각을 입력하세요"
    
    start_valid, start_err = validate_time(start_str)
    if not start_valid:
        return None, start_err
        
    end_valid, end_err = validate_time(end_str)
    if not end_valid:
        return None, end_err
        
    start_dt = datetime.strptime(start_str, "%H:%M")
    end_dt = datetime.strptime(end_str, "%H:%M")
    
    if end_dt <= start_dt:
        return None, "출차는 입차보다 뒤여야 합니다"
    
    duration_minutes = int((end_dt - start_dt).total_seconds() / 60)
    fee = calculate_fee(duration_minutes)
    
    return {
        'start': start_str,
        'end': end_str,
        'duration': duration_minutes,
        'fee': fee
    }, None
