from __future__ import annotations

from typing import Any


class Usuario:
    MORADIAS_VALIDAS = {"casa", "apto"}

    def __init__(
        self,
        nome: str,
        idade: int,
        moradia: str,
        area_util: float,
        experiencia: str,
        criancas: bool,
        outros_animais: bool,
        usuario_id: int | None = None,
    ):
        self.id = usuario_id
        self.nome = nome
        self.idade = idade
        self.moradia = moradia
        self.area_util = area_util
        self.experiencia = experiencia
        self.criancas = criancas
        self.outros_animais = outros_animais
        self._validar_campos()

    def _validar_campos(self) -> None:
        self.nome = str(self.nome).strip()
        if not self.nome:
            raise ValueError("nome não pode ser vazio")

        if not isinstance(self.idade, int) or self.idade < 0:
            raise ValueError("idade deve ser um inteiro >= 0")

        self.moradia = str(self.moradia).strip().lower()
        if self.moradia not in self.MORADIAS_VALIDAS:
            raise ValueError("moradia deve ser 'casa' ou 'apto'")

        if not isinstance(self.area_util, (int, float)) or float(self.area_util) < 0:
            raise ValueError("area_util deve ser um número >= 0")
        self.area_util = float(self.area_util)

        self.experiencia = str(self.experiencia).strip()
        if not self.experiencia:
            raise ValueError("experiencia não pode ser vazia")

        self.criancas = bool(self.criancas)
        self.outros_animais = bool(self.outros_animais)

    def cadastrar(self) -> None:
        self._validar_campos()

    def editar(
        self,
        novo_nome: str,
        nova_idade: int,
        nova_moradia: str,
        nova_area: float,
        nova_experiencia: str,
        tem_criancas: bool,
        novos_outros_animais: bool,
    ) -> None:
        self.nome = novo_nome
        self.idade = nova_idade
        self.moradia = nova_moradia
        self.area_util = nova_area
        self.experiencia = nova_experiencia
        self.criancas = tem_criancas
        self.outros_animais = novos_outros_animais
        self._validar_campos()

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,
            "moradia": self.moradia,
            "area_util": self.area_util,
            "experiencia": self.experiencia,
            "criancas": int(self.criancas),
            "outros_animais": int(self.outros_animais),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Usuario":
        return cls(
            nome=data["nome"],
            idade=int(data["idade"]),
            moradia=data["moradia"],
            area_util=float(data["area_util"]),
            experiencia=data["experiencia"],
            criancas=bool(data.get("criancas", False)),
            outros_animais=bool(data.get("outros_animais", False)),
            usuario_id=data.get("id"),
        )
