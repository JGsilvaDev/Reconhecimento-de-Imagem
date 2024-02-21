colunas = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h'}
linhas  = {0:'8',1:'7',2:'6',3:'5',4:'4',5:'3',6:'2',7:'1'}

pos_colunas = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
pos_linhas  = {'8':0,'7':1,'6':2,'5':3,'4':4,'3':5,'2':6,'1':7}

# Matrizes de exemplo
matrix1 = [
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1]
]
matrix2 = [
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1]
]

#Função de teste, converte posição da matriz para notação de xadrez
def to_pos(coords):
    # x = colunas
    # y = linhas
    # print(f'convertido para {colunas[coords[0]]}{linhas[coords[1]]}')
    return f"{colunas[coords[0]]}{linhas[coords[1]]}"
# Exemplo: to_pos((x,y))

# Função que converte notação de xadrez "b6" para coordenadas (1,2)
def to_coords(pos):
    if len(pos) != 2:
        print('Erro, este valor não é uma posição no xadrez')
        return
    return (pos_colunas[pos[0]], pos_linhas[pos[1]])
# Exemplo: to_coords('d4')

# Retorna verdadeiro caso posição selecionada seja igual a 1
def peca_existe(matriz,coords):
    to_pos(coords)
    return (matriz[coords[1]][coords[0]] == 1)

#Exemplo: peca_existe(matriz,(x,y))

# Retorna verdadeiro caso posição selecionada seja igual ao número selecionado
def peca_compara(matriz,coords,num):
    to_pos(coords)
    return (matriz[coords[1]][coords[0]] == num)

#Exemplo: peca_compara(matriz,(x,y), numero de 0 ou 1)

# Função que compara duas matrizes e retorna que movimento foi efetuado
def check_movement(matriz1,matriz2):
    # Matriz 1 é o ponto inicial
    # A função primeiramente compara as diferenças entre as duas matrizes e as armazena
    # Depois ela checa qual dessas diferenças não existe no ponto inical para determinar a ordem do movimento

    differences = [] # Lista de tuplas com (x,y,valor)
    order = [0] # Lista de tuplas já na ordem de eventos correta

    # Comparando e armazenando as diferenças entre matrizes
    for i in range(len(matriz1)):
        for j in range(len(matriz1)):
            if matriz1[i][j] != matriz2[i][j]:
                differences.append((j,i,matriz2[i][j]))

    print('diferencas antes de verificar: ',differences)

    # Caso não haja diferença
    if not differences:
        print('Nenhuma das peças foi movida, as matrizes estão iguais')
        return
    
    # Verificando qual das diferenças não existe no ponto inicial (primeira matriz)
    for difference in differences:
        print(peca_compara(matriz1,(difference[0],difference[1]),1))
        if peca_compara(matriz1,(difference[0],difference[1]),1):
            # Adicionando a jogada na ordem certa na lista order, e removendo a mesma da lista differences
            order[0] = (difference[0],difference[1])
            differences.remove((difference[0],difference[1],difference[2]))

    # Adicionando o restante das jogadas na lista de ordem
    for difference in differences:
        order.append((difference[0],difference[1]))

    print('Diferenças que sobraram',differences)
    print('ordem certa',order)
    
    # Caso a peça seja comida, ou seja, ela tem o movimento de partida, mas nao o final
    if len(order) <= 1:
        print(f'A PEÇA NA POSICAO {to_pos(order[0])} FOI COMIDA')
        return
    
    return {'coordenadas': order, 'notacao':f'{to_pos(order[0])}{to_pos(order[1])}'}
# Exemplo: check_movement(matriz inicial, matriz final)

# Testando a função
print(check_movement(matrix1,matrix2))

# print(peca_compara(matrix1,(2,5),0))