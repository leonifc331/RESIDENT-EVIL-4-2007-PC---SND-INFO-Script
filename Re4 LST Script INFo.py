import tkinter as tk
from tkinter import filedialog
import os

def extrair_informacoes(arquivo_lst):
    progressoes = []
    progressao_atual = []

    # Abrir o arquivo .lst e extrair as informações
    with open(arquivo_lst, 'r') as f:
        for linha in f:
            if linha.strip().startswith('//'):  # Início de uma nova progressão
                if progressao_atual:  # Adicionar a progressão atual à lista de progressões
                    progressoes.append(progressao_atual)
                progressao_atual = []  # Reiniciar a progressão atual
                # Obter o nome da progressão (sem os caracteres //)
                nome_progressao = linha.strip().replace('//', '').split('(')[1].split(')')[0].strip()
                progressao_atual.append(nome_progressao)
            elif linha.strip() == '0,-1':  # Fim do arquivo .lst
                break
            elif progressao_atual and '"' in linha:  # Se houver aspas na linha, adicionar o nome à progressão atual
                nome = linha.strip().split('"')[1]
                progressao_atual.append(nome)

    # Verificar se as informações foram extraídas corretamente
    for i, progressao in enumerate(progressoes):
        print(f"Progressão ID {i}: {progressao[0]}")
        for j, nome in enumerate(progressao[1:], start=12):
            print(f"SND audio ID {j}: {nome}")
        print()  # Pular uma linha entre cada progressão

    # Salvar as informações extraídas no arquivo de texto
    nome_arquivo_saida = os.path.splitext(arquivo_lst)[0] + "_Info.txt"
    with open(nome_arquivo_saida, "w") as output_file:
        for i, progressao in enumerate(progressoes):
            output_file.write(f"Progressão ID {i}: {progressao[0]}\n")
            for j, nome in enumerate(progressao[1:], start=12):
                output_file.write(f"SND audio ID {j}: {nome}\n")
            output_file.write("\n")  # Pular uma linha entre cada progressão

    return nome_arquivo_saida

def processar_arquivo():
    arquivo = filedialog.askopenfilename(filetypes=[("Arquivos lst", "*.lst")])
    if arquivo:
        arquivo_saida = extrair_informacoes(arquivo)
        if os.path.isfile(arquivo_saida):
            tk.messagebox.showinfo("Concluído", f"As informações foram extraídas com sucesso para o arquivo {arquivo_saida}")
        else:
            tk.messagebox.showwarning("Aviso", "O arquivo de saída está vazio.")

# Interface gráfica
root = tk.Tk()
root.title("RESIDENT EVIL 4 2007 PC - LST Script Info")

button = tk.Button(root, text="Selecionar Arquivo .lst", command=processar_arquivo)
button.pack(pady=20)

root.mainloop()
