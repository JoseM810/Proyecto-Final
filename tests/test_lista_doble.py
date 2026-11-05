"""Pruebas de ListaDoble (T-01). Soportan INV-01 e INV-02 de 03-feed."""
from estructuras.lista_doble import ListaDoble


# --- insertar_al_inicio ---
def test_insertar_aumenta_tamanio():
    """INV-01: insertar un elemento aumenta el tamaño en uno."""
    lista = ListaDoble()
    lista.insertar_al_inicio("A")
    assert lista.tamanio() == 1


def test_insertar_deja_el_cursor_en_el_nuevo():
    """INV-02: tras insertar, el elemento actual es el último insertado."""
    lista = ListaDoble()
    lista.insertar_al_inicio("A")
    lista.insertar_al_inicio("B")
    assert lista.actual() == "B"


def test_insertar_acepta_duplicados():
    """Caso extremo: el mismo valor dos veces cuenta dos veces."""
    lista = ListaDoble()
    lista.insertar_al_inicio("A")
    lista.insertar_al_inicio("A")
    assert lista.tamanio() == 2


# --- actual ---
def test_actual_en_lista_vacia_es_none():
    """INV-02: sin elementos, actual() es None."""
    assert ListaDoble().actual() is None


# --- avanzar ---
def test_avanzar_va_al_mas_antiguo():
    """CA-01: tras insertar A y luego B, actual es B y avanzar lleva a A."""
    lista = ListaDoble()
    lista.insertar_al_inicio("A")
    lista.insertar_al_inicio("B")
    assert lista.avanzar() is True
    assert lista.actual() == "A"


def test_avanzar_en_el_ultimo_no_se_mueve():
    """CA-03: avanzar en el más antiguo devuelve False y no cambia la posición."""
    lista = ListaDoble()
    lista.insertar_al_inicio("A")
    assert lista.avanzar() is False
    assert lista.actual() == "A"


def test_avanzar_en_lista_vacia_devuelve_false():
    """Caso extremo: con la lista vacía no hay a dónde avanzar."""
    assert ListaDoble().avanzar() is False


# --- retroceder ---
def test_retroceder_vuelve_al_mas_reciente():
    """CA-02: tras avanzar, retroceder deja en el mismo elemento de antes."""
    lista = ListaDoble()
    for x in ("A", "B", "C"):
        lista.insertar_al_inicio(x)
    lista.avanzar()
    assert lista.retroceder() is True
    assert lista.actual() == "C"


def test_retroceder_en_el_primero_no_se_mueve():
    """CA-03: retroceder en el más reciente devuelve False y no cambia la posición."""
    lista = ListaDoble()
    lista.insertar_al_inicio("A")
    lista.insertar_al_inicio("B")
    assert lista.retroceder() is False
    assert lista.actual() == "B"


def test_retroceder_en_lista_vacia_devuelve_false():
    """Caso extremo: con la lista vacía no hay a dónde retroceder."""
    assert ListaDoble().retroceder() is False


# --- enlaces ---
def test_insertar_en_medio_del_recorrido_mantiene_los_enlaces():
    """Riesgo del plan: tras insertar con el cursor en medio, ir y volver pasa por todos."""
    lista = ListaDoble()
    for x in ("A", "B", "C"):
        lista.insertar_al_inicio(x)   # lista: C, B, A
    lista.avanzar()                   # cursor en B
    lista.insertar_al_inicio("D")     # lista: D, C, B, A; cursor en D
    ida = [lista.actual()]
    while lista.avanzar():
        ida.append(lista.actual())
    vuelta = [lista.actual()]
    while lista.retroceder():
        vuelta.append(lista.actual())
    assert ida == ["D", "C",