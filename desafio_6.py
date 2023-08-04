import itertools
import tkinter as tk
from tkinter import messagebox


def distancia(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def calcular_distancia_rota(rota, cidades):
    distancia_total = 0
    for i in range(len(rota) - 1):
        distancia_total += distancia(cidades[rota[i]], cidades[rota[i + 1]])
    distancia_total += distancia(cidades[rota[-1]], cidades[rota[0]])
    return distancia_total


def caixeiro_viajante_forca_bruta(cidades):
    num_cidades = len(cidades)
    melhor_rota = None
    menor_distancia = float('inf')

    for permutacao in itertools.permutations(range(num_cidades)):
        distancia_atual = calcular_distancia_rota(permutacao, cidades)
        if distancia_atual < menor_distancia:
            menor_distancia = distancia_atual
            melhor_rota = permutacao

    return melhor_rota, menor_distancia


def resolver_caixeiro_viajante():
    cidades = []
    for entry_box in entry_boxes:
        x, y = entry_box[0].get(), entry_box[1].get()
        if x and y:
            try:
                x, y = float(x), float(y)
                cidades.append((x, y))
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira números válidos para as coordenadas.")
                return
        else:
            messagebox.showerror("Erro", "Por favor, preencha todas as coordenadas.")
            return

    if len(cidades) < 2:
        messagebox.showerror("Erro", "Insira pelo menos duas cidades.")
        return

    melhor_rota, menor_distancia = caixeiro_viajante_forca_bruta(cidades)

    resultado_label.config(text=f"Melhor rota: {melhor_rota}\nMenor distância: {menor_distancia:.2f}")


# Criar a janela
root = tk.Tk()
root.title("Problema do Caixeiro Viajante")

# Instruções
instrucoes_label = tk.Label(root, text="Insira as coordenadas das cidades (X e Y) e clique em 'Resolver':")
instrucoes_label.pack(pady=10)

# Criar caixas de entrada para coordenadas das cidades
entry_boxes = []
for i in range(5):  # Altere para o número de cidades desejado
    entry_frame = tk.Frame(root)
    entry_frame.pack()

    lbl = tk.Label(entry_frame, text=f"Cidade {i + 1}:")
    lbl.pack(side="left")

    entry_x = tk.Entry(entry_frame, width=10)
    entry_x.pack(side="left")

    entry_y = tk.Entry(entry_frame, width=10)
    entry_y.pack(side="left", padx=5)

    entry_boxes.append((entry_x, entry_y))

# Botão para resolver o problema
resolver_button = tk.Button(root, text="Resolver", command=resolver_caixeiro_viajante)
resolver_button.pack(pady=10)

# Rótulo para exibir o resultado
resultado_label = tk.Label(root, text="", justify="left")
resultado_label.pack()

root.mainloop()
