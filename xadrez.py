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
    # Faz uma cópia da imagem original para desenhar os resultados
    result_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    
    # Encontra os contornos na imagem
    contours, _ = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Inicializa uma lista para armazenar os centros das peças
    piece_centers = []
    
    for contour in contours:
        # Calcula o centroide do contorno
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            piece_centers.append((cX, cY))
            # Calcula as coordenadas dos cantos do quadrado com base no centro e nas dimensões da peça
            x, y, w, h = cv2.boundingRect(contour)
            square_side = max(w, h)
            x1 = cX - square_side // 2
            y1 = cY - square_side // 2
            x2 = cX + square_side // 2
            y2 = cY + square_side // 2
            cv2.rectangle(result_image, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Desenha o quadrado vermelho
            # Desenha o centro
            cv2.circle(result_image, (cX, cY), 3, (0, 0, 255), -1)  # Desenha um círculo vermelho
        
    # Exibe a imagem com os resultados
    cv2.imshow("Detected Pieces", result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return piece_centers

def filter_points(piece_centers, image):
    # Cria um dicionário para armazenar os pontos filtrados por casa
    filtered_points = {}
    
    for center in piece_centers:
        # Calcula a posição da casa no tabuleiro
        row = int(center[1] / (image.shape[0] / 8))
        col = int(center[0] / (image.shape[1] / 8))
        
        # Se a casa já tiver um ponto, verifica se o ponto atual está mais próximo do centro da casa
        if (row, col) in filtered_points:
            existing_center = filtered_points[(row, col)]
            existing_distance = (existing_center[0] - (image.shape[1] / 16))**2 + (existing_center[1] - (image.shape[0] / 16))**2
            new_distance = (center[0] - (image.shape[1] / 16))**2 + (center[1] - (image.shape[0] / 16))**2
            # Se o novo ponto estiver mais próximo do centro da casa, substitua o ponto existente
            if new_distance < existing_distance:
                filtered_points[(row, col)] = center
        else:
            # Se a casa ainda não tiver um ponto, adicione o ponto atual
            filtered_points[(row, col)] = center
    
    # Retorna os pontos filtrados
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
        print(f"Coord: {row, col} - {intensity}")
        
        if intensity > 100:  # Se a intensidade do pixel for maior que 100 (branco ou cinza claro)
            chessboard_matrix[row, col] = 1  # Peças brancas têm valor 1
        else:
            chessboard_matrix[row, col] = 5  # Peças pretas têm valor 5
    
    return chessboard_matrix

# Função para processar uma imagem e criar uma matriz correspondente
def process_image(image_path):
    # Carrega a imagem
    image = cv2.imread(image_path)
    
    # Pré-processa a imagem
    processed_image = preprocess_image(image)
    
    # Detecta as peças na imagem pré-processada
    piece_centers = detect_pieces(processed_image)
    
    # Cria a matriz do tabuleiro de xadrez
    chessboard_matrix = create_chessboard_matrix(piece_centers, image)
    
    return chessboard_matrix

# Caminho da imagem do tabuleiro de xadrez
image_path = input("Digite o caminho da imagem do tabuleiro de xadrez: ")

# Processa a imagem e cria a matriz correspondente
chessboard_matrix = process_image(image_path)

# Exibe a matriz correspondente à imagem
print("Matriz correspondente à imagem:")
print(chessboard_matrix)
