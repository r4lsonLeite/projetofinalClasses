

from animais import Animais
from usuario import Usuario
class triagem:
    def __init__(self, user: Usuario, animal: Animais, pontuacao:str, elegivel:bool, observacoes:str):
        self.pontuacao = pontuacao
        self.elegivel = elegivel
        self.observacoes = observacoes
        self.user = user
        self.animal = animal
    
    def cadastrar(self) -> None:
        print(f"Triagem cadastrada para o usuário {self.user.nome} e o animal {self.animal.nome}.")

    def avaliar(self) -> None:
        print(f"Avaliando triagem para o usuário {self.user.nome} e o animal {self.animal.nome}.")

    def calcular_compatibilidade(self) -> None:
        if self.pontuacao >= 50:
          self.elegivel = True
        else:
          self.elegivel = False
        return self.elegivel

    def validar_politicas(self) -> None:
        print(f"Validando políticas para o usuário {self.user.nome} e o animal {self.animal.nome}.")
   