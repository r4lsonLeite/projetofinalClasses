from usuario import usuario
from animais import animais


class triagem:
    def __init__(self, user: Usuario, animal: animal, pontuacao:str, elegivel:bool, observacoes:str):
        self.pontuacao = pontuacao
        self.elegivel = elegivel
        self.observacoes = observacoes
    if self.pontuação >= 50:
        self.elegivel = True
    else:
        self.elegivel = False
    