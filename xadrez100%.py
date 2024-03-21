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
    
    piece_centers = []
    
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
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
        intensity = np.mean(window)  # Calcula a média da intensidade dos pixels na vizinhança do centro
        
        # print(intensity)

        if intensity > 120:  # Ajuste do limiar para distinguir as peças pretas
            chessboard_matrix[row, col] = 1  # Peças brancas têm valor 1
        else:
            chessboard_matrix[row, col] = 5  # Peças pretas têm valor 5
        
    return chessboard_matrix

# Função para processar uma imagem e criar uma matriz correspondente
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

def agrupar_pares(lista):
    pares_agrupados = []
    par_atual = []

    for item in lista:
        if item[1] == 'F':
            par_atual.insert(0, item[0])
        elif item[1] == 'L':  
            par_atual.append(item[0])
            
        if(len(par_atual) == 2):    
            pares_agrupados.append(tuple(par_atual))
            par_atual = []

    return pares_agrupados

def display_difference(matrix1, matrix2):
    print("Movimento realizado:")
    move = []
    for i in range(matrix1.shape[0]):
        for j in range(matrix1.shape[1]):
            if (matrix1[i,j] == 5 and matrix2[i,j] == 0) or (matrix1[i,j] == 1 and matrix2[i,j] == 0):
                start_square = f"{chr(ord('a') + j)}{8 - i}"
                move.append((start_square, 'F'))
            elif (matrix1[i,j] == 0 and matrix2[i,j] == 5) or (matrix1[i,j] == 0 and matrix2[i,j] == 1) or (matrix1[i,j] == 1 and matrix2[i,j] == 5) or (matrix1[i,j] == 5 and matrix2[i,j] == 1):
                end_square = f"{chr(ord('a') + j)}{8 - i}"
                move.append((end_square, 'L'))
                
    moves = agrupar_pares(move)
    
    if(len(moves) != 2):
        for mv in moves:
            print(f"De: {mv[0]} Para: {mv[1]}")
    else:
        print(f"De: {moves[0][0]} Para: {moves[1][1]}")
        print(f"De: {moves[1][0]} Para: {moves[0][1]}")

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

