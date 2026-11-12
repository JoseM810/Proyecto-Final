"""Pruebas de la entidad Usuario. Criterios de specs/00-producto/historias.md."""
import pytest

from dominio.usuario import Usuario


def test_usuario_tiene_id_y_campos():
    """CA-01: el usuario guarda id, username, nombre_visible y biografía."""
    u = Usuario(5, "juan0005", "Juan Pérez", "Desarrollador")
    assert u.id == 5
    assert u.username == "juan0005"
    assert u.nombre_visible == "Juan Pérez"
    assert u.biografia == "Desarrollador"


def test_usuario_biografia_por_defecto_vacia():
    """CA-01: la biografía es cadena vacía si no se indica."""
    u = Usuario(0, "ana0000", "Ana")
    assert u.biografia == ""


def test_usuario_tiene_feed_vacio_inicialmente():
    """CA-02: un usuario nuevo tiene su feed con cantidad 0."""
    u = Usuario(1, "luis0001", "Luis")
    assert u.feed.cantidad() == 0
    assert u.feed.actual() is None


def test_usuario_tiene_bandeja_vacia_inicialmente():
    """CA-03: un usuario nuevo tiene su bandeja con 0 pendientes."""
    u = Usuario(1, "luis0001", "Luis")
    assert u.cantidad_notificaciones() == 0


def test_usuario_publicar_en_feed():
    """HU-03 CA-01: el usuario puede publicar y el feed lo registra."""
    u = Usuario(1, "luis0001", "Luis")
    u.publicar("Hola mundo", 1)
    assert u.feed.cantidad() == 1
    assert u.feed.actual().texto == "Hola mundo"


def test_usuario_agregar_notificacion():
    """HU-07 CA-01: el usuario recibe notificaciones en su bandeja."""
    u = Usuario(1, "luis0001", "Luis")
    u.agregar_notificacion("NUEVO_SEGUIDOR", "ana0000")
    assert u.cantidad_notificaciones() == 1


def test_usuario_feed_y_bandeja_son_independientes():
    """Caso extremo: publicar y notificar no interfieren entre sí."""
    u = Usuario(2, "eva0002", "Eva")
    u.publicar("Post 1", 1)
    u.agregar_notificacion("COMENTARIO", "ana0000")
    assert u.feed.cantidad() == 1
    assert u.cantidad_notificaciones() == 1
