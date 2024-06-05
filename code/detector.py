import tkinter as tk
from tkinter import filedialog, Label
from deepface import DeepFace
from PIL import Image, ImageTk

def analyze_image():
    
    file_path = filedialog.askopenfilename() #Abre um diálogo para o usuário selecionar um arquivo de imagem.
    if not file_path:
        return

  
    analysis = DeepFace.analyze(file_path, actions=['emotion'], enforce_detection=False) #Analisa a imagem para detectar emoções


    if isinstance(analysis, list) and len(analysis) > 0: #Verifica se a análise retornou uma lista com resultados.
        emotions = analysis[0]['emotion']
        result_text = "\n".join([f"{emotion}: {percentage:.2f}%" for emotion, percentage in emotions.items()])
    else:
        result_text = "No face detected or analysis failed."

    result_label.config(text=result_text) #Atualiza o rótulo na interface com os resultados das emoções.


    img = Image.open(file_path) #Abre a imagem selecionada.
    img = img.resize((250, 250)) #Redimensiona a imagem para um tamanho adequado.
    img = ImageTk.PhotoImage(img) #Converte a imagem para um formato exibível pelo Tkinter.
    img_label.config(image=img) #Atualiza o rótulo da imagem na interface.
    img_label.image = img #Mantém a referência da imagem para evitar que ela seja coletada pelo garbage collector.


#configuração da interface
root = tk.Tk()
root.title("Análise de Expressões Faciais")

analyze_button = tk.Button(root, text="Analisar Imagem", command=analyze_image) #Cria um botão que chama a função 
analyze_button.pack()

img_label = Label(root)
img_label.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
