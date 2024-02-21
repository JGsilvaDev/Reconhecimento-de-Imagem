import cv2
import numpy as np

# Função de callback para evento de clique
def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Calcula a coluna e a linha da casa clicada
        col_clicked = x // square_size_x
        row_clicked = 7 - (y // square_size_y)  # Inverte a ordem das linhas
        # Converte o índice da coluna para a letra correspondente (A-H)
        col_name = chr(65 + col_clicked)
        # Converte o índice da linha para o número correspondente (1-8)
        row_name = str(row_clicked + 1)  # Adiciona 1 ao índice da linha
        # Exibe as coordenadas da casa clicada
        print(f"Casa clicada: {col_name}{row_name}")

# Função para comparar as duas matrizes de tabuleiro e encontrar as diferenças
def compare_boards(board1, board2):
    differences = []
    for i in range(8):
        for j in range(8):
            if board1[i][j] != board2[i][j]:
                differences.append(((i, j), board2[i][j]))
    return differences

# Função para criar a matriz de tabuleiro a partir da imagem
def create_board(image):
    board = np.zeros((8, 8), dtype=int)
    # Identifica as casas com peças (valor diferente de 0 na imagem)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        col = x // square_size_x
        row = 7 - (y // square_size_y)  # Inverte a ordem das linhas
        board[row][col] = 1
    return board

# Carrega a imagem do tabuleiro de xadrez original e a imagem com as mudanças
original_image = cv2.imread('tabuleiro.png')
changed_image = cv2.imread('tabuleiro2.png')

# Define as dimensões do tabuleiro de xadrez
rows = 8
cols = 8

# Calcula o tamanho exato de cada quadrado do tabuleiro
square_size_x = original_image.shape[1] // cols
square_size_y = original_image.shape[0] // rows

# Exibe a imagem original com as coordenadas das casas
cv2.imshow('Chess Board', original_image)

# Define o evento de clique do mouse
cv2.setMouseCallback('Chess Board', click_event)

original_board = create_board(original_image)

# Mostra a matriz original no terminal
print("Matriz original:")
print(original_board)

while True:
    key = cv2.waitKey(1)
    if key == 32:  # Barra de espaço
        changed_board = create_board(changed_image)
        differences = compare_boards(original_board, changed_board)
        print("Matriz alterada:")
        print(changed_board)
        print("Diferenças:")
        for diff in differences:
            print(f"Casa alterada: {chr(diff[0][1] + 65)}{8 - diff[0][0]} para {chr(diff[0][1] + 65)}{8 - diff[1]}")
    elif key == 27:  # Tecla ESC para sair
        break

cv2.destroyAllWindows()
