import tkinter as tk
from tkinter import filedialog, Label, Toplevel
from deepface import DeepFace
from PIL import Image, ImageTk

# Dicionário com caminhos das imagens de cada emoção
caminhos_imagens = {
    'angry': "imgs/anger.png",
    'disgust': "imgs/disgust.png",
    'fear': "imgs/fear.png",
    'happy': "imgs/joy.png",
    'sad': "imgs/sadness.png",
    'surprise': "imgs/surprise.png"
}

# Função para analisar a imagem do usuário
def analisar_imagem(result_label, img_label):
    file_path = filedialog.askopenfilename()  # Abre um diálogo para o usuário selecionar um arquivo de imagem.
    if not file_path:
        return
    
    analise = DeepFace.analyze(file_path, actions=['emotion'], enforce_detection=False)  # Analisa a imagem para detectar emoções

    if isinstance(analise, list) and len(analise) > 0:  # Verifica se a análise retornou uma lista com resultados.
        emotions = analise[0]['emotion']
        result_text = "\n".join([f"{emotion}: {percentage:.2f}%" for emotion, percentage in emotions.items()])
    else:
        result_text = "No face detected or analysis failed."

    result_label.config(text=result_text)  # Atualiza o rótulo na interface com os resultados das emoções.

    img = Image.open(file_path)  # Abre a imagem selecionada.
    img = img.resize((250, 250))  # Redimensiona a imagem para um tamanho adequado.
    img = ImageTk.PhotoImage(img)  # Converte a imagem para um formato exibível pelo Tkinter.
    img_label.config(image=img)  # Atualiza o rótulo da imagem na interface.
    img_label.image = img  # Mantém a referência da imagem para evitar que ela seja coletada pelo garbage collector.

# Função para abrir a janela específica da emoção
def abrir_janela_emocao(emocao):
    janela_emocao = Toplevel(root)
    janela_emocao.title(emocao.capitalize())
    janela_emocao.configure(bg='lightblue')

    # Carregar e exibir a imagem da emoção
    img_path = caminhos_imagens.get(emocao)  # Pega o caminho da imagem correspondente à emoção
    img = Image.open(img_path)
    img = img.resize((250, 250))
    img = ImageTk.PhotoImage(img)

    img_label = Label(janela_emocao, image=img)
    img_label.image = img  # Manter a referência da imagem
    img_label.pack(pady=10)

    # Texto explicando a emoção
    explicacao = {
        'angry': "A raiva é uma emoção intensa que pode surgir quando nos sentimos ameaçados, frustrados ou injustiçados.",
        'disgust': "O nojo é uma reação emocional de repulsa em resposta a algo considerado desagradável ou ofensivo.",
        'fear': "O medo é uma emoção que surge em resposta a uma ameaça percebida, preparando-nos para enfrentar o perigo.",
        'happy': "A felicidade é uma emoção positiva que sentimos quando estamos contentes, satisfeitos ou alegres.",
        'sad': "A tristeza é uma emoção negativa que ocorre em resposta a perdas, decepções ou situações dolorosas.",
        'surprise': "A surpresa é uma emoção que ocorre quando algo inesperado ou repentino acontece."
    }

    explicacao_label = Label(janela_emocao, text=explicacao.get(emocao, ""), font=("Helvetica", 12), bg='lightblue', wraplength=300)
    explicacao_label.pack(pady=10)

    # Botão para selecionar uma imagem da galeria do usuário
    result_label = Label(janela_emocao, text="", font=("Helvetica", 12), bg='lightblue')
    result_label.pack(pady=10)

    galeria_button = tk.Button(janela_emocao, text="Sua Galeria", command=lambda: analisar_imagem(result_label, img_label), bg='blue', fg='white', font=("Helvetica", 12))
    galeria_button.pack(pady=10)

    result_label.pack(pady=10)

# Função para abrir a janela de emoções
def abrir_emocoes():
    emocoes_janela = Toplevel(root)
    emocoes_janela.title("Análise de Emoções")
    emocoes_janela.configure(bg='lightblue')

    def criar_botao_emocao(emocao, row, col):
        return tk.Button(emocoes_janela, text=emocao.capitalize(), command=lambda: abrir_janela_emocao(emocao), bg='blue', fg='white', font=("Helvetica", 12)).grid(row=row, column=col, padx=10, pady=5)

    # Criar botões para cada emoção
    emocoes = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise']
    for i, emocao in enumerate(emocoes):
        criar_botao_emocao(emocao, row=2 + i // 3, col=i % 3)

# Função para abrir a janela de descobrir (em construção)
def abrir_descobrir():
    descobrir_janela = Toplevel(root)
    descobrir_janela.title("Descobrir")
    # Adicione aqui os widgets e a lógica para a funcionalidade "Descobrir"
    Label(descobrir_janela, text="Funcionalidade 'Descobrir' em construção", font=("Helvetica", 12)).pack(pady=10)

# Função para configurar a interface principal
def configurar_interface():
    global root
    root = tk.Tk()
    root.title("Menu Principal")
    root.configure(bg='lightblue')

    title_label = tk.Label(root, text="Menu Principal", font=("Helvetica", 16, "bold"), bg='lightblue')
    title_label.pack(pady=10)

    emocoes_button = tk.Button(root, text="Emoções", command=abrir_emocoes, bg='green', fg='white', font=("Helvetica", 12))
    emocoes_button.pack(pady=10)

    descobrir_button = tk.Button(root, text="Descobrir", command=abrir_descobrir, bg='orange', fg='white', font=("Helvetica", 12))
    descobrir_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    configurar_interface()
