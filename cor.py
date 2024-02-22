import cv2
import numpy as np

# Carregar a imagem do tabuleiro de xadrez
image = cv2.imread('tabuleiro.png')

# Converter a imagem para o espaço de cores HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Definir os intervalos de cor para as peças pretas e brancas do xadrez
lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 70])

lower_white = np.array([0, 0, 150])
upper_white = np.array([180, 30, 255])

# Segmentar as peças pretas
mask_black = cv2.inRange(hsv, lower_black, upper_black)
black_pieces = cv2.bitwise_and(image, image, mask=mask_black)

# Segmentar as peças brancas
mask_white = cv2.inRange(hsv, lower_white, upper_white)
white_pieces = cv2.bitwise_and(image, image, mask=mask_white)

# Juntar as duas imagens lado a lado
result = np.concatenate((black_pieces, white_pieces), axis=1)

# Mostrar a imagem combinada
cv2.imshow('Peças Pretas e Brancas', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
