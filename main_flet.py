import flet as ft
import random
from perguntas import facil
import flet as ft
colors = ft.colors

# Função para tocar música usando flet-audio
class MusicaPlayer:
    def __init__(self, page):
        self.page = page
        self.audio_player = ft.Audio()
        # Adiciona o controle de áudio à página apenas se não estiver presente
        if self.audio_player not in self.page.overlay:
            self.page.overlay.append(self.audio_player)
            self.page.update()

    def tocar(self, i=0):
        musicas = [
            "/musics/music_game.mp3",
            "/musics/pergunta1.mp3",
            "/musics/acerto.mp3",
            "/musics/lose.mp3",
            "/musics/win.mp3"
        ]
        # Só chama pause se o controle já estiver anexado à página
        if self.audio_player in self.page.overlay:
            try:
                self.audio_player.pause()
            except AssertionError:
                pass
        self.audio_player.src = musicas[i]
        self.audio_player.autoplay = True
        self.page.update()

class ShowDoMilhao:
    def __init__(self, page):
        self.page = page
        self.page.title = "Show do Coutão"
        self.page.bgcolor = "#002e5c"
        self.musica = MusicaPlayer(page)
        self.pontos = 0
        self.checkpoint = 0
        self.perguntas_jogo = []
        self.pergunta_atual = None
        self.indice = 0
        self.ajuda_usada = False
        self.troca_usada = False
        self.ajuda_professor_usada = False
        self.labels_regua = []
        self.botoes = []
        self.tela_inicial()

    def tela_inicial(self):
        self.musica.tocar(0)
        self.page.clean()
        logo = ft.Image(src="/logo.png", width=1000, height=500)
        botao_jogar = ft.ElevatedButton(
            "Jogar",
            on_click=self.iniciar_jogo,
            bgcolor=colors.BLUE,
            color=colors.WHITE,
            width=300,
            height=70,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=28, weight=ft.FontWeight.BOLD)
            )
        )
        botao_sair = ft.ElevatedButton(
            "Sair",
            on_click=lambda _: self.page.window.close(),  # Correção aqui
            bgcolor=colors.RED,
            color=colors.WHITE,
            width=300,
            height=70,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=28, weight=ft.FontWeight.BOLD)
            )
        )
        self.page.add(
            ft.Column([
                logo,
                ft.Row([botao_jogar, botao_sair], alignment=ft.MainAxisAlignment.CENTER)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    def iniciar_jogo(self, e=None):
        self.musica.tocar(1)
        self.pontos = 0
        self.checkpoint = 0
        self.indice = 0
        self.ajuda_usada = False
        self.troca_usada = False
        self.ajuda_professor_usada = False
        self.perguntas_jogo = random.sample(facil, 10)
        self.tela_jogo()

    def tela_jogo(self):
        self.page.clean()
        self.labels_regua = []
        regua = []
        for i in range(len(self.perguntas_jogo)):
            texto = f"{i + 1}"
            icone = ""
            cor_fundo = colors.BLUE_900
            cor_texto = colors.WHITE
            borda = None
            # Bolinha ao redor do número
            bolinha = ft.Container(
                content=ft.Text(texto, size=16, color=cor_texto, weight=ft.FontWeight.BOLD),
                width=36,
                height=36,
                bgcolor=cor_fundo,
                border=ft.border.all(3, colors.YELLOW if i == self.indice else colors.WHITE),
                border_radius=18,
                alignment=ft.alignment.center,
                margin=ft.margin.only(right=0)  # Aproxima o emoji do número
            )
            if i + 1 in [3, 5, 8]:
                icone = "💰"
            elif i + 1 == 10:
                icone = "🏆"
            # Container para bolinha + ícone
            item = ft.Row([
                bolinha,
                ft.Text(icone, size=18, color=cor_texto) if icone else ft.Text("")
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=2)  # Reduz o espaçamento
            regua.append(item)
        self.labels_regua = regua
        self.label_pergunta = ft.Text("", size=18, color=colors.YELLOW, weight=ft.FontWeight.BOLD)
        self.botoes = []
        for i in range(4):
            botao = ft.ElevatedButton(
                "...",
                width=500,  # Largura igual à da pergunta
                bgcolor=colors.BLUE,
                color=colors.WHITE,
                on_click=lambda e, i=i: self.verificar_resposta(i)
            )
            self.botoes.append(botao)
        self.label_feedback = ft.Text("", size=16, color=colors.WHITE)
        self.label_saldo = ft.Text(f"Saldo atual: R${self.pontos}", size=16, color=colors.CYAN)
        self.botao_ajuda = ft.ElevatedButton(
            "Rodar Dados",
            bgcolor=colors.PURPLE,
            color=colors.WHITE,
            width=160,  # Largura igual à da pergunta
            on_click=self.ajuda_dado
        )
        self.botao_troca = ft.ElevatedButton(
            "Trocar Pergunta",
            bgcolor=colors.GREEN_900,
            color=colors.WHITE,
            width=160,  # Largura igual à da pergunta
            on_click=self.trocar_pergunta
        )
        self.botao_professor = ft.ElevatedButton(
            "Ajuda dos Professores",
            bgcolor=colors.ORANGE_900,
            color=colors.WHITE,
            width=160,  # Largura igual à da pergunta
            on_click=self.ajuda_professor
        )
        self.botao_desistir = ft.ElevatedButton("Desistir", bgcolor=colors.ORANGE, color=colors.WHITE, on_click=self.desistir)
        self.botao_sair = ft.ElevatedButton("Sair", bgcolor=colors.RED, color=colors.WHITE, on_click=lambda _: self.tela_inicial())
        self.page.add(
            ft.Row([
                ft.Column([
                    self.label_pergunta,
                    *self.botoes,
                    ft.Row([self.botao_ajuda, self.botao_troca, self.botao_professor]),
                    self.label_feedback,
                    self.label_saldo,
                    ft.Row([self.botao_desistir, self.botao_sair]),
                ], alignment=ft.MainAxisAlignment.START),
                ft.Column(regua, alignment=ft.MainAxisAlignment.START, spacing=0)
            ], alignment=ft.MainAxisAlignment.CENTER)
        )
        self.carregar_pergunta()

    def dividir_pergunta(self, texto, limite=90):
        # Limite aproximado de caracteres para a primeira "página"
        if len(texto) <= limite:
            return texto, ""
        # Tenta quebrar em espaço próximo ao limite
        idx = texto.rfind(" ", 0, limite)
        if idx == -1:
            idx = limite
        return texto[:idx], texto[idx:].lstrip()

    def dividir_ajuda(self, texto, limite=60):
        if len(texto) <= limite:
            return texto
        idx = texto.rfind(" ", 0, limite)
        if idx == -1:
            idx = limite
        return texto[:idx] + "\n" + texto[idx:].lstrip()

    def carregar_pergunta(self):
        self.musica.tocar(1)
        if self.indice < len(self.perguntas_jogo):
            self.pergunta_atual = self.perguntas_jogo[self.indice]
            alternativas = self.pergunta_atual["alternativas"][:]
            correta = self.pergunta_atual["correta"]
            alternativas_com_indices = list(enumerate(alternativas))
            random.shuffle(alternativas_com_indices)
            alternativas_embaralhadas = [alt for idx, alt in alternativas_com_indices]
            nova_correta = [idx for idx, alt in alternativas_com_indices].index(correta)
            self.pergunta_atual["alternativas_embaralhadas"] = alternativas_embaralhadas
            self.pergunta_atual["nova_correta"] = nova_correta
            # Junta o texto da pergunta em uma única string
            texto1, texto2 = self.dividir_pergunta(self.pergunta_atual["pergunta"], limite=500)
            texto_completo = texto1 + ("\n" + texto2 if texto2 else "")
            pergunta_principal = ft.Container(
                content=ft.Text(texto_completo, size=18, color=colors.YELLOW, weight=ft.FontWeight.BOLD, selectable=True),
                width=500,
                alignment=ft.alignment.center,
                padding=ft.padding.all(10),
                bgcolor=None
            )
            self.label_pergunta = pergunta_principal
            # Remove containers extras
            for i, alt in enumerate(alternativas_embaralhadas):
                self.botoes[i].text = alt
                self.botoes[i].disabled = False
            self.label_feedback.value = ""
            self.label_saldo.value = f"Saldo atual: R${self.pontos}"
            for i, item in enumerate(self.labels_regua):
                bolinha = item.controls[0]
                bolinha.bgcolor = colors.GREEN_700 if i < self.indice else (colors.YELLOW_300 if i == self.indice else colors.BLUE_900)
                bolinha.border = ft.border.all(3, colors.YELLOW if i == self.indice else colors.WHITE)
                bolinha.content.color = colors.BLACK if i == self.indice else colors.WHITE
            self.page.clean()
            self.page.add(
                ft.Row([
                    ft.Column([
                        self.label_pergunta,
                        # Removido linha separadora e pergunta_extra
                        *self.botoes,
                        ft.Row([self.botao_ajuda, self.botao_troca, self.botao_professor]),  # <-- corrigido aqui
                        self.label_feedback,
                        self.label_saldo,
                        ft.Row([self.botao_desistir, self.botao_sair]),
                    ], alignment=ft.MainAxisAlignment.START),
                    ft.Column(self.labels_regua, alignment=ft.MainAxisAlignment.START, spacing=0)
                ], alignment=ft.MainAxisAlignment.CENTER)
            )
            self.page.update()
        else:
            self.vitoria()

    def trocar_pergunta(self, e=None):
        if self.troca_usada:
            return
        self.troca_usada = True
        # Remover botão visualmente
        self.botao_troca.visible = False
        self.page.update()
        perguntas_possiveis = [p for p in facil if p not in self.perguntas_jogo]
        if perguntas_possiveis:
            nova_pergunta = random.choice(perguntas_possiveis)
            self.perguntas_jogo[self.indice] = nova_pergunta
            self.label_feedback.value = "🔄 Pergunta trocada!"
            self.label_feedback.color = colors.GREEN_900
            self.carregar_pergunta()
        else:
            self.label_feedback.value = "Não há perguntas disponíveis para troca."
            self.label_feedback.color = colors.RED
        self.page.update()

    def ajuda_dado(self, e=None):
        if self.ajuda_usada:
            return
        self.ajuda_usada = True
        # Remover botão visualmente
        self.botao_ajuda.visible = False
        self.page.update()
        correta = self.pergunta_atual["nova_correta"]
        alternativas_restantes = [i for i in range(4) if i != correta and not self.botoes[i].disabled]
        qtd_eliminar = min(random.randint(1, 3), len(alternativas_restantes))
        eliminar = random.sample(alternativas_restantes, qtd_eliminar)
        for i in eliminar:
            self.botoes[i].disabled = True
            self.botoes[i].text = " "  # CORRIGIDO: nunca deixe texto vazio, use espaço
        self.label_feedback.value = f"🎲 Dado rolado: {qtd_eliminar} alternativas eliminadas."
        self.label_feedback.color = colors.PURPLE
        self.page.update()

    def ajuda_professor(self, e=None):
        if self.ajuda_professor_usada:
            return
        self.ajuda_professor_usada = True
        # Remover botão visualmente
        self.botao_professor.visible = False
        self.page.update()
        texto_ajuda = self.pergunta_atual.get("ajuda", "👨‍🏫 Os professores sugerem que você pense bem antes de responder!")
        texto_ajuda = self.dividir_ajuda(texto_ajuda, limite=38)
        self.label_feedback.value = f"👨‍🏫 Ajuda dos Professores: {texto_ajuda}"
        self.label_feedback.color = colors.RED
        self.page.update()

    def verificar_resposta(self, escolha):
        for botao in self.botoes:
            botao.disabled = True
        correta = self.pergunta_atual["nova_correta"]
        if escolha == correta:
            self.musica.tocar(2)
            self.pontos += 1000
            if (self.indice + 1) in [3, 5, 8]:
                self.checkpoint = self.pontos
            self.label_feedback.value = f"✅ Correto! Ganhou R$1000"
            self.label_feedback.color = colors.GREEN
            self.label_saldo.value = f"Saldo atual: R${self.pontos}"
            self.indice += 1
            self.page.update()
            self.page.run_task(self._delay_carregar_pergunta)
        else:
            self.page.run_task(self._delay_derrota)
        self.page.update()

    async def _delay_carregar_pergunta(self):
        import asyncio
        await asyncio.sleep(1.5)
        self.carregar_pergunta()

    async def _delay_derrota(self):
        import asyncio
        await asyncio.sleep(0.5)
        self.derrota()

    def vitoria(self):
        self.page.clean()
        self.musica.tocar(4)
        msg = ft.Text(
            f"🎉 Parabéns, você ganhou!\nSaiu com R${self.pontos}",
            size=24,
            color=colors.YELLOW,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )
        botao_voltar = ft.ElevatedButton(
            "Voltar ao início",
            bgcolor=colors.BLUE,
            color=colors.WHITE,
            on_click=lambda _: self.tela_inicial()
        )
        self.page.add(
            ft.Container(
                content=ft.Column([msg, botao_voltar], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                expand=True
            )
        )

    def derrota(self):
        self.page.clean()
        self.musica.tocar(3)
        msg = ft.Text(
            f"❌ Você perdeu!\nSaiu com R${self.checkpoint}",
            size=24,
            color=colors.RED,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )
        botao_voltar = ft.ElevatedButton(
            "Voltar ao início",
            bgcolor=colors.BLUE,
            color=colors.WHITE,
            on_click=lambda _: self.tela_inicial()
        )
        self.page.add(
            ft.Container(
                content=ft.Column([msg, botao_voltar], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                expand=True
            )
        )

    def desistir(self, e=None):
        def confirmar_dlg(e):
            if e.control.text == "Sim":
                dlg.open = False
                self.page.update()
                # Remove o diálogo da tela
                self.page.dialog = None
                if dlg in self.page.overlay:
                    self.page.overlay.remove(dlg)
                self.page.clean()
                msg = ft.Text(
                    f"💰 Você desistiu!\nSaiu com R${self.pontos}",
                    size=24,
                    color=colors.ORANGE,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                )
                botao_voltar = ft.ElevatedButton(
                    "Voltar ao início",
                    bgcolor=colors.BLUE,
                    color=colors.WHITE,
                    on_click=lambda _: self.tela_inicial()
                )
                self.page.add(
                    ft.Container(
                        content=ft.Column([msg, botao_voltar], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        alignment=ft.alignment.center,
                        expand=True
                    )
                )
            else:
                dlg.open = False
                self.page.update()
                self.page.dialog = None
                if dlg in self.page.overlay:
                    self.page.overlay.remove(dlg)
        dlg = ft.AlertDialog(
            title=ft.Text("Desistir?"),
            content=ft.Text(f"Você deseja desistir e sair com R${self.pontos}?"),
            actions=[
                ft.TextButton("Sim", on_click=confirmar_dlg),
                ft.TextButton("Não", on_click=confirmar_dlg)
            ]
        )
        self.page.dialog = dlg
        if dlg not in self.page.overlay:
            self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()

    def _fechar_dialog(self, dlg):
        dlg.open = False
        self.page.update()


import os
import flet as ft

def main(page: ft.Page):
    ShowDoMilhao(page)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(
        target=main,
        view=ft.WEB_BROWSER,
        port=port,
        host="0.0.0.0"
    )
