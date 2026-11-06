"""Pruebas de ArbolBST (T-01). Soportan INV-01, INV-02 e INV-03 de 05-indice-usuarios."""
from estructuras.arbol_bst import ArbolBST


def _claves(arbol):
    """Convierte el recorrido en orden en una lista para poder compararlo."""
    return [clave for clave in arbol.recorrer_en_orden()]


# --- insertar ---
def test_insertar_en_arbol_vacio_sube_tamanio():
    """INV-01: insertar una clave nueva devuelve True y sube el tamaño en uno."""
    arbol = ArbolBST()
    assert arbol.insertar("m", 1) is True
    assert arbol.tamanio() == 1


def test_insertar_clave_repetida_devuelve_false_y_conserva_el_valor():
    """INV-02: una clave repetida devuelve False, no cambia el tamaño ni el valor."""
    arbol = ArbolBST()
    arbol.insertar("a", 1)
    assert arbol.insertar("a", 2) is False
    assert arbol.tamanio() == 1
    assert arbol.buscar("a") == 1


def test_tamanio_nuevo_es_cero():
    """INV-01: un árbol nuevo tiene tamaño 0."""
    assert ArbolBST().tamanio() == 0


# --- buscar ---
def test_buscar_clave_existente():
    """Buscar una clave presente devuelve su valor, esté a la izquierda, a la derecha o en la raíz."""
    arbol = ArbolBST()
    for clave, valor in (("m", 1), ("c", 2), ("x", 3)):
        arbol.insertar(clave, valor)
    assert arbol.buscar("m") == 1
    assert arbol.buscar("c") == 2
    assert arbol.buscar("x") == 3


def test_buscar_clave_inexistente_devuelve_none():
    """Buscar una clave ausente devuelve None."""
    arbol = ArbolBST()
    arbol.insertar("m", 1)
    assert arbol.buscar("z") is None


def test_buscar_en_arbol_vacio_devuelve_none():
    """Caso extremo: buscar en un árbol vacío devuelve None y no lanza error."""
    assert ArbolBST().buscar("a") is None


# --- recorrer_en_orden ---
def test_recorrer_entrega_las_claves_en_orden():
    """INV-03: el recorrido en orden entrega las claves de menor a mayor."""
    arbol = ArbolBST()
    for clave in ("m", "c", "x", "a", "e", "t", "z"):
        arbol.insertar(clave, clave)
    assert _claves(arbol) == ["a", "c", "e", "m", "t", "x", "z"]


def test_recorrer_arbol_vacio():
    """Caso extremo: un árbol vacío no entrega nada y no lanza error."""
    assert _claves(ArbolBST()) == []


def test_recorrer_un_solo_elemento():
    """Caso extremo: con una sola clave, el recorrido la entrega a ella sola."""
    arbol = ArbolBST()
    arbol.insertar("m", 1)
    assert _claves(arbol) == ["m"]


def test_recorrer_no_modifica_el_arbol():
    """Dos recorridos seguidos dan lo mismo y el tamaño no cambia."""
    arbol = ArbolBST()
    for clave in ("m", "c", "x"):
        arbol.insertar(clave, clave)
    primero = _claves(arbol)
    segundo = _claves(arbol)
    assert primero == segundo
    assert arbol.tamanio() == 3


def test_permutacion_sale_ordenada():
    """INV-03: 101 claves insertadas en desorden salen en orden estrictamente ascendente."""
    arbol = ArbolBST()
    for i in range(101):
        clave = (i * 37) % 101
        arbol.insertar(clave, clave)
    assert _claves(arbol) == list(range(101))
    assert arbol.tamanio() == 101


# --- árbol degenerado ---
def test_claves_ascendentes_no_desbordan():
    """Caso extremo: 1 000 claves ya ordenadas forman una rama larga y todo sigue funcionando sin recursión."""
    arbol = ArbolBST()
    for i in range(1_000):
        arbol.insertar(i, i)
    assert arbol.tamanio() == 1_000
    assert arbol.buscar(999) == 999
    assert _claves(arbol) == list(range(1_000))


def test_claves_descendentes_no_desbordan():
    """Caso extremo: 1 000 claves en orden inverso, igual que el caso anterior."""
    arbol = ArbolBST()
    for i in range(999, -1, -1):
        arbol.insertar(i, i)
    assert arbol.tamanio() == 1_000
    assert arbol.buscar(0) == 0
    assert _claves(arbol) == list(range(1_000))