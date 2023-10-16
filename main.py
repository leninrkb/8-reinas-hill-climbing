import random 
import copy

def crearTablero(n):
    tablero = []
    for _ in range(n):
        fila = [0 for _ in range(n)]
        indice1 = random.randint(0, n-1)
        fila[indice1] = 1
        tablero.append(fila)
    return tablero

def encontrarReinas(tablero, n):
    reinas = []
    for i in range(n):
        for j in range(n):
            celda = tablero[i][j]
            if celda == 1:
                reinas.append((i,j))
    return reinas
    
def verTablero(tablero):
    for i in range(len(tablero)):
        print(tablero[i]) 
    print()

def revisarCamino(tablero, n, i, j, l, m):
    encontrados = []
    while True:
        i += l
        j += m
        continuar = j >= 0 and j <= n-1 and i >= 0 and i <= n-1
        if not continuar:
            break
        celda = tablero[i][j]
        if celda == 1:
            encontrados.append((i,j))
    return encontrados

def revisarDiagonal1(tablero, n, i, j):
    return revisarCamino(tablero, n, i, j, -1, 1)
    
def revisarDiagonal2(tablero, n, i, j):
    return revisarCamino(tablero, n, i, j, -1, -1)
    
def revisarDiagonal3(tablero, n, i, j):
    return revisarCamino(tablero, n, i, j, 1, 1)
    
def revisarDiagonal4(tablero, n, i, j):
   return revisarCamino(tablero, n, i, j, 1, -1)

def revisarArriba(tablero, n, i, j):
    return revisarCamino(tablero, n, i, j, -1, 0)

def revisarAbajo(tablero, n, i, j):
    return revisarCamino(tablero, n, i, j, +1, 0)

def revisarDerecha(tablero, n, i, j):
    return revisarCamino(tablero, n, i, j, 0, 1)

def revisarIzquierda(tablero, n, i, j):
    return revisarCamino(tablero, n, i, j, 0, -1)

def agregarEncontrados(ataques, encontrados):
     if len(encontrados) > 0:
        ataques.extend(encontrados)
        
def encontrarAtaques(tablero, n, i, j):
    ataques = []
    resp = revisarDiagonal1(tablero, n, i, j)
    agregarEncontrados(ataques, resp)
    
    resp = revisarDiagonal2(tablero, n, i, j)
    agregarEncontrados(ataques, resp)
    
    resp = revisarDiagonal3(tablero, n, i, j)
    agregarEncontrados(ataques, resp)
    
    resp = revisarDiagonal4(tablero, n, i, j)
    agregarEncontrados(ataques, resp)
    
    resp = revisarArriba(tablero, n, i, j)
    agregarEncontrados(ataques, resp)
    
    resp = revisarAbajo(tablero, n, i, j)
    agregarEncontrados(ataques, resp)
    
    resp = revisarDerecha(tablero, n, i, j)
    agregarEncontrados(ataques, resp)
    
    resp = revisarIzquierda(tablero, n, i, j)
    agregarEncontrados(ataques, resp)
    
    return ataques

def calcHeuristica(tablero, reinas, n):
    h = 0
    mapaAtaques = {}
    for reina in reinas:
        i = reina[0]
        j = reina[1]
        ataques = encontrarAtaques(tablero, n, i, j)
        mapaAtaques[reina] = ataques
        h += len(ataques)
    return mapaAtaques, h

def mover(tablero, disponibles, i, j):
    tableroTemporal = copy.deepcopy(tablero)
    idd = random.randint(0, len(disponibles)-1)
    r = disponibles[idd]
    tableroTemporal[i][j] = 0
    tableroTemporal[r[0]][r[1]] = 1
    return tableroTemporal

def seleccionarReina(reinas, mapa):
    mayorH = 0
    r = None
    for reina in reinas:
        h = len(mapa[reina])
        if h > mayorH:
            mayorH = h
            r = reina
    return r

def encontrarDisponibles(tablero, n, r):
    fila = tablero[r[0]]
    disponibles = []
    for j in range(n):
        if fila[j] == 0:
            disponibles.append((r[0], j))
    return disponibles
        
    
def hillClimbing(tablero, n, H, p):
    h = 0
    mapa = {}
    while True:
        reinas = encontrarReinas(tablero, n)
        mapa, h = calcHeuristica(tablero, reinas, n)
        
        if h <= H:
            break
        
        r = seleccionarReina(reinas, mapa)
        disponibles = encontrarDisponibles(tablero, n, r)
        
        tableroTemporal = mover(tablero, disponibles, r[0], r[1])
        reinasTemporal = encontrarReinas(tableroTemporal, n)
        _, hTemporal = calcHeuristica(tableroTemporal, reinasTemporal, n)
        if hTemporal < h:
            tablero = tableroTemporal
        else:
            pRandom = random.random()
            if pRandom <= p:
                tablero = tableroTemporal
    return tablero

import chess  
import chess.svg
import cairosvg   

def dibujarTablero(tablero, n):
    tableroAjedrez = chess.Board()
    tableroAjedrez.clear()
    for i in range(n):
        for j in range(n):
            if tablero[i][j]:
                tableroAjedrez.set_piece_at(chess.square(i, j), chess.Piece(5, chess.WHITE))
    return tableroAjedrez.fen()

def guardarTablero(dibujo, nombre):
    tablero = chess.Board(dibujo)
    tablerosvg = chess.svg.board(board=tablero)
    archivo = open(nombre, "w")
    archivo.write(tablerosvg)
    archivo.close()
    print("guardado...")
    
def guardar(tablero, nombre,  n):
    dibujo = dibujarTablero(tablero, n)
    guardarTablero(dibujo, nombre)

                
n = 8
p = 1
H = 1
tablero = crearTablero(n)
verTablero(tablero)
guardar(tablero, 'original.svg', n)

solucion = hillClimbing(tablero, n, H, p)
verTablero(solucion)
guardar(solucion, 'solucion.svg', n)

print('terminado')
