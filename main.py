from animais import Animais
from usuario import Usuario
from triagem import triagem


def main() -> None:
    print("=== TESTE SIMPLES (manual) ===")

    print("\n[1] Usuario")
    usuario = Usuario(
        nome="Junio",
        idade=22,
        moradia="casa",
        area_util=80.0,
        experiencia="iniciante",
        criancas=False,
        outros_animais=True,
    )
    usuario.cadastrar()
    usuario.editar(
        "Junio Silva",
        23,
        "apartamento",
        65.5,
        "intermediaria",
        True,
        False,
    )

    print("\n[2] Animais")
    animal = Animais(
        especie="cachorro",
        raca="vira-lata",
        nome="Bob",
        sexo="M",
        idade_meses=18,
        porte="M",
        estado="SP",
        status="disponivel",
        animal_id=1,
    )
    animal.cadastrar()
    animal.editar(
        "cachorro",
        "vira-lata",
        "Bob Marley",
        "M",
        20,
        "G",
        "SP",
        "reservado",
    )
    animal.adotar()

    print("\n[3] Erro esperado (porte inválido)")
    try:
        Animais(
            especie="cachorro",
            raca="poodle",
            nome="Toby",
            sexo="M",
            idade_meses=5,
            porte="X",
            estado="MG",
        )
    except ValueError as e:
        print("Deu erro (como esperado):", e)

    print("\n[4] Triagem")
    # usa o `usuario` e `animal` já criados acima
    tri = triagem(
        user=usuario,
        animal=animal,
        pontuacao=75,
        elegivel=False,
        observacoes="Teste de compatibilidade",
    )
    tri.cadastrar()
    tri.avaliar()
    elegivel = tri.calcular_compatibilidade()
    print("Triagem elegível?", elegivel)
    tri.validar_politicas()


if __name__ == "__main__":
    main()

