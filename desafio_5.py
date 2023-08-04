import PyPDF2
import os
import docx2txt
import tkinter as tk
from tkinter import filedialog, messagebox

def criptografar_cesar(texto, chave):
    texto_criptografado = ''
    for caractere in texto:
        if caractere.isalpha():
            base = ord('a') if caractere.islower() else ord('A')
            indice_caractere = ord(caractere) - base
            novo_indice = (indice_caractere + chave) % 26
            novo_caractere = chr(base + novo_indice)
            texto_criptografado += novo_caractere
        else:
            texto_criptografado += caractere
    return texto_criptografado

def descriptografar_cesar(texto, chave):
    texto_descriptografado = criptografar_cesar(texto, -chave)
    return texto_descriptografado

def ler_arquivo_txt(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        return arquivo.read()

def escrever_arquivo_txt(caminho_arquivo, conteudo):
    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write(conteudo)

def ler_arquivo_pdf(caminho_arquivo):
    texto = ''
    with open(caminho_arquivo, 'rb') as arquivo:
        leitor_pdf = PyPDF2.PdfFileReader(arquivo)
        num_paginas = leitor_pdf.numPages
        for pagina_num in range(num_paginas):
            pagina = leitor_pdf.getPage(pagina_num)
            texto += pagina.extractText()
    return texto

def ler_arquivo_docx(caminho_arquivo):
    texto = docx2txt.process(caminho_arquivo)
    return texto

def listar_chaves_possiveis():
    chaves_possiveis = "\n".join([str(chave) for chave in range(1, 26)])
    messagebox.showinfo("Chaves Possíveis", f"Chaves possíveis para a criptografia de César:\n{chaves_possiveis}")

def carregar_arquivo():
    caminho_arquivo = filedialog.askopenfilename()
    if caminho_arquivo:
        entry_caminho_arquivo.delete(0, tk.END)
        entry_caminho_arquivo.insert(0, caminho_arquivo)

def criptografar_arquivo():
    caminho_arquivo = entry_caminho_arquivo.get()
    extensao_arquivo = os.path.splitext(caminho_arquivo)[1].lower()

    if not os.path.exists(caminho_arquivo):
        messagebox.showerror("Erro", "O arquivo selecionado não existe.")
        return

    chave = int(entry_chave.get())

    try:
        if extensao_arquivo == ".txt":
            texto_original = ler_arquivo_txt(caminho_arquivo)
        elif extensao_arquivo == ".pdf":
            texto_original = ler_arquivo_pdf(caminho_arquivo)
        elif extensao_arquivo == ".docx":
            texto_original = ler_arquivo_docx(caminho_arquivo)
        else:
            messagebox.showerror("Erro", "Extensão de arquivo não suportada.")
            return

        texto_criptografado = criptografar_cesar(texto_original, chave)

        caminho_arquivo_criptografado = caminho_arquivo + ".criptografado.txt"
        escrever_arquivo_txt(caminho_arquivo_criptografado, texto_criptografado)

        messagebox.showinfo("Sucesso", "Texto criptografado e salvo em:\n" + caminho_arquivo_criptografado)

    except Exception as e:
        messagebox.showerror("Erro", str(e))

def descriptografar_arquivo():
    caminho_arquivo = entry_caminho_arquivo.get()
    extensao_arquivo = os.path.splitext(caminho_arquivo)[1].lower()

    if not os.path.exists(caminho_arquivo):
        messagebox.showerror("Erro", "O arquivo selecionado não existe.")
        return

    chave = int(entry_chave.get())

    try:
        if extensao_arquivo == ".txt":
            texto_criptografado = ler_arquivo_txt(caminho_arquivo)
        elif extensao_arquivo == ".pdf":
            texto_criptografado = ler_arquivo_pdf(caminho_arquivo)
        elif extensao_arquivo == ".docx":
            texto_criptografado = ler_arquivo_docx(caminho_arquivo)
        else:
            messagebox.showerror("Erro", "Extensão de arquivo não suportada.")
            return

        texto_descriptografado = descriptografar_cesar(texto_criptografado, chave)

        caminho_arquivo_descriptografado = caminho_arquivo + ".descriptografado.txt"
        escrever_arquivo_txt(caminho_arquivo_descriptografado, texto_descriptografado)

        messagebox.showinfo("Sucesso", "Texto descriptografado e salvo em:\n" + caminho_arquivo_descriptografado)

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Configuração da janela
janela = tk.Tk()
janela.title("Criptografia de César")

# Labels e entradas
label_instrucao = tk.Label(janela, text="Selecione o arquivo a ser criptografado:")
label_instrucao.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

entry_caminho_arquivo = tk.Entry(janela)
entry_caminho_arquivo.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
botao_carregar_arquivo = tk.Button(janela, text="Carregar Arquivo", command=carregar_arquivo)
botao_carregar_arquivo.grid(row=1, column=2, padx=5, pady=5)

label_chave = tk.Label(janela, text="Chave:")
label_chave.grid(row=2, column=0, padx=5, pady=5)
entry_chave = tk.Entry(janela)
entry_chave.grid(row=2, column=1, padx=5, pady=5)

botao_criptografar = tk.Button(janela, text="Criptografar", command=criptografar_arquivo)
botao_criptografar.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

# Botão para descriptografar
botao_descriptografar = tk.Button(janela, text="Descriptografar", command=descriptografar_arquivo)
botao_descriptografar.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

# Botão para listar chaves possíveis
botao_listar_chaves = tk.Button(janela, text="Listar Chaves Possíveis", command=listar_chaves_possiveis)
botao_listar_chaves.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

# Inicia a interface
janela.mainloop()

