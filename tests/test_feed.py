"""Pruebas de Feed (T-02 y T-03). Criterios de specs/03-feed/spec.md."""
import pytest

from dominio.feed import Feed
from estructuras.errores import (
    BusquedaInvalidaError,
    FinDelFeedError,
    InicioDelFeedError,
    PublicacionInvalidaError,
)


# --- publicar ---
def test_publicar_aumenta_cantidad():
    """INV-01: publicar sube cantidad() en uno."""
    feed = Feed()
    feed.publicar("hola", 1)
    assert feed.cantidad() == 1


def test_publicar_guarda_texto_y_fecha():
    """CA-01: la publicación conserva su texto y su fecha."""
    feed = Feed()
    feed.publicar("hola", 5)
    assert feed.actual().texto == "hola"
    assert feed.actual().fecha == 5


def test_publicar_invalida():
    """CA-05: texto vacío o fecha inválida lanza PublicacionInvalidaError y no cambia cantidad()."""
    feed = Feed()
    feed.publicar("hola", 1)
    casos = [("", 1), (None, 1), ("x", -1), ("x", "ayer"), ("x", None), ("x", True)]
    for texto, fecha in casos:
        with pytest.raises(PublicacionInvalidaError):
            feed.publicar(texto, fecha)
    assert feed.cantidad() == 1


def test_publicar_en_medio_del_recorrido_deja_la_nueva_actual():
    """Caso extremo: publicar con el cursor en medio hace que la nueva sea la actual."""
    feed = Feed()
    feed.publicar("A", 1)
    feed.publicar("B", 2)
    feed.avanzar()
    feed.publicar("C", 3)
    assert feed.actual().texto == "C"
    assert feed.cantidad() == 3


# --- actual / feed vacío ---
def test_feed_vacio():
    """CA-04: con el feed vacío, actual() es None, cantidad() es 0 y no hay error."""
    feed = Feed()
    assert feed.actual() is None
    assert feed.cantidad() == 0


# --- orden y recorrido ---
def test_la_mas_reciente_aparece_primero():
    """CA-01: tras publicar A y luego B, actual() es B y avanzar() lleva a A."""
    feed = Feed()
    feed.publicar("A", 1)
    feed.publicar("B", 2)
    assert feed.actual().texto == "B"
    assert feed.avanzar().texto == "A"


def test_avanzar_y_retroceder():
    """CA-02: avanzar y luego retroceder deja en la misma publicación."""
    feed = Feed()
    feed.publicar("A", 1)
    feed.publicar("B", 2)
    feed.publicar("C", 3)
    feed.avanzar()
    feed.retroceder()
    assert feed.actual().texto == "C"


def test_limites_del_feed():
    """CA-03: retroceder en la más reciente y avanzar en la más antigua lanzan error sin mover la posición."""
    feed = Feed()
    feed.publicar("A", 1)
    feed.publicar("B", 2)
    with pytest.raises(InicioDelFeedError):
        feed.retroceder()
    assert feed.actual().texto == "B"
    feed.avanzar()
    with pytest.raises(FinDelFeedError):
        feed.avanzar()
    assert feed.actual().texto == "A"


def test_una_sola_publicacion_no_se_puede_mover():
    """Caso extremo: con una publicación, avanzar y retroceder lanzan error."""
    feed = Feed()
    feed.publicar("A", 1)
    with pytest.raises(FinDelFeedError):
        feed.avanzar()
    with pytest.raises(InicioDelFeedError):
        feed.retroceder()
    assert feed.actual().texto == "A"


def test_avanzar_con_feed_vacio_lanza_fin_del_feed():
    """CA-03: con el feed vacío no hay a dónde avanzar."""
    with pytest.raises(FinDelFeedError):
        Feed().avanzar()


def test_retroceder_con_feed_vacio_lanza_inicio_del_feed():
    """CA-03: con el feed vacío no hay a dónde retroceder."""
    with pytest.raises(InicioDelFeedError):
        Feed().retroceder()


# --- cantidad ---
def test_cantidad_no_cambia_al_recorrer():
    """INV-01: avanzar y retroceder no modifican cantidad()."""
    feed = Feed()
    feed.publicar("A", 1)
    feed.publicar("B", 2)
    feed.avanzar()
    feed.retroceder()
    assert feed.cantidad() == 2


def test_muchas_publicaciones():
    """Caso extremo: 5 000 publicaciones, la más reciente aparece primero."""
    feed = Feed()
    for i in range(5_000):
        feed.publicar(f"post{i}", i)
    assert feed.cantidad() == 5_000
    assert feed.actual().texto == "post4999"


# --- buscar (v1.1) ---
def _textos(resultado):
    """Convierte el resultado de buscar en una lista de textos."""
    return [p.texto for p in resultado]


def test_buscar_por_palabra():
    """CA-06: entrega solo las que contienen la palabra, sin distinguir mayúsculas, la más reciente primero."""
    feed = Feed()
    feed.publicar("Hola mundo", 1)
    feed.publicar("Estructuras de datos", 2)
    feed.publicar("Otro MUNDO", 3)
    assert _textos(feed.buscar("mundo")) == ["Otro MUNDO", "Hola mundo"]


def test_buscar_encuentra_la_palabra_dentro_del_texto():
    """CA-06 (caso extremo): una palabra que aparece dentro de otra también coincide."""
    feed = Feed()
    feed.publicar("Hola mundo", 1)
    assert _textos(feed.buscar("mun")) == ["Hola mundo"]


def test_buscar_sin_coincidencias():
    """CA-07: sin coincidencias, o con el feed vacío, no entrega nada y no lanza error."""
    feed = Feed()
    assert _textos(feed.buscar("hola")) == []
    feed.publicar("Hola mundo", 1)
    assert _textos(feed.buscar("adios")) == []


def test_buscar_palabra_invalida():
    """CA-08: una palabra vacía o que no es texto lanza BusquedaInvalidaError al llamar a buscar."""
    feed = Feed()
    feed.publicar("Hola", 1)
    for palabra in ("", None, 5):
        with pytest.raises(BusquedaInvalidaError):
            feed.buscar(palabra)
    assert feed.cantidad() == 1


def test_buscar_no_modifica_el_feed():
    """CA-09: buscar no cambia la posición actual ni cantidad()."""
    feed = Feed()
    for texto in ("A uno", "B dos", "C tres"):
        feed.publicar(texto, 1)
    feed.avanzar()
    _textos(feed.buscar("dos"))
    assert feed.actual().texto == "B dos"
    assert feed.cantidad() == 3


def test_buscar_en_muchas_publicaciones():
    """CA-06 (caso extremo): entre 2 000 publicaciones, 20 contienen la palabra y salen en orden."""
    feed = Feed()
    for i in range(2_000):
        texto = f"especial {i}" if i % 100 == 0 else f"normal {i}"
        feed.publicar(texto, i)
    encontrados = _textos(feed.buscar("especial"))
    assert len(encontrados) == 20
    assert encontrados[0] == "especial 1900"
    assert encontrados[-1] == "especial 0"