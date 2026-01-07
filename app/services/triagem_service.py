from __future__ import annotations

from typing import Any

from ..models.triagem import Triagem
from ..repositories.triagem_repo import TriagemRepository
from ..repositories.usuarios_repo import UsuariosRepository


class TriagemService:
    def __init__(self, triagem_repo: TriagemRepository, usuarios_repo: UsuariosRepository):
        self._triagens = triagem_repo
        self._usuarios = usuarios_repo

    def listar(self) -> list[dict[str, Any]]:
        return self._triagens.listar()

    def criar_avaliando(self, payload: dict[str, Any]) -> dict[str, Any]:
        triagem = Triagem.from_dict(payload)
        adotante = self._usuarios.buscar(triagem.adotante_id)
        if not adotante:
            raise ValueError("adotante não encontrado")
        triagem.avaliar(adotante)
        triagem_id = self._triagens.inserir(triagem.to_dict())
        return self._triagens.buscar(triagem_id) or {"id": triagem_id}
