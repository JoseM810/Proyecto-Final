"""Pruebas de ColaEnlazada (T-01). Soportan INV-01 e INV-02 de 02-notificaciones."""
import pytest

from estructuras.cola import ColaEnlazada
from estructuras.errores import ColaVaciaError


# --- encolar ---
def test_encolar_aumenta_tamanio():
    """INV-01: encolar un elemento aumenta el tamaño en uno."""
    cola = ColaEnlazada()
    cola.encolar("A")
    assert cola.tamanio() == 1


def test_encolar_en_cola_vacia_deja_ese_elemento_al_frente():
    """Caso extremo: el primer elemento encolado es también el del frente."""
    cola = ColaEnlazada()
    cola.encolar("A")
    assert cola.ver_frente() == "A"


def test_encolar_acepta_duplicados():
    """Caso extremo: el mismo valor dos veces cuenta dos veces."""
    cola = ColaEnlazada()
    cola.encolar("A")
    cola.encolar("A")
    assert cola.tamanio() == 2


# --- desencolar ---
def test_desencolar_devuelve_el_mas_antiguo():
    """INV-02: se sale en el orden en que se entró (primero en entrar, primero en salir)."""
    cola = ColaEnlazada()
    for x in ("A", "B", "C"):
        cola.encolar(x)
    assert cola.desencolar() == "A"
    assert cola.desencolar() == "B"
    assert cola.desencolar() == "C"


def test_desencolar_un_solo_elemento_deja_cola_vacia():
    """Caso extremo: con un elemento, desencolar deja tamaño 0."""
    cola = ColaEnlazada()
    cola.encolar("A")
    cola.desencolar()
    assert cola.tamanio() == 0


def test_desencolar_cola_vacia_lanza_error():
    """Caso extremo: desencolar sin elementos lanza ColaVaciaError."""
    cola = ColaEnlazada()
    with pytest.raises(ColaVaciaError):
        cola.desencolar()


def test_encolar_despues_de_vaciar_la_cola():
    """Riesgo del plan: tras vaciar la cola, encolar de nuevo debe funcionar."""
    cola = ColaEnlazada()
    cola.encolar("A")
    cola.desencolar()
    cola.encolar("B")
    cola.encolar("C")
    assert cola.desencolar() == "B"
    assert cola.desencolar() == "C"
    assert cola.tamanio() == 0


# --- ver_frente ---
def test_ver_frente_no_modifica_la_cola():
    """INV-01: ver_frente no cambia el tamaño."""
    cola = ColaEnlazada()
    cola.encolar("A")
    cola.ver_frente()
    assert cola.tamanio() == 1


def test_ver_frente_cola_vacia_lanza_error():
    """INV-02: sin elementos no hay frente; lanza ColaVaciaError."""
    cola = ColaEnlazada()
    with pytest.raises(ColaVaciaError):
        cola.ver_frente()


# --- tamanio ---
def test_tamanio_cola_nueva_es_cero():
    """INV-01: una cola nueva tiene tamaño 0."""
    assert ColaEnlazada().tamanio() == 0


def test_tamanio_sigue_encolados_menos_desencolados():
    """INV-01: el tamaño refleja encolar y desencolar y nunca baja de 0."""
    cola = ColaEnlazada()
    for i in range(5):
        cola.encolar(i)
    cola.desencolar()
    cola.desencolar()
    assert cola.tamanio() == 3


def test_muchos_elementos_conservan_el_orden():
    """Caso extremo: 10 000 elementos salen en el mismo orden en que entraron."""
    cola = ColaEnlazada()
    for i in range(10_000):
        cola.encolar(i)
    assert cola.tamanio() == 10_000
    assert cola.desencolar() == 0
    assert cola.desencolar() == 1