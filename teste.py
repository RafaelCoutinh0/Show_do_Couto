import flet as ft

def main(page: ft.Page):
    page.title = "Show do Milhão"
    page.theme_mode = "dark"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # Pergunta e respostas
    pergunta = ft.Text("Qual é a capital do Brasil?", size=24, weight=ft.FontWeight.BOLD)
    resultado = ft.Text("", size=20, color=ft.Colors.YELLOW)

    respostas = [
        ("A) São Paulo", False),
        ("B) Brasília", True),
        ("C) Rio de Janeiro", False),
        ("D) Salvador", False),
    ]

    def responder_clicado(e):
        if e.control.data:  # True = correta
            resultado.value = "✅ Resposta correta!"
            resultado.color = ft.Colors.GREEN
        else:
            resultado.value = "❌ Resposta errada!"
            resultado.color = ft.Colors.RED
        page.update()

    botoes = []
    for texto, correta in respostas:
        botoes.append(
            ft.ElevatedButton(
                texto,
                width=250,
                height=50,
                on_click=responder_clicado,
                data=correta,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.BLUE_GREY_700,
                    color=ft.Colors.WHITE,
                    shape=ft.RoundedRectangleBorder(radius=15)
                )
            )
        )

    # Layout da tela
    page.add(
        ft.Column(
            [
                ft.Text("💰 SHOW DO MILHÃO 💰", size=30, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                pergunta,
                *botoes,
                resultado,
            ],
            horizontal_alignment="center",
            spacing=20,
        )
    )

ft.app(target=main)
