import cv2
import numpy as np

def preprocess_image(image):
    # Convertendo a imagem para o espaço de cor HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Definindo os intervalos de cor para as peças brancas e pretas
    lower_white = np.array([0, 0, 200])  # Ajustado para capturar melhor as peças brancas
    upper_white = np.array([179, 50, 255])
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([179, 255, 50])  # Ajustado para capturar melhor as peças pretas
    
    # Segmentando as peças brancas e pretas
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    mask_black = cv2.inRange(hsv, lower_black, upper_black)
    
    # Combinando as máscaras
    mask = cv2.bitwise_or(mask_white, mask_black)
    
    # Aplicando operações morfológicas para limpar os contornos
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # Realiza a detecção de bordas usando Canny
    edges = cv2.Canny(mask, 50, 150)
    
    return edges

def detect_pieces(image):
    # Encontra os contornos na imagem
    contours, _ = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    piece_centers = []
    
    for contour in contours:
        # Obtém o retângulo delimitador do contorno
        x, y, w, h = cv2.boundingRect(contour)
        
        # Calcula o centro do retângulo delimitador
        cX = x + w // 2
        cY = y + h // 2
        
        piece_centers.append((cX, cY))
        
    return piece_centers

def filter_points(piece_centers, image):
    filtered_points = {}
    
    for center in piece_centers:
        # Calcula a posição da casa no tabuleiro
        row = int(center[1] / (image.shape[0] / 8))
        col = int(center[0] / (image.shape[1] / 8))
        
        # Calcula o ponto central da casa no tabuleiro
        x_center = (col + 0.5) * (image.shape[1] / 8)
        y_center = (row + 0.5) * (image.shape[0] / 8)
        
        # Adiciona o ponto central corrigido à lista de pontos filtrados
        filtered_points[(row, col)] = (int(x_center), int(y_center))
    
    return list(filtered_points.values())

def create_chessboard_matrix(piece_centers, image):
    # Inicializa uma matriz 8x8 com zeros
    chessboard_matrix = np.zeros((8, 8), dtype=int)
    
    # Itera sobre os centros das peças detectadas
    for center in piece_centers:
        # Calcula a posição da peça no tabuleiro
        row = int(center[1] / (image.shape[0] / 8))
        col = int(center[0] / (image.shape[1] / 8))
        
        # Verifica a cor da peça com base na intensidade do pixel na vizinhança do centro
        window = image[max(center[1]-5,0):min(center[1]+5,image.shape[0]), max(center[0]-5,0):min(center[0]+5,image.shape[1])]
        pixels_abaixo_de_120 = np.sum(window < 120)
        
        if pixels_abaixo_de_120 > (5 * 5) // 2:  # Mais da metade dos pixels tem intensidade baixa
            chessboard_matrix[row, col] = 5  # Peças pretas têm valor 5
        else:
            chessboard_matrix[row, col] = 1  # Peças brancas têm valor 1
        
    return chessboard_matrix

def process_image(image_path):
    image = cv2.imread(image_path)
    
    # Pré-processa a imagem
    processed_image = preprocess_image(image)
    
    # Detecta as peças na imagem pré-processada
    piece_centers = detect_pieces(processed_image)
    
    # Filtra os pontos para garantir que estejam no centro de cada casa do tabuleiro
    filtered_points = filter_points(piece_centers, image)
    
    # Cria a matriz do tabuleiro de xadrez
    chessboard_matrix = create_chessboard_matrix(filtered_points, image)
    
    return chessboard_matrix

def display_difference(matrix1, matrix2):
    print("Movimento realizado:")
    for i in range(matrix1.shape[0]):
        for j in range(matrix1.shape[1]):
            if (matrix1[i,j] == 5 and matrix2[i,j] == 0) or (matrix1[i,j] == 1 and matrix2[i,j] == 0):
                start_square = f"{chr(ord('a') + j)}{8 - i}"
            elif (matrix1[i,j] == 0 and matrix2[i,j] == 5) or (matrix1[i,j] == 0 and matrix2[i,j] == 1) or (matrix1[i,j] == 1 and matrix2[i,j] == 5) or (matrix1[i,j] == 5 and matrix2[i,j] == 1):
                end_square = f"{chr(ord('a') + j)}{8 - i}"
                
    print(f"De: {start_square} Para: {end_square}")


image_path = input("Digite o caminho da imagem do tabuleiro de xadrez: ")

chessboard_matrix = process_image(image_path)

print("Matriz correspondente à primeira imagem:")
print(chessboard_matrix)
print()

while True:
    input("Pressione a tecla Enter para continuar com a próxima imagem...")
    
    next_image_path = input("Digite o caminho da próxima imagem do tabuleiro de xadrez (ou pressione Enter para sair): ")
    
    if not next_image_path:
        break
    
    next_chessboard_matrix = process_image(next_image_path)

    print("Matriz correspondente à próxima imagem:")
    print(next_chessboard_matrix)
    print()

    display_difference(chessboard_matrix, next_chessboard_matrix)

    chessboard_matrix = next_chessboard_matrix
