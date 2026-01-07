from __future__ import annotations

from typing import Any

from ..models.adocao import Adocao
from ..repositories.adocoes_repo import AdocoesRepository
from ..repositories.animais_repo import AnimaisRepository
from ..repositories.usuarios_repo import UsuariosRepository


class AdocoesService:
    def __init__(self, repo: AdocoesRepository, animais_repo: AnimaisRepository, usuarios_repo: UsuariosRepository):
        self._repo = repo
        self._animais = animais_repo
        self._usuarios = usuarios_repo

    def listar(self) -> list[dict[str, Any]]:
        return self._repo.listar()

    def criar(self, payload: dict[str, Any]) -> dict[str, Any]:
        adocao = Adocao.from_dict(payload)
        if not self._animais.buscar(adocao.animal_id):
            raise ValueError("animal não encontrado")
        if not self._usuarios.buscar(adocao.adotante_id):
            raise ValueError("adotante não encontrado")
        adocao_id = self._repo.inserir(adocao.to_dict())
        return self._repo.buscar(adocao_id) or {"id": adocao_id}

    def finalizar(self, adocao_id: int) -> dict[str, Any] | None:
        item = self._repo.buscar(adocao_id)
        if not item:
            return None
        adocao = Adocao.from_dict(item)
        adocao.finalizar()
        self._repo.atualizar_status(adocao_id, adocao.status)
        self._animais.alterar_status(adocao.animal_id, "adotado")
        return self._repo.buscar(adocao_id)

    def cancelar(self, adocao_id: int) -> dict[str, Any] | None:
        item = self._repo.buscar(adocao_id)
        if not item:
            return None
        adocao = Adocao.from_dict(item)
        adocao.cancelar()
        self._repo.atualizar_status(adocao_id, adocao.status)
        return self._repo.buscar(adocao_id)

    def contrato(self, adocao_id: int) -> str | None:
        item = self._repo.buscar(adocao_id)
        if not item:
            return None
        adocao = Adocao.from_dict(item)
        adotante = self._usuarios.buscar(adocao.adotante_id) or {}
        animal = self._animais.buscar(adocao.animal_id) or {}
        return adocao.gerar_contrato(adotante.get("nome", ""), animal.get("nome", ""))
