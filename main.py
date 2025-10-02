import tkinter as tk
import random
from tkinter import messagebox
from perguntas import facil, media, dificil
import pygame


def tocar_musica(i = 0):
    pygame.mixer.init()
    musicas = ["musics/music_game.mp3", "musics/pergunta1.mp3", "musics/acerto.mp3", "musics/lose.mp3",
               "musics/win.mp3"]
    pygame.mixer.music.load(musicas[i])
    if i == 3 or i == 4:
        pygame.mixer.music.play(0)
    else:
        pygame.mixer.music.play(-1)  # -1 para repetir para sempre, ou 0 para tocar uma vez    def tocar_musica():
class ShowDoMilhao:
    def __init__(self, root):
        self.root = root
        self.root.title("Show do Coutão")
        self.root.geometry("700x700")
        self.root.configure(bg="#002e5c")
        # Variáveis do jogo
        self.pontos = 0
        self.checkpoint = 0
        self.perguntas_jogo = []
        self.pergunta_atual = None
        self.indice = 0
        self.ajuda_usada = False  # controla uso do dado
        self.troca_usada = False  # controla uso da troca de pergunta
        self.ajuda_professor_usada = False  # controla uso da ajuda dos professores

        self.tela_inicial()

    def tela_inicial(self):
        tocar_musica()
        self.limpar_tela()
        self.logo = tk.PhotoImage(file="logo.png")
        self.logo = self.logo.subsample(2, 2)  # divide largura e altura por 2
        img_label = tk.Label(self.root, image=self.logo, bg="#002e5c")
        img_label.pack(pady=10)

        # Cria um frame para agrupar os botões
        frame_botoes = tk.Frame(self.root, bg="#002e5c")
        frame_botoes.pack(pady=10)

        botao_jogar = tk.Button(frame_botoes, text="Jogar", font=("Arial", 16),
                                width=15, bg="blue", fg="white",
                                command=self.iniciar_jogo)
        botao_jogar.pack(side="left", padx=10)

        botao_sair = tk.Button(frame_botoes, text="Sair", font=("Arial", 16),
                               width=15, bg="red", fg="white",
                               command=self.root.destroy)
        botao_sair.pack(side="left", padx=10)

    def iniciar_jogo(self):
        tocar_musica(i = 1)
        # Reset
        self.pontos = 0
        self.checkpoint = 0
        self.indice = 0
        self.ajuda_usada = False
        self.troca_usada = False
        self.ajuda_professor_usada = False

        # Perguntas (3 fáceis, 4 médias, 3 difíceis)
        self.perguntas_jogo = random.sample(facil, 10)
        # self.perguntas_jogo = random.sample(facil, 3) + random.sample(media, 4) + random.sample(dificil, 3)

        self.limpar_tela()

        # Frame principal (perguntas e alternativas)
        frame_jogo = tk.Frame(self.root, bg="#002e5c")
        frame_jogo.pack(side="left", fill="both", expand=True)

        # Frame lateral da régua
        frame_regua = tk.Frame(self.root, bg="#002e5c")
        frame_regua.pack(side="right", fill="y", padx=10)

        # Labels da régua
        self.labels_regua = []
        for i in range(len(self.perguntas_jogo)):
            texto = f"{i + 1}"
            if i + 1 in [3, 5, 8]:  # checkpoints
                texto += " 💰"
            elif i + 1 == 10:
                texto += " 🏆"
            else:
                texto += "     "
            lbl = tk.Label(frame_regua, text=texto, font=("Arial", 12, "bold"),
                           fg="white", bg="#002e5c")

            lbl.pack(pady=3)
            self.labels_regua.append(lbl)

        # Pergunta
        self.label_pergunta = tk.Label(frame_jogo, text="", font=("Arial", 16, "bold"),
                                       wraplength=500, fg="yellow", bg="#002e5c")
        self.label_pergunta.pack(pady=10)

        # Botões de alternativas
        self.botoes = []
        for i in range(4):
            botao = tk.Button(frame_jogo, text="", font=("Arial", 14),
                              width=50, bg="blue", fg="white",
                              command=lambda i=i: self.verificar_resposta(i))
            botao.pack(pady=5)
            self.botoes.append(botao)

        # Botões de ajuda: Dado, Trocar Pergunta e Ajuda dos Professores (lado a lado)
        frame_ajuda = tk.Frame(frame_jogo, bg="#002e5c")
        frame_ajuda.pack(pady=5)

        self.botao_ajuda = tk.Button(frame_ajuda, text="Rodar Dados", font=("Arial", 12),
                                     width=12, bg="purple", fg="white",
                                     command=self.ajuda_dado)
        self.botao_ajuda.pack(side="left", padx=5)

        self.botao_troca = tk.Button(frame_ajuda, text="Trocar Pergunta", font=("Arial", 12),
                                     width=15, bg="darkgreen", fg="white",
                                     command=self.trocar_pergunta)
        self.botao_troca.pack(side="left", padx=5)

        self.botao_professor = tk.Button(frame_ajuda, text="Ajuda dos Professores", font=("Arial", 12),
                                         width=18, bg="darkorange", fg="white",
                                         command=self.ajuda_professor)
        self.botao_professor.pack(side="left", padx=5)

        # Feedback
        self.label_feedback = tk.Label(frame_jogo, text="", font=("Arial", 14, "bold"),
                                       fg="white", bg="#002e5c")
        self.label_feedback.pack(pady=5)

        # Saldo
        self.label_saldo = tk.Label(frame_jogo, text=f"Saldo atual: R${self.pontos}",
                                    font=("Arial", 14, "bold"),
                                    fg="cyan", bg="#002e5c")
        self.label_saldo.pack(pady=5)

        # Botões Desistir/Sair
        frame_botoes = tk.Frame(frame_jogo, bg="#002e5c")
        frame_botoes.pack(pady=15)

        self.botao_desistir = tk.Button(frame_botoes, text="Desistir", font=("Arial", 12),
                                        width=12, bg="orange", fg="white",
                                        command=self.desistir)
        self.botao_desistir.pack(side="left", padx=10)

        self.botao_sair = tk.Button(frame_botoes, text="Sair", font=("Arial", 12),
                                    width=12, bg="red", fg="white",
                                    command=self.sair_do_jogo)
        self.botao_sair.pack(side="left", padx=10)

        self.carregar_pergunta()

    def carregar_pergunta(self):
        tocar_musica(1)
        if self.indice < len(self.perguntas_jogo):
            self.pergunta_atual = self.perguntas_jogo[self.indice]

            # Copia alternativas e índice correto
            alternativas = self.pergunta_atual["alternativas"][:]
            correta = self.pergunta_atual["correta"]

            # Cria pares (alternativa, índice_original)
            alternativas_com_indices = list(enumerate(alternativas))
            random.shuffle(alternativas_com_indices)  # embaralha os pares

            # Monta lista embaralhada e acha novo índice da resposta correta
            alternativas_embaralhadas = [alt for idx, alt in alternativas_com_indices]
            nova_correta = [idx for idx, alt in alternativas_com_indices].index(correta)

            # Salva no objeto para verificação posterior
            self.pergunta_atual["alternativas_embaralhadas"] = alternativas_embaralhadas
            self.pergunta_atual["nova_correta"] = nova_correta

            self.label_pergunta.config(text=self.pergunta_atual["pergunta"])
            for i, alt in enumerate(alternativas_embaralhadas):
                self.botoes[i].config(text=alt, state="normal")
            self.label_feedback.config(text="")

            # Atualiza a régua
            for i, lbl in enumerate(self.labels_regua):
                lbl.config(fg="yellow" if i == self.indice else "white")
        else:
            self.vitoria()

    def trocar_pergunta(self):
        if self.troca_usada:
            return
        self.troca_usada = True
        self.botao_troca.config(state="disabled")

        # Gera uma nova pergunta aleatória que não está nas perguntas já usadas
        perguntas_possiveis = [p for p in facil if p not in self.perguntas_jogo]
        # Se quiser incluir media/dificil, adicione aqui
        if perguntas_possiveis:
            nova_pergunta = random.choice(perguntas_possiveis)
            self.perguntas_jogo[self.indice] = nova_pergunta
            self.label_feedback.config(
                text="🔄 Pergunta trocada!",
                fg="darkgreen"
            )
            self.carregar_pergunta()
        else:
            self.label_feedback.config(
                text="Não há perguntas disponíveis para troca.",
                fg="red"
            )

    def ajuda_dado(self):
        if self.ajuda_usada:
            return
        self.ajuda_usada = True
        self.botao_ajuda.config(state="disabled")

        correta = self.pergunta_atual["nova_correta"]
        alternativas_restantes = [i for i in range(4) if i != correta and self.botoes[i]['state'] == "normal"]

        qtd_eliminar = min(random.randint(1, 3), len(alternativas_restantes))
        eliminar = random.sample(alternativas_restantes, qtd_eliminar)

        for i in eliminar:
            self.botoes[i].config(state="disabled", text="")  # Remove texto da alternativa

        self.label_feedback.config(
            text=f"🎲 Dado rolado: {qtd_eliminar} alternativas eliminadas.",
            fg="purple"
        )

    def ajuda_professor(self):
        if self.ajuda_professor_usada:
            return
        self.ajuda_professor_usada = True
        self.botao_professor.config(state="disabled")
        self.label_feedback.config(
            text="👨‍🏫 Os professores sugerem que você pense bem antes de responder!",
            fg="orange"
        )

    def verificar_resposta(self, escolha):
        for botao in self.botoes:
            botao.config(state="disabled")

        correta = self.pergunta_atual["nova_correta"]
        if escolha == correta:
            tocar_musica(2)  # toca som de vitória
            self.pontos += 1000
            if (self.indice + 1) in [3, 5, 8]:  # checkpoints após pergunta 3, 5 e 8
                self.checkpoint = self.pontos
            self.label_feedback.config(text=f"✅ Correto! Ganhou R$1000", fg="green")
            self.label_saldo.config(text=f"Saldo atual: R${self.pontos}")
            self.indice += 1
            self.root.after(1500, self.carregar_pergunta)
        else:
            self.root.after(500, self.derrota)

    def vitoria(self):
        self.limpar_tela()
        tocar_musica(4)  # toca som de vitória
        msg = tk.Label(self.root, text=f"🎉 Parabéns, você ganhou!\nSaiu com R${self.pontos}",
                       font=("Arial", 18, "bold"), fg="yellow", bg="#002e5c")
        msg.pack(pady=100)
        botao_voltar = tk.Button(self.root, text="Voltar ao início", font=("Arial", 14),
                                 bg="blue", fg="white", command=self.tela_inicial)
        botao_voltar.pack(pady=20)

    def derrota(self):
        self.limpar_tela()
        tocar_musica(3)
        msg = tk.Label(self.root, text=f"❌ Você perdeu!\nSaiu com R${self.checkpoint}",
                       font=("Arial", 18, "bold"), fg="red", bg="#002e5c")
        msg.pack(pady=100)
        botao_voltar = tk.Button(self.root, text="Voltar ao início", font=("Arial", 14),
                                 bg="blue", fg="white", command=self.tela_inicial)
        botao_voltar.pack(pady=20)

    def desistir(self):
        confirmar = messagebox.askyesno("Desistir?", f"Você deseja desistir e sair com R${self.pontos}?")
        if confirmar:
            self.limpar_tela()
            msg = tk.Label(self.root, text=f"💰 Você desistiu!\nSaiu com R${self.pontos}",
                           font=("Arial", 18, "bold"), fg="orange", bg="#002e5c")
            msg.pack(pady=100)
            botao_voltar = tk.Button(self.root, text="Voltar ao início", font=("Arial", 14),
                                     bg="blue", fg="white", command=self.tela_inicial)
            botao_voltar.pack(pady=20)

    def sair_do_jogo(self):
        self.tela_inicial()

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ShowDoMilhao(root)
    root.mainloop()
