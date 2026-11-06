"""Pruebas de GrafoDirigido (T-01). Soportan INV-03 e INV-04 de 06-red."""
from estructuras.grafo import GrafoDirigido


def _grafo_con(n):
    """Crea un grafo con n vértices numerados desde 0."""
    grafo = GrafoDirigido()
    for _ in range(n):
        grafo.agregar_vertice()
    return grafo


def _vecinos(grafo, origen):
    """Convierte el recorrido de vecinos en una lista para compararlo."""
    return [v for v in grafo.vecinos(origen)]


# --- vértices ---
def test_agregar_vertice_devuelve_ids_consecutivos():
    """INV-04: los vértices se numeran 0, 1, 2… sin huecos."""
    grafo = GrafoDirigido()
    ids = [grafo.agregar_vertice() for _ in range(4)]
    assert ids == [0, 1, 2, 3]
    assert grafo.cantidad_vertices() == 4


def test_grafo_nuevo_no_tiene_vertices():
    """Caso extremo: un grafo nuevo tiene 0 vértices."""
    assert GrafoDirigido().cantidad_vertices() == 0


# --- agregar_arista ---
def test_agregar_arista_nueva_devuelve_true():
    """INV-03: una arista nueva se agrega y devuelve True."""
    grafo = _grafo_con(3)
    assert grafo.agregar_arista(0, 1) is True
    assert grafo.existe_arista(0, 1) is True


def test_agregar_arista_repetida_no_duplica():
    """INV-03: repetir una arista devuelve False y no la duplica."""
    grafo = _grafo_con(3)
    grafo.agregar_arista(0, 1)
    assert grafo.agregar_arista(0, 1) is False
    assert _vecinos(grafo, 0) == [1]


def test_la_arista_tiene_direccion():
    """Una arista de 0 a 1 no implica una de 1 a 0."""
    grafo = _grafo_con(2)
    grafo.agregar_arista(0, 1)
    assert grafo.existe_arista(1, 0) is False


# --- vecinos ---
def test_vecinos_en_orden_de_insercion():
    """Los vecinos salen en el orden en que se agregaron las aristas."""
    grafo = _grafo_con(4)
    for destino in (3, 1, 2):
        grafo.agregar_arista(0, destino)
    assert _vecinos(grafo, 0) == [3, 1, 2]


def test_vecinos_de_vertice_sin_aristas_es_vacio():
    """Caso extremo: un vértice sin aristas no entrega vecinos y no lanza error."""
    grafo = _grafo_con(3)
    assert _vecinos(grafo, 2) == []


# --- quitar_arista ---
def test_quitar_arista_existente():
    """Quitar una arista presente devuelve True y deja de existir."""
    grafo = _grafo_con(2)
    grafo.agregar_arista(0, 1)
    assert grafo.quitar_arista(0, 1) is True
    assert grafo.existe_arista(0, 1) is False
    assert _vecinos(grafo, 0) == []


def test_quitar_arista_inexistente_devuelve_false():
    """Quitar una arista ausente devuelve False y no cambia nada."""
    grafo = _grafo_con(3)
    assert grafo.quitar_arista(0, 1) is False
    grafo.agregar_arista(0, 2)
    assert grafo.quitar_arista(0, 1) is False
    assert _vecinos(grafo, 0) == [2]


def test_quitar_conserva_el_orden_de_los_demas():
    """Quitar el primero, uno del medio y el último deja los demás en su orden."""
    grafo = _grafo_con(5)
    for destino in (1, 2, 3, 4):
        grafo.agregar_arista(0, destino)
    grafo.quitar_arista(0, 1)
    assert _vecinos(grafo, 0) == [2, 3, 4]
    grafo.quitar_arista(0, 3)
    assert _vecinos(grafo, 0) == [2, 4]
    grafo.quitar_arista(0, 4)
    assert _vecinos(grafo, 0) == [2]


def test_agregar_despues_de_quitar_el_ultimo():
    """Riesgo del plan: tras quitar el último, agregar de nuevo debe enlazar bien."""
    grafo = _grafo_con(5)
    grafo.agregar_arista(0, 1)
    grafo.agregar_arista(0, 2)
    grafo.quitar_arista(0, 2)
    grafo.agregar_arista(0, 3)
    assert _vecinos(grafo, 0) == [1, 3]
    grafo.quitar_arista(0, 1)
    grafo.quitar_arista(0, 3)
    grafo.agregar_arista(0, 4)
    assert _vecinos(grafo, 0) == [4]


# --- muchas aristas ---
def test_muchas_aristas_de_un_vertice():
    """Caso extremo: 500 aristas de un mismo vértice conservan el orden."""
    grafo = _grafo_con(501)
    for destino in range(1, 501):
        assert grafo.agregar_arista(0, destino) is True
    vecinos = _vecinos(grafo, 0)
    assert len(vecinos) == 500
    assert vecinos[0] == 1
    assert vecinos[-1] == 500