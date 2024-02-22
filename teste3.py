import cv2
import numpy as np

colunas = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h'}
linhas  = {0:'8',1:'7',2:'6',3:'5',4:'4',5:'3',6:'2',7:'1'}

pos_colunas = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
pos_linhas  = {'8':0,'7':1,'6':2,'5':3,'4':4,'3':5,'2':6,'1':7}

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

    
def peca_compara(matriz,coords,num):
    # to_pos(coords)
    return (matriz[coords[1]][coords[0]] == num)

def to_pos(coords):
    # x = colunas
    # y = linhas
    print(f'convertido para {colunas[coords[0]]}{linhas[coords[1]]}')
    return f"{colunas[coords[0]]}{linhas[coords[1]]}"
    
def check_movement(matriz1, matriz2):
    differences = [] 
    order = []  # Inicializando como uma lista vazia

    for i in range(len(matriz1)):
        for j in range(len(matriz1)):
            if matriz1[i][j] != matriz2[i][j]:
                differences.append((j, i, matriz2[i][j]))

    if not differences:
        print('Nenhuma das peças foi movida, as matrizes estão iguais')
        return
    
    for difference in differences:
        if peca_compara(matriz1, (difference[0], difference[1]), 1):
            order.append((difference[0], difference[1]))  # Adicionando como uma tupla
    
    for difference in differences:
        if (difference[0], difference[1]) not in order:  # Verificando a ordem
            order.append((difference[0], difference[1]))  # Adicionando como uma tupla
    
    if len(order) <= 1:
        print(f'A PEÇA NA POSICAO {to_pos(order[0])} FOI COMIDA')
        return
    
    return {'coordenadas': order, 'notacao': f'{to_pos(order[0])}{to_pos(order[1])}'}

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
    
    check_movement(next_chessboard_matrix, chessboard_matrix)

    # Atualiza a matriz para a próxima comparação
    chessboard_matrix = next_chessboard_matrix
