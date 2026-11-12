"""Pruebas de la interfaz de consola (main.py).

Verifica las tareas M-01, M-02 y M-03.
"""

import io
import pytest
from unittest.mock import patch

from dominio.sistema_red import SistemaRed

import main


def test_mostrar_menu_muestra_opciones():
    """M-01 CA-01: El menú muestra el título y la opción de salida."""
    salida = io.StringIO()
    with patch("sys.stdout", salida):
        main.mostrar_menu()
    texto = salida.getvalue()
    assert "RED SOCIAL - MENÚ PRINCIPAL" in texto
    assert "0. Salir" in texto


def test_opcion_no_implementada_muestra_mensaje():
    """M-01 CA-02: La opción no implementada muestra un mensaje descriptivo."""
    salida = io.StringIO()
    with patch("sys.stdout", salida):
        main.opcion_no_implementada("5")
    texto = salida.getvalue()
    assert "5" in texto
    assert "no está implementada" in texto


def test_salir_termina_programa():
    """M-01 CA-03: La opción salir termina el programa con código 0."""
    try:
        main.salir()
    except SystemExit as e:
        assert e.code == 0
    else:
        assert False, "salir() no lanzó SystemExit"


def test_main_ejecuta_con_opcion_salir():
    """M-01 CA-03: La aplicación ejecuta sin errores y sale con la opción 0."""
    with patch("builtins.input", return_value="0"):
        try:
            main.main()
        except SystemExit:
            pass  # Esperado al salir


def test_cargar_usuarios_iniciales():
    """M-02 CA-01: Carga al menos 100 usuarios con semilla fija."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    assert sistema.cantidad_usuarios() == 100


def test_cargar_usuarios_ids_consecutivos():
    """M-02 CA-02: Los usuarios tienen IDs consecutivos desde 0."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    assert sistema.obtener_usuario_por_id(0).username == "usuario0000"
    assert sistema.obtener_usuario_por_id(99).username == "usuario0099"


def test_listar_usuarios_orden_alfabetico():
    """M-03 HU-05 CA-03: Lista usuarios en orden alfabético."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    nombres = list(sistema.listar_usuarios())
    assert nombres == sorted(nombres)
    assert len(nombres) == 100


def test_listar_usuarios_muestra_contenido():
    """M-03: listar_usuarios imprime los nombres de los usuarios."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    salida = io.StringIO()
    with patch("sys.stdout", salida):
        main.listar_usuarios(sistema)
    texto = salida.getvalue()
    assert "Usuarios registrados" in texto
    assert "usuario0000" in texto
    assert "usuario0099" in texto
    assert "Total: 100 usuarios" in texto


def test_seleccionar_usuario_existente():
    """M-04 HU-05 CA-01: Seleccionar usuario existente lo establece como activo."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    with patch("builtins.input", return_value="usuario0000"):
        usuario = main.seleccionar_usuario(sistema)
    assert usuario is not None
    assert usuario.username == "usuario0000"
    assert usuario.id == 0


def test_seleccionar_usuario_inexistente():
    """M-04 HU-05 CA-02: Seleccionar usuario inexistente retorna None y muestra mensaje."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    salida = io.StringIO()
    with patch("builtins.input", return_value="usuario_inexistente"):
        with patch("sys.stdout", salida):
            usuario = main.seleccionar_usuario(sistema)
    texto = salida.getvalue()
    assert usuario is None
    assert "usuario_inexistente" in texto
    assert "no existe" in texto


def test_seleccionar_usuario_conserva_activo():
    """M-04 HU-05 CA-01: Seleccionar usuario inexistente no reemplaza al activo."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    with patch("builtins.input", return_value="usuario0000"):
        usuario_activo = main.seleccionar_usuario(sistema)
    assert usuario_activo is not None
    assert usuario_activo.username == "usuario0000"
    with patch("builtins.input", return_value="usuario_inexistente"):
        resultado = main.seleccionar_usuario(sistema)
    assert resultado is None
    assert usuario_activo.username == "usuario0000"


def test_buscar_usuario_existente():
    """M-05 HU-05 CA-01: Buscar usuario existente muestra su información."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    salida = io.StringIO()
    with patch("builtins.input", return_value="usuario0000"):
        with patch("sys.stdout", salida):
            usuario = main.buscar_usuario(sistema)
    texto = salida.getvalue()
    assert usuario is not None
    assert usuario.username == "usuario0000"
    assert "usuario0000" in texto


def test_buscar_usuario_inexistente():
    """M-05 HU-05 CA-02: Buscar usuario inexistente devuelve None y muestra mensaje."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    salida = io.StringIO()
    with patch("builtins.input", return_value="usuario_inexistente"):
        with patch("sys.stdout", salida):
            usuario = main.buscar_usuario(sistema)
    texto = salida.getvalue()
    assert usuario is None
    assert "usuario_inexistente" in texto
    assert "no existe" in texto
