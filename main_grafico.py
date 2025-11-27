import pygame
from funciones import *
from config import *

DADOS_VALORES = [1, 2, 3, 4, 5]
DADOS_BLOQUEADOS = [False, False,False, False, False]
PUNTAJE_TOTAL_SIMULADO = 0
PANTALLA_SIMULADA = {"Maestro Jedi": None, "Sith": None}
RECTS_DADOS = []