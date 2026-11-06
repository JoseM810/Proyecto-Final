"""Pruebas de RedSeguimiento (T-02 y T-03). Criterios de specs/06-red/spec.md."""
import pytest

from dominio.red import RedSeguimiento
from estructuras.errores import AutoSeguimientoError, UsuarioNoExisteError


def _red_con(n):
    """Crea una red con n usuarios numerados desde 0."""
    red = RedSeguimiento()
    for _ in range(n):
        red.agregar_usuario()
    return red


def _seguidos(red, a):
    return [x for x in red.seguidos(a)]


def _recomendados(red, a):
    return [x for x in red.recomendar(a)]


# --- usuarios ---
def test_ids_consecutivos():
    """CA-01: los identificadores son 0, 1, 2… y cantidad_usuarios() sube en uno cada vez."""
    red = RedSeguimiento()
    ids = []
    for i in range(3):
        ids.append(red.agregar_usuario())
        assert red.cantidad_usuarios() == i + 1
    assert ids == [0, 1, 2]


def test_red_nueva_sin_usuarios():
    """INV-01: una red nueva tiene 0 usuarios."""
    assert RedSeguimiento().cantidad_usuarios() == 0


# --- seguir ---
def test_seguir_y_aparece():
    """CA-02: tras seguir(A, B) devuelve True, sigue(A, B) es True y B aparece en seguidos(A)."""
    red = _red_con(3)
    assert red.seguir(0, 1) is True
    assert red.sigue(0, 1) is True
    assert 1 in _seguidos(red, 0)


def test_seguir_repetido():
    """CA-03: seguir a quien ya sigo devuelve False, no lo duplica y no lanza error."""
    red = _red_con(3)
    red.seguir(0, 1)
    assert red.seguir(0, 1) is False
    assert _seguidos(red, 0) == [1]


def test_seguir_a_si_mismo():
    """CA-04: seguir a uno mismo lanza AutoSeguimientoError y no cambia nada."""
    red = _red_con(2)
    with pytest.raises(AutoSeguimientoError):
        red.seguir(0, 0)
    assert _seguidos(red, 0) == []
    assert red.sigue(0, 0) is False


def test_relacion_dirigida():
    """CA-05: si A sigue a B, sigue(B, A) es False y B no sigue a nadie."""
    red = _red_con(2)
    red.seguir(0, 1)
    assert red.sigue(1, 0) is False
    assert _seguidos(red, 1) == []


# --- dejar de seguir ---
def test_dejar_de_seguir():
    """CA-06: dejar de seguir a quien sigo devuelve True y lo quita sin alterar el orden de los demás."""
    red = _red_con(4)
    for destino in (1, 2, 3):
        red.seguir(0, destino)
    assert red.dejar_de_seguir(0, 2) is True
    assert _seguidos(red, 0) == [1, 3]
    assert red.sigue(0, 2) is False


def test_dejar_de_seguir_a_quien_no_sigo():
    """CA-06: dejar de seguir a quien no sigo devuelve False y no cambia nada."""
    red = _red_con(3)
    red.seguir(0, 1)
    assert red.dejar_de_seguir(0, 2) is False
    assert red.dejar_de_seguir(1, 0) is False
    assert _seguidos(red, 0) == [1]


# --- identificadores inexistentes ---
def test_usuario_inexistente():
    """CA-07: un identificador inexistente lanza UsuarioNoExisteError en cada operación y no cambia nada."""
    red = _red_con(2)
    red.seguir(0, 1)
    for malo in (-1, 2, 99, True, 1.5, "0", None):
        operaciones = (
            lambda: red.seguir(0, malo),
            lambda: red.seguir(malo, 0),
            lambda: red.dejar_de_seguir(0, malo),
            lambda: red.dejar_de_seguir(malo, 0),
            lambda: red.sigue(0, malo),
            lambda: red.sigue(malo, 0),
            lambda: red.seguidos(malo),
            lambda: red.recomendar(malo),
        )
        for operacion in operaciones:
            with pytest.raises(UsuarioNoExisteError):
                operacion()
    assert red.cantidad_usuarios() == 2
    assert _seguidos(red, 0) == [1]


def test_usuario_inexistente_en_red_vacia():
    """CA-07 (caso extremo): en una red sin usuarios, toda operación con un id lanza UsuarioNoExisteError."""
    red = RedSeguimiento()
    operaciones = (
        lambda: red.seguir(0, 1),
        lambda: red.dejar_de_seguir(0, 1),
        lambda: red.sigue(0, 1),
        lambda: red.seguidos(0),
        lambda: red.recomendar(0),
    )
    for operacion in operaciones:
        with pytest.raises(UsuarioNoExisteError):
            operacion()


def test_validacion_antes_que_autoseguimiento():
    """CA-07: si el identificador no existe, el error es UsuarioNoExisteError aunque a sea igual a b."""
    red = _red_con(2)
    with pytest.raises(UsuarioNoExisteError):
        red.seguir(99, 99)


# --- seguidos ---
def test_seguidos_en_orden():
    """CA-08: seguidos(A) entrega a quienes A sigue en el orden en que empezó a seguirlos."""
    red = _red_con(5)
    for destino in (3, 1, 4, 2):
        red.seguir(0, destino)
    assert _seguidos(red, 0) == [3, 1, 4, 2]


def test_seguidos_de_usuario_sin_relaciones():
    """CA-08 (caso extremo): un usuario sin relaciones no entrega seguidos y no lanza error."""
    red = _red_con(3)
    assert _seguidos(red, 2) == []


# --- recomendar ---
def test_recomendar_a_dos_saltos():
    """CA-09: si A sigue a B y B sigue a C, se recomienda C; una persona a tres relaciones no."""
    red = _red_con(4)
    red.seguir(0, 1)
    red.seguir(1, 2)
    red.seguir(2, 3)
    assert _recomendados(red, 0) == [2]
    assert _recomendados(red, 1) == [3]


def test_recomendar_sin_repetidos_ni_conocidos():
    """CA-10: nunca se recomienda a A ni a quienes A ya sigue, ni se repite a nadie."""
    red = _red_con(4)
    red.seguir(0, 1)
    red.seguir(0, 2)
    red.seguir(1, 2)
    red.seguir(1, 3)
    red.seguir(2, 3)
    red.seguir(2, 0)
    assert _recomendados(red, 0) == [3]


def test_recomendar_sin_candidatos():
    """CA-11: sin seguidos, o con seguidos que no siguen a nadie, devuelve vacío y no lanza error."""
    red = _red_con(3)
    assert _recomendados(red, 0) == []
    red.seguir(0, 1)
    assert _recomendados(red, 0) == []


def test_recomendar_orden():
    """CA-12: se recorren los seguidos de A en su orden y, de cada uno, sus seguidos en su orden."""
    red = _red_con(6)
    red.seguir(0, 1)
    red.seguir(0, 2)
    red.seguir(1, 4)
    red.seguir(1, 3)
    red.seguir(2, 3)
    red.seguir(2, 5)
    assert _recomendados(red, 0) == [4, 3, 5]


def test_recomendar_con_ciclo():
    """Caso extremo: con A sigue a B y B sigue a A, no se recomienda a A y sí a lo que sigue B."""
    red = _red_con(3)
    red.seguir(0, 1)
    red.seguir(1, 0)
    red.seguir(1, 2)
    assert _recomendados(red, 0) == [2]


def test_recomendar_no_modifica_la_red():
    """Spec: recomendar no cambia la red; dos llamadas seguidas dan lo mismo."""
    red = _red_con(4)
    red.seguir(0, 1)
    red.seguir(1, 2)
    red.seguir(1, 3)
    primero = _recomendados(red, 0)
    segundo = _recomendados(red, 0)
    assert primero == segundo == [2, 3]
    assert _seguidos(red, 0) == [1]
    assert _seguidos(red, 1) == [2, 3]


def test_recomendar_tras_dejar_de_seguir():
    """CA-09 (caso extremo): al dejar de seguir al intermediario, la recomendación desaparece."""
    red = _red_con(3)
    red.seguir(0, 1)
    red.seguir(1, 2)
    assert _recomendados(red, 0) == [2]
    red.dejar_de_seguir(0, 1)
    assert _recomendados(red, 0) == []


def test_muchos_usuarios_y_relaciones():
    """Caso extremo: 100 usuarios, cada uno sigue a los 5 siguientes; todo sigue funcionando."""
    red = _red_con(100)
    for i in range(100):
        for paso in range(1, 6):
            assert red.seguir(i, (i + paso) % 100) is True
    assert _seguidos(red, 0) == [1, 2, 3, 4, 5]
    assert _recomendados(red, 0) == [6, 7, 8, 9, 10]