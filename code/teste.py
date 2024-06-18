import cv2
from deepface import DeepFace

# Função para detectar expressão facial dominante em um quadro
def detect_face_expression(frame):
    try:
        result = DeepFace.analyze(frame, actions=['emotion'])
        dominant_expression = max(result[0]['emotion'].items(), key=lambda x: x[1])
        return dominant_expression[0]
    except Exception as e:
        print("Erro ao detectar rosto:", e)
        return None

# Função principal para capturar vídeo da webcam e analisar expressões faciais
def main():
    # Inicialização da webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Captura de um frame
        ret, frame = cap.read()

        if not ret:
            break

        # Redimensionamento do frame para acelerar o processo de análise
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Detecção da expressão facial dominante no frame
        expression = detect_face_expression(frame)

        # Se nenhuma expressão for detectada, continue para o próximo quadro
        if expression is None:
            continue

        # Exibição da expressão facial dominante no console
        print("Expressão Facial Dominante:", expression)

        # Exibição do frame com a expressão facial destacada
        cv2.putText(frame, expression, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Facial Expression Recognition', frame)

        # Verificação da tecla 'q' para sair do loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberação da webcam e fechamento das janelas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
