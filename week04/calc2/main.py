import flet as ft

from calc import Calculator


def main(page: ft.Page):
    page.title = "계산기"
    page.window.width = 340
    page.window.height = 520
    page.window.resizable = False

    calc = Calculator()
    display = ft.Text(value=calc.display, size=40, text_align=ft.TextAlign.RIGHT)

    def refresh():
        display.value = calc.display
        page.update()

    def on_button(e):
        calc.press(e.control.data)
        refresh()

    def on_key(e: ft.KeyboardEvent):
        key = e.key
        mapping = {
            "Enter": "=",
            "Backspace": "BS",
            "Escape": "C",
        }
        if key in mapping:
            calc.press(mapping[key])
            refresh()
        elif key in "0123456789.+-*/":
            calc.press(key)
            refresh()

    page.on_keyboard_event = on_key

    def make_button(label, key, bgcolor):
        return ft.Button(content=label, data=key, on_click=on_button, expand=1, height=60,
                         bgcolor=bgcolor, color=ft.Colors.WHITE)

    GREY_800 = ft.Colors.GREY_800
    ORANGE = ft.Colors.ORANGE
    GREY_600 = ft.Colors.GREY_600

    page.add(
        ft.Container(content=display, alignment=ft.Alignment.CENTER_RIGHT, padding=10, height=90),
        ft.Row(controls=[
            make_button("C", "C", GREY_600),
            make_button("+/-", "+/-", GREY_600),
            make_button("%", "%", GREY_600),
            make_button("÷", "/", ORANGE),
        ]),
        ft.Row(controls=[
            make_button("7", "7", GREY_800),
            make_button("8", "8", GREY_800),
            make_button("9", "9", GREY_800),
            make_button("×", "*", ORANGE),
        ]),
        ft.Row(controls=[
            make_button("4", "4", GREY_800),
            make_button("5", "5", GREY_800),
            make_button("6", "6", GREY_800),
            make_button("−", "-", ORANGE),
        ]),
        ft.Row(controls=[
            make_button("1", "1", GREY_800),
            make_button("2", "2", GREY_800),
            make_button("3", "3", GREY_800),
            make_button("+", "+", ORANGE),
        ]),
        ft.Row(controls=[
            make_button("0", "0", GREY_800),
            make_button(".", ".", GREY_800),
            make_button("⌫", "BS", GREY_800),
            make_button("=", "=", ORANGE),
        ]),
    )


ft.run(main)
