import cv2
import numpy as np

def preprocess_image(image):
    # Converte a imagem para tons de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Aplica um filtro Gaussiano para suavizar a imagem e reduzir o ruído
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Aplica uma limiarização adaptativa para binarizar a imagem
    binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 4)
    
    # Realiza a detecção de bordas usando Sobel
    sobel_x = cv2.Sobel(binary, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(binary, cv2.CV_64F, 0, 1, ksize=3)
    edges = cv2.magnitude(sobel_x, sobel_y)
    
    return edges


def detect_pieces(image):
    # Converte a imagem de bordas de volta para uma imagem binária
    _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY)

    # Garante que a imagem esteja no formato CV_8U
    binary_image = np.uint8(binary_image)

    # Encontra os componentes conectados na imagem binária
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_image, connectivity=8)

    piece_centers = []

    # Itera sobre os componentes conectados encontrados
    for label in range(1, num_labels):
        # Calcula o centróide do componente conectado
        cX, cY = centroids[label]

        # Adiciona o centróide à lista de centros das peças
        piece_centers.append((int(cX), int(cY)))

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

def create_chessboard_matrix_with_intensity(piece_centers, image):
    # Inicializa uma matriz 8x8 com zeros para o tabuleiro
    chessboard_matrix = np.zeros((8, 8), dtype=int)
    
    # Inicializa uma matriz 8x8 com zeros para as intensidades
    intensity_matrix = np.zeros((8, 8), dtype=int)
    
    # Itera sobre os centros das peças detectadas
    for center in piece_centers:
        # Calcula a posição da peça no tabuleiro
        row = int(center[1] / (image.shape[0] / 8))
        col = int(center[0] / (image.shape[1] / 8))
        
        # Verifica a cor da peça com base na intensidade do pixel na vizinhança do centro
        window = image[max(center[1]-10,0):min(center[1]+10,image.shape[0]), max(center[0]-10,0):min(center[0]+10,image.shape[1])]
        intensity = np.mean(window)  # Calcula a média da intensidade dos pixels na vizinhança do centro

        # Adiciona o valor da intensidade à matriz de intensidades
        intensity_matrix[row, col] = intensity
        
        # Determina o valor da peça na matriz do tabuleiro
        if intensity > 120:  # Ajuste do limiar para distinguir as peças pretas
            chessboard_matrix[row, col] = 1  # Peças brancas têm valor 1
        else:
            chessboard_matrix[row, col] = 5  # Peças pretas têm valor 5
        
    return chessboard_matrix, intensity_matrix

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
    chessboard_matrix = create_chessboard_matrix_with_intensity(filtered_points, image)
    
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
