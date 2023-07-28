import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from collections import Counter
import docx2txt
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import string
from unidecode import unidecode

nltk.download('stopwords')
stop_words = set(stopwords.words('portuguese'))

file_loaded = False  # Variável de controle para indicar se o arquivo foi carregado


def read_file_and_create_word_list():
    global file_loaded
    file_path = filedialog.askopenfilename(filetypes=[("Arquivos de texto", "*.txt;*.docx")])

    if file_path:
        if file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
                word_list = process_text(text)
        elif file_path.endswith(".docx"):
            text = docx2txt.process(file_path)
            word_list = process_text(text)
        else:
            print("Formato de arquivo não suportado.")
            return

        # Remover as stop words
        word_list = [word for word in word_list if word.lower() not in stop_words]

        create_word_frequency_chart(word_list)
        create_word_cloud(word_list)

        file_loaded = True  # Atualiza o estado da variável após o arquivo ser carregado
        update_info_label()


def process_text(text):
    # Converter todas as palavras para minúsculas e remover acentuações
    text = unidecode(text.lower())

    # Substituir 'ç' por 'c'
    text = text.replace("ç", "c")

    # Remover pontuação e outros caracteres não alfanuméricos
    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator)

    # Criar a lista de palavras
    word_list = text.split()

    return word_list


def create_word_frequency_chart(word_list):
    counter = Counter(word_list)
    most_common_words = counter.most_common(10)  # Exibir as 10 palavras mais frequentes

    words, frequencies = zip(*most_common_words)

    plt.figure(figsize=(10, 6))
    plt.bar(words, frequencies)
    plt.xlabel("Palavras")
    plt.ylabel("Frequência")
    plt.title("Palavras mais frequentes")
    plt.xticks(rotation=45)

    # Adicionar os valores de frequência acima das barras
    for i, v in enumerate(frequencies):
        plt.text(i, v, str(v), ha="center", va="bottom", fontsize=10, fontweight="bold")

    plt.tight_layout()

    # Salvar o gráfico em uma imagem temporária
    plt.savefig("word_frequency_chart.png")


def create_word_cloud(word_list):
    word_freq = Counter(word_list)
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_freq)

    plt.figure(figsize=(8, 4))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Nuvem de Palavras")
    plt.tight_layout()

    # Salvar a nuvem de palavras em uma imagem temporária
    plt.savefig("word_cloud.png")


def show_frequency_chart():
    if file_loaded:
        # Criar nova janela para exibir o gráfico
        window = tk.Toplevel(root)
        window.title("Gráfico de Frequência de Palavras")
        window.geometry("600x400")

        # Carregar a imagem do gráfico no canvas
        img = tk.PhotoImage(file="word_frequency_chart.png")
        canvas = tk.Canvas(window, width=600, height=400)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(0, 0, anchor=tk.NW, image=img)
        canvas.img = img
    else:
        print("Nenhum arquivo carregado.")


def show_word_cloud():
    if file_loaded:
        # Criar nova janela para exibir a nuvem de palavras
        window = tk.Toplevel(root)
        window.title("Nuvem de Palavras")
        window.geometry("800x400")

        # Carregar a imagem da nuvem de palavras no canvas
        img = tk.PhotoImage(file="word_cloud.png")
        canvas = tk.Canvas(window, width=800, height=400)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(0, 0, anchor=tk.NW, image=img)
        canvas.img = img
    else:
        print("Nenhum arquivo carregado.")


def update_info_label():
    if file_loaded:
        info_label.config(text="Arquivo carregado.")
        show_chart_button.config(state=tk.NORMAL)
        show_cloud_button.config(state=tk.NORMAL)
    else:
        info_label.config(text="Nenhum arquivo carregado.")
        show_chart_button.config(state=tk.DISABLED)
        show_cloud_button.config(state=tk.DISABLED)


root = tk.Tk()
root.title("Leitor de Arquivo de Texto")
root.geometry("400x250")

info_label = tk.Label(root, text="Nenhum arquivo carregado.", pady=10)
info_label.pack()

open_button = tk.Button(root, text="Abrir Arquivo", command=read_file_and_create_word_list)
open_button.pack(pady=10)

show_chart_button = tk.Button(root, text="Mostrar Gráfico de Frequência", command=show_frequency_chart,
                              state=tk.DISABLED)
show_chart_button.pack(pady=5)

show_cloud_button = tk.Button(root, text="Mostrar Nuvem de Palavras", command=show_word_cloud, state=tk.DISABLED)
show_cloud_button.pack(pady=5)

root.mainloop()

