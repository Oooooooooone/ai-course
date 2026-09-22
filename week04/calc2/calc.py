class Calculator:
    def __init__(self):
        self._acc = None
        self._pending_op = None
        self._cur = "0"
        self._start_new_number = True
        self._just_equals = False
        self._error = False
        self.display = "0"

    def press(self, key: str):
        if self._error:
            if key == "C":
                self._reset()
            return

        if key in "0123456789":
            self._press_digit(key)
        elif key == ".":
            self._press_dot()
        elif key in ("+", "-", "*", "/"):
            self._press_operator(key)
        elif key == "=":
            self._press_equals()
        elif key == "C":
            self._reset()
        elif key == "BS":
            self._press_bs()
        elif key == "+/-":
            self._press_sign()
        elif key == "%":
            self._press_percent()

    def _reset(self):
        self._acc = None
        self._pending_op = None
        self._cur = "0"
        self._start_new_number = True
        self._just_equals = False
        self._error = False
        self.display = "0"

    def _start_fresh_calc_if_needed(self):
        if self._just_equals:
            self._just_equals = False
            self._acc = None
            self._pending_op = None
            self._start_new_number = True

    def _press_digit(self, key):
        self._start_fresh_calc_if_needed()
        if self._start_new_number:
            self._cur = "0"
            self._start_new_number = False

        digit_count = sum(1 for c in self._cur if c.isdigit())
        if digit_count >= 12:
            return

        if self._cur == "0":
            self._cur = "0" if key == "0" else key
        else:
            self._cur += key

        self.display = self._cur

    def _press_dot(self):
        self._start_fresh_calc_if_needed()
        if self._start_new_number:
            self._cur = "0"
            self._start_new_number = False

        if "." not in self._cur:
            self._cur += "."
        self.display = self._cur

    def _press_operator(self, key):
        if self._just_equals:
            self._just_equals = False
            self._pending_op = key
            self._start_new_number = True
            return

        if self._start_new_number:
            self._pending_op = key
            return

        cur_value = float(self._cur)
        if self._acc is None:
            self._acc = cur_value
        else:
            try:
                self._acc = self._compute(self._acc, self._pending_op, cur_value)
            except ZeroDivisionError:
                self._enter_error()
                return

        self._pending_op = key
        self._start_new_number = True
        self.display = self._format(self._acc)
        self._cur = self.display

    def _press_equals(self):
        if self._just_equals:
            return
        if self._pending_op is None:
            self._just_equals = True
            return

        cur_value = float(self._cur)
        base = self._acc if self._acc is not None else 0
        try:
            result = self._compute(base, self._pending_op, cur_value)
        except ZeroDivisionError:
            self._enter_error()
            return

        self._acc = result
        self._pending_op = None
        self.display = self._format(result)
        self._cur = self.display
        self._just_equals = True
        self._start_new_number = True

    def _press_bs(self):
        if self._just_equals:
            return
        if self._start_new_number:
            return
        if len(self._cur) <= 1:
            self._cur = "0"
        else:
            self._cur = self._cur[:-1]
            if self._cur in ("", "-"):
                self._cur = "0"
        self.display = self._cur

    def _press_sign(self):
        if self._just_equals:
            self._just_equals = False
            self._acc = None
            self._start_new_number = False

        if self._cur.startswith("-"):
            self._cur = self._cur[1:]
        elif self._cur != "0":
            self._cur = "-" + self._cur
        self.display = self._cur

    def _press_percent(self):
        value = float(self._cur) / 100
        self._cur = self._format(value)
        self.display = self._cur
        if self._just_equals:
            self._just_equals = False
            self._acc = None
        self._start_new_number = False

    def _enter_error(self):
        self._error = True
        self.display = "0으로 나눌 수 없습니다"

    @staticmethod
    def _compute(a, op, b):
        if op == "+":
            return a + b
        if op == "-":
            return a - b
        if op == "*":
            return a * b
        if op == "/":
            if b == 0:
                raise ZeroDivisionError
            return a / b
        raise ValueError(f"unknown op {op}")

    @staticmethod
    def _format(value):
        rounded = round(value, 10)
        s = f"{rounded:.10f}"
        if "." in s:
            s = s.rstrip("0").rstrip(".")
        if s in ("", "-", "-0"):
            s = "0"
        return s
