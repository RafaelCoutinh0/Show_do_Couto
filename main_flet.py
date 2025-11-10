# main_flet.py
# Versão preparada para deploy em Railway (Flet 0.23.2) e áudio local (musics/).
import os
import random
import traceback

import flet as ft

# Compatibilidade com cores entre versões:
try:
    colors = ft.colors    # versão mais nova
except Exception:
    try:
        colors = ft.Colors  # fallback
    except Exception:
        colors = None  # raríssimo: fallback genérico

# Import de player de áudio com fallback
# flet_audio pode expor FletAudio (nomes variam entre versões)
FLET_AUDIO_AVAILABLE = False
try:
    from flet_audio import FletAudio  # pacote flet-audio (nome comum)
    FLET_AUDIO_AVAILABLE = True
except Exception:
    # fallback: talvez ft.Audio exista (algumas builds)
    try:
        _ = ft.Audio  # verifica existência
        FLET_AUDIO_AVAILABLE = False  # usaremos ft.Audio como fallback ad-hoc
    except Exception:
        FLET_AUDIO_AVAILABLE = False

# Caminhos de assets (relativos)
ASSET_LOGO = "logo.png"
ASSET_MUSICS = [
    "musics/music_game.mp3",
    "musics/pergunta1.mp3",
    "musics/acerto.mp3",
    "musics/lose.mp3",
    "musics/win.mp3",
]


class MusicaPlayer:
    def __init__(self, page: ft.Page):
        self.page = page
        self.player = None

        # Tenta criar FletAudio se disponível
        try:
            if 'FletAudio' in globals() and globals().get("FletAudio"):
                self.player = FletAudio(src="", autoplay=False)
            else:
                # fallback: usar ft.Audio se disponível
                if hasattr(ft, "Audio"):
                    self.player = ft.Audio(src="", autoplay=False)
                else:
                    self.player = None
        except Exception:
            self.player = None

        if self.player is not None and self.player not in self.page.overlay:
            try:
                self.page.overlay.append(self.player)
            except Exception:
                pass

    def tocar(self, i=0):
        if not self.player:
            return
        try:
            idx = int(i) if isinstance(i, int) else 0
            idx = max(0, min(idx, len(ASSET_MUSICS) - 1))
            src = ASSET_MUSICS[idx]
            # garante caminho relativo (sem leading slash)
            src = src.lstrip("/")
            self.player.src = src
            # autoplay pode não ser aceito por todas as classes; tente setar e update
            try:
                self.player.autoplay = True
            except Exception:
                pass
            try:
                self.page.update()
            except Exception:
                pass
        except Exception:
            # não deixar quebrar a aplicação por erro de áudio
            print("Erro ao tocar áudio:", traceback.format_exc())


class ShowDoMilhao:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Show do Coutão"
        try:
            self.page.bgcolor = "#002e5c"
        except Exception:
            pass
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

    # helpers para compatibilidade de ButtonStyle entre versões
    def _make_button_style(self):
        # Tentamos usar text_style (nova API). Se der TypeError, tentamos textstyle.
        try:
            return ft.ButtonStyle(
                text_style=ft.TextStyle(size=28, weight=ft.FontWeight.BOLD)
            )
        except TypeError:
            try:
                return ft.ButtonStyle(
                    textstyle=ft.TextStyle(size=28, weight=ft.FontWeight.BOLD)
                )
            except Exception:
                # fallback simples
                return None
        except Exception:
            return None

    def tela_inicial(self):
        try:
            self.musica.tocar(0)
        except Exception:
            pass
        self.page.clean()
        logo = ft.Image(src=ASSET_LOGO, width=1000, height=500)
        botao_style = self._make_button_style()
        botao_jogar = ft.ElevatedButton(
            "Jogar",
            on_click=self.iniciar_jogo,
            bgcolor=(colors.BLUE if colors is not None else None),
            color=(colors.WHITE if colors is not None else None),
            width=300,
            height=70,
            style=botao_style
        )
        botao_sair = ft.ElevatedButton(
            "Sair",
            on_click=lambda _: self.page.window.close() if hasattr(self.page, "window") else self.tela_inicial(),
            bgcolor=(colors.RED if colors is not None else None),
            color=(colors.WHITE if colors is not None else None),
            width=300,
            height=70,
            style=botao_style
        )
        self.page.add(
            ft.Column([
                logo,
                ft.Row([botao_jogar, botao_sair], alignment=ft.MainAxisAlignment.CENTER)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    def iniciar_jogo(self, e=None):
        try:
            self.musica.tocar(1)
        except Exception:
            pass
        self.pontos = 0
        self.checkpoint = 0
        self.indice = 0
        self.ajuda_usada = False
        self.troca_usada = False
        self.ajuda_professor_usada = False
        # importa perguntas dinamicamente para evitar import circular no topo
        try:
            from perguntas import facil
            self.perguntas_jogo = random.sample(facil, min(10, len(facil)))
        except Exception:
            self.perguntas_jogo = []
        self.tela_jogo()

    def tela_jogo(self):
        self.page.clean()
        self.labels_regua = []
        regua = []
        for i in range(len(self.perguntas_jogo)):
            texto = f"{i + 1}"
            icone = ""
            cor_fundo = (colors.BLUE_900 if colors is not None else None)
            cor_texto = (colors.WHITE if colors is not None else None)
            bolinha = ft.Container(
                content=ft.Text(texto, size=16, color=cor_texto, weight=ft.FontWeight.BOLD),
                width=36,
                height=36,
                bgcolor=cor_fundo,
                border=ft.border.all(3, (colors.YELLOW if (colors is not None) else None)),
                border_radius=18,
                alignment=ft.alignment.center,
                margin=ft.margin.only(right=0)
            )
            if i + 1 in [3, 5, 8]:
                icone = "💰"
            elif i + 1 == 10:
                icone = "🏆"
            item = ft.Row([
                bolinha,
                ft.Text(icone, size=18, color=cor_texto) if icone else ft.Text("")
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=2)
            regua.append(item)
        self.labels_regua = regua
        self.label_pergunta = ft.Text("", size=18, color=(colors.YELLOW if colors is not None else None), weight=ft.FontWeight.BOLD)
        self.botoes = []
        for i in range(4):
            botao = ft.ElevatedButton(
                "...",
                width=500,
                bgcolor=(colors.BLUE if colors is not None else None),
                color=(colors.WHITE if colors is not None else None),
                on_click=lambda e, i=i: self.verificar_resposta(i)
            )
            self.botoes.append(botao)
        self.label_feedback = ft.Text("", size=16, color=(colors.WHITE if colors is not None else None))
        self.label_saldo = ft.Text(f"Saldo atual: R${self.pontos}", size=16, color=(colors.CYAN if colors is not None else None))
        self.botao_ajuda = ft.ElevatedButton(
            "Rodar Dados",
            bgcolor=(colors.PURPLE if colors is not None else None),
            color=(colors.WHITE if colors is not None else None),
            width=160,
            on_click=self.ajuda_dado
        )
        self.botao_troca = ft.ElevatedButton(
            "Trocar Pergunta",
            bgcolor=(colors.GREEN_900 if colors is not None else None),
            color=(colors.WHITE if colors is not None else None),
            width=160,
            on_click=self.trocar_pergunta
        )
        self.botao_professor = ft.ElevatedButton(
            "Ajuda dos Professores",
            bgcolor=(colors.ORANGE_900 if colors is not None else None),
            color=(colors.WHITE if colors is not None else None),
            width=160,
            on_click=self.ajuda_professor
        )
        self.botao_desistir = ft.ElevatedButton("Desistir", bgcolor=(colors.ORANGE if colors is not None else None), color=(colors.WHITE if colors is not None else None), on_click=self.desistir)
        self.botao_sair = ft.ElevatedButton("Sair", bgcolor=(colors.RED if colors is not None else None), color=(colors.WHITE if colors is not None else None), on_click=lambda _: self.tela_inicial())
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

    # helpers de texto para dividir questão/ajuda
    def dividir_pergunta(self, texto, limite=90):
        if len(texto) <= limite:
            return texto, ""
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
        try:
            self.musica.tocar(1)
        except Exception:
            pass
        if self.indice < len(self.perguntas_jogo):
            self.pergunta_atual = self.perguntas_jogo[self.indice]
            alternativas = self.pergunta_atual["alternativas"][:]
            correta = self.pergunta_atual["correta"]
            alternativas_com_indices = list(enumerate(alternativas))
            random.shuffle(alternativas_com_indices)
            alternativas_embaralhadas = [alt for idx, alt in alternativas_com_indices]
            # novo índice da correta após embaralhar
            nova_correta = [idx for idx, alt in alternativas_com_indices].index(correta)
            self.pergunta_atual["alternativas_embaralhadas"] = alternativas_embaralhadas
            self.pergunta_atual["nova_correta"] = nova_correta
            texto1, texto2 = self.dividir_pergunta(self.pergunta_atual["pergunta"], limite=500)
            texto_completo = texto1 + ("\n" + texto2 if texto2 else "")
            pergunta_principal = ft.Container(
                content=ft.Text(texto_completo, size=18, color=(colors.YELLOW if colors is not None else None), weight=ft.FontWeight.BOLD, selectable=True),
                width=500,
                alignment=ft.alignment.center,
                padding=ft.padding.all(10),
                bgcolor=None
            )
            self.label_pergunta = pergunta_principal
            for i, alt in enumerate(alternativas_embaralhadas):
                self.botoes[i].text = alt
                self.botoes[i].disabled = False
            self.label_feedback.value = ""
            self.label_saldo.value = f"Saldo atual: R${self.pontos}"
            for i, item in enumerate(self.labels_regua):
                bolinha = item.controls[0]
                try:
                    bolinha.bgcolor = (colors.GREEN_700 if i < self.indice else (colors.YELLOW_300 if i == self.indice else colors.BLUE_900))
                    bolinha.border = ft.border.all(3, (colors.YELLOW if i == self.indice else colors.WHITE))
                    bolinha.content.color = (colors.BLACK if i == self.indice else colors.WHITE)
                except Exception:
                    pass
            self.page.clean()
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
                    ft.Column(self.labels_regua, alignment=ft.MainAxisAlignment.START, spacing=0)
                ], alignment=ft.MainAxisAlignment.CENTER)
            )
            try:
                self.page.update()
            except Exception:
                pass
        else:
            self.vitoria()

    def trocar_pergunta(self, e=None):
        if self.troca_usada:
            return
        self.troca_usada = True
        try:
            self.botao_troca.visible = False
            self.page.update()
        except Exception:
            pass
        try:
            from perguntas import facil
            perguntas_possiveis = [p for p in facil if p not in self.perguntas_jogo]
        except Exception:
            perguntas_possiveis = []
        if perguntas_possiveis:
            nova_pergunta = random.choice(perguntas_possiveis)
            self.perguntas_jogo[self.indice] = nova_pergunta
            self.label_feedback.value = "🔄 Pergunta trocada!"
            try:
                self.label_feedback.color = (colors.GREEN_900 if colors is not None else None)
            except Exception:
                pass
            self.carregar_pergunta()
        else:
            self.label_feedback.value = "Não há perguntas disponíveis para troca."
            try:
                self.label_feedback.color = colors.RED
            except Exception:
                pass
        try:
            self.page.update()
        except Exception:
            pass

    def ajuda_dado(self, e=None):
        if self.ajuda_usada:
            return
        self.ajuda_usada = True
        try:
            self.botao_ajuda.visible = False
            self.page.update()
        except Exception:
            pass
        correta = self.pergunta_atual["nova_correta"]
        alternativas_restantes = [i for i in range(4) if i != correta and not self.botoes[i].disabled]
        qtd_eliminar = min(random.randint(1, 3), len(alternativas_restantes))
        eliminar = random.sample(alternativas_restantes, qtd_eliminar)
        for i in eliminar:
            self.botoes[i].disabled = True
            self.botoes[i].text = " "
        self.label_feedback.value = f"🎲 Dado rolado: {qtd_eliminar} alternativas eliminadas."
        try:
            self.label_feedback.color = (colors.PURPLE if colors is not None else None)
        except Exception:
            pass
        try:
            self.page.update()
        except Exception:
            pass

    def ajuda_professor(self, e=None):
        if self.ajuda_professor_usada:
            return
        self.ajuda_professor_usada = True
        try:
            self.botao_professor.visible = False
            self.page.update()
        except Exception:
            pass
        texto_ajuda = self.pergunta_atual.get("ajuda", "👨‍🏫 Os professores sugerem que você pense bem antes de responder!")
        texto_ajuda = self.dividir_ajuda(texto_ajuda, limite=38)
        self.label_feedback.value = f"👨‍🏫 Ajuda dos Professores: {texto_ajuda}"
        try:
            self.label_feedback.color = (colors.RED if colors is not None else None)
        except Exception:
            pass
        try:
            self.page.update()
        except Exception:
            pass

    def verificar_resposta(self, escolha):
        for botao in self.botoes:
            botao.disabled = True
        correta = self.pergunta_atual["nova_correta"]
        if escolha == correta:
            try:
                self.musica.tocar(2)
            except Exception:
                pass
            self.pontos += 1000
            if (self.indice + 1) in [3, 5, 8]:
                self.checkpoint = self.pontos
            self.label_feedback.value = f"✅ Correto! Ganhou R$1000"
            try:
                self.label_feedback.color = (colors.GREEN if colors is not None else None)
            except Exception:
                pass
            self.label_saldo.value = f"Saldo atual: R${self.pontos}"
            self.indice += 1
            try:
                self.page.update()
            except Exception:
                pass
            self.page.run_task(self._delay_carregar_pergunta)
        else:
            self.page.run_task(self._delay_derrota)
        try:
            self.page.update()
        except Exception:
            pass

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
        try:
            self.musica.tocar(4)
        except Exception:
            pass
        msg = ft.Text(
            f"🎉 Parabéns, você ganhou!\nSaiu com R${self.pontos}",
            size=24,
            color=(colors.YELLOW if colors is not None else None),
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )
        botao_voltar = ft.ElevatedButton(
            "Voltar ao início",
            bgcolor=(colors.BLUE if colors is not None else None),
            color=(colors.WHITE if colors is not None else None),
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
        try:
            self.musica.tocar(3)
        except Exception:
            pass
        msg = ft.Text(
            f"❌ Você perdeu!\nSaiu com R${self.checkpoint}",
            size=24,
            color=(colors.RED if colors is not None else None),
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )
        botao_voltar = ft.ElevatedButton(
            "Voltar ao início",
            bgcolor=(colors.BLUE if colors is not None else None),
            color=(colors.WHITE if colors is not None else None),
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
                try:
                    self.page.update()
                except Exception:
                    pass
                self.page.dialog = None
                if dlg in self.page.overlay:
                    self.page.overlay.remove(dlg)
                self.page.clean()
                msg = ft.Text(
                    f"💰 Você desistiu!\nSaiu com R${self.pontos}",
                    size=24,
                    color=(colors.ORANGE if colors is not None else None),
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                )
                botao_voltar = ft.ElevatedButton(
                    "Voltar ao início",
                    bgcolor=(colors.BLUE if colors is not None else None),
                    color=(colors.WHITE if colors is not None else None),
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
                try:
                    self.page.update()
                except Exception:
                    pass
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
        try:
            self.page.update()
        except Exception:
            pass

    def _fechar_dialog(self, dlg):
        dlg.open = False
        try:
            self.page.update()
        except Exception:
            pass


def main(page: ft.Page):
    ShowDoMilhao(page)


if __name__ == "__main__":
    # Usa a porta do Railway se existir
    port = os.environ.get("PORT")

    if port:
        # 🌐 Modo WEB (Railway ou celular)
        ft.app(
            target=main,
            view=ft.WEB_BROWSER,
            port=int(port),
            host="0.0.0.0",
            assets_dir="."    # ✅ preciso para logo e audio funcionarem
        )
    else:
        # 💻 Modo APP (rodando no PC local)
        ft.app(
            target=main,
            view=ft.APP,      # ✅ importante para gerar APK e rodar localmente
            assets_dir="."    # ✅ necessário para carregar logo.png
        )

