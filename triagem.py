from usuario import usuario
from animais import animais


class triagem:
    def __init__(self, pontuacao:str, elegivel:bool, observacoes:str):
        self.pontuacao = pontuacao
        self.elegivel = elegivel
        self.observacoes = observacoes
        