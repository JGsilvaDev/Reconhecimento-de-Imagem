import cv2
import numpy as np

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    edges = cv2.Sobel(binary, cv2.CV_64F, 1, 1, ksize=3)  # Utiliza o operador de Sobel para detecção de bordas
    edges = np.uint8(np.absolute(edges))
    return edges

def detect_pieces(image):
    inverted_image = cv2.bitwise_not(image)
    _, binary = cv2.threshold(inverted_image, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    piece_centers = []
    image_with_centers = np.copy(image)  # Criando uma cópia da imagem original
    
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            piece_centers.append((cX, cY))
            cv2.circle(image_with_centers, (cX, cY), 3, (0, 255, 0), -1)  # Desenha um círculo no centro da peça
    
    resized_image = cv2.resize(image_with_centers, (600, 600))  # Redimensiona a imagem para 600x600 pixels
    cv2.imshow("Image with Piece Centers", resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return piece_centers

def filter_points(piece_centers, image):
    filtered_points = {}
    
    for center in piece_centers:
        row = int(center[1] / (image.shape[0] / 8))
        col = int(center[0] / (image.shape[1] / 8))
        
        x_center = (col + 0.5) * (image.shape[1] / 8)
        y_center = (row + 0.5) * (image.shape[0] / 8)
        
        filtered_points[(row, col)] = (int(x_center), int(y_center))
    
    return list(filtered_points.values())

def create_chessboard_matrix(piece_centers, image):
    chessboard_matrix = np.zeros((8, 8), dtype=int)
    
    for center in piece_centers:
        row = int(center[1] / (image.shape[0] / 8))
        col = int(center[0] / (image.shape[1] / 8))
        
        window = image[max(center[1]-5,0):min(center[1]+5,image.shape[0]), max(center[0]-5,0):min(center[0]+5,image.shape[1])]
        intensity = np.mean(window)
        
        if intensity > 120:
            chessboard_matrix[row, col] = 1
        else:
            chessboard_matrix[row, col] = 5
        
    return chessboard_matrix

def process_image(image_path):
    image = cv2.imread(image_path)
    processed_image = preprocess_image(image)
    piece_centers = detect_pieces(processed_image)
    filtered_points = filter_points(piece_centers, image)
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
