class Usuario:
    def __init__(self, nome:str, idade: int, moradia: str, area_util: float, experiencia: str, criancas: bool, outros_animais:bool):
        self.nome = nome
        self.idade = idade
        self.moradia = moradia 
        self.area_util = area_util
        self.experiencia = experiencia
        self.criancas = criancas  
        self.outros_animais = outros_animais
    def cadastrar(self):
        print(f" Usuário {self.nome} cadastrado com sucesso!") 
    def editar(self, novo_nome, nova_idade, nova_moradia, nova_area, nova_experiencia, tem_criancas, novos_outros_animais):
        self.nome = novo_nome
        self.idade = nova_idade
        self.moradia = nova_moradia
        self.area_util = nova_area
        self.experiencia = nova_experiencia
        self.criancas = tem_criancas
        self.outros_animais = novos_outros_animais
        print(f" Dados de {self.nome} atualizados!")


    
