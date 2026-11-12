"""Pruebas de GeneradorUsuarios. Criterios de HU-01 en specs/00-producto/historias.md."""
import pytest

from dominio.generador_usuarios import GeneradorUsuarios


def test_generador_produce_mismos_usuarios_con_misma_semilla():
    """HU-01 CA-01: misma semilla genera mismos usuarios en mismo orden."""
    datos1 = GeneradorUsuarios(42).generar(10)
    datos2 = GeneradorUsuarios(42).generar(10)
    assert datos1 == datos2


def test_generador_semilla_distinta_produce_datos_distintos():
    """Caso extremo: semillas diferentes generan biografías diferentes."""
    datos1 = GeneradorUsuarios(1).generar(5)
    datos2 = GeneradorUsuarios(2).generar(5)
    assert datos1 != datos2


def test_generador_produce_al_menos_100_usuarios():
    """HU-01 CA-02: se generan al menos 100 usuarios."""
    datos = GeneradorUsuarios(42).generar(100)
    assert len(datos) == 100


def test_generador_cantidad_personalizable():
    """Caso extremo: se puede generar cualquier cantidad de usuarios."""
    datos = GeneradorUsuarios(7).generar(250)
    assert len(datos) == 250


def test_generador_nombres_unicos():
    """HU-01 CA-02: cada usuario tiene un nombre único."""
    datos = GeneradorUsuarios(42).generar(100)
    usernames = [d[0] for d in datos]
    assert len(usernames) == len(set(usernames))


def test_generador_nombres_secuenciales():
    """Caso extremo: los nombres son usuario0000, usuario0001, …"""
    datos = GeneradorUsuarios(42).generar(5)
    assert datos[0][0] == "usuario0000"
    assert datos[1][0] == "usuario0001"
    assert datos[4][0] == "usuario0004"


def test_generador_todos_tienen_nombre_visible_y_biografia():
    """Caso extremo: cada entrada tiene los tres campos esperados."""
    datos = GeneradorUsuarios(42).generar(3)
    for username, nombre_visible, biografia in datos:
        assert username != ""
        assert nombre_visible != ""
        assert biografia != ""
