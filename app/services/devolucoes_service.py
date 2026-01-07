from __future__ import annotations

from typing import Any

from ..models.devolucao import Devolucao
from ..repositories.devolucoes_repo import DevolucoesRepository
from ..repositories.animais_repo import AnimaisRepository


class DevolucoesService:
    def __init__(self, repo: DevolucoesRepository, animais_repo: AnimaisRepository):
        self._repo = repo
        self._animais = animais_repo

    def listar(self) -> list[dict[str, Any]]:
        return self._repo.listar()

    def criar(self, payload: dict[str, Any]) -> dict[str, Any]:
        devolucao = Devolucao.from_dict(payload)
        if not self._animais.buscar(devolucao.animal_id):
            raise ValueError("animal não encontrado")
        devolucao_id = self._repo.inserir(devolucao.to_dict())
        self._animais.alterar_status(devolucao.animal_id, "devolvido")
        return self._repo.buscar(devolucao_id) or {"id": devolucao_id}

    def reavaliacao(self, devolucao_id: int) -> dict[str, Any] | None:
        item = self._repo.buscar(devolucao_id)
        if not item:
            return None
        devolucao = Devolucao.from_dict(item)
        devolucao.reavaliacao()
        self._repo.atualizar_status(devolucao_id, devolucao.status)
        return self._repo.buscar(devolucao_id)
