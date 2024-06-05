import tkinter as tk
from tkinter import filedialog, Label
from deepface import DeepFace
from PIL import Image, ImageTk

def analyze_image():
    # Carrega uma imagem usando um diálogo de arquivo
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    # Analisa a imagem para detectar emoções
    analysis = DeepFace.analyze(file_path, actions=['emotion'], enforce_detection=False)

    # Mostra os resultados na interface
    if isinstance(analysis, list) and len(analysis) > 0:
        emotions = analysis[0]['emotion']
        result_text = "\n".join([f"{emotion}: {percentage:.2f}%" for emotion, percentage in emotions.items()])
    else:
        result_text = "No face detected or analysis failed."

    result_label.config(text=result_text)

    # Mostra a imagem na interface
    img = Image.open(file_path)
    img = img.resize((250, 250))
    img = ImageTk.PhotoImage(img)
    img_label.config(image=img)
    img_label.image = img

# Configura a interface
root = tk.Tk()
root.title("Análise de Expressões Faciais")

analyze_button = tk.Button(root, text="Analisar Imagem", command=analyze_image)
analyze_button.pack()

img_label = Label(root)
img_label.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
