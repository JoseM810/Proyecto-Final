"""Pruebas de BandejaNotificaciones (T-02 y T-03). Criterios de specs/02-notificaciones/spec.md."""
import pytest

from dominio.notificaciones import (
    COMENTARIO,
    NUEVO_SEGUIDOR,
    RESPUESTA,
    BandejaNotificaciones,
)
from estructuras.errores import NotificacionInvalidaError


# --- agregar ---
def test_agregar_deja_la_notificacion_pendiente():
    """INV-01: agregar una notificación sube pendientes() en uno."""
    bandeja = BandejaNotificaciones()
    bandeja.agregar(NUEVO_SEGUIDOR, "Ana")
    assert bandeja.pendientes() == 1


def test_agregar_invalida_lanza_error_y_no_cambia_pendientes():
    """CA-04: tipo u origen inválido lanza NotificacionInvalidaError y no cambia pendientes()."""
    bandeja = BandejaNotificaciones()
    bandeja.agregar(COMENTARIO, "Ana")
    with pytest.raises(NotificacionInvalidaError):
        bandeja.agregar("OTRO_TIPO", "Luis")
    with pytest.raises(NotificacionInvalidaError):
        bandeja.agregar(RESPUESTA, "")
    with pytest.raises(NotificacionInvalidaError):
        bandeja.agregar(RESPUESTA, None)
    assert bandeja.pendientes() == 1


def test_agregar_acepta_los_tres_tipos():
    """Spec: NUEVO_SEGUIDOR, COMENTARIO y RESPUESTA son tipos válidos."""
    bandeja = BandejaNotificaciones()
    bandeja.agregar(NUEVO_SEGUIDOR, "Ana")
    bandeja.agregar(COMENTARIO, "Luis")
    bandeja.agregar(RESPUESTA, "Sara")
    assert bandeja.pendientes() == 3


def test_agregar_despues_de_leer_todas():
    """Caso extremo: con la bandeja vaciada, agregar vuelve a funcionar."""
    bandeja = BandejaNotificaciones()
    bandeja.agregar(COMENTARIO, "Ana")
    bandeja.leer_siguiente()
    bandeja.agregar(RESPUESTA, "Luis")
    assert bandeja.pendientes() == 1
    assert bandeja.leer_siguiente().origen == "Luis"


# --- leer_siguiente ---
def test_leer_en_orden_de_llegada():
    """CA-01: las notificaciones se leen en el orden en que llegaron."""
    bandeja = BandejaNotificaciones()
    bandeja.agregar(NUEVO_SEGUIDOR, "Ana")
    bandeja.agregar(COMENTARIO, "Luis")
    bandeja.agregar(RESPUESTA, "Sara")
    assert bandeja.leer_siguiente().origen == "Ana"
    assert bandeja.leer_siguiente().origen == "Luis"
    assert bandeja.leer_siguiente().origen == "Sara"


def test_leer_sin_pendientes():
    """CA-02: leer sin pendientes devuelve None y no lanza error."""
    bandeja = BandejaNotificaciones()
    assert bandeja.leer_siguiente() is None
    assert bandeja.pendientes() == 0


def test_leer_la_quita():
    """CA-03: leer una notificación la quita; no se puede leer otra vez."""
    bandeja = BandejaNotificaciones()
    bandeja.agregar(COMENTARIO, "Ana")
    bandeja.leer_siguiente()
    assert bandeja.pendientes() == 0
    assert bandeja.leer_siguiente() is None


def test_leer_devuelve_tipo_y_origen():
    """CA-01: la notificación leída conserva su tipo y su origen."""
    bandeja = BandejaNotificaciones()
    bandeja.agregar(RESPUESTA, "Sara")
    leida = bandeja.leer_siguiente()
    assert leida.tipo == RESPUESTA
    assert leida.origen == "Sara"


# --- pendientes ---
def test_pendientes_inicial_es_cero():
    """INV-01: una bandeja nueva tiene 0 pendientes."""
    assert BandejaNotificaciones().pendientes() == 0


def test_pendientes_no_modifica_la_bandeja():
    """INV-01: consultar pendientes no cambia nada."""
    bandeja = BandejaNotificaciones()
    bandeja.agregar(COMENTARIO, "Ana")
    bandeja.pendientes()
    bandeja.pendientes()
    assert bandeja.pendientes() == 1


def test_pendientes_son_agregadas_menos_leidas():
    """INV-02: lo leído no vuelve a estar pendiente; pendientes nunca baja de 0."""
    bandeja = BandejaNotificaciones()
    for nombre in ("Ana", "Luis", "Sara", "Eva"):
        bandeja.agregar(COMENTARIO, nombre)
    bandeja.leer_siguiente()
    bandeja.leer_siguiente()
    bandeja.leer_siguiente()
    bandeja.leer_siguiente()
    bandeja.leer_siguiente()  # una lectura de más
    assert bandeja.pendientes() == 0


def test_muchas_notificaciones_en_orden():
    """Caso extremo: 5 000 notificaciones salen en orden de llegada."""
    bandeja = BandejaNotificaciones()
    for i in range(5_000):
        bandeja.agregar(COMENTARIO, f"usuario{i}")
    assert bandeja.pendientes() == 5_000
    assert bandeja.leer_siguiente().origen == "usuario0"
    assert bandeja.leer_siguiente().origen == "usuario1"