"""Pruebas de Historial (T-02 y T-03). Criterios de specs/01-historial/spec.md."""
import pytest

from dominio.historial import Historial
from estructuras.errores import NadaAtrasError, PantallaInvalidaError


# --- visitar ---
def test_visitar_cambia_la_pantalla_actual():
    """INV-02: tras visitar, esa pantalla es la actual."""
    h = Historial()
    h.visitar("inicio")
    assert h.actual() == "inicio"


def test_visitar_invalida_lanza_error_y_no_cambia_cantidad():
    """CA-04: pantalla nula o vacía lanza PantallaInvalidaError y no cambia cantidad()."""
    h = Historial()
    h.visitar("inicio")
    for invalida in (None, ""):
        with pytest.raises(PantallaInvalidaError):
            h.visitar(invalida)
    assert h.cantidad() == 1


def test_visitar_la_misma_pantalla_dos_veces_cuenta_dos():
    """Caso extremo: repetir la pantalla seguida cuenta como dos visitas."""
    h = Historial()
    h.visitar("feed")
    h.visitar("feed")
    assert h.cantidad() == 2


# --- volver ---
def test_volver_en_orden():
    """CA-01: tras visitar A, B y C, volver lleva a B y luego a A."""
    h = Historial()
    for p in ("A", "B", "C"):
        h.visitar(p)
    assert h.volver() == "B"
    assert h.volver() == "A"


def test_volver_sin_anterior():
    """CA-02: volver con cero o una sola pantalla lanza NadaAtrasError."""
    h = Historial()
    with pytest.raises(NadaAtrasError):
        h.volver()
    h.visitar("A")
    with pytest.raises(NadaAtrasError):
        h.volver()


def test_visitar_tras_volver():
    """CA-03: A, B, C; volver (B); visitar D; volver lleva a B y C ya no es alcanzable."""
    h = Historial()
    for p in ("A", "B", "C"):
        h.visitar(p)
    h.volver()
    h.visitar("D")
    assert h.volver() == "B"
    assert h.cantidad() == 2  # solo A y B quedan; C desapareció


def test_volver_no_deja_el_historial_vacio():
    """INV-02: aun tras volver hasta el límite, siempre queda una pantalla actual."""
    h = Historial()
    h.visitar("A")
    h.visitar("B")
    h.volver()
    assert h.actual() == "A"


# --- actual ---
def test_actual_sin_visitas_es_none():
    """INV-02: actual() es None si y solo si cantidad() es 0."""
    h = Historial()
    assert h.actual() is None
    assert h.cantidad() == 0


def test_actual_devuelve_la_ultima_visitada():
    """CA-01: la actual es siempre la más reciente."""
    h = Historial()
    h.visitar("A")
    h.visitar("B")
    assert h.actual() == "B"


def test_actual_no_modifica_el_historial():
    """INV-01: consultar la actual no cambia la cantidad."""
    h = Historial()
    h.visitar("A")
    h.actual()
    h.actual()
    assert h.cantidad() == 1


# --- cantidad ---
def test_cantidad_inicial_es_cero():
    """INV-01: un historial nuevo tiene cantidad 0."""
    assert Historial().cantidad() == 0


def test_cantidad_cuenta_la_actual():
    """Spec: cantidad() cuenta las pantallas alcanzables, incluida la actual."""
    h = Historial()
    for p in ("A", "B", "C"):
        h.visitar(p)
    assert h.cantidad() == 3


def test_cantidad_baja_al_volver():
    """INV-01: volver reduce la cantidad en uno y nunca baja de 0."""
    h = Historial()
    h.visitar("A")
    h.visitar("B")
    h.volver()
    assert h.cantidad() == 1