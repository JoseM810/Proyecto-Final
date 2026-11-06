"""Pruebas de IndiceUsuarios (T-02 y T-03). Criterios de specs/05-indice-usuarios/spec.md."""
import pytest

from dominio.indice_usuarios import IndiceUsuarios
from estructuras.errores import EntradaInvalidaError, NombreDuplicadoError


def _nombres(indice):
    """Convierte listar() en una lista para poder compararla."""
    return [nombre for nombre in indice.listar()]


# --- buscar ---
def test_buscar_existente():
    """CA-01: buscar un nombre registrado devuelve ese usuario."""
    indice = IndiceUsuarios()
    ana = object()
    indice.agregar("Ana", ana)
    assert indice.buscar("Ana") is ana


def test_buscar_devuelve_el_usuario_correcto():
    """CA-01: con varios usuarios, cada nombre devuelve el suyo."""
    indice = IndiceUsuarios()
    ana, luis, sara = object(), object(), object()
    indice.agregar("Luis", luis)
    indice.agregar("Ana", ana)
    indice.agregar("Sara", sara)
    assert indice.buscar("Ana") is ana
    assert indice.buscar("Luis") is luis
    assert indice.buscar("Sara") is sara


def test_buscar_inexistente():
    """CA-02: buscar un nombre inexistente devuelve None y no lanza error, también con el índice vacío."""
    indice = IndiceUsuarios()
    assert indice.buscar("Ana") is None
    indice.agregar("Luis", object())
    assert indice.buscar("Ana") is None


def test_buscar_nombre_que_no_es_texto():
    """CA-02: un nombre que no es texto devuelve None y no lanza error."""
    indice = IndiceUsuarios()
    indice.agregar("Ana", object())
    assert indice.buscar(None) is None
    assert indice.buscar(5) is None


def test_buscar_distingue_mayusculas():
    """Spec: 'Ana' y 'ana' son nombres distintos."""
    indice = IndiceUsuarios()
    indice.agregar("Ana", object())
    assert indice.buscar("ana") is None


# --- agregar ---
def test_agregar_duplicado():
    """CA-04: un nombre ya existente lanza NombreDuplicadoError, no cambia cantidad() y conserva el original."""
    indice = IndiceUsuarios()
    original = object()
    indice.agregar("Ana", original)
    with pytest.raises(NombreDuplicadoError):
        indice.agregar("Ana", object())
    assert indice.cantidad() == 1
    assert indice.buscar("Ana") is original


def test_agregar_invalido():
    """CA-05: nombre vacío o no texto, o usuario nulo, lanza EntradaInvalidaError y no cambia cantidad()."""
    indice = IndiceUsuarios()
    indice.agregar("Ana", object())
    casos = [("", object()), (None, object()), (5, object()), ("Luis", None)]
    for nombre, usuario in casos:
        with pytest.raises(EntradaInvalidaError):
            indice.agregar(nombre, usuario)
    assert indice.cantidad() == 1


def test_invalido_se_revisa_antes_que_duplicado():
    """CA-05: si el nombre ya existe pero el usuario es nulo, el error es EntradaInvalidaError."""
    indice = IndiceUsuarios()
    indice.agregar("Ana", object())
    with pytest.raises(EntradaInvalidaError):
        indice.agregar("Ana", None)


def test_nombres_con_espacios_y_tildes():
    """Caso extremo: los nombres con espacios y tildes se guardan y se encuentran."""
    indice = IndiceUsuarios()
    jose, maria = object(), object()
    indice.agregar("José Pérez", jose)
    indice.agregar("Ana María", maria)
    assert indice.buscar("José Pérez") is jose
    assert indice.buscar("Ana María") is maria


# --- listar ---
def test_listar_en_orden():
    """CA-03: listar entrega los nombres en orden alfabético sin importar el orden en que se agregaron."""
    indice = IndiceUsuarios()
    for nombre in ("Sara", "Ana", "Luis", "Eva"):
        indice.agregar(nombre, object())
    assert _nombres(indice) == ["Ana", "Eva", "Luis", "Sara"]


def test_listar_mayusculas_antes_que_minusculas():
    """CA-03: la comparación es la de Python, así que las mayúsculas van antes que las minúsculas."""
    indice = IndiceUsuarios()
    for nombre in ("ana", "Zoe", "Ana"):
        indice.agregar(nombre, object())
    assert _nombres(indice) == ["Ana", "Zoe", "ana"]


def test_indice_vacio():
    """CA-06: un índice vacío tiene cantidad() 0 y listar() no entrega nada ni lanza error."""
    indice = IndiceUsuarios()
    assert indice.cantidad() == 0
    assert _nombres(indice) == []


def test_nombres_ya_ordenados():
    """CA-07: con 2 000 nombres agregados ya ordenados, buscar encuentra el primero, uno del medio y el último, y listar() los entrega todos."""
    indice = IndiceUsuarios()
    nombres = [f"usuario{i:04d}" for i in range(2_000)]
    for nombre in nombres:
        indice.agregar(nombre, nombre)
    assert indice.buscar(nombres[0]) == nombres[0]
    assert indice.buscar(nombres[1_000]) == nombres[1_000]
    assert indice.buscar(nombres[-1]) == nombres[-1]
    assert _nombres(indice) == nombres
    assert indice.cantidad() == 2_000


def test_nombres_en_orden_inverso():
    """CA-03 (caso extremo): 2 000 nombres agregados al revés salen igual en orden ascendente."""
    indice = IndiceUsuarios()
    nombres = [f"usuario{i:04d}" for i in range(2_000)]
    for nombre in reversed(nombres):
        indice.agregar(nombre, nombre)
    assert _nombres(indice) == nombres


# --- cantidad ---
def test_cantidad_inicial_es_cero():
    """INV-01: un índice nuevo tiene cantidad 0."""
    assert IndiceUsuarios().cantidad() == 0


def test_listar_no_modifica_el_indice():
    """Spec: listar no cambia el índice; dos listados seguidos dan lo mismo."""
    indice = IndiceUsuarios()
    for nombre in ("Sara", "Ana"):
        indice.agregar(nombre, object())
    primero = _nombres(indice)
    segundo = _nombres(indice)
    assert primero == segundo
    assert indice.cantidad() == 2