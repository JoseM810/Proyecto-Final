"""Pruebas de SistemaRed. Criterios de integración entre IndiceUsuarios,
RedSeguimiento y Usuario. Soporta HU-02, HU-05, HU-07."""
import pytest

from dominio.generador_usuarios import GeneradorUsuarios
from dominio.sistema_red import SistemaRed
from estructuras.errores import UsuarioNoExisteError


def test_registrar_usuario():
    """CA-01: registrar un usuario lo indexa y le asigna ID."""
    sistema = SistemaRed()
    u = sistema.registrar_usuario("ana0000", "Ana", "Desarrolladora")
    assert u.id == 0
    assert u.username == "ana0000"
    assert sistema.buscar_usuario_por_nombre("ana0000") is u
    assert sistema.obtener_usuario_por_id(0) is u
    assert sistema.cantidad_usuarios() == 1


def test_registrar_varios_usuarios_ids_consecutivos():
    """CA-01: los IDs son consecutivos a partir de 0."""
    sistema = SistemaRed()
    u1 = sistema.registrar_usuario("ana0000", "Ana")
    u2 = sistema.registrar_usuario("luis0001", "Luis")
    u3 = sistema.registrar_usuario("eva0002", "Eva")
    assert u1.id == 0
    assert u2.id == 1
    assert u3.id == 2


def test_buscar_usuario_por_nombre():
    """CA-02: buscar por nombre existente devuelve el usuario."""
    sistema = SistemaRed()
    sistema.registrar_usuario("ana0000", "Ana")
    sistema.registrar_usuario("luis0001", "Luis")
    assert sistema.buscar_usuario_por_nombre("Ana") is None
    assert sistema.buscar_usuario_por_nombre("ana0000") is not None
    assert sistema.buscar_usuario_por_nombre("ana0000").nombre_visible == "Ana"


def test_buscar_usuario_inexistente_devuelve_none():
    """CA-02: buscar nombre inexistente devuelve None sin error."""
    sistema = SistemaRed()
    assert sistema.buscar_usuario_por_nombre("nadie") is None


def test_seguir_usuario_genera_notificacion():
    """CA-03 y HU-07 CA-03: seguir a alguien le genera notificación."""
    sistema = SistemaRed()
    sistema.registrar_usuario("ana0000", "Ana")
    sistema.registrar_usuario("luis0001", "Luis")
    sistema.seguir("ana0000", "luis0001")
    luis = sistema.buscar_usuario_por_nombre("luis0001")
    assert luis.cantidad_notificaciones() == 1
    notif = luis.bandeja.leer_siguiente()
    assert notif.tipo == "NUEVO_SEGUIDOR"
    assert notif.origen == "ana0000"


def test_seguir_repetido_no_genera_notificacion_duplicada():
    """CA-03: seguir repetido no genera notificación adicional."""
    sistema = SistemaRed()
    sistema.registrar_usuario("ana0000", "Ana")
    sistema.registrar_usuario("luis0001", "Luis")
    sistema.seguir("ana0000", "luis0001")
    sistema.seguir("ana0000", "luis0001")
    luis = sistema.buscar_usuario_por_nombre("luis0001")
    assert luis.cantidad_notificaciones() == 1


def test_seguir_usuario_inexistente_lanza_error():
    """CA-03: seguir a usuario que no existe lanza UsuarioNoExisteError."""
    sistema = SistemaRed()
    sistema.registrar_usuario("ana0000", "Ana")
    with pytest.raises(UsuarioNoExisteError):
        sistema.seguir("ana0000", "inesistente0000")
    with pytest.raises(UsuarioNoExisteError):
        sistema.seguir("inesistente0000", "ana0000")


def test_listar_usuarios_orden_alfabetico():
    """HU-05 CA-03: listar entrega nombres en orden alfabético."""
    sistema = SistemaRed()
    sistema.registrar_usuario("sara0003", "Sara")
    sistema.registrar_usuario("ana0000", "Ana")
    sistema.registrar_usuario("luis0001", "Luis")
    sistema.registrar_usuario("eva0002", "Eva")
    assert list(sistema.listar_usuarios()) == ["ana0000", "eva0002", "luis0001", "sara0003"]


def test_cargar_desde_generador():
    """HU-01 CA-02: cargar 100 usuarios desde el generador funciona."""
    sistema = SistemaRed()
    datos = GeneradorUsuarios(42).generar(100)
    sistema.cargar_desde_generador(datos)
    assert sistema.cantidad_usuarios() == 100
    assert sistema.buscar_usuario_por_nombre("usuario0000") is not None
    assert sistema.buscar_usuario_por_nombre("usuario0099") is not None


def test_cargar_desde_generador_ids_consecutivos():
    """HU-01 CA-01: usuarios cargados tienen IDs consecutivos."""
    sistema = SistemaRed()
    sistema.cargar_desde_generador(GeneradorUsuarios(42).generar(5))
    assert sistema.obtener_usuario_por_id(0).username == "usuario0000"
    assert sistema.obtener_usuario_por_id(4).username == "usuario0004"


def test_obtener_usuario_por_id_negativo_devuelve_none():
    """CA-01: obtener_usuario_por_id con ID negativo devuelve None."""
    sistema = SistemaRed()
    sistema.registrar_usuario("ana0000", "Ana")
    assert sistema.obtener_usuario_por_id(-1) is None


def test_obtener_usuario_por_id_fuera_de_rango_devuelve_none():
    """CA-01: obtener_usuario_por_id con ID mayor al máximo devuelve None."""
    sistema = SistemaRed()
    sistema.registrar_usuario("ana0000", "Ana")
    assert sistema.obtener_usuario_por_id(1) is None
    assert sistema.obtener_usuario_por_id(99) is None


def test_cargar_desde_generador_con_duplicados_no_carga_parcial():
    """Caso extremo: nombres duplicados lanzan NombreDuplicadoError sin dejar carga parcial."""
    from estructuras.errores import NombreDuplicadoError

    sistema = SistemaRed()
    datos = [("usuario0001", "Uno", "bio1"), ("usuario0001", "Uno otra vez", "bio2")]
    with pytest.raises(NombreDuplicadoError):
        sistema.cargar_desde_generador(datos)
    assert sistema.cantidad_usuarios() == 0


def test_dejar_de_seguir():
    """HU-02 CA-03: dejar de seguir funciona a través del sistema."""
    sistema = SistemaRed()
    sistema.registrar_usuario("ana0000", "Ana")
    sistema.registrar_usuario("luis0001", "Luis")
    sistema.seguir("ana0000", "luis0001")
    assert sistema.dejar_de_seguir("ana0000", "luis0001") is True
    assert sistema.dejar_de_seguir("ana0000", "luis0001") is False


def test_recomendar_a_traves_del_sistema():
    """HU-08 CA-01: recomendar funciona a través del sistema."""
    sistema = SistemaRed()
    sistema.cargar_desde_generador(GeneradorUsuarios(1).generar(10))
    sistema.seguir("usuario0000", "usuario0001")
    sistema.seguir("usuario0001", "usuario0002")
    recomendados = list(sistema._red.recomendar(0))
    assert 2 in recomendados
