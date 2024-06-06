import tkinter as tk
from tkinter import filedialog, Label, Toplevel
from deepface import DeepFace
from PIL import Image, ImageTk

def analisar_imagem(emocao):
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

def abrir_emocoes():
    emocoes_janela = Toplevel(root)
    emocoes_janela.title("Análise de Emoções")
    emocoes_janela.configure(bg='lightblue')

    global img_label
    img_label = Label(emocoes_janela)
    img_label.pack(pady=10)

    global result_label
    result_label = tk.Label(emocoes_janela, text="", font=("Helvetica", 12), bg='lightblue')
    result_label.pack(pady=10)

    def criar_botao_emocao(emocao):
        return tk.Button(emocoes_janela, text=emocao.capitalize(), command=lambda: analisar_imagem(emocao), bg='blue', fg='white', font=("Helvetica", 12))

    # Criar botões para cada emoção
    emocoes = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise']
    for emocao in emocoes:
        criar_botao_emocao(emocao).pack(pady=5)

def abrir_descobrir():
    descobrir_janela = Toplevel(root)
    descobrir_janela.title("Descobrir")
    # Adicione aqui os widgets e a lógica para a funcionalidade "Descobrir"
    Label(descobrir_janela, text="Funcionalidade 'Descobrir' em construção", font=("Helvetica", 12)).pack(pady=10)

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
