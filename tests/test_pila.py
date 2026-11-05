"""Pruebas de PilaEnlazada (T-01). Soportan INV-01 e INV-02 de 01-historial."""
import pytest

from estructuras.pila import PilaEnlazada
from estructuras.errores import PilaVaciaError

#--- apilar ----
def test_apilar_aumenta_tamanio():
    """INV-01: apilar un elemento aumenta el tamaño en uno."""
    pila = PilaEnlazada()
    pila.apilar("A")
    assert pila.tamanio() == 1


def test_apilar_deja_el_ultimo_en_el_tope():
    """INV-02: tras apilar varios, el tope es el último apilado."""
    pila = PilaEnlazada()
    for pantalla in ("A", "B", "C"):
        pila.apilar(pantalla)
    assert pila.ver_tope() == "C"


def test_apilar_acepta_duplicados():
    """Caso extremo: el mismo valor dos veces seguidas cuenta dos veces."""
    pila = PilaEnlazada()
    pila.apilar("A")
    pila.apilar("A")
    assert pila.tamanio() == 2


# --- desapilar ---
def test_desapilar_devuelve_el_ultimo_apilado():
    """INV-02: desapilar devuelve el tope y deja el anterior como tope."""
    pila = PilaEnlazada()
    pila.apilar("A")
    pila.apilar("B")
    assert pila.desapilar() == "B"
    assert pila.ver_tope() == "A"


def test_desapilar_un_solo_elemento_deja_pila_vacia():
    """Caso extremo: con un elemento, desapilar deja tamaño 0."""
    pila = PilaEnlazada()
    pila.apilar("A")
    pila.desapilar()
    assert pila.tamanio() == 0


def test_desapilar_pila_vacia_lanza_error():
    """Caso extremo: desapilar sin elementos lanza PilaVaciaError."""
    pila = PilaEnlazada()
    with pytest.raises(PilaVaciaError):
        pila.desapilar()


# --- ver_tope ---
def test_ver_tope_no_modifica_la_pila():
    """INV-01: ver_tope no cambia el tamaño."""
    pila = PilaEnlazada()
    pila.apilar("A")
    pila.ver_tope()
    assert pila.tamanio() == 1


def test_ver_tope_pila_vacia_lanza_error():
    """INV-02: sin elementos no hay tope; lanza PilaVaciaError."""
    pila = PilaEnlazada()
    with pytest.raises(PilaVaciaError):
        pila.ver_tope()


def test_ver_tope_un_elemento():
    """Caso extremo: con un solo elemento, ese es el tope."""
    pila = PilaEnlazada()
    pila.apilar("A")
    assert pila.ver_tope() == "A"


# --- tamanio ---
def test_tamanio_pila_nueva_es_cero():
    """INV-01: una pila nueva tiene tamaño 0."""
    assert PilaEnlazada().tamanio() == 0


def test_tamanio_sigue_apilados_menos_desapilados():
    """INV-01: el tamaño nunca baja de 0 y refleja apilar/desapilar."""
    pila = PilaEnlazada()
    for i in range(5):
        pila.apilar(i)
    pila.desapilar()
    pila.desapilar()
    assert pila.tamanio() == 3


def test_tamanio_con_muchos_elementos():
    """Caso extremo: 10 000 elementos, sin recorrer la pila para contarlos."""
    pila = PilaEnlazada()
    for i in range(10_000):
        pila.apilar(i)
    assert pila.tamanio() == 10_000
    