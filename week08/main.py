import flet as ft
import logic


def main(page: ft.Page):
    page.title = "주차 요금 계산기"
    page.window.width = 480
    page.window.height = 600
    page.window.resizable = False

    start_input = ft.TextField(label="입차 시각 (HH:MM)", expand=True)
    end_input = ft.TextField(label="출차 시각 (HH:MM)", expand=True)
    notice_text = ft.Text(value="", color=ft.Colors.RED)
    items_list = ft.ListView(expand=True, spacing=4)
    total_text = ft.Text(value="오늘 합계: 0원")

    fees = []

    def on_calculate(e):
        res, err = logic.process_calculation(start_input.value, end_input.value)
        if err:
            notice_text.value = err
        else:
            notice_text.value = ""
            fees.append(res["fee"])
            item_str = f"{res['start']} → {res['end']} | {res['duration']}분 | {logic.format_currency(res['fee'])}원"
            items_list.controls.append(ft.Text(value=item_str))
            total_sum = logic.calculate_total(fees)
            total_text.value = f"오늘 합계: {logic.format_currency(total_sum)}원"
        page.update()

    page.add(
        ft.Row(controls=[start_input, end_input]),
        ft.Row(controls=[ft.Button(content="계산하기", on_click=on_calculate, expand=True)]),
        notice_text,
        items_list,
        total_text,
    )


ft.run(main)