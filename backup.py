import cv2

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

# Carrega a imagem do tabuleiro de xadrez
image = cv2.imread('tabuleiro.png')

# Define as dimensões do tabuleiro de xadrez
rows = 8
cols = 8

# Calcula o tamanho exato de cada quadrado do tabuleiro
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
        # cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        # Calcula o centro do quadrado
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        # Desenha um círculo nas coordenadas da casa
        # cv2.circle(image, (cx, cy), 5, (0, 255, 0), -1)
        # Escreve as coordenadas da casa
        cv2.putText(image, f'{col_name}{row_name}', (cx - 10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# Redimensiona a imagem
width = int(image.shape[1])
height = int(image.shape[0])
dim = (width, height)
resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

# Exibe a imagem com as coordenadas das casas e os quadrados delimitando cada casa
cv2.imshow('Chess Board', resized_image)

# Define o evento de clique do mouse
cv2.setMouseCallback('Chess Board', click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()
