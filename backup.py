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

# Carrega a imagem do tabuleiro de xadrez original e a imagem com as mudanças
original_image = cv2.imread('tabuleiro.png')
changed_image = cv2.imread('tabuleiro2.png')

# Define as dimensões do tabuleiro de xadrez
rows = 8
cols = 8

# Calcula o tamanho exato de cada quadrado do tabuleiro
square_size_x = original_image.shape[1] // cols
square_size_y = original_image.shape[0] // rows

# Flag para controlar qual imagem está sendo exibida
show_original = True

# Função para comparar as duas imagens e destacar as diferenças
def highlight_differences(original, changed):
    # Converte as imagens para escala de cinza
    original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    changed_gray = cv2.cvtColor(changed, cv2.COLOR_BGR2GRAY)
    # Calcula a diferença entre as imagens
    difference = cv2.absdiff(original_gray, changed_gray)
    # Define um limiar para destacar as diferenças
    _, threshold = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)
    # Encontra os contornos das diferenças
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Desenha os contornos das diferenças na imagem original
    highlighted_image = original.copy()
    movements = set()  # Armazena os movimentos únicos
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # Calcula as coordenadas das casas onde a peça estava e para onde foi
        col_original = x // square_size_x
        row_original = 7 - (y // square_size_y)
        col_changed = (x + w) // square_size_x
        row_changed = 7 - ((y + h) // square_size_y)
        # Converte os índices das colunas para as letras correspondentes (A-H)
        col_original_name = chr(65 + col_original)
        col_changed_name = chr(65 + col_changed)
        # Converte os índices das linhas para os números correspondentes (1-8)
        row_original_name = str(row_original + 1)
        row_changed_name = str(row_changed + 1)
        # Adiciona o movimento à lista de movimentos
        movement = f"{col_original_name}{row_original_name}-{col_changed_name}{row_changed_name}"
        movements.add(movement)
        # Desenha o contorno da diferença na imagem original
        cv2.rectangle(highlighted_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
      
    coordenadas = []
    
    for movement in movements:
        coordenadas.append(movement[0:2])
        
    coordenada_final = f"{coordenadas[1]}{coordenadas[0]}"
    print(coordenada_final)
        
    return highlighted_image

# Redimensiona as imagens
width = int(original_image.shape[1])
height = int(original_image.shape[0])
dim = (width, height)
original_resized = cv2.resize(original_image, dim, interpolation=cv2.INTER_AREA)
changed_resized = cv2.resize(changed_image, dim, interpolation=cv2.INTER_AREA)

# Exibe a imagem original com as coordenadas das casas
cv2.imshow('Chess Board', original_resized)

# Define o evento de clique do mouse
cv2.setMouseCallback('Chess Board', click_event)

while True:
    key = cv2.waitKey(1)
    if key == 32:  # Barra de espaço
        show_original = not show_original
        if show_original:
            cv2.imshow('Chess Board', original_resized)
        else:
            # Destaca as diferenças entre as imagens
            highlighted_image = highlight_differences(original_resized, changed_resized)
            cv2.imshow('Chess Board', highlighted_image)
    elif key == 27:  # Tecla ESC para sair
        break

cv2.destroyAllWindows()
