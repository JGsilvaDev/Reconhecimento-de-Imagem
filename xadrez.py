import cv2

# Webcam (para análise em tempo real)
webcam = cv2.VideoCapture(0)

# Define as dimensões do tabuleiro de xadrez
rows = 8
cols = 8

# Define as coordenadas da região onde a matriz 8x8 será desenhada
roi_start_x, roi_start_y = 100, 100  # Ajuste conforme necessário
roi_end_x, roi_end_y = roi_start_x + 400, roi_start_y + 400  # Ajuste conforme necessário

# Calcula o tamanho aproximado de cada quadrado do tabuleiro
square_size_x = (roi_end_x - roi_start_x) // cols
square_size_y = (roi_end_y - roi_start_y) // rows

def processar_frame(frame):
    # Itera sobre as linhas e colunas para identificar as coordenadas das casas
    for row in range(rows):
        for col in range(cols):
            # Calcula as coordenadas do canto superior esquerdo do quadrado
            x1 = roi_start_x + col * square_size_x
            y1 = roi_start_y + row * square_size_y
            # Calcula as coordenadas do canto inferior direito do quadrado
            x2 = roi_start_x + (col + 1) * square_size_x
            y2 = roi_start_y + (row + 1) * square_size_y
            # Calcula a coordenada da casa
            col_name = chr(65 + col)  # Converte o valor da coluna para a letra correspondente (A-H)
            row_name = str(8 - row)    # Converte o valor da linha para o número correspondente (1-8)
            # Desenha um quadrado delimitando a casa
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            # Calcula o centro do quadrado
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            # Desenha um círculo nas coordenadas da casa
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
            # Escreve as coordenadas da casa
            cv2.putText(frame, f'{col_name}{row_name}', (cx - 10, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# Loop para capturar e processar frames em tempo real
while True:
    ret, frame = webcam.read()

    if not ret:
        print("Erro ao capturar frame")

    processar_frame(frame)

    # Desenha um retângulo delimitando a região de interesse
    cv2.rectangle(frame, (roi_start_x, roi_start_y), (roi_end_x, roi_end_y), (0, 255, 0), 2)

    # Exibe a imagem com as coordenadas das casas e os quadrados delimitando cada casa
    cv2.imshow('Webcam', frame)

    # Verifica se a tecla 'q' foi pressionada para sair do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos ao sair
webcam.release()
cv2.destroyAllWindows()
