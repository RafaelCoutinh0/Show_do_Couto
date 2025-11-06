# main_flet.py (responsivo - Régua abaixo no celular)
import os
import random
import traceback

import flet as ft

# --------------------------
# Compatibilidade de cores
# --------------------------
try:
    colors = ft.colors  # versão nova
except Exception:
    try:
        colors = ft.Colors  # fallback
    except Exception:
        colors = None

# --------------------------
# Áudio: tenta FletAudio, depois ft.Audio, senão None
# --------------------------
FLET_AUDIO_CLASS = None
try:
    from flet_audio import FletAudio  # pacote comum
    FLET_AUDIO_CLASS = FletAudio
except Exception:
    # fallback: verificar existência de ft.Audio
    if hasattr(ft, "Audio"):
        FLET_AUDIO_CLASS = ft.Audio
    else:
        FLET_AUDIO_CLASS = None

# --------------------------
# Assets
# --------------------------
ASSET_LOGO = "logo.png"
ASSET_MUSICS = [
    "musics/music_game.mp3",
    "musics/pergunta1.mp3",
    "musics/acerto.mp3",
    "musics/lose.mp3",
    "musics/win.mp3",
]

# --------------------------
# MusicaPlayer (safe)
# --------------------------
class MusicaPlayer:
    def __init__(self, page: ft.Page):
        self.page = page
        self.player = None
        try:
            if FLET_AUDIO_CLASS:
                # criar instância da classe detectada
                try:
                    # FletAudio signature pode variar, usar kwargs mínimos
                    self.player = FLET_AUDIO_CLASS(src="", autoplay=False)
                except TypeError:
                    # fallback sem kwargs
                    self.player = FLET_AUDIO_CLASS()
                    try:
                        self.player.src = ""
                        self.player.autoplay = False
                    except Exception:
                        pass
        except Exception:
            self.player = None

        # tentar anexar ao overlay
        try:
            if self.player is not None and self.player not in self.page.overlay:
                self.page.overlay.append(self.player)
        except Exception:
            pass

    def tocar(self, i=0):
        if not self.player:
            return
        try:
            idx = int(i) if isinstance(i, int) else 0
            idx = max(0, min(idx, len(ASSET_MUSICS) - 1))
            src = ASSET_MUSICS[idx].lstrip("/")  # relativo, sem leading slash
            try:
                self.player.src = src
            except Exception:
                # algumas versões usam set_source etc - tentamos fallback
                try:
                    setattr(self.player, "src", src)
                except Exception:
                    pass
            try:
                self.player.autoplay = True
            except Exception:
                pass
            try:
                self.page.update()
            except Exception:
                pass
        except Exception:
            print("Erro ao tocar áudio:", traceback.format_exc())


# --------------------------
# Helper: button style compatível
# --------------------------
def make_button_style():
    try:
        return ft.ButtonStyle(
            text_style=ft.TextStyle(size=22, weight=ft.FontWeight.BOLD)
        )
    except TypeError:
        try:
            return ft.ButtonStyle(
                textstyle=ft.TextStyle(size=22, weight=ft.FontWeight.BOLD)
            )
        except Exception:
            return None
    except Exception:
        return None


# --------------------------
# The Game
# --------------------------
class ShowDoMilhao:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Show do Coutão"
        # safe bgcolor
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

        # botão style único
        self._btn_style = make_button_style()

        # inicializa a tela
        self.tela_inicial()

    # UTIL: detectar largura efetiva
    def _page_width(self):
        # page.window_width existe em algumas versões; fallback para page.width
        try:
            return getattr(self.page, "window_width", getattr(self.page, "width", 800)) or 800
        except Exception:
            return 800

    def _is_mobile(self):
        try:
            return self._page_width() < 600
        except Exception:
            return False

    # layout: tela inicial
    def tela_inicial(self):
        try:
            self.musica.tocar(0)
        except Exception:
            pass

        self.page.clean()
        page_w = self._page_width()
        logo_w = min(page_w * 0.9, 1000)

        logo = ft.Image(src=ASSET_LOGO, width=logo_w, height=int(logo_w * 0.5), fit=ft.ImageFit.CONTAIN)

        btn_width = int(page_w * 0.6) if self._is_mobile() else 300

        botao_jogar = ft.ElevatedButton(
            "Jogar",
            on_click=self.iniciar_jogo,
            bgcolor=(colors.BLUE if colors is not None else None),
            color=(colors.WHITE if colors is not None else None),
            width=btn_width,
            height=60,
            style=self._btn_style
        )
        botao_sair = ft.ElevatedButton(
            "Sair",
            on_click=lambda _: self.page.window.close() if hasattr(self.page, "window") else self.tela_inicial(),
            bgcolor=(colors.RED if colors is not None else None),
            color=(colors.WHITE if colors is not None else None),
            width=btn_width,
            height=60,
            style=self._btn_style
        )

        # centraliza e permite scroll se necessário
        content = ft.Column(
            [
                logo,
                ft.Row([botao_jogar], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([botao_sair], alignment=ft.MainAxisAlignment.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            spacing=20,
            expand=True,
        )

        container = ft.Container(content=content, alignment=ft.alignment.center, expand=True, padding=ft.padding.all(12))
        self.page.add(container)
        try:
            self.page.update()
        except Exception:
            pass

    # iniciar jogo: carrega perguntas (import dinâmico)
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

        try:
            from perguntas import facil
            self.perguntas_jogo = random.sample(facil, min(10, len(facil)))
        except Exception:
            self.perguntas_jogo = []

        self.tela_jogo()

    # tela_jogo responsiva
    def tela_jogo(self):
        self.page.clean()
        page_w = self._page_width()
        mobile = self._is_mobile()

        # criar régua (visual)
        self.labels_regua = []
        regua_controls = []
        for i in range(len(self.perguntas_jogo)):
            texto = f"{i + 1}"
            cor_fundo = (colors.BLUE_900 if colors is not None else None)
            cor_texto = (colors.WHITE if colors is not None else None)
            bolinha = ft.Container(
                content=ft.Text(texto, size=14, color=cor_texto, weight=ft.FontWeight.BOLD),
                width=36,
                height=36,
                bgcolor=cor_fundo,
                border=ft.border.all(2, (colors.YELLOW if colors is not None else None)),
                border_radius=18,
                alignment=ft.alignment.center,
                margin=ft.margin.only(right=6)
            )
            # ícone pequeno ao lado
            icon = ""
            if i + 1 in [3, 5, 8]:
                icon = "💰"
            elif i + 1 == 10:
                icon = "🏆"
            item = ft.Row([bolinha, ft.Text(icon, size=16, color=cor_texto) if icon else ft.Text("")], alignment=ft.MainAxisAlignment.CENTER, spacing=2)
            regua_controls.append(item)
            self.labels_regua.append(item)

        # pergunta (será substituída por Container depois)
        self.label_pergunta = ft.Text("", size=18, color=(colors.YELLOW if colors is not None else None), weight=ft.FontWeight.BOLD)

        # botões de alternativas
        self.botoes = []
        btn_w = int(page_w * 0.9) if mobile else 500
        for i in range(4):
            botao = ft.ElevatedButton(
                "...",
                width=btn_w,
                bgcolor=(colors.BLUE if colors is not None else None),
                color=(colors.WHITE if colors is not None else None),
                on_click=lambda e, i=i: self.verificar_resposta(i),
                style=self._btn_style
            )
            self.botoes.append(botao)

        # labels e ações
        self.label_feedback = ft.Text("", size=16, color=(colors.WHITE if colors is not None else None))
        self.label_saldo = ft.Text(f"Saldo atual: R${self.pontos}", size=16, color=(colors.CYAN if colors is not None else None))

        self.botao_ajuda = ft.ElevatedButton("Rodar Dados", bgcolor=(colors.PURPLE if colors is not None else None), color=(colors.WHITE if colors is not None else None), width=int(btn_w * 0.65), on_click=self.ajuda_dado, style=self._btn_style)
        self.botao_troca = ft.ElevatedButton("Trocar Pergunta", bgcolor=(colors.GREEN_900 if colors is not None else None), color=(colors.WHITE if colors is not None else None), width=int(btn_w * 0.65), on_click=self.trocar_pergunta, style=self._btn_style)
        self.botao_professor = ft.ElevatedButton("Ajuda dos Professores", bgcolor=(colors.ORANGE_900 if colors is not None else None), color=(colors.WHITE if colors is not None else None), width=int(btn_w * 0.65), on_click=self.ajuda_professor, style=self._btn_style)
        self.botao_desistir = ft.ElevatedButton("Desistir", bgcolor=(colors.ORANGE if colors is not None else None), color=(colors.WHITE if colors is not None else None), on_click=self.desistir, style=self._btn_style)
        self.botao_sair = ft.ElevatedButton("Sair", bgcolor=(colors.RED if colors is not None else None), color=(colors.WHITE if colors is not None else None), on_click=lambda _: self.tela_inicial(), style=self._btn_style)

        # Montagem responsiva:
        # - Desktop: pergunta + botoes à esquerda, régua à direita (side-by-side)
        # - Mobile: tudo em coluna, régua embaixo (OPÇÃO A)
        left_column = ft.Column(
            [
                ft.Container(content=self.label_pergunta, width=(int(page_w * 0.9) if mobile else 600)),
                *self.botoes,
                ft.Row([self.botao_ajuda, self.botao_troca, self.botao_professor], alignment=ft.MainAxisAlignment.CENTER, spacing=12),
                self.label_feedback,
                self.label_saldo,
                ft.Row([self.botao_desistir, self.botao_sair], alignment=ft.MainAxisAlignment.CENTER, spacing=12),
            ],
            spacing=12,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO if mobile else ft.ScrollMode.NEVER,
            expand=True,
        )

        # Régua container: no mobile será adicionada abaixo; no desktop ficará em coluna lateral
        regua_row = ft.Row(regua_controls, alignment=ft.MainAxisAlignment.CENTER, spacing=6, wrap=True)

        if mobile:
            # mobile: column com left + régua embaixo
            page_content = ft.Column(
                [
                    left_column,
                    ft.Divider(),
                    ft.Container(content=regua_row, alignment=ft.alignment.center, padding=ft.padding.all(6))
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
            self.page.add(ft.Container(content=page_content, padding=ft.padding.symmetric(8), expand=True))
        else:
            # desktop: row com left e régua à direita
            right_column = ft.Column([regua_row], alignment=ft.MainAxisAlignment.START, spacing=6)
            page_content = ft.Row([left_column, ft.Container(content=right_column, width=150)], expand=True, alignment=ft.MainAxisAlignment.CENTER)
            self.page.add(ft.Container(content=page_content, padding=ft.padding.all(12), expand=True))

        # carregar primeira pergunta / atualizar UI
        self.carregar_pergunta()

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

        if self.indice >= len(self.perguntas_jogo):
            self.vitoria()
            return

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

        # Container responsivo para a pergunta
        page_w = self._page_width()
        pergunta_container = ft.Container(
            content=ft.Text(texto_completo, size=18, color=(colors.YELLOW if colors is not None else None), weight=ft.FontWeight.BOLD, selectable=True),
            width=(int(page_w * 0.95) if self._is_mobile() else 600),
            padding=ft.padding.all(8),
        )
        self.label_pergunta = pergunta_container

        # atualizar botoes
        for i, alt in enumerate(alternativas_embaralhadas):
            try:
                self.botoes[i].text = alt
                self.botoes[i].disabled = False
            except Exception:
                pass

        try:
            self.label_feedback.value = ""
            self.label_saldo.value = f"Saldo atual: R${self.pontos}"
        except Exception:
            pass

        # atualizar cores das bolinhas da régua (se existirem)
        try:
            for i, item in enumerate(self.labels_regua):
                bolinha = item.controls[0]
                try:
                    bolinha.bgcolor = (colors.GREEN_700 if i < self.indice else (colors.YELLOW_300 if i == self.indice else colors.BLUE_900))
                    bolinha.border = ft.border.all(3, (colors.YELLOW if i == self.indice else colors.WHITE))
                    bolinha.content.color = (colors.BLACK if i == self.indice else colors.WHITE)
                except Exception:
                    pass
        except Exception:
            pass

        # forçar atualização da página
        try:
            self.page.clean()
            # reconstruir tela (reusar tela_jogo layout)
            self.tela_jogo()
        except Exception:
            try:
                self.page.update()
            except Exception:
                pass

    def trocar_pergunta(self, e=None):
        if self.troca_usada:
            return
        self.troca_usada = True
        try:
            from perguntas import facil
            perguntas_possiveis = [p for p in facil if p not in self.perguntas_jogo]
        except Exception:
            perguntas_possiveis = []
        if perguntas_possiveis:
            self.perguntas_jogo[self.indice] = random.choice(perguntas_possiveis)
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
        try:
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
        try:
            texto_ajuda = self.pergunta_atual.get("ajuda", "👨‍🏫 Pense bem antes de responder!")
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
        except Exception:
            pass

    def verificar_resposta(self, escolha):
        for botao in self.botoes:
            botao.disabled = True
        try:
            correta = self.pergunta_atual["nova_correta"]
        except Exception:
            correta = None
        if escolha == correta:
            try:
                self.musica.tocar(2)
            except Exception:
                pass
            self.pontos += 1000
            if (self.indice + 1) in [3, 5, 8]:
                self.checkpoint = self.pontos
            try:
                self.label_feedback.value = f"✅ Correto! Ganhou R$1000"
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
        await asyncio.sleep(1.2)
        self.carregar_pergunta()

    async def _delay_derrota(self):
        import asyncio
        await asyncio.sleep(0.6)
        self.derrota()

    def vitoria(self):
        self.page.clean()
        try:
            self.musica.tocar(4)
        except Exception:
            pass
        msg = ft.Text(f"🎉 Parabéns, você ganhou!\nSaiu com R${self.pontos}", size=22, color=(colors.YELLOW if colors is not None else None), weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
        botao_voltar = ft.ElevatedButton("Voltar ao início", bgcolor=(colors.BLUE if colors is not None else None), color=(colors.WHITE if colors is not None else None), on_click=lambda _: self.tela_inicial(), style=self._btn_style)
        self.page.add(ft.Container(content=ft.Column([msg, botao_voltar], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), alignment=ft.alignment.center, expand=True))

    def derrota(self):
        self.page.clean()
        try:
            self.musica.tocar(3)
        except Exception:
            pass
        msg = ft.Text(f"❌ Você perdeu!\nSaiu com R${self.checkpoint}", size=22, color=(colors.RED if colors is not None else None), weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
        botao_voltar = ft.ElevatedButton("Voltar ao início", bgcolor=(colors.BLUE if colors is not None else None), color=(colors.WHITE if colors is not None else None), on_click=lambda _: self.tela_inicial(), style=self._btn_style)
        self.page.add(ft.Container(content=ft.Column([msg, botao_voltar], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), alignment=ft.alignment.center, expand=True))

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
                msg = ft.Text(f"💰 Você desistiu!\nSaiu com R${self.pontos}", size=20, color=(colors.ORANGE if colors is not None else None), weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
                botao_voltar = ft.ElevatedButton("Voltar ao início", bgcolor=(colors.BLUE if colors is not None else None), color=(colors.WHITE if colors is not None else None), on_click=lambda _: self.tela_inicial(), style=self._btn_style)
                self.page.add(ft.Container(content=ft.Column([msg, botao_voltar], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), alignment=ft.alignment.center, expand=True))
            else:
                dlg.open = False
                try:
                    self.page.update()
                except Exception:
                    pass
                self.page.dialog = None
                if dlg in self.page.overlay:
                    self.page.overlay.remove(dlg)

        dlg = ft.AlertDialog(title=ft.Text("Desistir?"), content=ft.Text(f"Você deseja desistir e sair com R${self.pontos}?"), actions=[ft.TextButton("Sim", on_click=confirmar_dlg), ft.TextButton("Não", on_click=confirmar_dlg)])
        self.page.dialog = dlg
        try:
            if dlg not in self.page.overlay:
                self.page.overlay.append(dlg)
            dlg.open = True
            self.page.update()
        except Exception:
            pass


# --------------------------
# Entrypoint
# --------------------------
def main(page: ft.Page):
    # Ajustes iniciais responsivos
    try:
        # força avaliação inicial de window size
        page.window_width = getattr(page, "window_width", getattr(page, "width", 800))
    except Exception:
        pass

    # Ajustes de padding para mobile
    try:
        if getattr(page, "window_width", getattr(page, "width", 800)) < 600:
            page.padding = ft.padding.all(6)
    except Exception:
        pass

    ShowDoMilhao(page)


if __name__ == "__main__":
    # se estiver em ambiente com PORT (Railway) roda como web
    port = int(os.environ.get("PORT", 0) or 0)
    if port:
        ft.app(target=main, view=ft.WEB_BROWSER, port=port, host="0.0.0.0")
    else:
        # no PC local, rodar em modo APP (útil para gerar APK com flet build apk)
        ft.app(target=main, view=ft.APP)
