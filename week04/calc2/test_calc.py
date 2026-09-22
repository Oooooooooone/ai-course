from calc import Calculator


def run_case(inputs):
    calc = Calculator()
    for key in inputs:
        calc.press(key)
    return calc.display


def test():
    tests = [
        ([], "0"),
        (["1", "2", "+", "3", "="], "15"),
        (["2", "+", "3", "*", "4", "="], "20"),
        (["5", "+", "-", "3", "="], "2"),
        (["0", ".", "1", "+", "0", ".", "2", "="], "0.3"),
        (["6", "/", "3", "="], "2"),
        (["7", "/", "2", "="], "3.5"),
        (["5", "/", "0", "="], "0으로 나눌 수 없습니다"),
        (["5", "/", "0", "=", "7"], "0으로 나눌 수 없습니다"),
        (["5", "/", "0", "=", "C"], "0"),
        (["1", ".", ".", "5"], "1.5"),
        (["."], "0."),
        (["0", "0", "7"], "7"),
        (["1", "2", "3", "BS"], "12"),
        (["5", "BS"], "0"),
        (["9", "+/-"], "-9"),
        (["5", "0", "%"], "0.5"),
        (["2", "+", "3", "=", "4"], "4"),
        (["2", "+", "3", "=", "+", "4", "="], "9"),
        (["2", "+", "3", "=", "="], "5"),
    ]

    failures = []
    for inputs, expected in tests:
        actual = run_case(inputs)
        if actual != expected:
            failures.append((inputs, expected, actual))

    if not failures:
        print(f"모든 테스트 통과 ({len(tests)}개)")
    else:
        for inputs, expected, actual in failures:
            print(f"실패: inputs={inputs}, expected={expected!r}, actual={actual!r}")
        print(f"테스트 실패: {len(failures)}개 실패")


if __name__ == "__main__":
    test()
