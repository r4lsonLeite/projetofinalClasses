from __future__ import annotations

from typing import Any


class Animais:
    STATUS_VALIDOS = {
        "disponivel",
        "reservado",
        "adotado",
        "devolvido",
        "quarentena",
        "inadotavel",
    }
    PORTES_VALIDOS = {"P", "M", "G"}

    def __init__(
        self,
        especie: str,
        raca: str,
        nome: str,
        sexo: str,
        idade_meses: int,
        porte: str,
        estado: str,
        status: str = "disponivel",
        animal_id: int | None = None,
    ):
        self.id = animal_id
        self.especie = especie
        self.raca = raca
        self.nome = nome
        self.sexo = sexo
        self.idade_meses = idade_meses
        self.porte = porte
        self.estado = estado
        self.status = status
        self._validar_campos()

    def _validar_campos(self) -> None:
        if not isinstance(self.idade_meses, int) or self.idade_meses < 0:
            raise ValueError("idade_meses deve ser um inteiro >= 0")

        self.porte = str(self.porte).strip().upper()
        if self.porte not in self.PORTES_VALIDOS:
            raise ValueError("porte deve ser 'P', 'M' ou 'G'")

        self.status = str(self.status).strip().lower()
        if self.status not in self.STATUS_VALIDOS:
            raise ValueError(
                "status inválido. Use: disponivel, reservado, adotado, devolvido, quarentena, inadotavel"
            )

        self.sexo = str(self.sexo).strip()
        if not self.sexo:
            raise ValueError("sexo não pode ser vazio")

        self.especie = str(self.especie).strip()
        self.raca = str(self.raca).strip()
        self.nome = str(self.nome).strip()
        self.estado = str(self.estado).strip()

        if not self.especie:
            raise ValueError("espécie não pode ser vazia")
        if not self.raca:
            raise ValueError("raça não pode ser vazia")
        if not self.nome:
            raise ValueError("nome não pode ser vazio")
        if not self.estado:
            raise ValueError("estado não pode ser vazio")

    def cadastrar(self) -> None:
        self._validar_campos()

    def editar(
        self,
        nova_especie: str,
        nova_raca: str,
        novo_nome: str,
        novo_sexo: str,
        nova_idade_meses: int,
        novo_porte: str,
        novo_estado: str,
        novo_status: str,
    ) -> None:
        self.especie = nova_especie
        self.raca = nova_raca
        self.nome = novo_nome
        self.sexo = novo_sexo
        self.idade_meses = nova_idade_meses
        self.porte = novo_porte
        self.estado = novo_estado
        self.status = novo_status
        self._validar_campos()

    def remover(self) -> None:
        # Remoção real é responsabilidade do repositório
        return

    def adotar(self) -> None:
        if self.status in {"quarentena", "inadotavel"}:
            raise ValueError(f"Animal {self.nome} não pode ser adotado (status: {self.status}).")
        if self.status == "adotado":
            raise ValueError(f"Animal {self.nome} já está adotado.")
        self.status = "adotado"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "especie": self.especie,
            "raca": self.raca,
            "nome": self.nome,
            "sexo": self.sexo,
            "idade_meses": self.idade_meses,
            "porte": self.porte,
            "estado": self.estado,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Animais":
        return cls(
            especie=data["especie"],
            raca=data["raca"],
            nome=data["nome"],
            sexo=data["sexo"],
            idade_meses=int(data["idade_meses"]),
            porte=data["porte"],
            estado=data["estado"],
            status=data.get("status", "disponivel"),
            animal_id=data.get("id"),
        )
