from logic import validate_time, calculate_fee, format_currency, calculate_total, process_calculation

def run_tests():
    passed = 0
    failed = 0

    def assert_equal(actual, expected, test_name):
        nonlocal passed, failed
        if actual == expected:
            passed += 1
        else:
            print(f"FAIL: {test_name}")
            print(f"  Expected: {expected}")
            print(f"  Actual:   {actual}")
            failed += 1

    print("--- Starting Tests ---")

    v_cases = [
        ("", (False, "시각은 09:30처럼 입력하세요")),
        (" 09:30 ", (True, None)),
        ("9:30", (False, "시각은 09:30처럼 입력하세요")),
        ("0930", (False, "시각은 09:30처럼 입력하세요")),
        ("09:3", (False, "시각은 09:30처럼 입력하세요")),
        ("24:00", (False, "없는 시각입니다")),
        ("12:60", (False, "없는 시각입니다")),
    ]
    for i, (inp, exp) in enumerate(v_cases):
        assert_equal(validate_time(inp), exp, f"validate_time[{i}]")

    p_cases = [
        ("", "10:00", (None, "입차 시각을 입력하세요")),
        ("10:00", "", (None, "출차 시각을 입력하세요")),
        ("", "", (None, "입차 시각을 입력하세요")),
        ("9:30", "10:00", (None, "시각은 09:30처럼 입력하세요")),
        ("10:00", "10:3", (None, "시각은 09:30처럼 입력하세요")),
        ("10:00", "25:00", (None, "없는 시각입니다")),
        ("10:00", "10:00", (None, "출차는 입차보다 뒤여야 합니다")),
        ("11:00", "10:00", (None, "출차는 입차보다 뒤여야 합니다")),
        ("09:00", "09:30", ({'start': '09:00', 'end': '09:30', 'duration': 30, 'fee': 0}, None)),
        ("09:00", "10:00", ({'start': '09:00', 'end': '10:00', 'duration': 60, 'fee': 1500}, None)),
        ("09:00", "16:01", ({'start': '09:00', 'end': '16:01', 'duration': 421, 'fee': 20000}, None)),
    ]
    for i, (inp1, inp2, exp) in enumerate(p_cases):
        assert_equal(process_calculation(inp1, inp2), exp, f"process_calculation[{i}]")

    f_cases = [
        (0, 0),
        (30, 0),
        (31, 500),
        (40, 500),
        (41, 1000),
        (420, 19500),
        (421, 20000),
        (1439, 20000),
    ]
    for i, (inp, exp) in enumerate(f_cases):
        assert_equal(calculate_fee(inp), exp, f"calculate_fee[{i}]")

    t_cases = [
        ([], 0),
        ([500], 500),
        ([500, 1000, 20000], 21500),
    ]
    for i, (inp, exp) in enumerate(t_cases):
        assert_equal(calculate_total(inp), exp, f"calculate_total[{i}]")

    c_cases = [
        (0, "0"),
        (500, "500"),
        (3500, "3,500"),
        (20000, "20,000"),
        (123456, "123,456"),
    ]
    for i, (inp, exp) in enumerate(c_cases):
        assert_equal(format_currency(inp), exp, f"format_currency[{i}]")

    print("--- Results ---")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    if failed == 0:
        print("ALL TESTS PASSED!")
    else:
        print("SOME TESTS FAILED.")

if __name__ == "__main__":
    run_tests()
