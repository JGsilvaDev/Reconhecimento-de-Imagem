import cv2
import numpy as np

# Carrega a imagem do tabuleiro de xadrez
image = cv2.imread('tabuleiro.png')

# Define as dimensões do tabuleiro de xadrez
rows = 8
cols = 8

# Calcula o tamanho aproximado de cada quadrado do tabuleiro
square_size_x = image.shape[1] // cols
square_size_y = image.shape[0] // rows

# Itera sobre as linhas e colunas para identificar as coordenadas das casas
for row in range(rows):
    for col in range(cols):
        # Calcula as coordenadas do canto superior esquerdo do quadrado
        x1 = col * square_size_x
        y1 = row * square_size_y
        # Calcula as coordenadas do canto inferior direito do quadrado
        x2 = (col + 1) * square_size_x
        y2 = (row + 1) * square_size_y
        # Calcula a coordenada da casa
        col_name = chr(65 + col)  # Converte o valor da coluna para a letra correspondente (A-H)
        row_name = str(8 - row)    # Converte o valor da linha para o número correspondente (1-8)
        # Desenha um quadrado delimitando a casa
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        # Calcula o centro do quadrado
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        # Desenha um círculo nas coordenadas da casa
        cv2.circle(image, (cx, cy), 5, (0, 255, 0), -1)
        # Escreve as coordenadas da casa
        cv2.putText(image, f'{col_name}{row_name}', (cx - 10, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# Redimensiona a imagem para 60% do seu tamanho original
scale_percent = 60  
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

# Exibe a imagem com as coordenadas das casas e os quadrados delimitando cada casa
cv2.imshow('Chess Board', resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()