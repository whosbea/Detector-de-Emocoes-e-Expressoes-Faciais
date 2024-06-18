import tkinter as tk
from tkinter import filedialog, Label, Toplevel, Button
from deepface import DeepFace
from PIL import Image, ImageTk
import cv2

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
def analisar_imagem(result_label, img_label, escolha_janela):
    file_path = filedialog.askopenfilename()  # Abre um diálogo para o usuário selecionar um arquivo de imagem.
    escolha_janela.destroy()  # Fecha a janela de "Escolhendo Imagem"
    if not file_path:
        return

    # Exibir janela de "Analisando Imagem"
    analisando_janela = Toplevel(root)
    analisando_janela.title("Analisando Imagem")
    analisando_janela.configure(bg='lightblue')
    analisando_label = Label(analisando_janela, text="Analisando imagem...", font=("Helvetica", 16), bg='lightblue')
    analisando_label.pack(pady=20)

    root.update()  # Atualiza a interface para exibir a janela de "Analisando Imagem"

    analise = DeepFace.analyze(file_path, actions=['emotion'], enforce_detection=False)  # Analisa a imagem para detectar emoções
    analisando_janela.destroy()  # Fecha a janela de "Analisando Imagem"

    # Exibir resultados
    resultado_janela = Toplevel(root)
    resultado_janela.title("Resultado da Análise")
    resultado_janela.configure(bg='lightblue')

    if isinstance(analise, list) and len(analise) > 0:  # Verifica se a análise retornou uma lista com resultados.
        emotions = analise[0]['emotion']
        result_text = "\n".join([f"{emotion}: {percentage:.2f}%" for emotion, percentage in emotions.items()])
    else:
        result_text = "No face detected or analysis failed."

    result_label = Label(resultado_janela, text=result_text, font=("Helvetica", 12), bg='lightblue')
    result_label.pack(pady=10)

    img = Image.open(file_path)  # Abre a imagem selecionada.
    img = img.resize((250, 250))  # Redimensiona a imagem para um tamanho adequado.
    img = ImageTk.PhotoImage(img)  # Converte a imagem para um formato exibível pelo Tkinter.
    img_label = Label(resultado_janela, image=img)  # Cria um rótulo de imagem
    img_label.image = img  # Mantém a referência da imagem para evitar que ela seja coletada pelo garbage collector.
    img_label.pack(pady=10)


# Função para detectar expressão facial dominante em um quadro
def detect_face_expression(frame):
    try:
        result = DeepFace.analyze(frame, actions=['emotion'])
        dominant_expression = max(result[0]['emotion'].items(), key=lambda x: x[1])
        return dominant_expression[0], result[0]['region']
    except Exception as e:
        print("Erro ao detectar rosto:", e)
        return None, None

# Função para análise em tempo real usando webcam
def analisar_webcam_tempo_real():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro: Não foi possível abrir a webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Redimensionamento do frame para acelerar o processo de análise
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Detecção da expressão facial dominante no frame
        expression, region = detect_face_expression(frame)

        # Se nenhuma expressão for detectada, continue para o próximo quadro
        if expression is None:
            continue

        # Exibição da expressão facial dominante no console
        print("Expressão Facial Dominante:", expression)

        # Desenhar um retângulo ao redor do rosto detectado
        if region:
            x, y, w, h = region['x'], region['y'], region['w'], region['h']
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, expression, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 128, 255), 1)

        # Exibição do frame com a expressão facial destacada
        cv2.imshow('Facial Expression Recognition', frame)

        # Verificação da tecla 'q' para sair do loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberação da webcam e fechamento das janelas
    cap.release()
    cv2.destroyAllWindows()

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

    galeria_button = tk.Button(janela_emocao, text="Sua Galeria", command=lambda: analisar_imagem(result_label, img_label, janela_emocao), bg='blue', fg='white', font=("Helvetica", 12))
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
        criar_botao_emocao(emocao, row=i // 3, col=i % 3)

# Função para abrir a janela de descobrir
def abrir_descobrir():
    descobrir_janela = Toplevel(root)
    descobrir_janela.title("Descobrir")
    descobrir_janela.configure(bg='lightblue')

    analyze_button = tk.Button(descobrir_janela, text="Analisar Imagem", command=lambda: abrir_chooser_window(descobrir_janela), bg='blue', fg='white', font=("Helvetica", 12))
    analyze_button.pack(pady=20)

    camera_button = tk.Button(descobrir_janela, text="Camera", command=analisar_webcam_tempo_real, bg='blue', fg='white', font=("Helvetica", 12))
    camera_button.pack(pady=20)

def abrir_chooser_window(parent_window):
    # Fecha a janela de "Descobrir"
    parent_window.destroy()

    # Exibir janela de "Escolhendo Imagem"
    escolha_janela = Toplevel(root)
    escolha_janela.title("Escolhendo Imagem")
    escolha_janela.configure(bg='lightblue')
    escolha_label = Label(escolha_janela, text="Escolhendo imagem...", font=("Helvetica", 16), bg='lightblue')
    escolha_label.pack(pady=20)

    # Chamar a função para analisar a imagem
    analisar_imagem(None, None, escolha_janela)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Aplicativo de Emoções")
    root.configure(bg='lightblue')

    emocoes_button = tk.Button(root, text="Emoções", command=abrir_emocoes, bg='blue', fg='white', font=("Helvetica", 14))
    emocoes_button.pack(pady=20)

    descobrir_button = tk.Button(root, text="Descobrir", command=abrir_descobrir, bg='blue', fg='white', font=("Helvetica", 14))
    descobrir_button.pack(pady=20)

    root.mainloop()
