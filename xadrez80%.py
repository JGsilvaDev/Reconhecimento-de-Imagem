import cv2
import numpy as np

def preprocess_image(image):
    # Converte a imagem para tons de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Aplica uma limiarização para binarizar a imagem
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    
    # Realiza a detecção de bordas usando Canny
    edges = cv2.Canny(binary, 50, 150)
    
    return edges

def detect_pieces(image):
    # Encontra os contornos na imagem
    contours, _ = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Inicializa uma lista para armazenar os centros das peças
    piece_centers = []
    
    for contour in contours:
        # Calcula o centro do contorno
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            piece_centers.append((cX, cY))
    
    return piece_centers

def create_chessboard_matrix(piece_centers, image_shape):
    # Inicializa uma matriz 8x8 com zeros
    chessboard_matrix = np.zeros((8, 8), dtype=int)
    
    # Itera sobre os centros das peças detectadas
    for center in piece_centers:
        # Calcula a posição da peça no tabuleiro
        row = int(center[1] / (image_shape[0] / 8))
        col = int(center[0] / (image_shape[1] / 8))
        
        # Marca a posição da peça na matriz do tabuleiro
        chessboard_matrix[row, col] = 1
    
    return chessboard_matrix

# Função para exibir a diferença entre as matrizes usando coordenadas de xadrez
def display_difference(difference_matrix):
    print("Movimento realizado:")
    for i in range(difference_matrix.shape[0]):
        for j in range(difference_matrix.shape[1]):
            if difference_matrix[i, j] == 1 or end_square == None:
                end_square = f"{chr(ord('a') + j)}{8 - i}"
            elif difference_matrix[i, j] == -1:
                start_square = f"{chr(ord('a') + j)}{8 - i}"
                
    print(f"De: {start_square} Para: {end_square}")

# Função para processar uma imagem e criar uma matriz correspondente
def process_image(image_path):
    # Carrega a imagem
    image = cv2.imread(image_path)
    
    # Pré-processa a imagem
    processed_image = preprocess_image(image)
    
    # Detecta as peças na imagem pré-processada
    piece_centers = detect_pieces(processed_image)
    
    # Cria a matriz do tabuleiro de xadrez
    chessboard_matrix = create_chessboard_matrix(piece_centers, image.shape)
    
    return chessboard_matrix

# Caminho da imagem do tabuleiro de xadrez
image_path = input("Digite o caminho da imagem do tabuleiro de xadrez: ")

# Processa a primeira imagem e cria a matriz correspondente
chessboard_matrix = process_image(image_path)

# Exibe a matriz correspondente à primeira imagem
print("Matriz correspondente à primeira imagem:")
print(chessboard_matrix)
print()

# Loop para continuar com a próxima imagem
while True:
    input("Pressione a tecla Enter para continuar com a próxima imagem...")
    
    # Caminho da próxima imagem do tabuleiro de xadrez
    next_image_path = input("Digite o caminho da próxima imagem do tabuleiro de xadrez (ou pressione Enter para sair): ")
    
    if not next_image_path:
        break
    
    # Processa a próxima imagem e cria a matriz correspondente
    next_chessboard_matrix = process_image(next_image_path)

    # Exibe a matriz correspondente à próxima imagem
    print("Matriz correspondente à próxima imagem:")
    print(next_chessboard_matrix)
    print()

    # Comparação das matrizes
    difference_matrix = next_chessboard_matrix - chessboard_matrix

    # Exibição da diferença entre as matrizes usando coordenadas de xadrez
    display_difference(difference_matrix)

    # Atualiza a matriz para a próxima comparação
    chessboard_matrix = next_chessboard_matrix
