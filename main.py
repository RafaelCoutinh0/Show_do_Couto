import tkinter as tk
import random
from tkinter import messagebox
from perguntas import facil, media, dificil

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

        self.tela_inicial()

    def tela_inicial(self):
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
        # Reset
        self.pontos = 0
        self.checkpoint = 0
        self.indice = 0

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
        if self.indice < len(self.perguntas_jogo):
            self.pergunta_atual = self.perguntas_jogo[self.indice]
            self.label_pergunta.config(text=self.pergunta_atual["pergunta"])
            for i, alt in enumerate(self.pergunta_atual["alternativas"]):
                self.botoes[i].config(text=alt, state="normal")
            self.label_feedback.config(text="")

            # Atualiza a régua
            for i, lbl in enumerate(self.labels_regua):
                if i == self.indice:
                    lbl.config(fg="yellow")
                else:
                    lbl.config(fg="white")
        else:
            self.vitoria()

    def verificar_resposta(self, escolha):
        for botao in self.botoes:
            botao.config(state="disabled")

        correta = self.pergunta_atual["correta"]
        if escolha == correta:
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
        msg = tk.Label(self.root, text=f"🎉 Parabéns, você ganhou!\nSaiu com R${self.pontos}",
                       font=("Arial", 18, "bold"), fg="yellow", bg="#002e5c")
        msg.pack(pady=100)
        botao_voltar = tk.Button(self.root, text="Voltar ao início", font=("Arial", 14),
                                 bg="blue", fg="white", command=self.tela_inicial)
        botao_voltar.pack(pady=20)

    def derrota(self):
        self.limpar_tela()
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
